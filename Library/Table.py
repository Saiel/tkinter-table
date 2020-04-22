# -*- coding: utf-8 -*-
"""
Модуль работы с таблицей

Автор: Зайцев А.Д.
"""

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mb

# Список заголовков колонок и их типы
headers = ()
headerTypes = {}

# Таблица
table = ttk.Treeview
font = ('arial', 12)
fontHead = ('arial', 11, 'bold')
mainColor = 'light blue'

def addNew():
	"""
	Процедура добавления новой записи
	Параметров нет
	Ничего не возвращает
	Автор: Зайцев А.Д.
	"""
	i = '0'
	for i in table.get_children():
		pass
	i=str(int(i)+1)
	empty = [''] * len(headers)
	table.insert('', 'end', iid=i, values=empty)
	clearSelection()
	table.selection_add(i)
	change('Добавить')


def clearSelection():
	"""
	Процедура очистки выделения
	Параметров нет
	Ничего не возвращает
	Автор: Зайцев А.Д.P
	"""
	for i in table.get_children():
		table.selection_remove(i)


def popup(x, y):
	"""
	Процедура вызова всплывающего меню
	x, y - координаты меню
	Ничего не возвращает
	Автор: Зайцев А.Д.
	"""
	menu = tk.Menu(tearoff=0)
	menu.add_command(label='Добавить', command=addNew)
	if len(table.selection()) != 1:
		menu.add_command(label='Изменить', command=change, state='disabled')
	else:
		menu.add_command(label='Изменить', command=change)
	menu.add_command(label='Удалить', command=deleteSelected)
	menu.add_command(label='Очистить выделение', command=clearSelection)
	menu.post(x, y)


def onRB(event):
	"""
	Событие на нажатие ПКМ
	Вызвает popup(x,y)
	Автор: Зайцев А.Д.
	"""
	row = table.identify_row(event.y)
	if 'Control' not in str(event) and row not in table.selection():
		clearSelection()
	table.selection_add(row)
	popup(event.x_root, event.y_root)


def deleteSelected():
	"""
	Процедура удаления выделенных записей
	Параметров нет
	Ничего не возвращает
	Автор: Зайцев А.Д.
	"""
	if len(table.selection()) != 0:
		if mb.askyesno(title='Удалить', message='Вы уверены?'):
			for i in table.selection():
				table.delete(i)


def onDel(event):
	"""
	Событие на нажатие клавиши Del
	Вызывает deleteSelected()
	Автор: Зайцев А.Д.
	"""
	deleteSelected()


def onOKChange(win, vals={}):
	"""
	Событие на нажатие кнопки ОК в меню изменения записи
	win - окно изменения записи
	vals - строки, связанные с полями ввода
	Ничего не возвращает
	Автор: Зайцев А.Д.
	"""
	values = []
	invalidHeaders = []
	for head in headers:
		columnType = headerTypes[head]
		try:
			values.append(columnType(vals[head].get()))
		except ValueError:
			invalidHeaders.append(head)
		if columnType == str and vals[head].get() == '':
			invalidHeaders.append(head)
	if len(invalidHeaders) != 0:
		mb.showwarning('Предупреждение',
						 'Некорректный формат ввода: '+', '.join(invalidHeaders))
	else:
		win.destroy()
		table.item(table.selection(), values=values)


def onCancChange(win, vals={}, title=''):
	"""
	Событие на кнопку Отмена в меню изменения записи
	win - окно изменения записи
	vals - строки, связанные с полями ввода
	title - заголовок окна
	Ничего не возвращает
	Автор: Зайцев А.Д.
	"""
	if title == 'Изменить':
		win.destroy()
	else:
		isFullEmpty = True
		isPartlyEmpty = True
		for v in vals:
			isFullEmpty = vals[v].get() == '' and isFullEmpty
			isPartlyEmpty = vals[v].get() == ''

		quest = 'В полях ввода остались введенные значения.\
		Вы уверены, что хотите отменить добавление?'
		if isFullEmpty:
			table.delete(table.selection())
			win.destroy()
		else:
			if isPartlyEmpty:
				if mb.askyesno('Добавление', quest):
					table.delete(table.selection())
					win.destroy()


def empty():
	"""
	Пустая функция
	Автор : Зайцев А.Д.
	"""
	pass


