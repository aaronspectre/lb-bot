import datetime
import json

class Config:
	def __init__(self):
		self.TOKEN = '2023199506:AAExb6Ne1RburJg970UOSKz8YXDXOedB3AI'
		self.SERVER_TOKEN = ''


	def logg(self, message, level = 3, sep = False):
		if level == 1:
			log_file = open('log.txt', 'a', encoding = 'utf-8')
			log_file.write(f'[!] {message} || {datetime.datetime.now()}')
			print(f'[!] {message}')
			log_file.close()
		elif level == 2:
			print(f'[#] {message}')
		else:
			print(f'[+] {message}')


		if sep:
			print('\n\n')



	def getName(self, inline_set, key):
		for name_set in inline_set:
			for name in name_set:
				if name.callback_data == key:
					return name.text


	def safer(self, func):
		try:
			func()
		except Exception as e:
			self.logg(e, 1)




def buildOrder(data, user):
	final = {
		'order': list(),
		'cname': user['name'],
		'phone': user['contact'],
		'location': user['location'],
		'id': user['id'],
		'username': '@'+user['username']
	}
	for item in data:
		final['order'].append(item.details())

	print(final)
	return final


def buildUser(message):
	user = dict()
	user['id'] = message['from'].id
	user['username'] = message['from'].username
	user['name'] = message['from'].first_name
	user['location'] = list()
	user['contact'] = str()

	if user['username'] is None:
		user['username'] = 'empty'

	return user


def makeUser(message):
	user = list()
	user.append(message['from'].id)
	if message['from'].username == None:
		user.append('empty')
	else:
		user.append(message['from'].username)
	user.append(message['from'].first_name)
	user.append(message.contact.phone_number)
	user.append(json.dumps(list()))
	user.append(json.dumps(list()))

	return user

config = Config()