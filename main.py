from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
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
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        main_layout.add_widget(Label(text="Willy ClientSync - Moduli 25 za Biashara", font_size=18, size_hint_y=None, height=40))
        
        modules = [
            "1. Wateja", "2. Mauzo", "3. Stoko/Stock", "4. Madeni",
            "5. Miamala", "6. Wagavi", "7. Purchase Orders", "8. Matumizi",
            "9. Faida & Hasara", "10. Ripoti Mauzo", "11. Wafanyakazi", "12. Mahudhurio",
            "13. Mishahara", "14. Invoices", "15. Kodi/VAT", "16. Offa/Discounts",
            "17. Loyalty Points", "18. Matawi", "19. Returns", "20. SMS/Email",
            "21. Offline Sync", "22. Ruhusa/Roles", "23. Activity Logs", "24. Nyaraka",
            "25. Backup Data"
        ]
        
        grid = GridLayout(cols=2, spacing=10, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        
        for mod in modules:
            btn = Button(text=mod, size_hint_y=None, height=50)
            grid.add_widget(btn)
            
        scroll = ScrollView()
        scroll.add_widget(grid)
        main_layout.add_widget(scroll)
        
        self.add_widget(main_layout)

class WillyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(DashboardScreen(name='dashboard'))
        return sm

if __name__ == '__main__':
    WillyApp().run()
