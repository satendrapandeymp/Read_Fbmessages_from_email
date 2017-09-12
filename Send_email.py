import textwrap, smtplib, os, glob, urllib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
from zipfile import ZipFile

def zipping():
	files = glob.glob('msg/*/*')
	with ZipFile('Fb_data.zip','w') as zip:
		# writing each file one by one
		for file in files:
        	     zip.write(file)
	for file in files:
        	     os.remove(file)

def sendEmail(FROM, TO, username, password):
    
    SUBJECT = 'Last 20 messages'
    textMessage = 'Here is a zip file containing all the 20 messages you got in last few days.'
    
    zf = open("Fb_data.zip")
    
    msg = MIMEMultipart()
    msg['From'] = FROM
    msg['To'] = TO
    msg['Date'] = formatdate(localtime = True)
    msg['Subject'] = SUBJECT
    msg.attach (MIMEText(textMessage))
    part = MIMEBase('application', "octet-stream")
    part.set_payload(zf.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="Fb_data.zip"')
    msg.attach(part)

    # send the message
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username,password)
    server.sendmail(FROM, TO, str(msg))
    server.quit()

