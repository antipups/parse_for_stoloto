# from kivy.app import App
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.button import Button
# from kivy.uix.screenmanager import ScreenManager, Screen
# import xlrd, xlwt
#
#
# class MyApp(App):
#     def build(self):
#         sm = ScreenManager()
#         screen = Screen()
#         bl = BoxLayout(orientation="vertical")
#         bl.add_widget(Button(text="1",
#                              on_press=lambda x: sm.switch_to(screen1)))
#         bl.add_widget(Button(text="2",
#                              on_press=lambda x: sm.switch_to(screen2)))
#         screen.add_widget(bl)
#         screen1 = Screen(name="id1")
#         screen2 = Screen(name="id2")
#         sm.add_widget(screen)
#         sm.add_widget(screen1)
#         sm.add_widget(screen2)
#         return sm
#
#
# if __name__ == '__main__':
#     MyApp().run()


import xlrd, xlwt

wb = xlwt.Workbook()
ws = wb.add_sheet('Архив')

with open('test.txt', 'r', encoding='utf-8') as f:
    old_tirags = tuple(f.readlines())

title = ('Тираж', ) + tuple(x for x in range(1, 21)) + ('Сумма очков', )

for i in enumerate(title):
    ws.write(0, i[0], i[1])

for index, one_tirage in enumerate(old_tirags[::-1]):
    ws.write(index + 1, 0, int(one_tirage[:one_tirage.find('; ')]))
    one_tirage = one_tirage[one_tirage.find('; ') + 2:].split(', ')
    one_tirage[-1] = one_tirage[-1][:-1]

    for k in enumerate(one_tirage):
        ws.write(index + 1, k[0] + 1, int(k[1]))
    else:
        ws.write(index + 1, 21, xlwt.Formula(' + '.join((chr(sym) + str(index + 2) for sym in range(66, 86)))))

wb.save('all_tirags.xls')