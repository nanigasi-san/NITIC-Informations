import email
import ssl
import imaplib
from email.header import decode_header, make_header

import my_info

def get_gmali_information(sender_addresses):
    host = "imap.gmail.com"
    nego_combo = ("ssl", 993)

    if nego_combo[0] == "no-encrypt":
        imapclient = imaplib.IMAP4(host, nego_combo[1])
    elif nego_combo[0] == "starttls":
        context = ssl.create_default_context()
        imapclient = imaplib.IMAP4(host, nego_combo[1])
        imapclient.starttls(ssl_context=context)
    elif nego_combo[0] == "ssl":
        context = ssl.create_default_context()
        imapclient = imaplib.IMAP4_SSL(host, nego_combo[1], ssl_context=context)
    imapclient.debug = 3

    username = my_info.username
    password = my_info.password
    imapclient.login(username, password)

    imapclient.select()
    typ, data = imapclient.search(None, "UNSEEN")
    datas = data[0].split()
    fetch_num = 1
    if (len(datas)-fetch_num) < 0:
        fetch_num = len(datas)
    msg_list = []
    for num in datas[len(datas)-fetch_num::]:
        typ, data = imapclient.fetch(num, '(RFC822)')
        msg = email.message_from_bytes(data[0][1])
        msg_list.append(msg)
    imapclient.close()
    imapclient.logout()

    for msg in msg_list:
        from_addr = str(make_header(decode_header(msg["From"])))
        subject = str(make_header(decode_header(msg["Subject"])))

        if msg.is_multipart() is False:
            # シングルパートのとき
            payload = msg.get_payload(decode=True)
            charset = msg.get_content_charset()
            if charset is not None:
                payload = payload.decode(charset, "ignore")
        else:
            # マルチパートのとき
            for part in msg.walk():
                payload = part.get_payload(decode=True)
                if payload is None:
                    continue
                charset = part.get_content_charset()
                if charset is not None:
                    payload = payload.decode(charset, "ignore")
        mail_address = email.header.decode_header(msg.get('From'))
        mail_address = mail_address[1][0].decode('utf-8')
        mail_address = mail_address.replace('<', "")
        mail_address = mail_address.replace('>', "")
        mail_address = mail_address[1:]
        mail_title = email.header.decode_header(msg.get('Subject'))
        mail_title = mail_title[0][0].decode('utf-8')
        mail_body = payload.split("</div>")

        for address in sender_addresses:
            if address == mail_address:
                send_message = "\n【メール受信】\n差出人: "
                send_message += mail_address
                send_message += "\n件名: "
                send_message += mail_title
                send_message += "\n\n本文\n------------\n"
                for line in mail_body:
                    send_message += line[16:]
                    send_message += "\n"
                return send_message
    return "No new mail"
