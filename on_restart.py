import smtplib, ssl

import logging

#log file configuration
logging.basicConfig(filename='/home/pi/Deep_data/Logs/restart_logs.log' , filemode='a',format='%(asctime)s - %(message)s', level=logging.INFO)


port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = "plant.managment.platform@gmail.com"
receiver_email = "imeshsps@gmail.com"
password = 'Imesh1993'
message = """\
Subject: Restart Detected

Please check your project system.
Thanks.

This message is sent from Python."""

context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, port) as server:
    server.ehlo()  # Can be omitted
    server.starttls(context=context)
    server.ehlo()  # Can be omitted
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)

logging.info('System Restart Detected..')
