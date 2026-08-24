import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen

API_BASE_URL = "http://127.0.0.1:5000"

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        layout.add_widget(Label(text="WillyClientSync Login", font_size=24))
        
        self.username_input = TextInput(hint_text="Username", multiline=False)
        self.password_input = TextInput(hint_text="Password", password=True, multiline=False)
        
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        
        btn_login = Button(text="Ingia (Login)", on_press=self.do_login)
        btn_register = Button(text="Jisajili (Register)", on_press=self.do_register)
        
        layout.add_widget(btn_login)
        layout.add_widget(btn_register)
        
        self.status_label = Label(text="")
        layout.add_widget(self.status_label)
        
        self.add_widget(layout)

    def do_login(self, instance):
        url = f"{API_BASE_URL}/login"
        payload = {
            "username": self.username_input.text,
            "password": self.password_input.text
        }
        try:
            res = requests.post(url, json=payload)
            data = res.json()
            if res.status_code == 200:
                self.status_label.text = f"Mafanikio! Token: {data.get('token')[:15]}..."
            else:
                self.status_label.text = data.get("message", "Imefeli kuingia")
        except Exception as e:
            self.status_label.text = "Haikuweza kuunganisha na Server"

    def do_register(self, instance):
        url = f"{API_BASE_URL}/register"
        payload = {
            "username": self.username_input.text,
            "password": self.password_input.text
        }
        try:
            res = requests.post(url, json=payload)
            data = res.json()
            self.status_label.text = data.get("message", "Usajili umekamilika")
        except Exception as e:
            self.status_label.text = "Haikuweza kuunganisha na Server"

class WillyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        return sm

if __name__ == '__main__':
    WillyApp().run()
