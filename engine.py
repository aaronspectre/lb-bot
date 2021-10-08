import config
import webhook

from aiogram import Bot, Dispatcher, executor, types




bot = Bot(token = config.config.TOKEN)
dispatch = Dispatcher(bot)
server = webhook.Server()

active_users = dict()




@dispatch.callback_query_handler(lambda c: 'corndog' in c.data)
async def replyMenu(callback):
	config.config.logg(callback, sep = True)
	active_users[callback['from'].id]['menu_message'] = callback.message.message_id
	active_users[callback['from'].id]['progress'] = config.config.getName(callback.message.reply_markup.inline_keyboard, callback.data)

	await bot.answer_callback_query(callback.id)
	await getAmount(callback)





@dispatch.callback_query_handler(lambda c: 'amount' in c.data)
async def replyAmount(callback):

	config.config.logg(callback, sep = True)

	if '5' in callback.data:
		if '-5' in callback.data:
			active_users[callback['from'].id]['amount'] -= 5
		else:
			active_users[callback['from'].id]['amount'] += 5
	elif '1' in callback.data:
		if '-1' in callback.data:
			active_users[callback['from'].id]['amount'] -= 1
		else:
			active_users[callback['from'].id]['amount'] += 1
	elif 'done' in callback.data:
		active_users[callback['from'].id]['progress'] += f" x{active_users[callback['from'].id]['amount']}"
		active_users[callback['from'].id]['busket'].append(active_users[callback['from'].id]['progress'])
		active_users[callback['from'].id]['progress'] = str()
		await bot.answer_callback_query(callback.id, 'Добавлено в корзину')
		await bot.delete_message(callback.from_user.id, callback.message.message_id)
		await getMenu(callback)
		return
	else:
		pass


	await bot.answer_callback_query(callback.id)
	keyboard = types.InlineKeyboardMarkup(row_width = 5)
	keyboard.insert(types.InlineKeyboardButton('-5', callback_data = '-5_amount'))
	keyboard.insert(types.InlineKeyboardButton('-1', callback_data = '-1_amount'))
	keyboard.insert(types.InlineKeyboardButton(active_users[callback['from'].id]['amount'], callback_data = 'final_amount'))
	keyboard.insert(types.InlineKeyboardButton('+1', callback_data = '+1_amount'))
	keyboard.insert(types.InlineKeyboardButton('+5', callback_data = '+5_amount'))
	keyboard.insert(types.InlineKeyboardButton('🆗', callback_data = 'done_amount'))
	await bot.edit_message_reply_markup(callback.from_user.id, callback.message.message_id, reply_markup = keyboard)



@dispatch.callback_query_handler(lambda c: 'busket' in c.data)
async def showBusket(callback):
	config.config.logg(active_users[callback['from'].id]['busket'], sep = True)
	await bot.answer_callback_query(callback.id)

	order_list = '\n'.join([f'\t{item}' for item in active_users[callback['from'].id]['busket']])
	keyboard = types.InlineKeyboardMarkup(row_width = 1)
	keyboard.insert(types.InlineKeyboardButton('Очистить корзину ❌', callback_data = 'clear'))
	keyboard.insert(types.InlineKeyboardButton('Назад ⬅️', callback_data = 'goback'))

	await bot.send_message(callback.from_user.id, f'Ваш заказ:\n\n{order_list}', reply_markup = keyboard)



@dispatch.callback_query_handler(lambda c: 'goback' in c.data)
async def goBack(callback):
	config.config.logg(callback, sep = True)

	await bot.delete_message(callback.from_user.id, callback.message.message_id)
	await getMenu(callback)



@dispatch.callback_query_handler(lambda c: 'clear' in c.data)
async def clearBusket(callback):
	config.config.logg(callback, sep = True)
	active_users[callback['from'].id]['busket'].clear()

	await bot.delete_message(callback.from_user.id, callback.message.message_id)
	await getMenu(callback)



@dispatch.callback_query_handler(lambda c: 'ready' in c.data)
async def ready(callback):
	config.config.logg(active_users[callback['from'].id]['busket'])

	order_list = '\n'.join([f'\t{item}' for item in active_users[callback['from'].id]['busket']])
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
	keyboard.add(types.KeyboardButton('Отправить 📍', request_location = True))
	await bot.send_message(
		callback.from_user.id,
		f'Ваш заказ:\n\n{order_list}\n\nПожалуйста отправьте нам вашe местоположение',
		reply_markup = keyboard
	)



async def orderDone(message):

	config.config.logg(message, sep = True)

	if server.send(active_users[message['from'].id]['busket'], active_users[message['from'].id]['user']):
		order_list = '\n'.join([f'\t{item}' for item in active_users[message['from'].id]['busket']])
		bill_of_order_text = f"""Чек\n\nВаш заказ:\n{order_list}\n\nОбщая цена: 31,823.92$\nid: {message['from'].id}\n\nBon Appétit!"""
		await message.answer(bill_of_order_text, reply_markup = types.ReplyKeyboardRemove())
		active_users[message['from'].id]['has_menu'] = False
		active_users[message['from'].id]['busket'].clear()
		await bot.delete_message(message['from'].id, active_users[message['from'].id]['menu_message'])
	else:
		await message.answer('Что-то пошло не так 🙁, Пожалуйста повторите позже')
		await bot.delete_message(message['from'].id, active_users[message['from'].id]['menu_message'])