def change(title='Изменить'):
	"""
	Процедура изменения записи в таблице
	title - заголовок окна (может использоваться для добавления)
	Ничего не возвращает
	Автор: Зайцев А.Д.
	"""
	if len(table.selection()) == 1:
		row = table.selection()
		row = dict(zip(headers, table.item(row, 'value')))
		values = {}

		win = tk.Toplevel(padx=5, pady=5, bg=mainColor)
		win.title(title)
		win.focus_set()
		win.grab_set()
		# Запрет на закртыие окна кнопкой Закрыть
		win.protocol('WM_DELETE_WINDOW', lambda : empty())


		mainFrame = ttk.Frame(win)
		mainFrame.pack(side='left', anchor='nw')

		for head in headers:
			frame = ttk.Frame(mainFrame)
			frame.pack(side='top')
			values[head] = tk.StringVar()
			values[head].set(row[head])
			ttk.Label(frame, text=head, width=8).pack(side='left', anchor='w')
			ttk.Entry(frame, textvar=values[head]).pack(side='right')

		butOk = ttk.Button(win, text='OK',
							 command=lambda f=values: onOKChange(win, f))
		butOk.pack(side='top', anchor='n')
		butCancel = ttk.Button(win, text='Отмена', command=lambda f=values:
								  onCancChange(win, f, title))
		butCancel.pack(side='top', anchor='n')

		win.resizable(False, False)


def onDoubleLB(event):
	"""
	Событие на двойной клик
	Вызывает onChange()
	Автор: Зайцев А.Д.
	"""
	change('Изменить')


def getDataBase(onlySelected=False):
	"""
	Функция получения базы данных из таблицы
	onlySelected - сделать базу данных только из выделенных
	Возвращает базу данных
	Автор: Зайцев А.Д.
	"""
	result = {}
	if onlySelected:
		for j in table.selection():
			result[int(j)] = dict(zip(headers, table.item(j)['values']))
	else:
		for j in table.get_children():
			result[int(j)] = dict(zip(headers, table.item(j)['values']))
			for k in result[int(j)]:
				result[int(j)][k] = headerTypes[k](result[int(j)][k])
	return result


def updateTable(base={}, columns=(), types={}):
	"""
	Процедура оюновления создержимого таблицы
	base - база данных
	columns - список названий столбцов
	types - словарь типов столбцов
	Ничего не возвращает
	Автор: Зайцев А.Д.
	"""
	for i in table.get_children():
		table.delete(i)

	for col in columns:
		table.heading(col, text=col, anchor='center')
		table.column(col, anchor='center')

	for i in base:
		values = [base[i][j] for j in columns]
		table.insert('', 'end', iid=i, values=values)


def createTable(master=None, base={}, columns=(),
				  types={}, font=font, fontHead=fontHead, mainCol=mainColor):
	"""
	Функция создания таблицы
	master - родительский виджет
	base - база данных
	columns - список названий столбцов
	types - словарь типов столбцов
	Возвращает созданную таблицу
	Автор: Зайцев А.Д.
	"""
	global table
	global headers
	global mainColor
	mainColor = mainCol
	headers = columns
	global headerTypes
	headerTypes = types

	ttk.Style().configure('Treeview', font=font)
	ttk.Style().configure('Treeview.Heading', font=fontHead)

	table = ttk.Treeview(master, columns=columns, show='headings', height=20)

	scrl = ttk.Scrollbar(master, command=table.yview)
	table.configure(yscrollcommand=scrl.set)

	for col in columns:
		table.heading(col, text=col, anchor='center')
		table.column(col, anchor='center')
		if types[col] in (int, float):
			table.column(col, width=65)
		else:
			table.column(col, width=200)

	for i in base:
		values = [base[i][j] for j in columns]
		table.insert('', 'end', iid=i, values=values)

	table.bind('<Delete>', onDel)
	table.bind('<Button-3>', onRB)
	table.bind('<Double-Button-1>', onDoubleLB)

	scrl.pack(side = 'right', anchor='e', fill = 'y')
	table.pack(side='left', anchor='center', expand=1)

	return table


#Test
#import DataBase as db #!!!
#root = tk.Tk()
#table = createTable(root, db.testBase(), db.columns, db.types)
#tk.mainloop()
