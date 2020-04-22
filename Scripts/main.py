# -*- coding: utf-8 -*-
"""
Основной модуль

Авторы: Зайцев А.Д., Николенко М.В, Ерофеева А.
"""

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fd
import tkinter.messagebox as mb

import configparser
import os
import sys


config = configparser.ConfigParser()

config.read_file(open(os.path.join(os.path.dirname(
        os.path.realpath(__file__)), "Config.ini"), "r", encoding="utf-8"))

for path in config['path']:
    config['path'][path] = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), config['path'][path])

sys.path.append(config['path']['parent'])

from Library import DataBase as db
from Library import Table as tb


root = tk.Tk()
root.title('Data base')


def readProps():
    """
    Процедура чтения настроек приложения
    Автор: Зайцев А.Д.
    """
    f = open('props.ini', 'r')
    props = {}
    for linerow in f.readlines():
        linerow = linerow.replace('\n', '')
        i = linerow.find('#')
        if i != -1:
            linerow = linerow[:i]
        lines = linerow.split('=')
        if len(lines) > 1:
            lines[0] = lines[0].rstrip()
            props[lines[0]] = lines[1]
    return props


props = readProps()


def setProp(val=''):
    if val in props: return props[val]
    else:
        return None


mainColor  = setProp('mainCol')
subColor   = '#'+setProp('subCol')
fontBut    = setProp('fontBut')
heightBut  = setProp('heightBut')
widthBut   = setProp('widthBut')
padButx    = setProp('padButx')
padButy    = setProp('padButy')
fontTable  = (setProp('fontTable'),
              setProp('fontTableSize'), setProp('fontTableType')
             )
fontHeader = (setProp('fontHeader'),
              setProp('fontHeaderSize'), setProp('fontHeaderType')
             )
fontL      = (setProp('fontLab'), setProp('fontLabSize'), setProp('fontLabType'))

S = ttk.Style()
S.configure('TButton', width=widthBut, height=heightBut,
            font=fontBut, adx=padButx, pady=padButy, background=subColor, border=subColor)
S.configure('TCombobox', font=fontBut,
            padx=padButx, pady=padButy,background=mainColor)
S.configure('TLabel',    font=fontL,
            padx=padButx, pady=padButy, background=mainColor)
S.configure('TFrame', background=mainColor)
S.configure('TCheckbutton', background=mainColor)

root.config(bg=mainColor)

def search(win, bools={}, strs={}):
    """
    Функция поиска по выбранным параметрам
    Параметры: win - отцовское окно
    bools - словарь, определяющий, по каким
    параметрам делать поиск
    strs - список StringVars, связанных с полями ввода
    Автор: Зайцев А.
    """
    keys = []
    base = tb.getDataBase()
    for i in bools:
        if bools[i].get():
            if db.types[i] not in (int, float):
                ## Строки
                strs[i].set(strs[i].get().rstrip())
                if strs[i].get() == '':
                    mb.showwarning('Внимание', 'Введите непустые строки')
                    return
                keys.extend(db.strSearch(base, i, strs[i].get()))
                print(i, keys)
            else:
                ## Числа
                if (strs[i][1].get().rstrip() == '' and
                    strs[i][2].get().rstrip() == ''
                ):
                    # Если поля промежутка пустые ищем конкретное значение
                    keys.extend(db.numSearch(base, i,
                                             strs[i][0].get(), strs[i][0].get()))
                else:
                    if strs[i][1].get().rstrip() == '':
                        keys.extend(db.numSearch(base, i,
                                                 0, strs[i][2].get()))
                    elif strs[i][2].get().rstrip() == '':
                        keys.extend(db.numSearch(base, i,
                                                 strs[i][1].get(), 100000000))
                    else:
                        i1 = int(strs[i][1].get())
                        i2 = int(strs[i][2].get())
                        if i1 > i2:
                            mb.showwarning('Внимание', 'Некорректный диапазон')
                            return
                        keys.extend(db.numSearch(base, i,
                                                 i1, i2))
                print(i, keys)
    tb.table.selection_add(keys)
    if len(keys) == 0:
        mb.showinfo('Поиск', 'Ничего не найдено')
    else:
        win.destroy()


def searchEl(master):
    """
    Открывающееся окно при нажатии на кнопку поиска из основого меню
    Параметры: master - родительское окно
    Автор: Николенко М.В,
    """
    base = tb.getDataBase()
    if len(base) == 0:
        mb.showerror('Ошибка', 'База данных пуста')
        return
    win = tk.Toplevel(master, bg=mainColor)
    win.title('Поиск')

    win.grab_set()
    win.focus_set()

    columns = {i: [] for i in db.columns}

    for i in base:
        for j in base[i]:
            if base[i][j] not in columns[j]:
                columns[j].append(base[i][j])

    checks = {}
    strings = {}
    for i in db.columns:
        fr = ttk.Frame(win, padding=3)
        fr.pack(side='top', anchor='w')

        # Флаг
        chBut = ttk.Checkbutton(fr, text=i, width=8)
        chBut.pack(side='left', anchor='n')
        checks[i] = tk.BooleanVar(chBut)
        chBut.config(variable=checks[i], onvalue=True, offvalue=False)

        if db.types[i] not in (int, float):
            ## Строковое
            # Поле для ввода
            frSub = ttk.Frame(fr)
            frSub.pack(side='left', anchor='n')

            strings[i] = tk.StringVar()
            ttk.Combobox(frSub, width=15,
                         textvariable=strings[i],
                         values=columns[i]
            ).pack(side='top', anchor='w')
            ttk.Label(frSub, text=' ').pack(side='top', anchor='w')
        else:
            ## Числовое
            # Поле для ввода
            strings[i] = [tk.StringVar(), tk.StringVar(), tk.StringVar()]
            ttk.Entry(fr, width=18,
                      textvariable=strings[i][0]
            ).pack(side='left', anchor='n')

            # Поле для ввода минимального значения
            frame1 = tk.Frame(fr, padx=2, bg=mainColor)
            frame1.pack(side='left', anchor='n')

            ttk.Entry(frame1,
                      textvariable=strings[i][1],
                      width=12
            ).pack(side='top', anchor='w')
            ttk.Label(frame1,
                      text='min = '+str(min(columns[i]))
            ).pack(side='top', anchor='w')

            # Строка
            ttk.Label(fr, text='≤ x ≤').pack(side='left', anchor='n')

            # Поле для ввода максимального значения
            frame2 = tk.Frame(fr, padx=2, bg=mainColor)
            frame2.pack(side='left', anchor='n')

            ttk.Entry(frame2,
                      textvariable=strings[i][2],
                      width=12
            ).pack(side='top', anchor='w')
            ttk.Label(frame2,
                      text='min = '+str(max(columns[i]))
            ).pack(side='top', anchor='w')

    ttk.Button(win, text='Поиск',
               command=lambda b=checks, s=strings, w=win: search(w, b, s)
    ).pack(side='bottom', anchor='s')
    win.resizable(False, False)


