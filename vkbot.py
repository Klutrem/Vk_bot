import vk_api 
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import bs4 as bs4
import requests
import random
from datetime import date 
from pycbrf.toolbox import ExchangeRates


class VkBot() :

	def __init__(self, user_id):
		print('bot created')
		self._USER_ID = user_id
		self.w = 0 
		self._USERNAME = self._get_user_name_from_vk_id(user_id)
		self.city = 'санкт-петербург'


		self.IDONTKNOWCOMMANDS =['Извините, я не понимаю', 'Не знаю такой команды. Напишите "Команды, чтобы узнать, что я умею', 
		'Не понимаю о чем вы...', 'Не могу распознать.', 'Меня такому ещё не научили.']

		self.can = 'Я умею здороваться и прощаться (Напишите "Привет" или "Пока") .' \
				'Напишите "Время", если хотите узнать точное время. Напишите "Погода", если хотите узнать погоду. \n'\
				'Также добавлены курсы валют (биткоин(в долларах), доллары, евро, гривны, кроны) '

		self.bye_commands = ['до свидания', "бывай", "пока", "прощайте", "бывай"]

		self.Thank_commands = ["Рад помочь!", "Не за что", "Это моя работа", "Я был создан для этого" ]

		self.hi_commands = ["привет", "приветствую", "здравствуйте", "добрый день"]

		self._COMMANDS = [["погода", 'узнать погоду', "тепло", "холодно"],
		 				  ["уремя", 'точное время', "часы", "который час"],
		  				  ["команды", "функции", "что умеешь?" ,"что ты умеешь?"],
		   				  ["спасибо", 'спасибки', "thx", 'thank you', 'tU', 'Благодарю'],
		                  'сегодня', 
		                  ["закрой", "закройся", "выключись", 'выход'], 
		                  ['курс биткоина', 'btc', 'биткоин', "биткоины" "крипта", "биток"],
		                  ["курс доллара", "доллар", 'доллары' "usd"], #7
		                  ["курс евро", "евро", "eur"  ], #8
		                  ['курс крон', "рона", 'czk', "кроны"], #9
		                  ["курс гривны", "гривна", "uah", "гривны"]] #10


	def _get_user_name_from_vk_id(self, user_id):
		request = requests.get('https://vk.com/id'+str(user_id))
		bs = bs4.BeautifulSoup(request.text, 'html.parser')
		user_name = self._clean_all_tag_from_str(bs.findAll('title')[0])
		return user_name.split()[0]

	def create_keyboard(self, message):

		keyboard = VkKeyboard(one_time = True)

		keyboard.add_button('Погода', color = VkKeyboardColor.PRIMARY)
		keyboard.add_button('Время', color = VkKeyboardColor.PRIMARY)

		keyboard.add_line()

		keyboard.add_button('Курс доллара', color = VkKeyboardColor.DEFAULT)
		keyboard.add_button('Курс евро', color = VkKeyboardColor.DEFAULT)

		keyboard.add_line()

		keyboard.add_button('Курс крон', color = VkKeyboardColor.DEFAULT)
		keyboard.add_button('Курс гривны', color = VkKeyboardColor.DEFAULT)

		keyboard.add_line()

		keyboard.add_button('Курс биткоина', color = VkKeyboardColor.NEGATIVE)

		return keyboard.get_keyboard()



	def _get_time(self):
		request = requests.get('https://my-calend.ru/date-and-time-today')
		b = bs4.BeautifulSoup(request.text, 'html.parser')
		return self._clean_all_tag_from_str(str(b.select('.page')[0].findAll('h2')[1])).split()[1]

	def _get_weather(self, city = 'санкт-петербург'):
		weather = 'https://sinoptik.com.ru/погода-' + city
		request = requests.get(weather)
		b = bs4.BeautifulSoup(request.text, 'html.parser')
		p3 = b.select('.temperature .p3')
		weather1 = p3[0].getText()
		p4 = b.select('.temperature .p4')
		weather2 = p4[0].getText()
		p5 = b.select('.temperature .p5')
		weather3 = p5[0].getText()
		p6 = b.select('.temperature .p6')
		weather4 = p6[0].getText()
		result = ''
		result = result + ('Утром :' + weather1 + '' + weather2) + '\n'
		result = result + ('Днём : ' + weather4 + '' + weather4) + '\n'
		temp = b.select('.rSide .description')
		weather = temp[0].getText()
		result = result + weather.strip()

		return result 

	def btc(self):
		bitcoin_api_url = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/'
		response = requests.get(bitcoin_api_url)
		response_json = response.json()

		return response_json[0]['price_usd']

	def values(self, currency):
		rates = ExchangeRates(date.today())
		return rates[currency][6]


	@staticmethod 
	def _clean_all_tag_from_str(string_line):
		result = ''
		not_skip = True 
		for i in list(string_line):
			if not_skip:
				if i == '<':
					not_skip = False
				else :
					result += i 
			else :
				if i == '>':
					not_skip = True
		return result

	def Today(self):
		day = str(date.today())
		file = open('days.txt', 'a')
		file.write('\n' + day)
		file.close()
		return 'Заношу в журнал.'



	def new_message(self, message):

		for i in self.hi_commands:
			if message == i :
				return random.choice(self.hi_commands)
		for i in self._COMMANDS[0]:
			if message == i:
				return self._get_weather()
		for i in  self._COMMANDS[1]:
			if message == i :
				return self._get_time()
		for i in self.bye_commands :
			if message == i :
				return random.choice(self.bye_commands)
		for i in self._COMMANDS[2]:
			if message == i :
				return self.can
		for i in self._COMMANDS[3]:
			if message == i :
				return random.choice(self.Thank_commands)
		for i in self._COMMANDS[5]:
			if message == i:	
				return 'Выключаюсь'
		for i in self._COMMANDS[6]:
			if message == i:
				return self.btc()
		for i in self._COMMANDS[7]:
			if message == i :
				return self.values('USD')

		for i in self._COMMANDS[8]:
			if message == i :
				return self.values('EUR')

		for i in self._COMMANDS[9]:
			if message == i :
				return self.values('CZK')

		for i in self._COMMANDS[10]:
			if message == i :
				return self.values('UAH')


		if message == self._COMMANDS[4]:
			return self.Today()

		else :
			return random.choice(self.IDONTKNOWCOMMANDS)
