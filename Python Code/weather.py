import requests, time
def getData():
	weather = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Troy,NY&APPID=b782107ddb936c241a37c77376aa6505')
	forcast = requests.get('http://api.openweathermap.org/data/2.5/forecast?q=Troy,NY&APPID=b782107ddb936c241a37c77376aa6505')
	data = weather.json()
	# for element in data:
		# print(element, data[element])
	temp = data['main']['temp']
	forcast = forcast.json()
	totalPrecipitation = 0
	for element in forcast['list']:
		# print(element['rain'], element['snow'])
		for type in ['rain', 'snow']:
			if len(element[type]) > 0:
				totalPrecipitation += element[type]['3h']
	# print(totalPrecipitation)
	# print(temp - 273.15)
	# print(list(time.localtime())[3])
	return(temp - 273.15, totalPrecipitation, list(time.localtime())[3])

if __name__ == '__main__':
	print(getData())