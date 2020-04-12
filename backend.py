import os
import time
import requests
import re
import xlwt
import psutil


def write_to_excel(amount):
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Архив')

    # для подсчёта серий
    three = 800
    four = 810
    fifth = 820

    dict_of_summ = {three: 0,
                    four: 0,
                    fifth: 0, }

    max1, max2, max3 = 0, 0, 0

    with open('test.txt', 'r', encoding='utf-8') as f:
        old_tirags = tuple(f.readlines())

    title = ('Тираж',) + tuple(x for x in range(1, 21)) + ('Сумма очков', '', 'Кол-во серий < 800', 'Кол-во серий < 810', 'Кол-во серий < 820')

    for i in enumerate(title):
        ws.write(0, i[0], i[1])

    for index, one_tirage in enumerate(old_tirags[::-1]):
        ws.write(index + 1, 0, int(one_tirage[:one_tirage.find('; ')]))
        one_tirage = one_tirage[one_tirage.find('; ') + 2:].split(', ')
        one_tirage[-1] = one_tirage[-1][:-1]
        one_tirage = tuple(int(x) for x in one_tirage)

        for k in enumerate(one_tirage):
            ws.write(index + 1, k[0] + 1, k[1])
        else:
            one_summ = sum(one_tirage)
            ws.write(index + 1, 21, one_summ)

            # серия
            if one_summ < three:
                if max1 >= dict_of_summ[three]:
                    max1 += 1
                    dict_of_summ[three] = max1
                else:
                    max1 += 1
            else:
                max1 = 0

            if one_summ < four:
                if max2 >= dict_of_summ[four]:
                    max2 += 1
                    dict_of_summ[four] = max2
                else:
                    max2 += 1
            else:
                max2 = 0

            if one_summ < fifth:
                if max3 >= dict_of_summ[fifth]:
                    max3 += 1
                    dict_of_summ[fifth] = max3
                else:
                    max3 += 1
            else:
                max3 = 0

    ws.write(1, 23, dict_of_summ.get(800))
    ws.write(1, 24, dict_of_summ.get(810))
    ws.write(1, 25, dict_of_summ.get(820))

    wb.save('all_tirags.xls')
    if amount != 0:
        sorting(amount)
    os.startfile('all_tirags.xls')


def parse():
    # задаем начальные данные
    data = {
        'page': '1',
        'mode': 'date',
        'super': 'false',
        'from': '10.10.2015',
        'to': '12.04.2020',
    }
    request = requests.post('https://www.stoloto.ru/draw-results/keno/load', data=data)

    old_tirags = list()
    with open('test.txt', 'r', encoding='utf-8') as f:
        old_tirags = tuple(f.readlines())

    last_tirag = str()
    if len(old_tirags) > 1:
        last_tirag = old_tirags[-1]

    list_of_new_tirags = list()

    with open('test.txt', 'w', encoding='utf-8') as f:
        while request.status_code == 200:
            request = request.text
            for one_tirag in re.findall(r"/keno/archive/[^⚲]*</span>", request):
                date = re.search(r'\d{6}', one_tirag).group() + '; '
                if last_tirag.startswith(date):
                    f.write(''.join(old_tirags + tuple(list_of_new_tirags[::-1])))
                    print('Данные добавлены')
                    return
                else:
                    one_tirag = one_tirag[one_tirag.find('<div class=\\"container cleared\\">'):]
                    bals = re.findall(r'\d\d?\d?', one_tirag)
                    list_of_new_tirags.append(date + ', '.join(bals) + '\n')
            data['page'] = str(int(data.get('page')) + 1)
            request = requests.post('https://www.stoloto.ru/draw-results/keno/load', data=data)
            print("Страница № " + data.get('page'))
        else:
            f.write(''.join(tuple(list_of_new_tirags[::-1])))
            print("Все данные считаны")


