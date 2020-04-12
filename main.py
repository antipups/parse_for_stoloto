from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        screen = Screen()
        bl = BoxLayout(orientation="vertical")
        bl.add_widget(Button(text="1",
                             on_press=lambda x: sm.switch_to(screen1)))
        bl.add_widget(Button(text="2",
                             on_press=lambda x: sm.switch_to(screen2)))
        screen.add_widget(bl)
        screen1 = Screen(name="id1")
        screen2 = Screen(name="id2")
        sm.add_widget(screen)
        sm.add_widget(screen1)
        sm.add_widget(screen2)
        return sm


if __name__ == '__main__':
    MyApp().run()
