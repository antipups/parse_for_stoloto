# from kivy.app import App
# from kivy.uix.button import Button
#
#
# class MyApp(App):
#     def build(self):
#         return Button()
#
#
# if __name__ == '__main__':
#     MyApp().run()


# import pymysql
# connect = pymysql.Connect(user='root', password='', db='test', host='localhost')
# cursor = connect.cursor()
# # cursor.execute('SELECT * FROM main_lot')
# cursor.execute('INSERT INTO sex (first_col, sec_col) VALUES (20, 20), (30, 30)')
# connect.commit()
# connect.close()


# class execute:
#     def __init__(self):
#         self.connect = pymysql.Connect(user='root', password='', db='school_work', host='localhost')
#
#     def __enter__(self):
#         return self.connect.cursor()
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         print('Конеект закрыт')
#         self.connect.close()
#
#
# with execute() as cursor:
#     cursor.execute('SELECT * FROM main_lot')
#     print(cursor.fetchall())
#     # cursor.execute('INSERT INTO main_country (sex, keks) VALUES ("")');
#     raise Exception


# for i in range(0, 230, 50):
#     print(i)
# else:
#     print(i)


# try:
#     raise Exception
# except:
#     try:
#         print(1/0)
#     except ZeroDivisionError:
#         print('lox')


# import pymysql.cursors
# import config

# paramstyle = "%s"
#
# def connect():
#     """
#      Подключение к базе данных
#     """
#     return pymysql.connect(
#         config.db_host,
#         config.db_user,
#         config.db_password,
#         config.db_database,
#         use_unicode=True,
#         charset=config.db_charset,
#         cursorclass=pymysql.cursors.DictCursor)
#
#
# def execute(sql, *args, commit=False):
#     """
#      Формат запроса:
#      execute('<Запрос>', <передаваемые параметры>, <commit=True>)
#     """
#     db = connect()
#     cur = db.cursor()
#     try:
#         cur.execute(sql % {"p": paramstyle}, args)
#     except pymysql.err.InternalError as e:  # обработайся тут сука
#         if sql.find('texts') == -1:
#             print('Cannot execute mysql request: ' + str(e))
#         return 'Error'
#     except ValueError:  # если вдруг ошибка с символами
#         return 'unsupported format character'
#     if commit:
#         db.commit()
#         db.close()
#         return True
#     else:
#         ans = cur.fetchall()
#         db.close()
#         return ans


import xlrd, xlwt


import random
all_numbers = tuple(str(random.randint(0, 9)) for x in range(150))
amount_of_numbers = {'0': 0,
                     '1': 0,
                     '2': 0,
                     '3': 0,
                     '4': 0,
                     '5': 0,
                     '6': 0,
                     '7': 0,
                     '8': 0,
                     '9': 0}

print(all_numbers)
for i in all_numbers:
    print(i)
    for j in i:
        amount_of_numbers[j] += 1

print(amount_of_numbers, sum(x for x in amount_of_numbers.values()))
wb = xlwt.Workbook()
ws = wb.add_sheet('Test')
for i in range(150):
    ws.write(i, 0, int(all_numbers[i]))
i = 3

for key, value in amount_of_numbers.items():
    ws.write(0, i, int(key))
    ws.write(1, i, value)
    ws.write(2, i, f'=(-100*0,1)/(100*0,1)')
    i += 1

wb.save('sex.xls')