async def getMenu(message):
	keyboard = types.InlineKeyboardMarkup(row_width = 2)
	keyboard.insert(types.InlineKeyboardButton('Corndog 🥩', callback_data = 'corndogsimp'))
	keyboard.insert(types.InlineKeyboardButton('Corndog 🍗', callback_data = 'corndogchick'))
	keyboard.insert(types.InlineKeyboardButton('Corndog 🥩 with 🧀', callback_data = 'corndogsimp_ch'))
	keyboard.insert(types.InlineKeyboardButton('Corndog 🍗 with 🧀', callback_data = 'corndogchick_ch'))
	keyboard.add(types.InlineKeyboardButton('Корзина 🛒', callback_data = 'busket'))

	if len(active_users[message['from'].id]['busket']) != 0:
		keyboard.insert(types.InlineKeyboardButton('Готово ✅', callback_data = 'ready'))

	try:
		if active_users[message['from'].id]['has_menu']:
			await bot.edit_message_reply_markup(message.from_user.id, active_users[message['from'].id]['menu_message'], reply_markup = keyboard)
		else:
			await bot.send_message(active_users[message['from'].id]['chat_id'], 'Ок', reply_markup = types.ReplyKeyboardRemove())
			active_users[message['from'].id]['has_menu'] = True
			await bot.send_message(active_users[message['from'].id]['chat_id'], 'Меню', reply_markup = keyboard)
	except Exception as e:
		config.config.logg(e, 1, True)





async def getAmount(callback):
	active_users[callback['from'].id]['amount'] = 0
	keyboard = types.InlineKeyboardMarkup(row_width = 5)
	keyboard.insert(types.InlineKeyboardButton('-5', callback_data = '-5_amount'))
	keyboard.insert(types.InlineKeyboardButton('-1', callback_data = '-1_amount'))
	keyboard.insert(types.InlineKeyboardButton('0', callback_data = 'final_amount'))
	keyboard.insert(types.InlineKeyboardButton('+1', callback_data = '+1_amount'))
	keyboard.insert(types.InlineKeyboardButton('+5', callback_data = '+5_amount'))

	await bot.send_message(callback.from_user.id,
		f"Пожалуйста выберите количество {active_users[callback['from'].id]['progress']}",
		reply_markup = keyboard
	)





@dispatch.message_handler(commands = ['start', 'help', 'restart'])
async def greet(message):
	config.config.logg(message, sep = True)

	active_users[message['from']['id']] = {
		'has_menu': False,
		'amount': 0,
		'progress': str(),
		'busket': list(),
		'menu_message': None,
		'chat_id': message['from']['id'],
		'user': {
			'id': -1,
			'location': dict(),
			'username': str(),
			'name': str()
		}
	}


	if active_users[message['from']['id']]['user']['id'] == -1:
		active_users[message['from']['id']]['user'] = config.buildUser(message)


	button = types.KeyboardButton('Отправить ☎️', request_contact = True)
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True).add(button)

	await bot.send_sticker(chat_id = message.chat.id, sticker = 'CAACAgIAAxkBAAIFNWEwZLjnx4jwfiBI2RNt1_Fm1G8zAAJnDgACFdNxSGikxIOzFJ0VIAQ')
	await message.answer('🎉🎊Добро поджаловать Los Burgos🎊🎉\nПожалуйста, перед началом отправьте нам ваш номер телефона',
		reply_markup = keyboard)




@dispatch.message_handler(content_types = types.ContentType.CONTACT)
async def receive_contact(message):
	config.config.logg(message, sep = True)

	active_users[message['from']['id']]['user']['contact'] = message.contact.phone_number

	await getMenu(message)



@dispatch.message_handler(content_types = types.ContentType.LOCATION)
async def receive_location(message):
	config.config.logg(message, sep = True)

	active_users[message['from']['id']]['user']['location']['latitude'] = message.location['latitude']
	active_users[message['from']['id']]['user']['location']['longitude'] = message.location['longitude']

	await orderDone(message)





@dispatch.message_handler(content_types = types.ContentType.ANY)
async def answer_validator(message):
	config.config.logg(message, sep = True)


	active_users[message['from']['id']] = {
		'has_menu': False,
		'amount': 0,
		'price': 0,
		'progress': str(),
		'busket': list(),
		'menu_message': None,
		'chat_id': message['from']['id'],
		'user': config.buildUser()
	}
	active_users[message['from']['id']]['has_menu'] = False
	active_users[message['from']['id']]['progress'] = str()

	await getMenu(message)

	# if config.step == 1:
	# 	await greet(message)
	# elif config.step == 2:
	# 	await getMenu(message)
	# elif config.step == 3:
	# 	await getAmount(message)
	# elif config.step == 4:
	# 	await ready(message)
	# else:
	# 	await greet(message)












if __name__ == '__main__':
	try:
		executor.start_polling(dispatch, skip_updates = True)
	except Exception as e:
		config.config.logg(e, 1, True)