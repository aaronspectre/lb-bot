import config
import webhook
import json
import requests


from aiogram import Bot, Dispatcher, executor, types




bot = Bot(token = config.config.TOKEN)
dispatch = Dispatcher(bot)
step = 0
server = webhook.Server()





@dispatch.callback_query_handler(lambda c: 'taco' in c.data)
async def reply_menu(callback):
	await bot.answer_callback_query(callback.id)
	await bot.send_message(callback.from_user.id, 'Ok')
	config.config.logg(callback, sep = True)





async def getMenu(message):
	keyboard = types.InlineKeyboardMarkup(row_width = 2)
	keyboard.add(types.InlineKeyboardButton('Taco 🌮', callback_data = 'tacosimple'))
	keyboard.add(types.InlineKeyboardButton('Taco with 🧀', callback_data = 'tacocheese'))

	await bot.send_sticker(chat_id = message.chat.id, sticker = 'CAACAgIAAxkBAANMYRdtdnDsfvy_bUJ5Y5P25J1DvfcAAkACAALKAwYLErYLnAsKDVUgBA')
	await message.answer('Here is the menu', reply_markup = keyboard)




async def getSize(message):
	product = message.text
	keyboard = types.InlineKeyboardMarkup()
	keyboard.add(types.InlineKeyboardButton(f'{product} Big'), callback_data = 'big')
	keyboard.add(types.InlineKeyboardButton(f'{product} Ordinary'), callback_data = 'mid')
	keyboard.add(types.InlineKeyboardButton(f'{product} Small'), callback_data = 'small')
	
	await message.answer('Please Choose Size', reply_markup = keyboard)



@dispatch.message_handler(commands = ['start', 'help'])
async def greet(message):
	config.config.logg(message, sep = True)

	config.user.id = message['from'].id
	config.user.username = message['from'].username
	config.user.name = message['from'].first_name

	step = 1

	button = types.KeyboardButton('Share ☎️', request_contact = True)
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True).add(button)

	await message.answer('Welcome to Los Burgos Delivery\nPlease, before starting share with us your phone number',
		reply_markup = keyboard)




@dispatch.message_handler(content_types = types.ContentType.CONTACT)
async def receive_contact(message):
	config.config.logg(message, sep = True)

	config.user.contact = message.contact.phone_number

	await message.answer('Got It', reply_markup = types.ReplyKeyboardRemove())
	await getMenu(message)





@dispatch.message_handler(content_types = types.ContentType.ANY)
async def answer_validator(message):
	config.config.logg(message, sep = True)


	await getMenu(message)





if __name__ == '__main__':
	executor.start_polling(dispatch, skip_updates = True)