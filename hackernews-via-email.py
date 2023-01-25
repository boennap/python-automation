# in order to run the script locally, follow these steps:
# install python
# install following libraries: requests, BeautifulSoup, smtplib, email.mime, datetime
# install mailhog and run mailhog
# run script with python3 hackernews-via-email.py
# mails can be checked on http://0.0.0.0:8025/ per default

import requests  # http requests
from bs4 import BeautifulSoup  # webscraping
import smtplib  # sending email
from email.mime.multipart import MIMEMultipart  # email body
from email.mime.text import MIMEText  # email body
import datetime  # system date and time manipulation
now = datetime.datetime.now()
content = ''  # email content placeholder


# extracting Hacker News Stories

def extract_news(url):
    print('Extracting Hacker News Stories...')
    content_tmp = ''
    content_tmp += ('<h1>Hacker News Top Stories:</h1>\n' +
                    '<br>'+'-'*50 + '<br>')
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    for i, tag in enumerate(soup.find_all('td', attrs={'class': 'title', 'valign': ''})):
        a = tag.find_all('a')[0]
        content_tmp += ((str(i + 1) + ' :: ' + '<a href="' + a.attrs['href'] + '">' + tag.text +
                         "\n" + '</a>' + '<br>') if tag.text != 'More' else '')
    return (content_tmp)


content_tmp = extract_news('https://news.ycombinator.com/')
content += content_tmp
content += ('<br>'+'-'*50 + '<br>' + 'Automaticaly Generated Email')

# creating email

print('Composing email...')

SERVER = 'localhost'
PORT = 1025
FROM = 'recipient@test.com'
TO = 'sender@test.com'
PASS = ''

msg = MIMEMultipart()
msg['Subject'] = ' [Automated Email] Hacker News Top Stories' + \
    ' ' + str(now.day) + '-' + str(now.month) + '-' + str(now.year)
msg['From'] = FROM
msg['To'] = TO

msg.attach(MIMEText(content, 'html'))

# setting up server and sending email

print('Intiating server...')

server = smtplib.SMTP(SERVER, PORT)  # initiate server
server.set_debuglevel(1)
server.ehlo()
# server.starttls()  # start tls secure connection
server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print('Email sent...')

server.quit()
