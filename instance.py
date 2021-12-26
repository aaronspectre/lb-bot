class Taco:
	def __init__(self, name):
		self.name = name
		self.amount = str()
		self.type = None
		self.price = 0
		self.has_condiments = True
		self.has_vegitable = True
		self.vegitables = {
			'Огурец': False,
			'Помидор': False,
			'Зелень': False
		}
		self.condiments = {
			'Уксус': False,
			'Карри': False,
			'Масала': False,
			'Хмели-сунели': False
		}

	def __repr__(self):
		return f"{self.type} x {self.amount} - {self.price}\n- {', '.join(self.vegitables.keys())}\n- {', '.join(self.condiments.keys())}"


	def details(self):
		template = f"{self.type} x {self.amount} - {self.price}\n"
		container = list()
		for veg, has in self.vegitables.items():
			if has:
				container.append(veg)

		if len(container) != 0:
			template += '↳ '+', '.join(container)+'\n'
			container.clear()

		for cond, has in self.condiments.items():
			if has:
				container.append(cond)

		if len(container) != 0:
			template += '↳ '+', '.join(container)

		return template


class Corn:
	def __init__(self, name):
		self.name = name
		self.amount = str()
		self.type = None
		self.price = 0
		self.has_condiments = True
		self.has_vegitable = False
		self.condiments = {
			'Уксус': False,
			'Карри': False,
			'Масала': False,
			'Хмели-сунели': False
		}

	def details(self):
		template = f"{self.type} x {self.amount} - {self.price}\n"
		container = list()
		for cond, has in self.condiments.items():
			if has:
				container.append(cond)

		if len(container) != 0:
			template += '↳ '+', '.join(container)
			container.clear()
		return template


class Drink:
	def __init__(self, name):
		self.name = name
		self.amount = str()
		self.type = None
		self.price = 0
		self.has_vegitable = False
		self.has_condiments = False


def getFood(name):
	if name == 'Тако':
		return Taco(name)
	elif name == 'Корндог':
		return Corn(name)
	elif name == 'Напитки':
		return Drink(name)