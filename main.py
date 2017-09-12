import os, glob, urllib
from fbchat import Client, log
from getpass import getpass
from Send_email import sendEmail, zipping

media = ['mp3', 'mp4']

Email_username = str(raw_input("Gmail_Username till @: "))
Email_pass = getpass()

TO = Email_username + "@gmail.com"
FROM = TO

username = str(raw_input("Facebook_Username: "))
password = getpass()

arr = []

class EchoBot(Client):
    def onMessage(self, author_id, message, thread_id, thread_type, **kwargs):
        #self.markAsDelivered(author_id, thread_id)
        #self.markAsRead(author_id) 

	global arr	

	if not os.path.exists('msg/'):
			os.mkdir('msg/')

        if author_id != self.uid:

		arr.append(author_id)
		
		user = client.fetchUserInfo(author_id)[author_id]
		Folder_name = 'msg/' + user.name + '/'

		if not os.path.exists(Folder_name):
			os.mkdir(Folder_name)

		file = open(Folder_name + user.name + '.txt', 'a' )
	
		Message = client.fetchThreadMessages(thread_id=thread_id, limit=1)[0]

		if Message.text is not None:
			file.write( user.name + ' -- ' + Message.text.encode('utf-8') + ' \n' )
		if Message.attachments:
			for attachment in Message.attachments:
			# For Image
				Filename =  attachment['filename']
				if  Filename.split("-")[0] == 'image':
					add = attachment['large_preview']['uri']
					name = Folder_name + user.name + '_' + attachment['filename']+'.'+attachment['original_extension']
					urllib.urlretrieve(add, name)
				elif len(Filename.split(".")) > 1 and Filename.split(".")[1] in media:
					add = attachment['playable_url']
					Filename = Folder_name +  user.name + '_' + Filename
					urllib.urlretrieve(add, Filename)
				else:
					add = attachment['url']
					test = urllib.urlopen(add)
					temp = test.read().split('replace("')[1]
					temp = temp.split('");</script>')[0]
					temp = temp.replace("\\","")
					Filename = Folder_name + user.name + '_'  + Filename
					urllib.urlretrieve(temp, Filename)
		file.close()

		if len(arr) > 20:
			zipping()
			sendEmail(FROM, TO, Email_username, Email_pass)
			arr = []

    		
client = EchoBot(username, password)
client.listen()

