import datetime
import os
import threading
import time

from kivy.clock import Clock
from kivy.config import Config
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout

Config.set('graphics', 'width', 450)
Config.set('graphics', 'height', 300)
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import backend


class MyApp(App):

    au = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'Столото'
        self.label = Label(text='Строка состояния - Загрузка...',
                           size_hint_y=.2)
        self.bl = BoxLayout(orientation="vertical")
        threading.Thread(target=self.regular_update, daemon=True).start()
        self.au = True

    def build(self):
        self.bl.add_widget(Button(text='Открыть Excel',
                                  on_press=self.open_file,
                                  size_hint_y=0.3,
                                  disabled=True,
                                  id='button_1'
                                  ))
        table = GridLayout(cols=2,
                           id='grid')
        table.add_widget(Button(text='Обновить',
                                on_press=self.update,
                                disabled=True,
                                id='button_2'))
        table.add_widget(Button(text='Автообновление ВКЛ.',
                                on_press=self.auto_update,
                                disabled=True,
                                id='button_3'))
        for text_button in ('50', '100', '250', '500', '750', '1000'):
            table.add_widget(Button(text=text_button,
                                    on_press=self.sorting,
                                    disabled=True,
                                    id='button_' + text_button))
        self.bl.add_widget(table)
        self.bl.add_widget(self.label)
        return self.bl

    def open_file(self, instance):
        backend.write_to_excel()
        os.startfile('excel.xlsx')

    def sorting(self, instance):
        result_text = backend.sorting(int(instance.text))
        if result_text is not True:
            self.label.text = result_text
        else:
            self.label.text = self.label.text[: self.label.text.find(';') + 1] + ' Отсортированно ' + instance.text

    def update(self, instance):
        warning = 'Перед обновлением,\n закройте Excel файл.\nИ нажмите ещё раз'
        if instance.text != warning:
            instance.text = warning
            return
        else:
            instance.text = 'Данные обновленны.'
        backend.parse()
        result_text = backend.write_to_excel()
        if result_text is not True:
            self.label.text = result_text
        else:
            self.label.text = 'Последнее обновление : ' + datetime.datetime.now().strftime("%H:%M:%S") + ' ;'
        os.startfile('excel.xlsx')

    def auto_update(self, instance):
        if self.au:
            self.au = False
            instance.text = 'Автообновления ОТКЛ.'
        else:
            self.au = True
            instance.text = 'Автообновления ВКЛ.'

    def regular_update(self):
        while self.au:
            backend.parse()
            result_text = backend.write_to_excel()
            if result_text is not True:
                self.label.text = result_text
            else:
                self.label.text = 'Последнее обновление : ' + datetime.datetime.now().strftime("%H:%M:%S") + ' ;'
                self.disable_all(False)
            time.sleep(960)

    def disable_all(self, boolean):
        for widget in self.bl.children:
            if widget.id != 'grid':
                widget.disabled = boolean
            elif widget.id == 'grid':
                for buttons_in_grid in widget.children:
                    buttons_in_grid.disabled = boolean


if __name__ == '__main__':
    MyApp().run()
