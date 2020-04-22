# -*- coding: utf-8 -*-
"""
Модуль работы с базой данных

Авторы: Зайцев А.Д., Ерофеева А.Е.
"""

columns = ("Name", "Type", "Price", "E.Value", "Weight", "Suplier")
types = dict(zip(columns, (str, str, int, int, int, str)))


def testBase():
	"""
	Тестовая база данных
	Параметров нет
	Возвращает словарь словарей
	Автор: Ерофеева А.Е.
	"""
	lst = []
	lst.append(["Radish"     , "vegetable", 80 , 19,  4 , "Mr. Proper"      ])
	lst.append(["Eggplant"   , "vegetable", 50 , 27,  10, "Mr. Potter"      ])
	lst.append(["Cabbage"    , "vegetable", 30 , 27,  10, "Mr. Darth Vader" ])
	lst.append(["Potato"     , "vegetable", 25 , 77,  15, "Mr. Dumbledore"  ])
	lst.append(["Onion"      , "vegetable", 20 , 40,  10, "Mr. Stark"       ])
	lst.append(["Carrot"     , "vegetable", 30 , 41,  10, "Mr. Shrek"       ])
	lst.append(["Сucumber"   , "vegetable", 70 , 16,  8 , "Mr. Batman"      ])
	lst.append(["Tomato"     , "vegetable", 80 , 18,  6 , "Mr. Terminator"  ])
	lst.append(["Pepper"     , "vegetable", 120, 27,  5 , "Mr. Bond"        ])
	lst.append(["Apricot"    , "fruit"    , 180, 41,  3 , "Mr. Logan"       ])
	lst.append(["Banana"     , "fruit"    , 55 , 89,  12, "Mr. Jack Sparrow"])
	lst.append(["Grape"      , "fruit"    , 110, 67,  7 , "Mr. Rambo"       ])
	lst.append(["Grapefruit" , "fruit"    , 80 , 47,  4 , "Mr. Dumbledore"  ])
	lst.append(["Pear"       , "fruit"    , 80 , 57,  13, "Mr. Batman"      ])
	lst.append(["Lemon"      , "fruit"    , 80 , 29,  8 , "Mr. Jack Sparrow"])
	lst.append(["Tangerine"  , "fruit"    , 50 , 33,  10, "Mr. Proper"      ])
	lst.append(["Peach"      , "fruit"    , 220, 39,  3 , "Mr. Bond"        ])
	lst.append(["Apple"      , "fruit"    , 65 , 52,  18, "Mr. Terminator"  ])
	lst.append(["Kiwi"       , "fruit"    , 80 , 61,  6 , "Mr. Rambo"       ])
	lst.append(["Mango"      , "fruit"    , 180, 60,  2 , "Mr. Shrek"       ])
	lst.append(["Pomegranate", "fruit"    , 105, 85,  4 , "Mr. Stark"       ])
	lst.append(["Watermelon" , "berry"    , 25 , 23,  6 , "Mr. Darth Vader" ])
	lst.append(["Cowberry"   , "berry"    , 230, 53,  2 , "Mr. Bond"        ])
	lst.append(["Cherry"     , "berry"    , 280, 52,  3 , "Mr. Jack Sparrow"])
	lst.append(["Blackberry" , "berry"    , 250, 35,  2 , "Mr. Batman"      ])
	lst.append(["Strawberry" , "berry"    , 220, 33,  3 , "Mr. Dumbledore"  ])
	lst.append(["Raspberry"  , "berry"    , 180, 34,  1 , "Mr. Darth Vader" ])

	return {i+1: dict(zip(columns, lst[i])) for i in range(0, len(lst))}


def isNum(test=""):
	"""
	Функция проверки строки на число
	test - проверяемая строка
	Возвращает True или False в зависимости от результата проверки
	Автор: Ерофеева А.Е.
	"""
	if test.replace('.', '', 1).isdigit() or test.replace(',', '', 1).isdigit():
		return True
	else:
		return False


