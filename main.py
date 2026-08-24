from kivy.app import App
from kivy.uix.label import Label

class WillyClientSync(App):
    def build(self):
        return Label(text='Willy ClientSync App Is Ready!')

if __name__ == '__main__':
    WillyClientSync().run()
