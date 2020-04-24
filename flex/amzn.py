#!/usr/bin/env python
from .config import config_opts
import requests
import logging
import time
import uuid
import json
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
import rule_engine


class amzn_flex(object):
    def __init__(self, flex_user_id, flex_password):
        # Define logger
        self.logger = logging.getLogger('amzn_flex')
        logging.basicConfig(level = logging.INFO)

        # Get configuration opts
        self.config = config_opts(
            flex_user_id=flex_user_id, 
            flex_password=flex_password
        )

        # init as not logged in
        self.logged_in = False

        # Path to store block info
        self.file_path = "/tmp/flex"

        # Timeout login after 50 minutes (token expires after 3600seconds)
        self.timeout_after = 3200
        self.seconds_between_block_checks = 2

        # Empty list for found blocks
        self.found_offers_id_list = []

        # Criteria for accepting block
        self.criteria_block_service_ids = ["290578f2-4c88-40d5-8f4c-7d5773177540"]
        self.criteria_block_duration_hours = "<= 2"
        self.criteria_block_currency = "GBP"
        self.criteria_block_price = ">= 26"
        self.criteria_accept_block_same_day = False

    def flex_login(self):
        try:
            # Login to amazon flex
            response = requests.post(
                url=self.config.flex_login_url,
                headers=self.config.flex_headers,
                json=self.config.flex_login_json
            )
            json_login_response = response.json()
        
            # Set the timeout from after login
            self.timeout = time.time() + self.timeout_after

            if 'success' in json_login_response["response"]:
                self.logger.info('successfully logged in')

            return json_login_response['response']['success']['tokens']['bearer']['access_token']
        except Exception as e:
            raise e

    def flex_get_blocks(self, login_token):
        # Find available blocks
        try:
            blocks_headers = self.config.flex_headers
            blocks_headers['x-amz-access-token'] = login_token
            response = requests.post(
                url=self.config.flex_get_offers_url, 
                headers=blocks_headers, 
                json=self.config.flex_get_offers_json
            )

            if len(response.json()['offerList']) > 0:
                return response.json()
            else:
                return None
        except Exception as e:
            self.logger.error('failed to get blocks')
            self.logged_in = False

    def flex_calculate_block_duration(self, start, end):
        try:
            block_start = datetime.fromtimestamp(start)
            block_end = datetime.fromtimestamp(end)
            block_relative_time = relativedelta(block_end, block_start)
            return block_start, block_end, block_relative_time
        except Exception as e:
            self.logger.error('failed to calculate block duration')
            raise

    def flex_check_block_criteria(self, offer):
        try:
            # Calculate the relative time between start and end time
            block_start, block_end, block_relative_time = self.flex_calculate_block_duration(
                offer['startTime'], 
                offer['endTime']
            )
           
            # Add block_relative_time.hours to offer dict to evaluate
            offer['block_relative_hours'] = block_relative_time.hours
            # Add a list of acceptable service_area_ids to evaluate
            offer['accepted_service_area_ids'] = self.criteria_block_service_ids
        
            # Rule engine
            criteria_met = True

            # Get datetime object of today
            today = datetime.now()

            # Check if blocks today are acceptable, if not, check that the 
            # block_start.day is greater than today. if it isn't fail the criteria
            if not self.criteria_accept_block_same_day:
                if block_start.day <= today.day:
                    self.logger.info(f'block falls outside criteria {block_start.day} {today.day}')
                    criteria_met = False

            # Specify criteria to meet to accept a block
            if criteria_met:
                rule = rule_engine.Rule(
                    f""" rateInfo.currency == '{self.criteria_block_currency}' 
                        and rateInfo.priceAmount {self.criteria_block_price}
                        and block_relative_hours {self.criteria_block_duration_hours}
                        and serviceAreaId in accepted_service_area_ids
                     """
                )
                criteria_met = rule.matches(offer)
            return criteria_met
        except Exception as e:
            self.logger.error(f'failed to evaluate block criteria {e}')
            raise e

    def flex_accept_block(self):
        pass

    def check_timer(self):
        # Check if token is still valid
        return not time.time() > self.timeout

    def store_block_offers(self, offers):
        try:
            # Check if this offer has been seen before
            for offer in offers['offerList']:
                if offer['offerId'] not in self.found_offers_id_list:
                    # Check if this offer meets criteria
                    if self.flex_check_block_criteria(offer):
                        self.logger.info("block matches request criteria")
                        filename = f"{self.file_path}/{uuid.uuid1()}.json"
                        os.makedirs(os.path.dirname(filename), exist_ok=True)
                        with open(filename, "w") as f:
                            f.write(json.dumps(offer))
                        # Add offer to found list
                        self.found_offers_id_list.append(offer['offerId'])
                        self.logger.info(f"generated {filename}")
                    else:
                        # Add offer to found list
                        self.found_offers_id_list.append(offer['offerId'])
                        self.logger.info('block did not meet criteria')
        except Exception as e:
            self.logger.info(f"could not write file {e}")
            raise e

    def flex_control_loop(self):
        # Check if logged in, if not login
        self.logger.info(f"Checking every {self.seconds_between_block_checks}s for blocks before timeout in {self.timeout_after}s")
        try:
            if not self.logged_in:
                login_token = self.flex_login()

            while self.check_timer():
                check_for_available_blocks_result = self.flex_get_blocks(login_token)
                if check_for_available_blocks_result is not None:
                    self.store_block_offers(check_for_available_blocks_result)

                # Pause to emulate human interaction
                time.sleep(self.seconds_between_block_checks)

            self.logger.info("finished")
            self.logged_in = False
        except Exception as e:
            self.logged_in = False
