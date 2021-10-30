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
	active_users[callback['from'].id]['busket'][active_users[callback['from'].id]['progress']] = str()

	await bot.answer_callback_query(callback.id)
	await bot.delete_message(callback.from_user.id, callback.message.message_id)
	await getAmount(callback)





@dispatch.callback_query_handler(lambda c: 'amount' in c.data)
async def replyAmount(callback):

	config.config.logg(callback, sep = True)


	if 'done' in callback.data:
		active_users[callback['from'].id]['amount'] = int(active_users[callback['from'].id]['amount'])
		await bot.answer_callback_query(callback.id, 'Добавлено в корзину')
		await bot.delete_message(callback.from_user.id, callback.message.message_id)
		if active_users[callback['from'].id]['amount'] <= 0:
			active_users[callback['from'].id]['amount'] = str()
		else:
			active_users[callback['from'].id]['busket'][active_users[callback['from'].id]['progress']] = active_users[callback['from'].id]['amount']
			active_users[callback['from'].id]['amount'] = str()
		await getMenu(callback)
		return
	elif 'reset' in callback.data:
		await bot.answer_callback_query(callback.id)
		active_users[callback['from'].id]['amount'] = str()

	else:
		await bot.answer_callback_query(callback.id)
		active_users[callback['from'].id]['amount'] = str(active_users[callback['from'].id]['amount']+callback.data.split('_')[0])


	try:
		keyboard = types.InlineKeyboardMarkup(row_width = 3)
		keyboard.insert(types.InlineKeyboardButton('1', callback_data = '1_amount'))
		keyboard.insert(types.InlineKeyboardButton('2', callback_data = '2_amount'))
		keyboard.insert(types.InlineKeyboardButton('3', callback_data = '3_amount'))
		keyboard.insert(types.InlineKeyboardButton('4', callback_data = '4_amount'))
		keyboard.insert(types.InlineKeyboardButton('5', callback_data = '5_amount'))
		keyboard.insert(types.InlineKeyboardButton('6', callback_data = '6_amount'))
		keyboard.insert(types.InlineKeyboardButton('7', callback_data = '7_amount'))
		keyboard.insert(types.InlineKeyboardButton('8', callback_data = '8_amount'))
		keyboard.insert(types.InlineKeyboardButton('9', callback_data = '9_amount'))
		keyboard.insert(types.InlineKeyboardButton('🔄', callback_data = 'reset_amount'))
		keyboard.insert(types.InlineKeyboardButton('0', callback_data = '0_amount'))
		keyboard.insert(types.InlineKeyboardButton('✅', callback_data = 'done_amount'))
		await bot.edit_message_text(
			text = f"Выберите количество {active_users[callback['from'].id]['progress']}: {active_users[callback['from'].id]['amount']}",
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
		order_list = '\n'.join([f'- {item} x {amount}' for item, amount in active_users[callback['from'].id]['busket'].items()])
		keyboard = types.InlineKeyboardMarkup(row_width = 3)
		for item in active_users[callback['from'].id]['busket'].keys():
			keyboard.insert(types.InlineKeyboardButton('➖', callback_data = f'edit_minus_{item}'))
			keyboard.insert(types.InlineKeyboardButton(str(item), callback_data = f'ignore'))
			keyboard.insert(types.InlineKeyboardButton('➕', callback_data = f'edit_plus_{item}'))
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

	await manage_busket(callback)



@dispatch.callback_query_handler(lambda c: 'edit' in c.data)
async def edit_busket(callback):
	config.config.logg(callback, sep = True)
	action = callback.data.split('_')[1]
	item = callback.data.split('_')[2]
	if action == 'plus':
		config.config.logg(item, sep = True)
		active_users[callback['from']['id']]['busket'][item] += 1
	else:
		if active_users[callback['from']['id']]['busket'][item] > 0:
			active_users[callback['from']['id']]['busket'][item] -= 1
			if active_users[callback['from']['id']]['busket'][item] == 0:
				del active_users[callback['from']['id']]['busket'][item]

	await bot.answer_callback_query(callback.id)

	await manage_busket(callback, 'edit')



@dispatch.callback_query_handler(lambda c: 'goback' in c.data)
async def goBack(callback):
	config.config.logg(callback, sep = True)
	await bot.answer_callback_query(callback.id)

	await bot.delete_message(callback.from_user.id, callback.message.message_id)
	await getMenu(callback)



@dispatch.callback_query_handler(lambda c: 'clear' in c.data)
async def clearBusket(callback):
	config.config.logg(callback, sep = True)
	await bot.answer_callback_query(callback.id)
	active_users[callback['from'].id]['busket'].clear()

	await bot.delete_message(callback.from_user.id, callback.message.message_id)
	await getMenu(callback)



@dispatch.callback_query_handler(lambda c: 'ready' in c.data)
async def ready(callback):
	await bot.answer_callback_query(callback.id)
	active_users[callback['from'].id]['menu_message'] = callback.message.message_id
	config.config.logg(active_users[callback['from'].id]['busket'], 3, True)

	order_list = '\n'.join([f'- {item} x {amount}' for item, amount in active_users[callback['from'].id]['busket'].items()])
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
	keyboard.add(types.KeyboardButton('Отправить 📍', request_location = True))
	await bot.send_message(
		callback.from_user.id,
		f'Ваш заказ:\n\n{order_list}\n\nПожалуйста отправьте нам вашe местоположение',
		reply_markup = keyboard
	)


@dispatch.callback_query_handler(lambda c: 'ignore' in c.data)
async def ignore(callback):
	await bot.answer_callback_query(callback.id)



async def orderDone(message):

	config.config.logg(message, sep = True)
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
	keyboard.add(types.KeyboardButton('Новый Заказ'))


	if server.send(active_users[message['from'].id]['busket'], active_users[message['from'].id]['user']):
		order_list = '\n'.join([f'- {item}' for item in active_users[message['from'].id]['busket']])
		bill_of_order_text = f"""Чек\n\nВаш заказ:\n{order_list}\n\nОбщая цена: 150000UZS\n№ заказа: {message['from'].id}"""
		await message.answer(bill_of_order_text, reply_markup = keyboard)
		active_users[message['from'].id]['busket'].clear()
		await bot.delete_message(message['from'].id, active_users[message['from'].id]['menu_message'])
	else:
		await message.answer('Что-то пошло не так 🙁, Пожалуйста повторите позже', reply_markup = keyboard)
		await bot.delete_message(message['from'].id, active_users[message['from'].id]['menu_message'])






async def getMenu(message):
	inline_keyboard = build_keyboard('menu')


	if len(active_users[message['from'].id]['busket']) != 0:
		inline_keyboard.insert(types.InlineKeyboardButton('Готово ✅', callback_data = 'ready'))

	try:
		await bot.send_message(active_users[message['from'].id]['chat_id'], 'Меню', reply_markup = inline_keyboard)
	except Exception as e:
		config.config.logg(e, 1, True)





async def getAmount(callback):
	keyboard = types.InlineKeyboardMarkup(row_width = 3)
	keyboard.insert(types.InlineKeyboardButton('1', callback_data = '1_amount'))
	keyboard.insert(types.InlineKeyboardButton('2', callback_data = '2_amount'))
	keyboard.insert(types.InlineKeyboardButton('3', callback_data = '3_amount'))
	keyboard.insert(types.InlineKeyboardButton('4', callback_data = '4_amount'))
	keyboard.insert(types.InlineKeyboardButton('5', callback_data = '5_amount'))
	keyboard.insert(types.InlineKeyboardButton('6', callback_data = '6_amount'))
	keyboard.insert(types.InlineKeyboardButton('7', callback_data = '7_amount'))
	keyboard.insert(types.InlineKeyboardButton('8', callback_data = '8_amount'))
	keyboard.insert(types.InlineKeyboardButton('9', callback_data = '9_amount'))
	keyboard.insert(types.InlineKeyboardButton('🔄', callback_data = 'reset_amount'))
	keyboard.insert(types.InlineKeyboardButton('0', callback_data = '0_amount'))

	await bot.send_message(callback.from_user.id,
		f"Выберите количество {active_users[callback['from'].id]['progress']}: 0",
		reply_markup = keyboard
	)





@dispatch.message_handler(commands = ['start', 'help', 'restart'])
async def greet(message):
	config.config.logg(message, sep = True)

	active_users[message['from']['id']] = {
		'amount': str(),
		'progress': str(),
		'busket': dict(),
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

	await bot.send_sticker(chat_id = message.chat.id, sticker = 'CAACAgIAAxkBAAICR2FppV14VYaIV6jec4y4USLfPVjQAALoEgACE5FIS5lDWMG4Gy9oIQQ')
	await message.answer('Добро поджаловать Los Burgos\n\nПожалуйста, перед началом отправьте нам ваш номер телефона',
		reply_markup = keyboard)




@dispatch.message_handler(content_types = types.ContentType.CONTACT)
async def receive_contact(message):
	config.config.logg(message, sep = True)

	active_users[message['from']['id']]['user']['contact'] = message.contact.phone_number

	menu = 'AgACAgIAAxkBAAIFEmF1T-puaG17jHxJFziorW_YF7b_AAKytDEbZCqoSxeL7OMpkrRWAQADAgADcwADIQQ'
	await bot.send_photo(message['from'].id, menu, reply_markup = build_keyboard('menu_pic'))
	await getMenu(message)



@dispatch.message_handler(content_types = types.ContentType.LOCATION)
async def receive_location(message):
	config.config.logg(message, sep = True)

	active_users[message['from']['id']]['user']['location']['latitude'] = message.location['latitude']
	active_users[message['from']['id']]['user']['location']['longitude'] = message.location['longitude']

	if len(active_users[message['from']['id']]['busket']) == 0:
		await bot.delete_message(message['from']['id'], message.message_id)
		return

	await orderDone(message)





@dispatch.message_handler(content_types = types.ContentType.ANY)
async def answer_validator(message):
	config.config.logg(message, sep = True)

	try:
		if 'Новый' in message.text:
			menu = 'AgACAgIAAxkBAAIFEmF1T-puaG17jHxJFziorW_YF7b_AAKytDEbZCqoSxeL7OMpkrRWAQADAgADcwADIQQ'
			await bot.send_photo(message['from'].id, menu, reply_markup = build_keyboard('menu_pic'))
			await getMenu(message)
			del menu
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
	if source == 'menu':
		keyboard = types.InlineKeyboardMarkup(row_width = 2)
		keyboard.insert(types.InlineKeyboardButton('Corndog 🥩', callback_data = 'corndogsimp'))
		keyboard.insert(types.InlineKeyboardButton('Corndog 🍗', callback_data = 'corndogchick'))
		keyboard.insert(types.InlineKeyboardButton('Corndog 🥩 with 🧀', callback_data = 'corndogsimp_ch'))
		keyboard.insert(types.InlineKeyboardButton('Corndog 🍗 with 🧀', callback_data = 'corndogchick_ch'))
		keyboard.add(types.InlineKeyboardButton('Корзина 🛒', callback_data = 'busket'))
		return keyboard





if __name__ == '__main__':
	try:
		executor.start_polling(dispatch, skip_updates = True)
	except Exception as e:
		config.config.logg(e, 1, True)