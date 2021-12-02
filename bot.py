import vk_api 
from vk_api.longpoll import VkLongPoll, VkEventType
from vkbot import VkBot
import random
import sys

def write_msg(user_id, message, keyboard):
	vk.method('messages.send', {'user_id':user_id, 'message':message, 'random_id':random.randint(0 ,2048), 'keyboard' : keyboard })

def pen():
	vk.method('messages.send', {'user_id':my_id, 'message':'Penek', 'random_id':random.randint(0 ,2048), 'peer_id' : 7821099})

token = ''
vk = vk_api.VkApi(token = token)
longpoll = VkLongPoll(vk)
my_id = 62310117
print('bot started')



for event in longpoll.listen():
	if event.type == VkEventType.MESSAGE_NEW :
		if event.to_me :
			print(f'New message from : {event.user_id}', end = '')
			bot = VkBot(event.user_id)
			write_msg(event.user_id, bot.new_message(event.text.lower()), bot.create_keyboard(event.text.lower()))
			print('Text:', event.text)
			for i in bot._COMMANDS[5]:
				if event.text == i:
					sys.exit()
