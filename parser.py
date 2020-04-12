import requests
import re


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


if __name__ == '__main__':
    parse()