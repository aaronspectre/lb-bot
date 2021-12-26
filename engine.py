import json
import config
import webhook
import database

from instance import getFood
from constructor import Constructor
from geopy.geocoders import Nominatim
from aiogram import Bot, Dispatcher, executor, types



bot = Bot(token = config.config.TOKEN)
dispatch = Dispatcher(bot)
db = database.DataBase()
server = webhook.Server()
active_users = dict()


class TelegramBot:

	bot = bot


	@dispatch.message_handler(commands = ['start', 'help', 'restart'])
	async def greet(message):
		config.config.logg(message, sep = True)

		respone = db.getById(id = message['from']['id'])
		keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
		keyboard.add(types.KeyboardButton('Отправить ☎️', request_contact = True))
		print(respone)

		if len(respone) == 0:
			active_users[message['from']['id']] = {
				'progress': str(),
				'busket': list(),
				'menu_message': None,
				'chat_id': message['from']['id'],
				'user': config.buildUser(message)
			}
			await bot.send_sticker(chat_id = message.chat.id, sticker = 'CAACAgIAAxkBAAICR2FppV14VYaIV6jec4y4USLfPVjQAALoEgACE5FIS5lDWMG4Gy9oIQQ')
			await message.answer('Добро пожаловать Los Burgos\n\nПожалуйста, перед началом отправьте нам ваш номер телефона',
			reply_markup = keyboard)
		else:
			active_users[message['from']['id']] = {
				'progress': str(),
				'busket': list(),
				'menu_message': None,
				'chat_id': message['from']['id'],
				'user': {
					'id': respone[0],
					'username': respone[1],
					'name': respone[2],
					'location': json.loads(respone[4]),
					'contact': respone[3]
				}
			}
			try:
				menu = 'AgACAgIAAxkDAAPyYcWYmigwduGDwQXtEL_QYt7tmjsAApK2MRuoojBKuDormlziobYBAAMCAANtAAMjBA'
				await bot.send_photo(message['from'].id, menu, reply_markup = TelegramBot.build_keyboard('menu_pic'))
			except:
				with open('menu.jpg', 'rb') as menu:
					await bot.send_photo(message['from'].id, menu, reply_markup = TelegramBot.build_keyboard('menu_pic'))

			await Constructor.getMenu(active_users, message, TelegramBot)









	@dispatch.callback_query_handler(lambda c: 'constructor' in c.data)
	async def replyMenu(callback):
		config.config.logg(callback, sep = True)
		active_users[callback['from'].id]['menu_message'] = callback.message.message_id
		food = getFood(config.config.getName(callback.message.reply_markup.inline_keyboard, callback.data).split(' ')[0])
		active_users[callback['from'].id]['progress'] = food

		await bot.answer_callback_query(callback.id)
		await bot.delete_message(callback.from_user.id, callback.message.message_id)
		await Constructor.getType(callback, bot, food)


	@dispatch.callback_query_handler(lambda c: 'food_type' in c.data)
	async def replyType(callback):
		config.config.logg(callback, sep = True)
		active_users[callback['from'].id]['progress'].type = config.config.getName(callback.message.reply_markup.inline_keyboard, callback.data)

		await bot.answer_callback_query(callback.id)
		await bot.delete_message(callback.from_user.id, callback.message.message_id)
		if active_users[callback['from'].id]['progress'].has_vegitable:
			await Constructor.getVegitable(callback, bot, active_users[callback['from'].id]['progress'])
		else:
			await Constructor.getCondiments(callback, bot, active_users[callback['from'].id]['progress'])


	@dispatch.callback_query_handler(lambda c: 'food_veg' in c.data)
	async def replyVegitable(callback):
		await bot.answer_callback_query(callback.id)
		if callback.data == 'food_veg_done':
			await bot.delete_message(callback.from_user.id, callback.message.message_id)
			if active_users[callback['from'].id]['progress'].has_condiments:
				await Constructor.getCondiments(callback, bot, active_users[callback['from'].id]['progress'])
			else:
				await Constructor.getAmount(callback, active_users, bot)
		else:
			config.config.logg(callback, sep = True)
			vegitable = config.config.getName(callback.message.reply_markup.inline_keyboard, callback.data).split(' ')[0]
			if active_users[callback['from'].id]['progress'].vegitables[vegitable]:
				active_users[callback['from'].id]['progress'].vegitables[vegitable] = False
			else:
				active_users[callback['from'].id]['progress'].vegitables[vegitable] = True


			await bot.delete_message(callback.from_user.id, callback.message.message_id)
			await Constructor.getVegitable(callback, bot, active_users[callback['from'].id]['progress'])



	@dispatch.callback_query_handler(lambda c: 'food_con' in c.data)
	async def replyCondiments(callback):
		if callback.data == 'food_cond_done':
			await bot.delete_message(callback.from_user.id, callback.message.message_id)
			await Constructor.getAmount(callback, active_users, bot)
		else:
			config.config.logg(callback, sep = True)
			vegitable = config.config.getName(callback.message.reply_markup.inline_keyboard, callback.data).split(' ')[0]
			if active_users[callback['from'].id]['progress'].condiments[vegitable]:
				active_users[callback['from'].id]['progress'].condiments[vegitable] = False
			else:
				active_users[callback['from'].id]['progress'].condiments[vegitable] = True


			await bot.answer_callback_query(callback.id)
			await bot.delete_message(callback.from_user.id, callback.message.message_id)
			await Constructor.getCondiments(callback, bot, active_users[callback['from'].id]['progress'])



	@dispatch.callback_query_handler(lambda c: 'amount' in c.data)
	async def replyAmount(callback):
		config.config.logg(callback, sep = True)

		if 'done' in callback.data:
			active_users[callback['from'].id]['progress'].amount = int(active_users[callback['from'].id]['progress'].amount)
			await bot.answer_callback_query(callback.id, 'Добавлено в корзину')
			await bot.delete_message(callback.from_user.id, callback.message.message_id)
			active_users[callback['from'].id]['busket'].append(active_users[callback['from'].id]['progress'])
			await Constructor.getMenu(active_users, callback, TelegramBot)
			return
		elif 'reset' in callback.data:
			await bot.answer_callback_query(callback.id)
			active_users[callback['from'].id]['progress'].amount = str()
		else:
			await bot.answer_callback_query(callback.id)
			active_users[callback['from'].id]['progress'].amount = str(active_users[callback['from'].id]['progress'].amount)+callback.data.split('_')[0]


		try:
			keyboard = types.InlineKeyboardMarkup(row_width = 3)
			for i in range(1, 10):
				keyboard.insert(types.InlineKeyboardButton(i, callback_data = f'{i}_amount'))

			keyboard.insert(types.InlineKeyboardButton('🔄', callback_data = 'reset_amount'))
			keyboard.insert(types.InlineKeyboardButton('0', callback_data = '0_amount'))
			keyboard.insert(types.InlineKeyboardButton('✅', callback_data = 'done_amount'))
			keyboard.add(types.InlineKeyboardButton('Назад ⬅️', callback_data = 'goback'))
			await bot.edit_message_text(
				text = f"Выберите количество {active_users[callback['from'].id]['progress'].type}: {active_users[callback['from'].id]['progress'].amount}",
				chat_id = callback.from_user.id,
				message_id = callback.message.message_id,
				reply_markup = keyboard
			)

		except Exception as e:
			config.config.logg(e, sep = True)







	async def manage_busket(callback, flag = None):
		if len(active_users[callback['from'].id]['busket']) == 0:
			keyboard = types.InlineKeyboardMarkup(row_width = 1)
			keyboard.add(types.InlineKeyboardButton('Меню ⬅️', callback_data = 'goback'))
			if flag == 'edit':
				await bot.edit_message_text(
					chat_id = callback.from_user.id,
					text = 'Корзина пуста',
					message_id = callback.message.message_id,
					reply_markup = keyboard)
			else:
				await bot.send_message(callback.from_user.id, 'Корзина пуста', reply_markup = keyboard)

		else:
			order_list = '\n'.join([f'◽️ {item.type} x {item.amount}' for item in active_users[callback['from'].id]['busket']])
			keyboard = types.InlineKeyboardMarkup(row_width = 3)
			for item in active_users[callback['from'].id]['busket']:
				keyboard.insert(types.InlineKeyboardButton('➖', callback_data = f"edit_minus_{active_users[callback['from'].id]['busket'].index(item)}"))
				keyboard.insert(types.InlineKeyboardButton(str(item.type), callback_data = f'ignore'))
				keyboard.insert(types.InlineKeyboardButton('➕', callback_data = f"edit_plus_{active_users[callback['from'].id]['busket'].index(item)}"))
			keyboard.add(types.InlineKeyboardButton('Очистить корзину ❌', callback_data = 'clear'))
			keyboard.add(types.InlineKeyboardButton('Назад ⬅️', callback_data = 'goback'))
			if flag == 'edit':
				await bot.edit_message_text(
					chat_id = callback.from_user.id,
					text = f"Ваш заказ:\n\n{order_list}\n",
					message_id = callback.message.message_id,
					reply_markup = keyboard)
			else:
				await bot.send_message(callback.from_user.id, f"Ваш заказ:\n\n{order_list}\n", reply_markup = keyboard)



	@dispatch.callback_query_handler(lambda c: 'busket' in c.data)
	async def showBusket(callback):
		config.config.logg(active_users[callback['from'].id]['busket'], sep = True)
		await bot.answer_callback_query(callback.id)
		await bot.delete_message(callback.from_user.id, callback.message.message_id)

		await TelegramBot.manage_busket(callback)



	@dispatch.callback_query_handler(lambda c: 'edit' in c.data)
	async def edit_busket(callback):
		config.config.logg(callback, sep = True)
		action = callback.data.split('_')[1]
		item = int(callback.data.split('_')[2])
		if action == 'plus':
			active_users[callback['from']['id']]['busket'][0].amount += 1
		else:
			if active_users[callback['from']['id']]['busket'][0].amount > 0:
				active_users[callback['from']['id']]['busket'][0].amount -= 1
				if active_users[callback['from']['id']]['busket'][0].amount == 0:
					del active_users[callback['from']['id']]['busket'][0].amount


		await bot.answer_callback_query(callback.id)
		await TelegramBot.manage_busket(callback, 'edit')


	@dispatch.callback_query_handler(lambda c: 'clear' in c.data)
	async def clearBusket(callback):
		config.config.logg(callback, sep = True)
		await bot.answer_callback_query(callback.id)
		active_users[callback['from'].id]['busket'].clear()

		await bot.delete_message(callback.from_user.id, callback.message.message_id)
		await Constructor.getMenu(active_users, callback, TelegramBot)








	@dispatch.callback_query_handler(lambda c: 'ignore' in c.data)
	async def ignore(callback):
		await bot.answer_callback_query(callback.id)


	@dispatch.callback_query_handler(lambda c: 'goback' in c.data)
	async def goBack(callback):
		config.config.logg(callback, sep = True)
		await bot.answer_callback_query(callback.id)

		active_users[callback['from'].id]['amount'] = str()
		await bot.delete_message(callback.from_user.id, callback.message.message_id)
		await Constructor.getMenu(active_users, callback, TelegramBot)









	@dispatch.callback_query_handler(lambda c: 'ready' in c.data)
	async def ready(callback):
		await bot.answer_callback_query(callback.id)
		config.config.logg(active_users[callback['from'].id]['busket'], 3, True)

		order_list = '\n'.join([f'◽️ {item.details()}' for item in active_users[callback['from'].id]['busket']])
		keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
		keyboard.add(types.KeyboardButton('Отправить 📍', request_location = True))
		await bot.delete_message(callback.from_user.id, callback.message.message_id)
		await bot.send_message(
			callback.from_user.id,
			f'Ваш заказ:\n\n{order_list}\n\nПожалуйста отправьте нам вашe местоположение',
			reply_markup = keyboard
		)


	async def orderDone(message):
		config.config.logg(message, sep = True)
		keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
		keyboard.add(types.KeyboardButton('Новый Заказ'))


		if server.send(active_users[message['from'].id]['busket'], active_users[message['from'].id]['user'], db):
			order_list = '\n'.join([f'◽️ {item.details()}' for item in active_users[message['from'].id]['busket']])
			bill_of_order_text = f"""Чек\n\nВаш заказ:\n{order_list}\n\nОбщая цена: 150000UZS\n№ заказа: {message['from'].id}"""
			await message.answer(bill_of_order_text, reply_markup = keyboard)
			active_users[message['from'].id]['busket'].clear()
		else:
			await message.answer('Что-то пошло не так 🙁, Пожалуйста повторите позже', reply_markup = keyboard)












	@dispatch.message_handler(content_types = types.ContentType.CONTACT)
	async def receive_contact(message):
		config.config.logg(message, sep = True)

		active_users[message['from']['id']]['user']['contact'] = message.contact.phone_number
		db.write(config.makeUser(message))

		try:
			menu = 'AgACAgIAAxkDAAPyYcWYmigwduGDwQXtEL_QYt7tmjsAApK2MRuoojBKuDormlziobYBAAMCAANtAAMjBA'
			await bot.send_photo(message['from'].id, menu, reply_markup = TelegramBot.build_keyboard('menu_pic'))
		except:
			with open('menu.jpg', 'rb') as menu:
				await bot.send_photo(message['from'].id, menu, reply_markup = TelegramBot.build_keyboard('menu_pic'))

		await Constructor.getMenu(active_users, message, TelegramBot)



	@dispatch.message_handler(content_types = types.ContentType.LOCATION)
	async def receive_location(message):
		config.config.logg(message, sep = True)
		if len(active_users[message['from']['id']]['busket']) == 0:
			await bot.delete_message(message['from']['id'], message.message_id)
			return

		active_users[message['from']['id']]['user']['location'] = message.location['latitude'], message.location['longitude']
		db.edit('location', json.dumps(active_users[message['from']['id']]['user']['location']), message['from']['id'])

		await TelegramBot.orderDone(message)









	@dispatch.message_handler(content_types = types.ContentType.ANY)
	async def answer_validator(message):
		config.config.logg(message, sep = True)

		try:
			if 'Настройки' in message.text:
				keyboard = types.InlineKeyboardMarkup(row_width = 3)
				keyboard.add(types.InlineKeyboardButton('Назад ⬅️', callback_data = 'goback'))
				await bot.delete_message(message.from_user.id, callback.message.message_id)
				await message.answer('Настройки', reply_markup = keyboard)
				return
		except Exception as e:
			config.config.logg(e, 1, True)


		try:
			await bot.delete_message(message['from'].id, message.message_id)
		except Exception as e:
			config.config.logg(e, 1, True)


	def build_keyboard(source = None):
		if source == 'menu_pic':
			keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
			keyboard.add(types.KeyboardButton('Настройки'))
			keyboard.insert(types.KeyboardButton('Условия использования'))
			keyboard.add(types.KeyboardButton('Помощь'))
			keyboard.insert(types.KeyboardButton('История заказов'))
			return keyboard

		elif source == 'menu':
			keyboard = types.InlineKeyboardMarkup(row_width = 2)
			keyboard.insert(types.InlineKeyboardButton('Корндог 🌭', callback_data = 'corndog_constructor'))
			keyboard.insert(types.InlineKeyboardButton('Тако 🌮', callback_data = 'taco_constructor'))
			keyboard.insert(types.InlineKeyboardButton('Напитки 🥤', callback_data = 'drink_constructor'))
			keyboard.add(types.InlineKeyboardButton('Корзина 🛒', callback_data = 'busket'))
			return keyboard





if __name__ == '__main__':
	try:
		executor.start_polling(dispatch, skip_updates = True)
	except Exception as e:
		config.config.logg(e, 1, True)