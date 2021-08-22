import requests
import json
import config


class Server:
	def __init__(self):
		self.ADDRESS = 'http://localhost:8000/bot/'


	def send(self, data):
		final = {
			'order': data,
			'cname': config.user.name,
			'phone': config.user.contact,
			'location': config.user.location,
			'id': config.user.id,
			'username': '@'+config.user.username
		}
		final = json.dumps(final)
		config.config.logg(final, sep = True)

		requests.post(self.ADDRESS, {'data': final})