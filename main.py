from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
import requests

API_BASE_URL = "http://127.0.0.1:5000"

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        layout.add_widget(Label(text="WillyClientSync - Login", font_size=24))
        self.username_input = TextInput(hint_text="Username", multiline=False)
        self.password_input = TextInput(hint_text="Password", password=True, multiline=False)
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        
        btn_login = Button(text="Ingia (Login)", on_press=self.do_login)
        btn_register = Button(text="Sajili Akaunti", on_press=self.do_register)
        layout.add_widget(btn_login)
        layout.add_widget(btn_register)
        
        self.status_label = Label(text="")
        layout.add_widget(self.status_label)
        self.add_widget(layout)

    def do_login(self, instance):
        url = f"{API_BASE_URL}/login"
        payload = {"username": self.username_input.text, "password": self.password_input.text}
        try:
            res = requests.post(url, json=payload)
            if res.status_code == 200:
                self.manager.current = 'dashboard'
            else:
                self.status_label.text = res.json().get("message", "Imefeli")
        except:
            self.status_label.text = "Haikuweza kuunganisha na Server"

    def do_register(self, instance):
        url = f"{API_BASE_URL}/register"
        payload = {"username": self.username_input.text, "password": self.password_input.text}
        try:
            res = requests.post(url, json=payload)
            self.status_label.text = res.json().get("message", "Tayari")
        except:
            self.status_label.text = "Haikuweza kuunganisha na Server"

class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        layout.add_widget(Label(text="Dashboard - Wateja Wako", font_size=20))
        
        self.name_input = TextInput(hint_text="Jina la Mteja", multiline=False)
        self.phone_input = TextInput(hint_text="Namba ya Simu", multiline=False)
        layout.add_widget(self.name_input)
        layout.add_widget(self.phone_input)
        
        btn_add = Button(text="Hifadhi Mteja", on_press=self.add_client)
        btn_refresh = Button(text="Onyesha Wateja", on_press=self.fetch_clients)
        layout.add_widget(btn_add)
        layout.add_widget(btn_refresh)
        
        self.clients_label = Label(text="Bonyeza 'Onyesha Wateja' kupata orodha", size_hint_y=None)
        self.clients_label.bind(texture_size=self.clients_label.setter('size'))
        
        scroll = ScrollView()
        scroll.add_widget(self.clients_label)
        layout.add_widget(scroll)
        
        self.add_widget(layout)

    def add_client(self, instance):
        url = f"{API_BASE_URL}/clients"
        payload = {"name": self.name_input.text, "phone": self.phone_input.text}
        try:
            res = requests.post(url, json=payload)
            if res.status_code == 201:
                self.name_input.text = ""
                self.phone_input.text = ""
                self.fetch_clients(None)
        except:
            pass

    def fetch_clients(self, instance):
        url = f"{API_BASE_URL}/clients"
        try:
            res = requests.get(url)
            if res.status_code == 200:
                data = res.json()
                text = "\n".join([f"• {c['name']} - {c['phone']}" for c in data])
                self.clients_label.text = text if text else "Hakuna mteja aliyesajiliwa"
        except:
            self.clients_label.text = "Haikuweza kupata data"

class WillyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(DashboardScreen(name='dashboard'))
        return sm

if __name__ == '__main__':
    WillyApp().run()
