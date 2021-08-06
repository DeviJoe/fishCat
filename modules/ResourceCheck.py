import requests
import json
import difflib
from bs4 import BeautifulSoup
from urllib.parse import urlparse

'''
Мы скачиваем и парсим ресурсы с определённого юрла.

Дальше мы проверяем, есть ли на сайте какие-то поля для ввода кредов/платёжек
(в зависимости, на что нацелен фишинговый сервис).

Прокликиваем ссылки, смотрим респонс коды

Чекаем переадресацию, чекаем "похожесть" названия

"Отчёт" возвращаем в формате json
'''
class ResourceCheck:
	'''
	Это основной метод, который делает все действия.
	Из класса вызывается только он.
	'''
	@staticmethod
	def Scan(url):

		# Переменные, которые хранят значения, что найдено, а что нет

		try:
			Credentials = False
			PaymentFileds = False
			DeadLinks = False
			RelatedLinks = {}

			# Качаем данные по юрлу, создаём объект парсера

			r = requests.get(url)
			soup = BeautifulSoup(r.text, 'html.parser')

			# Находим поля для ввода

			input_fields = soup.find_all('input')

			if (len(input_fields) > 0):

				# Проверяем, есть ли поля для ввода кредов

				for field in input_fields:
					if (field['type'] == 'password' or
						field['type'] == 'login' or
						field['name'] == 'login' or
						field['id'] == 'login'):
						Credentials = True

				# Проверяем, есть ли платежные поля

				payment_keywords = ['cvv', 'card-number', 'pay', 'номер карты', 'оплатить', 'оплатить']

				for keyword in payment_keywords:
					for field in input_fields:
						if (keyword in str.lower(field['name']) or
							keyword in str.lower(field['id']) or
							keyword in str.lower(field['value'])):
							PaymentFileds = True

				# Теперь обработаем ссылки...

				links = soup.findAll('a')
				matchers = []
				match_percents = []
				match_resp = {}

				for i in range(0,len(links) - 1):
					# Ищем ссылки, "прокликиваем" их
					
					try:
						response = requests.get(links[i].get('href'))
						if (response.status_code == 404):
							DeadLinks += 1
						pass

					except Exception:
						pass

					# Сравниваем домен самого сайта со ссылкой

					if (urlparse(links[i].get('href')).netloc != urlparse(url).netloc):
						link_domain = urlparse(links[i].get('href')).netloc
						site_domain = urlparse(links[i].get(url)).netloc

						matcher = difflib.SequenceMatcher(None, link_domain, site_domain).ratio()

						if (matcher >= 0.60):
							matchers.append(str(link_domain))
							match_percents.append(str(matcher * 100) + "%")

				if (len(matchers) > 0):
					for x in range(0, len(matchers) - 1):
						match_resp.update({matchers[x]: match_percents[x]})
						pass

				if match_resp:
					RelatedLinks = match_resp
				else:
					RelatedLinks = {"Not found":""}

			# Возвращаем результат в формате json

			return json.dumps({
					"Credentials: ": Credentials,
					"PaymentFileds: ": PaymentFileds,
					"DeadLinks": DeadLinks,
					"RelatedLinks": RelatedLinks,

				})

			pass

		except Exception as e:
			raise e