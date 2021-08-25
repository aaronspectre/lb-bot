import config
import webhook
import pprint

from aiogram import Bot, Dispatcher, executor, types




bot = Bot(token = config.config.TOKEN)
dispatch = Dispatcher(bot)
server = webhook.Server()





@dispatch.callback_query_handler(lambda c: 'taco' in c.data)
async def reply_menu(callback):
	config.config.logg(callback, sep = True)
	config.menu_message = callback.message.message_id

	await bot.answer_callback_query(callback.id)
	await getSize(callback)



@dispatch.callback_query_handler(lambda c: 'size' in c.data)
async def reply_size(callback):
	config.config.logg(callback, sep = True)

	config.progress += config.config.getName(callback.message.reply_markup.inline_keyboard, callback.data)

	await bot.answer_callback_query(callback.id)
	await bot.delete_message(callback.from_user.id, callback.message.message_id)
	await getAmount(callback)




@dispatch.callback_query_handler(lambda c: 'amount' in c.data)
async def reply_amount(callback):

	config.config.logg(callback, sep = True)

	if '5' in callback.data:
		if '-5' in callback.data:
			config.amount -= 5
		else:
			config.amount += 5
	elif '1' in callback.data:
		if '-1' in callback.data:
			config.amount -= 1
		else:
			config.amount += 1
	elif 'done' in callback.data:
		config.progress += f' x{config.amount}'
		config.busket.append(config.progress)
		config.progress = str()
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
	keyboard.insert(types.InlineKeyboardButton(config.amount, callback_data = 'final_amount'))
	keyboard.insert(types.InlineKeyboardButton('+1', callback_data = '+1_amount'))
	keyboard.insert(types.InlineKeyboardButton('+5', callback_data = '+5_amount'))
	keyboard.insert(types.InlineKeyboardButton('🆗', callback_data = 'done_amount'))
	await bot.edit_message_reply_markup(callback.from_user.id, callback.message.message_id, reply_markup = keyboard)



@dispatch.callback_query_handler(lambda c: 'busket' in c.data)
async def showBusket(callback):
	config.config.logg(config.busket, sep = True)
	await bot.answer_callback_query(callback.id)

	order_list = '\n'.join([f'\t{item}' for item in config.busket])
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
async def goBack(callback):
	config.config.logg(callback, sep = True)
	config.busket.clear()

	await bot.delete_message(callback.from_user.id, callback.message.message_id)
	await getMenu(callback)



@dispatch.callback_query_handler(lambda c: 'ready' in c.data)
async def ready(callback):
	config.config.logg(config.busket)

	order_list = '\n'.join([f'\t{item}' for item in config.busket])
	# keyboard = types.InlineKeyboardMarkup().insert(types.InlineKeyboardButton('Order 🚚', callback_data = 'order_done'))
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
	keyboard.add(types.KeyboardButton('Отправить 📍', request_location = True))
	await bot.send_message(
		callback.from_user.id,
		f'Ваш заказ:\n\n{order_list}\n\nПожалуйста отправьте нам вашe местоположение',
		reply_markup = keyboard
	)



async def order_done(message):

	if server.send(config.busket):
		order_list = '\n'.join([f'\t{item}' for item in config.busket])
		bill_of_order_text = f"""Чек\n\nВаш заказ:\n{order_list}\n\nОбщая цена: 31,823.92$\nid: {config.user.chat_id}\n\nBon Appétit!"""
		await message.answer(bill_of_order_text, reply_markup = types.ReplyKeyboardRemove())
	else:
		await message.answer('Что-то пошло не так 🙁, Пожалуйста повторите позже')




