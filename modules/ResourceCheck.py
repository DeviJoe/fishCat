import requests
import json
from bs4 import BeautifulSoup

'''
Так, чо вообще будет происходить в этом модуле.
Мы скачиваем и парсим ресурсы с определённого юрла.

Дальше мы проверяем, есть ли на сайте какие-то платежки. 
По идее, для этого можно использовать регулярки (которые надо ещё составить или нагуглить)

Проверяем, есть ли 3d secure (если бы я знал, что это за хрень)

Проверяем, есть ли SSL-сертификат, а также, валидный ли он

Прокликиваем ссылки, смотрим респонс коды

Чекаем переадресацию, чекаем "похожесть" названия (осталось придумать как...)

"Отчёт" возвращаем в формате json

Регулярки для поиска, кстати, можно хранить в отдельном месте, например,
выгружать их из базы данных. Это даст возможность потом добавлять
образцы фишинговых страниц
'''
class ResourceCheck:
	'''
	Это основной метод, который делает все действия.
	Из класса вызывается только он.
	'''
	@staticmethod
	def Scan(url):

		# Переменные, которые хранят значения, что найдено, а что нет

		Credentials = False
		PaymentFields = False
		DeadLinks = False
		RelatedLinks = False

		# Качаем данные по юрлу, создаём объект парсера

		r = requests.get(url)
		soup = BeautifulSoup(r.text, 'html.parser')

		# Находим поля для ввода

		input_fields = soup.find_all('input')

		if (len(input_fields) > 0):

			# Проверяем, есть ли поля для ввода кредов

			# Это можно как-то детализировать, но если будет время.
			# В целом, это уже должно кое-как определять поля для кредов
			for field in input_fields:
				if (field['type'] == 'email' or
					field['type'] == 'password' or
					field['type'] == 'login'):
					Credentials = True

			# Проверяем, есть ли платежные поля

			# card_number_fields = soup.find()
			# Я пока хуй знает как

			# Ищем ссылки, "прокликиваем" их

			links = soup.find('a')

			#if (len(links) > 0):
			#	requests.head()

			# Ищем среди ссылок похожие на входной юрл (бля, КАК?!)

			# ...

		# Возвращаем результат в формате json

		return json.dumps({
				"Credentials: ": Credentials,
				"PaymentFileds: ": PaymentFileds,
				"DeadLinks": DeadLinks,
				"RelatedLinks": RelatedLinks,

			})