def changeRecord(record={}, ch_column='', userText=''):
	"""
	Функция изменения ячейки записи
	record - исходная запись
	ch_column - ячейка изменяемой записи
	userText - новое значение ячейки
	Возвращает измененную запись
	Возвращает неизмененную запись при неудачной попытке
	Автор: Зайцев А.Д.
	"""

	ch_type = types[ch_column] # Тип изменяемой ячейки
	if record.get(ch_column) is None:
		print("Неверный столбец")
	elif ch_type in (float, int) and not isNum(userText):
		print("Некорректные данные")
	else:
		# Замена запятой на точку при введении вещ. числа
		if ch_type == float:
			userText = userText.replace(',', '.', 1)
		record[ch_column] = ch_type(userText)
	return record


def createRecord(db=testBase(), values=("", "", 0, 0, 0.0, "")):
	"""
	Функция создания новой записи в базе данных
	db - исходная база данных
	values - данные в новой записи
	Возвращает базу данных с новой записью
	Автор: Зайцев А.Д.
	"""

	newKey = max(db.keys()) + 1
	db[newKey] = dict(zip(columns, values))
	return db


def deleteRecord(db=testBase(), key=-1):
	"""
	Функция удаления записи из базы данных
	db - исходная база данных
	key - номер удаляемой записи записи
	Возвращает базу данных без удаляемой записи
	Автор: Ерофеева А.Е.
	"""

	if db.get(key) is not None:
		db.pop(key)
	return db


def writeToFile(base=testBase(), path="file"):
	"""
	Функция записи базы в файл
	Параметры: base - объект для сохранения
	path - путь к файлу
	Автор: Ерофеева А.Е.
	"""
	import pickle
	file = open(path, 'wb')
	pickle.dump(base, file)
	file.close()


def readFromFile(path="file"):
	"""
	Функция извлечения базы из файла
	Параметры: путь к файлу
	Возващает объект из файла
	Автор: Ерофеева А.Е.
	"""
	import pickle
	file = open(path, 'rb')
	tmp = pickle.load(file)
	file.close()
	return tmp


def numSearch(base, key, valMin=0, valMax=100000):
	"""
	Функция поиска элементов по числовому столбцу от минимального до
	максимального значения
	Параметры: base - база
	key - ключ, по которому ведется поиск
	valMin, valMax - макс. и мин. значения
	Возвращает список ключей
	Автор: Ерофеева А.Е.
	"""
	valMax = int(valMax)
	valMin = int(valMin)
	x = []
	for i in base:
		if valMin <= base[i][key] <= valMax:
			x.append(i)
	return x


def strSearch(base, key, val):
	"""
	Функция поиска строковых элементов по одинаковым значениям
	Параметры: base - база для поиска
	key - ключ, по которому ведется поиск
	val - строковое значение для поиска
	Возвращает список ключей
	Автор: Ерофеева А.Е.
	"""
	x = []
	for i in base:
		if base[i][key] == val:
			x.append(i)
	return x


def getAverage(base, key):
	"""
	Функция подсчета среднего значения элементов столбца базы
	Параметры: base - база для поиска
	key - ключ, по которому ведется поиск
	Возвращает ср. значение
	Автор: Ерофеева А.Е.
	"""
	x = 0
	i = 0
	for j in base:
		x += base[j][key]
		i += 1
	return x/i


def getDispersion(base, key):
	"""
	Функция подсчета выборочной дисперсии элементов стоблбца базы
	Параметры: base - база для поиска
	key - ключ, по которому ведется поиск
	Возвращает значение выборочной дисперсии
	Автор: Ерофеева А.Е.
	"""
	x = 0
	average = getAverage(base, key)
	i = 0
	for j in base:
		x += (base[j][key] - average) ** 2
		i += 1
	return x/i


def pushReport(data, info = "информация))" + '\n', path="отчет.txt"):
	"""
	Добавляет данные в конец отчета
	Параметры: data - данные для добавления
	info - информация о данных, размешающаяся в файле
	path - путь к файлу
	Автор: Ерофеева А.Е.
	"""
	file = open(path, 'a')
	file.write(info + str(data) + '\n')
	file.close()