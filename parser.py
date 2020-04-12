import requests
import re
import xlwt
from collections import Counter


def write_to_excel():
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

    ws = wb.add_sheet('Отфильтрованные тиражы')

    wb.save('all_tirags.xls')


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
                    write_to_excel()
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
            write_to_excel()
            f.write(''.join(tuple(list_of_new_tirags[::-1])))
            print("Все данные считаны")


if __name__ == '__main__':
    write_to_excel()