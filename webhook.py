import requests
import json
import config


class Server:
	def __init__(self):
		self.ADDRESS = 'https://lbcontrol.pythonanywhere.com/bot/'


	def send(self, data):
		final = {
			'order': data,
			'cname': config.user.name,
			'phone': '+'+config.user.contact,
			'location': config.user.location,
			'id': config.user.id,
			'username': '@'+config.user.username
		}
		final = json.dumps(final)
		config.config.logg(final, sep = True)

		try:
			requests.post(self.ADDRESS, {'data': final})
			return True
		except:
			return False