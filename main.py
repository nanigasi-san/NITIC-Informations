import receive_gmail
import notifying_to_LINE
import my_info

message = receive_gmail.get_gmali_information(my_info.sender_addresses)
if message != "No new mail":
    notifying_to_LINE.notifying(message)