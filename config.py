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



class UserData:
	def __init__(self):
		self.id = -1
		self.username = str()
		self.contact = str()
		self.location = dict()
		self.name = str()
		self.chat_id = str()



	def buildUser(self, message):
		self.id = message['from'].id
		self.username = message['from'].username
		self.name = message['from'].first_name
		self.chat_id = message['chat'].id

		if self.username is None:
			self.username = 'empty'


	def buildOrder(self, data):
		final = {
			'order': data,
			'cname': self.name,
			'phone': '+'+self.contact,
			'location': self.location,
			'id': self.id,
			'username': '@'+self.username
		}

		return final



user = UserData()
config = Config()