async def getMenu(message):
	config.step = 2
	keyboard = types.InlineKeyboardMarkup(row_width = 2)
	keyboard.insert(types.InlineKeyboardButton('Taco 🌮', callback_data = 'tacosimple'))
	keyboard.insert(types.InlineKeyboardButton('Taco with 🧀', callback_data = 'tacocheese'))
	keyboard.insert(types.InlineKeyboardButton('Корзина 🛒', callback_data = 'busket'))

	if len(config.busket) != 0:
		keyboard.insert(types.InlineKeyboardButton('Готово ✅', callback_data = 'ready'))

	if config.has_menu:
		await bot.edit_message_reply_markup(message.from_user.id, config.menu_message, reply_markup = keyboard)
	else:
		await bot.send_message(config.user.chat_id, 'Ок', reply_markup = types.ReplyKeyboardRemove())
		config.has_menu = True
		await bot.send_message(config.user.chat_id, 'Меню', reply_markup = keyboard)




async def getSize(callback):
	product = config.config.getName(callback.message.reply_markup.inline_keyboard, callback.data)
	config.step = 3
	keyboard = types.InlineKeyboardMarkup(row_width = 2)
	keyboard.insert(types.InlineKeyboardButton(f'{product} Big', callback_data = 'big_size'))
	keyboard.insert(types.InlineKeyboardButton(f'{product} Medium', callback_data = 'mid_size'))
	keyboard.insert(types.InlineKeyboardButton(f'{product} Small', callback_data = 'small_size'))

	await bot.send_message(callback.from_user.id, 'Please Choose Size', reply_markup = keyboard)




async def getAmount(callback):
	config.step = 4
	config.amount = 0
	keyboard = types.InlineKeyboardMarkup(row_width = 5)
	keyboard.insert(types.InlineKeyboardButton('-5', callback_data = '-5_amount'))
	keyboard.insert(types.InlineKeyboardButton('-1', callback_data = '-1_amount'))
	keyboard.insert(types.InlineKeyboardButton('0', callback_data = 'final_amount'))
	keyboard.insert(types.InlineKeyboardButton('+1', callback_data = '+1_amount'))
	keyboard.insert(types.InlineKeyboardButton('+5', callback_data = '+5_amount'))

	await bot.send_message(callback.from_user.id, f'Please choose amount for {config.progress}', reply_markup = keyboard)





@dispatch.message_handler(commands = ['start', 'help'])
async def greet(message):
	config.config.logg(message, sep = True)

	if config.user.username is None:
		config.user.id = message['from'].id
		config.user.username = message['from'].username
		config.user.name = message['from'].first_name
		config.user.chat_id = message['chat'].id

	config.step = 1

	button = types.KeyboardButton('Отправить ☎️', request_contact = True)
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True).add(button)

	await bot.send_sticker(chat_id = message.chat.id, sticker = 'CAACAgIAAxkBAANMYRdtdnDsfvy_bUJ5Y5P25J1DvfcAAkACAALKAwYLErYLnAsKDVUgBA')
	await message.answer('🎉🎊Добро поджаловать Los Burgos🎊🎉\nПожалуйста, перед началом отправьте нам ваш номер телефона',
		reply_markup = keyboard)




@dispatch.message_handler(content_types = types.ContentType.CONTACT)
async def receive_contact(message):
	config.config.logg(message, sep = True)

	config.user.contact = message.contact.phone_number

	await getMenu(message)



@dispatch.message_handler(content_types = types.ContentType.LOCATION)
async def receive_contact(message):
	config.config.logg(message, sep = True)

	config.user.location["latitude"] = message.location['latitude']
	config.user.location["longitude"] = message.location['longitude']

	await order_done(message)





@dispatch.message_handler(content_types = types.ContentType.ANY)
async def answer_validator(message):
	config.config.logg(message, sep = True)

	if config.step == 1:
		await greet(message)
	elif config.step == 2:
		await getMenu(message)
	elif config.step == 3:
		await getSize(message)
	elif config.step == 4:
		await getAmount(message)
	else:
		await greet(message)












if __name__ == '__main__':
	try:
		executor.start_polling(dispatch, skip_updates = True)
	except Exception as e:
		config.config.logg(e, 1, True)