def xls_bg_colour(colour):  # для покраски

    """ Colour index
    8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta,
    7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown),
    20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, """

    dict_colour = {"green": 17,
                   "red": 2,
                   "white": 1,
                   "yellow": 5,
                   "gray": 22,
                   "blue": 4,
                   "magenta": 6,
                   "cyan": 7, }
    bg_colour = xlwt.XFStyle()
    p = xlwt.Pattern()
    p.pattern = xlwt.Pattern.SOLID_PATTERN
    p.pattern_fore_colour = dict_colour[colour]
    bg_colour.pattern = p
    return bg_colour


def sorting(amount):
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Тиражы')
    list_of_tirags = list()
    with open('test.txt', 'r', encoding='utf-8') as f:
        list_of_tirags = f.readlines()[:amount]
    ws = wb.add_sheet('Отфильтрованные тиражы')

    title = ('Тираж',) + tuple(x for x in range(1, 21)) + ('Сумма очков', 'MAX', 'MIN', 'Серия MAX', 'Серия MIN', 'Кол-во серий < 800', 'Кол-во серий < 810', 'Кол-во серий < 820')

    for i in enumerate(title):
        ws.write(0, i[0], i[1])

    # для подсчёта серий
    one = 78
    two = 3
    three = 800
    four = 810
    fifth = 820

    dict_of_summ = {one: 0,
                    two: 0,
                    three: 0,
                    four: 0,
                    fifth: 0, }

    max1, max2, max3 = 0, 0, 0
    max4, max5 = 0, 0

    for index, one_tirage in enumerate(list_of_tirags):
        ws.write(index + 1, 0, int(one_tirage[:one_tirage.find('; ')]))
        one_tirage = one_tirage[one_tirage.find('; ') + 2:].split(', ')
        one_tirage[-1] = one_tirage[-1][:-1]
        one_tirage = tuple(int(x) for x in one_tirage)

        max_ = max(one_tirage)
        min_ = min(one_tirage)
        for k in enumerate(one_tirage):
            if k[1] == max_:
                ws.write(index + 1, k[0] + 1, k[1], xls_bg_colour('green'))
            elif k[1] == min_:
                ws.write(index + 1, k[0] + 1, k[1], xls_bg_colour('yellow'))
            else:
                ws.write(index + 1, k[0] + 1, k[1])
        else:
            ws.write(index + 1, 22, max_, xls_bg_colour('green') if max_ > 78 else xls_bg_colour('white'))
            ws.write(index + 1, 23, min_, xls_bg_colour('yellow') if min_ < 3 else xls_bg_colour('white'))

            if max_ > one:
                if max4 >= dict_of_summ[one]:
                    max4 += 1
                    dict_of_summ[one] = max4
                else:
                    max4 += 1
            else:
                max4 = 0

            if min_ < two:
                if max5 >= dict_of_summ[two]:
                    max5 += 1
                    dict_of_summ[two] = max5
                else:
                    max5 += 1
            else:
                max5 = 0

            one_summ = sum(one_tirage)
            ws.write(index + 1, 21, one_summ)

            # серия
            if one_summ < three:
                if max1 >= dict_of_summ[three]:
                    max1 += 1
                    dict_of_summ[three] = max1
                else:
                    max1 += 1
            else:
                max1 = 0

            if one_summ < four:
                if max2 >= dict_of_summ[four]:
                    max2 += 1
                    dict_of_summ[four] = max2
                else:
                    max2 += 1
            else:
                max2 = 0

            if one_summ < fifth:
                if max3 >= dict_of_summ[fifth]:
                    max3 += 1
                    dict_of_summ[fifth] = max3
                else:
                    max3 += 1
            else:
                max3 = 0

    ws.write(1, 24, dict_of_summ.get(one), xls_bg_colour('cyan'))
    ws.write(1, 25, dict_of_summ.get(two), xls_bg_colour('cyan'))
    ws.write(1, 26, dict_of_summ.get(800), xls_bg_colour('green'))
    ws.write(1, 27, dict_of_summ.get(810), xls_bg_colour('green'))
    ws.write(1, 28, dict_of_summ.get(820), xls_bg_colour('green'))
    wb.save('filtred.xls')


if __name__ == '__main__':
    write_to_excel(50)
