import requests
import json
import difflib
from bs4 import BeautifulSoup
from urllib.parse import urlparse

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
		PaymentFileds = False
		DeadLinks = 0
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

			# Теперь обработаем ссылки...

			links = soup.find('a')
			matchers = []
			match_percents = []

			for link in links:
				# Ищем ссылки, "прокликиваем" их
				breakpoint()
				if (requests.get(link['href']) == 404):
					DeadLinks += 1

				# Сравниваем домен самого сайта со ссылкой

				if (urlparse(link[href]).netloc != urlparse(url).netloc):
					link_domain = urlparse(link[href]).netloc
					site_domain = urlparse(url).netloc

					matcher = difflib.SequenceMatcher(None, link_domain, site_domain).ratio()

					if (matcher >= 0.70):
						matchers.Append(str(link_domain))
						match_percents.Append(str(matcher * 100) + "%")

			if (len(matchers) > 0):
				match_resp = {}

				for x in range(0, len(matchers) - 1):
					match_resp.Append({matchers[x], match_percents[x]})
					pass

		breakpoint()


		# Возвращаем результат в формате json

		return json.dumps({
				"Credentials: ": Credentials,
				"PaymentFileds: ": PaymentFileds,
				"DeadLinks": DeadLinks,
				"RelatedLinks": RelatedLinks,

			})