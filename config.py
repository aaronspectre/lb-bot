class Config:
	def __init__(self):
		self.TOKEN = '1912018363:AAHN2Vd__wMe-t5YoKH5XqDBqN6pK-1W9JA'
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


	def safer(self, func):
		try:
			func()
		except Exception as e:
			self.logg(e, 1)



class UserData:
	def __init__(self):
		self.id = 0
		self.username = None
		self.contact = None
		self.location = None
		self.name = None



user = UserData()
config = Config()