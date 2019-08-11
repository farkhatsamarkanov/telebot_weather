import telebot
import requests
import datetime

bot = telebot.TeleBot("974589976:AAHAwPf5g28i1euYB0jX9AJIccWynonQLn4")

url = 'https://wttr.in'

weather_parameters = {
    'format': 4,  
    'M': '',  
}

temp_parameter = {
    'format': '%t',  
}

def greet():
	now = datetime.datetime.now()
	today = now.day
	hour = now.hour
	if today == now.day and 6 <= hour < 12:
		return 'Good morning, '	
	elif today == now.day and 12 <= hour < 17:
		return 'Good day, '	
	elif today == now.day and 17 <= hour < 23:
		return 'Good evening, '	
	elif today == now.day and 23 <= hour <= 24:
		return 'Good night, '
		

def temp_string():
	try:
		response1 = requests.get(url, params = temp_parameter)
	except requests.ConnectionError:
		return '<Oops...Connection error>'
	if response1.status_code == 200:
		return response1.text
	else:
		return '<Something gone wrong on the weather server...>'

def recommendations():
	temp_storage = list(temp_string())
	if temp_storage[0] == '-':
		temp_int = int(f'{temp_storage[0]}{temp_storage[1]}{temp_storage[2]}')
	else:
		temp_int = int(f'{temp_storage[1]}{temp_storage[2]}')
		if temp_int <= 15:
			return 'Pretty cold out there...Better wrap up well!'
		elif 16 <= temp_int <= 23:
			return 'Temperature is ok, but don\'t go outside naked' 
		else:
			return 'Pretty warm...Beach time!'
			

def what_weather():
    try:
        response = requests.get(url, params = weather_parameters)
    except requests.ConnectionError:
        return '<Oops...Connection error>'
    if response.status_code == 200:
        return response.text
    else:
        return '<Something gone wrong on the weather server...>'

@bot.message_handler(content_types=['text'])

def send_weather(message):
	name = message.from_user.first_name
	bot.send_message(message.chat.id, f'{greet()}{name}!')
	bot.send_message(message.chat.id, what_weather())
	bot.send_message(message.chat.id, recommendations())

bot.polling(none_stop = True)