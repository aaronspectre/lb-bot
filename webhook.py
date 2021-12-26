import requests
import json
import config


class Server:
	def __init__(self):
		self.ADDRESS = 'https://lbcontrol.pythonanywhere.com/bot/'
		# self.ADDRESS = 'http://localhost:8000/bot/'


	def send(self, data, user, db):
		final = config.buildOrder(data, user)
		config.config.logg(final, sep = True)
		final = json.dumps(final)
		try:
			response = requests.post(self.ADDRESS, {'data': final})
			if response.text == 'Got':
				config.config.logg(response.text, sep = True)
				return True
			config.config.logg(response.text, sep = True)
			return False
		except Exception as e:
			config.config.logg(e, 1, True)
			return False