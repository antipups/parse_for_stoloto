import os
import time

import psutil
from kivy.config import Config
Config.set('graphics', 'width', 800)
Config.set('graphics', 'height', 600)
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import threading
import backend


class MyApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'Столото'

    def build(self):
        bl = BoxLayout(orientation="vertical")
        bl.add_widget(Button(text='Открыть Excel',
                             on_press=lambda x: os.startfile('all_tirags.xls')))
        bl.add_widget(Button(text='Обновить',
                             on_press=self.update))
        for text_button in ('50', '100', '250', '500', '750', '1000'):
            bl.add_widget(Button(text=text_button,
                                 on_press=lambda instance: backend.sorting(int(instance.text))))
        return bl

    def update(self, instance):
        warning = 'Перед обновлением закройте Excel файл. И нажмите ещё раз'
        if instance.text != warning:
            instance.text = warning
            return
        else:
            instance.text = 'Данные обновленны.'
        backend.parse()
        backend.write_to_excel()


if __name__ == '__main__':
    MyApp().run()
