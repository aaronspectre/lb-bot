import config

from aiogram import types

class Constructor:
	async def getMenu(active_users, message, TelegramBot):
		inline_keyboard = TelegramBot.build_keyboard(source = 'menu')

		if len(active_users[message['from'].id]['busket']) != 0:
			inline_keyboard.insert(types.InlineKeyboardButton('Готово ✅', callback_data = 'ready'))

		try:
			await TelegramBot.bot.send_message(active_users[message['from'].id]['chat_id'], 'Меню', reply_markup = inline_keyboard)
		except Exception as e:
			config.config.logg(e, 1, True)



	async def getType(callback, bot, food):
		keyboard = types.InlineKeyboardMarkup(row_width = 2)
		keyboard.insert(types.InlineKeyboardButton(f'{food.name} 🥩', callback_data = 'food_type_meat'))
		keyboard.insert(types.InlineKeyboardButton(f'{food.name} 🍗', callback_data = 'food_type_chick'))
		keyboard.add(types.InlineKeyboardButton('Назад ⬅️', callback_data = 'goback'))
		await bot.send_message(callback['from'].id, 'Выберите тесто', reply_markup = keyboard)



	async def getVegitable(callback, bot, food):
		keyboard = types.InlineKeyboardMarkup(row_width = 2)
		for name, has in food.vegitables.items():
			if has:
				keyboard.insert(types.InlineKeyboardButton(f'{name} ✅', callback_data = f'food_veg_{name}'))
			else:
				keyboard.insert(types.InlineKeyboardButton(f'{name} ❌', callback_data = f'food_veg_{name}'))

		keyboard.add(types.InlineKeyboardButton('Далее ➡️', callback_data = 'food_veg_done'))
		keyboard.add(types.InlineKeyboardButton('Назад ⬅️', callback_data = 'goback'))
		await bot.send_message(callback['from'].id, 'Нажмите на кнопку чтобы добавить ингредиент', reply_markup = keyboard)


	async def getCondiments(callback, bot, food):
		keyboard = types.InlineKeyboardMarkup(row_width = 2)
		for name, has in food.condiments.items():
			if has:
				keyboard.insert(types.InlineKeyboardButton(f'{name} ✅', callback_data = f'food_cond_{name}'))
			else:
				keyboard.insert(types.InlineKeyboardButton(f'{name} ❌', callback_data = f'food_cond_{name}'))

		keyboard.add(types.InlineKeyboardButton('Далее ➡️', callback_data = 'food_cond_done'))
		keyboard.add(types.InlineKeyboardButton('Назад ⬅️', callback_data = 'goback'))
		await bot.send_message(callback['from'].id, 'Нажмите на кнопку чтобы добавить приправу', reply_markup = keyboard)


	async def getAmount(callback, active_users, bot):
		keyboard = types.InlineKeyboardMarkup(row_width = 3)
		for i in range(1, 10):
			keyboard.insert(types.InlineKeyboardButton(i, callback_data = f'{i}_amount'))

		keyboard.insert(types.InlineKeyboardButton('🔄', callback_data = 'reset_amount'))
		keyboard.insert(types.InlineKeyboardButton('0', callback_data = '0_amount'))
		keyboard.add(types.InlineKeyboardButton('Назад ⬅️', callback_data = 'goback'))

		await bot.send_message(callback.from_user.id,
			f"Выберите количество {active_users[callback['from'].id]['progress'].name}: 0",
			reply_markup = keyboard
		)