#!/usr/bin/env python
from .config import config_opts
import requests
import logging
import time
import uuid


class amzn_flex(object):
    def __init__(self, flex_user_id, flex_password):
        self.config = config_opts(
            flex_user_id=flex_user_id, 
            flex_password=flex_password
        )

        self.logged_in = False

        self.file_path = "/tmp/flex"

        # Timeout login after 50 minutes (token expires after 3600seconds)
        self.timeout_after = 300 

    def flex_login(self):
        # Login to amazon flex
        response = requests.post(
            url=self.config.flex_login_url,
            headers=self.config.flex_headers,
            json=self.config.flex_login_json
        )
        json_login_response = response.json()
        
        # Set the timeout from after login
        self.timeout = time.time() + self.timeout_after

        return json_login_response['response']['success']['tokens']['bearer']['access_token']

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

            if response.json()['offerList'] > 0:
                return response.json()
            else:
                return None
        except Exception as e:
            self.logged_in = False

    def flex_accept_block(self):
        pass

    def check_timer(self):
        # Check if token is still valid
        return not time.time() > self.timeout

    def store_block_offers(self, offers):
        filename = f"{self.file_path}/{uuid.uuid1()}.json"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as f:
            f.write(str(offers))

    def flex_control_loop(self):
        # Check if logged in, if not login
        try:
            if not self.logged_in:
                login_token = self.flex_login()

            while self.check_timer():
                if self.flex_get_blocks(login_token) is not None:
                    print("found block")

                time.sleep(2)

            print("finished")
            self.logged_in = False
        except Exception as e:
            self.logged_in = False