def importEl():
    """
    Открывающееся окно при нажатии на кнопку импорта из основого меню

    Автор: Николенко М.В,
    """
    fileName = fd.askopenfilename(filetypes=[("Data base", "*.bd"),
                                             ("all files","*.*")])
    if fileName:
        base = db.readFromFile(fileName)
        tb.updateTable(base, db.columns, db.types)


def exportEl():
    """
    Открывающееся окно при нажатии на кнопку экспорта из основого меню

    Автор: Николенко М.В,
    """
    base = tb.getDataBase()
    if len(base) == 0:
        mb.showerror('Ошибка', 'База данных пуста')
        return

    fileName = fd.asksaveasfilename(filetypes=(("Data base","*.bd"),
                                               ("all files","*.*")))
    if fileName:
        if not fileName.endswith('.bd'):
            fileName = fileName + '.bd'
        db.writeToFile(base, fileName)


def reportEl(master):
    """
    Открывающееся окно при нажатии на кнопку поиска из основого меню
    Параметры: master - отцовское окно
    Автор: Николенко М.В.
    """
    base = tb.getDataBase()
    if len(base) == 0:
        mb.showerror('Ошибка', 'База данных пуста')
        return

    win = tk.Toplevel(master, padx=30, pady=5, bg=mainColor)
    win.title('Отчет')
    win.resizable(False, False)

    frame = ttk.Frame(win)
    frame.pack(side='top', anchor='nw')

    check = ttk.Checkbutton(frame, text='Только выделенные')
    check.pack()
    isSel = tk.BooleanVar(check)
    check.config(variable=isSel, onvalue=True, offvalue=False)

    if len(tb.table.selection()) == 0:
        check.config(state='disabled')

    values = []
    for i in db.columns:
        if db.types[i] in (int, float):
            values.append(i)
    box = ttk.Combobox(frame, state='readonly', values=values)
    box.set('<Столбец>')
    box.pack()

    but = ttk.Button(frame, text = "Отчет", padding=2,
                    command=lambda b=box, boo=isSel , m=win: report(b, boo, m))
    but.pack(side='bottom')

    win.grab_set()
    win.focus_set()
    win.wait_window()


def report(box, boo, win):
    """
    Функция составления отчета по выбранным параметрам
    Параметры: box - выпадающее меню их отцовского
    окна. Подается для получения значения из него.
    boo - отчет только по выделенным
    win - отцовское окно
    Автор: Николенко М., Зайцев А.
    """
    key = box.get()
    base = tb.getDataBase(boo.get())
    if key != '<Столбец>':
        fileName = fd.asksaveasfilename(filetypes=(("Text files","*.txt"),
                                                   ("all files","*.*")))
        if fileName:
            f = open(fileName, 'w')
            f.write('Отчет "' + key + '"' + '\n')
            f.close()
            db.pushReport(db.getDispersion(base, key),
                          "Дисперсия:", fileName)
            db.pushReport(db.getAverage(base, key),
                          "Среднее значение:", fileName)
            db.pushReport(len(base),
                          "Кол-во элементов:", fileName)
            win.destroy()
    else:
        mb.showerror("Ошибка", "Выберете столбец")



butFrame = ttk.Frame(root, padding=3)
butFrame.pack(side='top', anchor='nw', fill='x')

searchBut = ttk.Button(butFrame, text="Поиск",
                       command=lambda r=root: searchEl(r))
searchBut.pack(side='left',padx=padButx, pady=padButy)

importBut = ttk.Button(butFrame, text="Импорт", command=importEl)
importBut.pack(side='left', padx=padButx, pady=padButy)

exportBut = ttk.Button(butFrame, text="Экспорт", command=exportEl)
exportBut.pack(side='left', padx=padButx, pady=padButy)

reportBut = ttk.Button(butFrame, text="Отчет",
                       command=lambda r=root: reportEl(r))
reportBut.pack(side='left', padx=padButx, pady=padButy)

ttk.Button(butFrame, text='Рук-во',
           command=lambda:os.startfile(config['path']['parent']+'/Notes/Руководство пользователя.doc')).pack(side='left', padx=padButx, pady=padButy)

ttk.Separator(root, orient='horizontal').pack(fill='x')

#child = tk.Toplevel(root)
#child.title('child')

tb.createTable(root, db.readFromFile(config['path']['parent']+'/Data/Data.bd'),
               db.columns, db.types, fontTable, fontHeader, mainColor)

root.resizable(False, False)

tk.mainloop()

