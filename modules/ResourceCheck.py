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
	Этот метод класса скачивает и возвращает html-данные сайта
	'''
	def getDataFromSite(url):
		r = requests.get(url)

		return r.text

	def returnVerdictInJson():
		

	'''
	Это основной метод, который делает все действия.
	Из класса вызывается только он.
	'''
	@staticmethod
	def Scan(url):
		soup = BeautifulSoup(getDataFromSite(url), 'html.parser')


