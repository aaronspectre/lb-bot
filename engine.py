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

	await bot.answer_callback_query(callback.id)
	await getSize(callback)



@dispatch.callback_query_handler(lambda c: 'size' in c.data)
async def reply_size(callback):
	config.config.logg(callback, sep = True)

	await bot.answer_callback_query(callback.id)
	await getAmount(callback)



@dispatch.callback_query_handler(lambda c: 'amount' in c.data)
async def reply_amount(callback):

	await bot.answer_callback_query(callback.id)

	amount = config.config.getName(callback.message.reply_markup.inline_keyboard, callback.data)
	config.progress += ' x'+amount
	config.busket.append(config.progress)
	config.progress = str()

	await getMenu(callback)



@dispatch.callback_query_handler(lambda c: 'busket' in c.data)
async def showBusket(callback):
	product = config.config.getName(callback.message.reply_markup.inline_keyboard, callback.data)
	config.config.logg(config.busket)
	await bot.answer_callback_query(callback.id)



@dispatch.callback_query_handler(lambda c: 'back' in c.data)
async def goBack(callback):
	config.config.logg(callback, sep = True)

	config.step -= 1
	await answer_validator(callback)



@dispatch.callback_query_handler(lambda c: 'ready' in c.data)
async def ready(callback):
	config.config.logg(config.busket)

	order_list = '\n'.join([f'\t{item}' for item in config.busket])
	# keyboard = types.InlineKeyboardMarkup().insert(types.InlineKeyboardButton('Order 🚚', callback_data = 'order_done'))
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
	keyboard.add(types.KeyboardButton('Share 📍', request_location = True))
	await bot.send_message(callback.from_user.id, f'Your Order:\n{order_list}\n\nPlease share with us your location', reply_markup = keyboard)



async def order_done(message):

	server.send(config.busket)
	order_list = '\n'.join([f'\t{item}' for item in config.busket])
	bill_of_order_text = f"""Bill of Order\n\nYour order:\n{order_list}\n\nTotal: 31,823.92$\nid: {config.user.chat_id}\n\nBon Appétit!"""
	await message.answer(bill_of_order_text, reply_markup = types.ReplyKeyboardRemove())




async def getMenu(message):
	config.step = 2
	keyboard = types.InlineKeyboardMarkup(row_width = 2)
	keyboard.insert(types.InlineKeyboardButton('Taco 🌮', callback_data = 'tacosimple'))
	keyboard.insert(types.InlineKeyboardButton('Taco with 🧀', callback_data = 'tacocheese'))
	keyboard.insert(types.InlineKeyboardButton('Busket 🛒', callback_data = 'busket'))

	if len(config.busket) != 0:
		keyboard.insert(types.InlineKeyboardButton('Ready ✅', callback_data = 'ready'))

	await bot.send_message(config.user.chat_id, 'Got it', reply_markup = types.ReplyKeyboardRemove())
	await bot.send_message(config.user.chat_id, 'Here is the menu', reply_markup = keyboard)




async def getSize(callback):
	product = config.config.getName(callback.message.reply_markup.inline_keyboard, callback.data)
	config.step = 3
	keyboard = types.InlineKeyboardMarkup(row_width = 2)
	keyboard.insert(types.InlineKeyboardButton(f'{product} Big', callback_data = 'big_size'))
	keyboard.insert(types.InlineKeyboardButton(f'{product} Medium', callback_data = 'mid_size'))
	keyboard.insert(types.InlineKeyboardButton(f'{product} Small', callback_data = 'small_size'))

	await bot.send_message(callback.from_user.id, 'Please Choose Size', reply_markup = keyboard)




async def getAmount(callback):
	config.progress += config.config.getName(callback.message.reply_markup.inline_keyboard, callback.data)
	config.step = 4
	keyboard = types.InlineKeyboardMarkup(row_width = 3)
	for i in range(1, 21):
		keyboard.insert(types.InlineKeyboardButton(i, callback_data = f'{i}_amount'))

	await bot.send_message(callback.from_user.id, 'Please Choose Amount', reply_markup = keyboard)


@dispatch.message_handler(commands = ['start', 'help'])
async def greet(message):
	config.config.logg(message, sep = True)

	if config.user.username is None:
		config.user.id = message['from'].id
		config.user.username = message['from'].username
		config.user.name = message['from'].first_name
		config.user.chat_id = message['chat'].id

	config.step = 1

	button = types.KeyboardButton('Share ☎️', request_contact = True)
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True).add(button)

	await bot.send_sticker(chat_id = message.chat.id, sticker = 'CAACAgIAAxkBAANMYRdtdnDsfvy_bUJ5Y5P25J1DvfcAAkACAALKAwYLErYLnAsKDVUgBA')
	await message.answer('Welcome to Los Burgos Delivery\nPlease, before starting share with us your phone number',
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