import argparse
import requests
import my_info

def notifying(message, image_path="No image"):
    """
    LINEへ通知する
    参考: https://kuroyagikun.com/python-line-message-picture-send/

    Parameters
    ----------
    message : string
        通知する文章。
    image_path : string
        通知する画像の絶対パス。
    """

    line_notify_api = 'https://notify-api.line.me/api/notify'
    line_notify_token = my_info.access_token
    headers = {'Authorization': 'Bearer ' + line_notify_token}
    payload = {'message': message}
    if image_path == "No image":
        requests.post(line_notify_api, data=payload, headers=headers)
    else:
        files = {"imageFile": open(image_path, "rb")}
        requests.post(line_notify_api, data=payload, headers=headers, files=files)
