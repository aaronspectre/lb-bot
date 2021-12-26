import sqlite3


class DataBase:
	def __init__(self):
		self.connection = sqlite3.connect('db.sqlite')
		self.cursor = self.connection.cursor()
		self.result = None


	def get(self, field):
		self.cursor.execute(f'select {field} from users')
		self.result = [item[0] for item in self.cursor.fetchall()]
		return self.result


	def getById(self, id):
		self.cursor.execute(f'select * from users where chat_id = "{id}"')
		self.result = [item for item in self.cursor.fetchall()]
		if len(self.result) == 0:
			return self.result

		return self.result[0]



	def filter(self, field, symbol):
		self.cursor.execute(f'select * from users where {field} like "{symbol}"')
		self.result = [item for item in self.cursor.fetchall()]
		return self.result


	def write(self, data):
		try:
			self.cursor.execute(f'insert into users values (?, ?, ?, ?, ?, ?)', data)
			self.connection.commit()
			return True
		except:
			return False


	def edit(self, field, data, symbol):
		print(data)
		self.cursor.execute(f"""update users set {field} = ? where chat_id = ?""", (data, symbol))
		self.connection.commit()
		return True
		try:
			pass
		except Exception as e:
			print(e)
			return False



	def delete(self, field, symbol):
		try:
			self.cursor.execute(f'delete from users where {field} = "{symbol}"')
			self.connection.commit()
			return True
		except:
			return False



if __name__ == '__main__':
	db = DataBase()
	print(db.edit('order', '["Тако 🍗 x 8 - 0"]', 710810997))