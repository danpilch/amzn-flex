#!/usr/bin/env python
# configuration params

class config_opts(object):
    def __init__(self, flex_user_id, flex_password):
        self.flex_login_json = {
            'auth_data': {'use_global_authentication': 'true',
            'user_id_password': {'user_id': f'{flex_user_id}',
            'password': f'{flex_password}'}},
            'registration_data': {'domain': 'Device',
            'device_type': 'A1MPSLFC7L5AFK',
            'device_serial': '8efadac26ff449a8824aceadea9a4a09',
            'app_name': 'com.amazon.rabbit',
            'app_version': '303584574',
            'device_model': 'ONEPLUS A5000',
            'os_version': 'OnePlus/OnePlus5/OnePlus5:9/PKQ1.180716.001/2002242003:user/release-keys',
            'software_version': '130050002'},
            'requested_token_type': ['bearer',
            'mac_dms',
            'store_authentication_cookie',
            'website_cookies'],
            'cookies': {'domain': 'amazon.com', 'website_cookies': []},
            'user_context_map': {'frc': 'APiDytWgaiIj96vbh7zSA/pAMzl/RV/c7vmudhbqPBgKgcHV80/bkyf8wHYLyArR4aVn320sGPuM4ASMcTseSPw3GCtMVYL4HGcOb53WBjOA14Fg5S9cvCSEuGopCrtqgRZEEkwIWjcNuLvx35gquHCvzI2ZygPVUy1zCGnrKMI5R0yx8VJSjSrRlsd43HU7mCdY16Pg2Yj05xYe39vNowTnCmzydmI//N+oiHXNyh8YcvmzJhZ5KvG+jieV6RMMViUvgaMMunJ4XlDNQwyxpg0xH073cFvLflXdl0onUvrq7fzvA5ZtgATk9glukqkfmkD3f+PtwlQk30cdESIoh+7qvNHAEI2I9c2+aSN1pPiRkq8Uu1CQGGJe+MjYSX3JcKpjUs9tbumi9JyFGoXR2UVIixGCvWlXCQ=='},
            'device_metadata': {'device_os_family': 'android',
            'device_type': 'A1MPSLFC7L5AFK',
            'device_serial': '8efadac26ff449a8824aceadea9a4a09',
            'mac_address': 'C248C629AF1FE0A8C46B95668064C1D2952A9E91D207BC0CC3C5D584C2F7553A',
            'imei': '391A64A6A13BE598F8E5FB45CE6BC383EC95D77EB1F552224747E8F733E15DDA',
            'manufacturer': 'OnePlus',
            'model': 'ONEPLUS A5000',
            'os_version': '28',
            'android_id': '255263dcb21507a3',
            'build_serial': 'bffa5ca7',
            'product': 'OnePlus5'},
            'requested_extensions': ['device_info', 'customer_info']}

        self.flex_login_url = "https://api.amazon.com/auth/register"
        self.flex_get_offers_url = "https://flex-capacity-eu.amazon.com/GetOffersForProviderPost"
        self.flex_accept_offers_url = "https://flex-capacity-eu.amazon.com/AcceptOffer"

        self.user_agent_string = "Dalvik/2.1.0 (Linux; U; Android 9; ONEPLUS A5000 Build/PKQ1.180716.001) RabbitAndroid/3.33.224.0"

        self.flex_headers = {
            'Content-Type': 'application/json',
            'User-Agent': f'{self.user_agent_string}',
        }

        self.service_area_ids = {
            "33743755-d9b5-44b6-b03d-9e1723247169": "Morrisons Portsmouth"
        }

        self.flex_get_offers_json = {"apiVersion": "V2", "filters": { "serviceAreaFilter": [], "timeFilter": {} }, "serviceAreaIds": [ "33743755-d9b5-44b6-b03d-9e1723247169" ] }
        
        self.accept_json = {
            "__type": "AcceptOfferInput:http://internal.amazon.com/coral/com.amazon.omwbuseyservice.offers/",
#            "offerId": f"" 
        }

