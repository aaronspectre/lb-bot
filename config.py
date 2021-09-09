class Config:
	def __init__(self):
		self.TOKEN = '1978222621:AAEzW9QW1mPOvww8tnlBS9-MtVLyEGuZqQo'
		self.SERVER_TOKEN = ''


	def logg(self, message, level = 3, sep = False):
		if sep:
			print('\n\n')

		if level == 1:
			print(f'[!] {message}')
		elif level == 2:
			print(f'[#] {message}')
		else:
			print(f'[+] {message}')



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
		'order': data,
		'cname': user['name'],
		'phone': '+'+user['contact'],
		'location': user['location'],
		'id': user['id'],
		'username': '@'+user['username']
	}

	return final


def buildUser(message):
	user = dict()
	user['id'] = message['from'].id
	user['username'] = message['from'].username
	user['name'] = message['from'].first_name
	user['chat_id'] = message['chat'].id
	user['location'] = dict()
	user['contact'] = str()

	if user['username'] is None:
		user['username'] = 'empty'

	return user


config = Config()