import telebot
import requests
from bs4 import BeautifulSoup
from telebot import types

bot = telebot.TeleBot('TOKEN') 

headers = {'User agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

x = 0


def the_cost_cripto(link, headers = headers):
	"""Выдаёт стоимость криптовалюты в рублях"""
	full_page = requests.get(link, headers=headers)
	soup = BeautifulSoup(full_page.text, "lxml")
	convert = soup.find("div", "crypto_curr_val")
	convert = convert.text
	convert = convert[1 : ]
	return convert


def inline_keyboard(message):
	"""Создаёт сообщение и прикрепляет к нему Inline-Keyboard"""
	markup = types.InlineKeyboardMarkup()
	btn_btc = types.InlineKeyboardButton('Bitcoin', callback_data='BTC')
	btn_eth = types.InlineKeyboardButton('Ethereum', callback_data='ETH')
	btn_ltc = types.InlineKeyboardButton('Litecoin', callback_data='LTC')
	btn_mnr = types.InlineKeyboardButton('Monero', callback_data='MNR')
	btn_eth_classic = types.InlineKeyboardButton('Ethereum classic', callback_data='ETH_CLASSIC')
	markup.add(btn_btc)
	markup.add(btn_eth)
	markup.add(btn_ltc)
	markup.add(btn_mnr)
	markup.add(btn_eth_classic)
	bot.send_message(message.chat.id, 'Выберите криптовалюту, стоимость которой хотите узнат: ', reply_markup=markup)


@bot.message_handler(content_types = ['text'])
def bot_say(message):
	# Создаёт две обычные кнопки 
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	butten_one = types.KeyboardButton('Узнать стоимоть криптовалюты')
	butten_two = types.KeyboardButton('🤖 О боте 🤖')
	markup.add(butten_one, butten_two)
	global x

	if message.text == '/start':
		"""Приветствие бота."""
		greeting = '''
Бот crypto рад приветствовать вас!
Я умею узнавать и передавать вам актуальную цену 5 криптовалют.
Цены будут в рублях и долларах.
Если хотите узнать подробнее, то напишите /help или нажмите на кнопку "О боте".
'''
		bot.send_message(message.chat.id, greeting, reply_markup=markup)

	elif message.text == 'Узнать стоимоть криптовалюты':
		x = 1
		inline_keyboard(message)

	elif message.text == '🤖 О боте 🤖' or message.text == '/help':
		help_message = '''
Если вы читаете это, значит вам интересно узнать обо мне.
Я создан в ознакомительных целях, просто для того, чтобы узнать что-же это такое, ваше программирование.
Я не понимаю ваших сообщений, но понимаю нажатия на кнопки.
Написан на языке Python, с использованием библиотеки Telebot.
Данные я беру с сайта myfin.ru.
Ещё раз скажу, бот создан в ознакомительных целях, а значит с ним вы можете лишь поиграть, а ни как не использовать в профессиональной среде.
Ну что-же, обо всём я вас предупредил, так что развлекайтесь.
		'''
		if x:
			bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id - 1, text='🤖 О боте 🤖', reply_markup=None)
			bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id - 1, text='/help', reply_markup=None)
		bot.send_message(message.chat.id, help_message, reply_markup=markup)
		x = 0
	else: 
		bot.send_message(message.chat.id, 'Я вас не понимаю.\nНажмите на кнопку "О Боте"\
			или напишите /help для навигации по боту.', reply_markup=markup)
		if x:
			bot.edit_message_reply_markup(message.chat.id, message_id = message.message_id-1, reply_markup = '')
			x = 0


@bot.callback_query_handler(func=lambda call: True)
def clicke_inline_butten(call):
	if call.message:
		global x
		x = 0
		if call.data == 'BTC':
			bit_cost_rub = the_cost_cripto(link = 'https://mainfin.ru/crypto/bitcoin-rub')
			bit_cost_dol = the_cost_cripto(link = 'https://mainfin.ru/crypto/bitcoin')
			bit_cost_dol = bit_cost_dol[ : len(bit_cost_dol) - 2]
			crypto_value_message = 'Bitcoin на данный момент стоит: \n\n' + bit_cost_rub + ' Руб\n' + 'или\n' + bit_cost_dol + ' Долларов'
			bot.send_message(call.message.chat.id, crypto_value_message)
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Bitcoin", reply_markup=None)
		
		elif call.data == 'ETH':
			eth_cost_rub = the_cost_cripto(link = 'https://mainfin.ru/crypto/1-ethereum-rub')
			eth_cost_dol = the_cost_cripto(link = 'https://mainfin.ru/crypto/ethereum')
			eth_cost_dol = eth_cost_dol[ : len(eth_cost_dol) - 2]
			crypto_value_message = 'Ethereum на данный момент стоит: \n\n' + eth_cost_rub + ' Руб\n' + 'или\n'  + eth_cost_dol + ' Долларов'
			bot.send_message(call.message.chat.id, crypto_value_message)
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Ethereum", reply_markup=None)
		
		elif call.data == 'LTC':
			lit_cost_rub = the_cost_cripto(link = 'https://mainfin.ru/crypto/litecoin-rub')
			lit_cost_dol = the_cost_cripto(link = 'https://mainfin.ru/crypto/litecoin')
			lit_cost_dol = lit_cost_dol[ : len(lit_cost_dol) - 2]
			crypto_value_message = 'Litecoin на данный момент стоит: \n\n' + lit_cost_rub + ' Руб\n' + 'или\n'  + lit_cost_dol + ' Долларов'
			bot.send_message(call.message.chat.id, crypto_value_message)
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Litecoin", reply_markup=None)
		
		elif call.data == 'MNR':
			mnr_cost_rub = the_cost_cripto(link = 'https://mainfin.ru/crypto/monero-rub')
			mnr_cost_dol = the_cost_cripto(link = 'https://mainfin.ru/crypto/monero')
			mnr_cost_dol = mnr_cost_dol[ : len(mnr_cost_dol) - 2]
			crypto_value_message = 'Monero на данный момент стоит: \n\n' + mnr_cost_rub + ' Руб\n' + 'или\n'  + mnr_cost_dol + ' Долларов'			
			bot.send_message(call.message.chat.id, crypto_value_message)
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Monero", reply_markup=None)
		
		elif call.data == 'ETH_CLASSIC':
			eth_clas_cost_rub = the_cost_cripto(link = 'https://mainfin.ru/crypto/1-ethereumclassic-rub')
			eth_clas_cost_dol = the_cost_cripto(link = 'https://mainfin.ru/crypto/ethereumclassic')
			eth_clas_cost_dol = eth_clas_cost_dol[ : len(eth_clas_cost_dol)]
			crypto_value_message = 'Ethereum classicна данный момент стоит: \n\n' + eth_clas_cost_rub + ' Руб\n' + 'или\n'  + eth_clas_cost_dol + ' Долларов'
			bot.send_message(call.message.chat.id, crypto_value_message)
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Ethereum classic", reply_markup=None)


bot.polling()