#/usr/bin/env python
from flex.amzn import amzn_flex
import os

user_id = os.getenv('FLEX_USER_ID', 'test')
password = os.getenv('FLEX_PASSWORD', 'test')
run_forever = os.getenv('FLEX_RUN_FOREVER', True)

def main():
    flex = amzn_flex(
        flex_user_id=user_id,
        flex_password=password
    )
    if run_forever:
        # Run loop forever
        while run_forever:
            flex.flex_control_loop()
    else: 
        # Run once
        flex.flex_control_loop()


if __name__ == "__main__":
    main()
