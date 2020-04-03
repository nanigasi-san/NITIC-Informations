import schedule
import time

import receive_gmail
import notifying_to_LINE
import my_info

def main_action():
    message = receive_gmail.get_gmali_information(my_info.block_addresses)
    if message != "No new mail":
        notifying_to_LINE.notifying(message)

schedule.every(1).minutes.do(main_action)

while True:
    schedule.run_pending()
    time.sleep(1)
