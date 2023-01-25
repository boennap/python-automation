# in order to run the script locally, follow these steps:
# install python and following libraries: requests, BeautifulSoup, smtplib, email.mime, datetime
# install mailhog and run mailhog
# run script with command "python3 hackernews-via-email.py"
# mails can be checked on http://0.0.0.0:8025/ per default

# http requests
import requests

# webscraping
from bs4 import BeautifulSoup

# sending emails
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# utils
import datetime
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

now = datetime.datetime.now()

# email content placeholder
content = ''


# extracting Hacker News Stories

def extract_news(url):

    # function that extracts news from the provided url

    logger.debug('Extracting Hacker News Stories...')

    content_tmp = ''
    content_tmp += f'<h1>Hacker News Top Stories:</h1>\n'

    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')

    for i, tag in enumerate(soup.find_all('td', attrs={'class': 'title', 'valign': ''})):
        a = tag.find_all('a')[0]
        content_tmp += (
            f'{i + 1}. <a href="{a.attrs["href"]}">{tag.text}\n</a><br>' if tag.text != 'More' else '')
    return (content_tmp)


content_tmp = extract_news('https://news.ycombinator.com/')
content += content_tmp
content += f'<br>{"-"*50}<br>Automatically Generated Email'

# composing the email

logger.debug('Composing email...')

SERVER = 'localhost'
PORT = 1025
FROM = 'recipient@test.com'
TO = 'sender@test.com'
PASS = ''

msg = MIMEMultipart()
msg['Subject'] = f'[Automated Email] Hacker News Top Stories {now.day}-{now.month}-{now.year}'
msg['From'] = FROM
msg['To'] = TO

msg.attach(MIMEText(content, 'html'))

# setting up server and sending email

logger.debug('Intiating server...')

try:

    # using "with" statement to open the SMTP server, it will automatically close the server when the block is done
    with smtplib.SMTP(SERVER, PORT) as server:

        # set debug level to 1 to see all the messages exchanged between the server and the client - activate If debugging is needed
        # server.set_debuglevel(1)

        # initiate a new SMTP session
        server.ehlo()

        # start tls secure connection - activate If secure connection is needed
        # server.starttls()

        server.login(FROM, PASS)

        server.sendmail(FROM, TO, msg.as_string())

        logger.debug('Email sent...')

except Exception as e:
    logger.error(e)
