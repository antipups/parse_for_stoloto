from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen



class MyApp(App):
    def build(self):
        sm = ScreenManager()
        return sm


if __name__ == '__main__':
    MyApp().run()
