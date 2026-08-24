from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

# 1. Skrini ya Login
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        layout.add_widget(Label(text="Willy ClientSync Login", font_size=24, bold=True))
        
        self.username = TextInput(hint_text="Username", multiline=False)
        self.password = TextInput(hint_text="Password", password=True, multiline=False)
        
        layout.add_widget(self.username)
        layout.add_widget(self.password)
        
        btn_login = Button(text="Ingia (Login)", background_color=(0, 0.7, 0.3, 1))
        btn_login.bind(on_press=self.do_login)
        layout.add_widget(btn_login)
        
        self.msg_label = Label(text="")
        layout.add_widget(self.msg_label)
        
        self.add_widget(layout)

    def do_login(self, instance):
        if self.username.text and self.password.text:
            self.manager.current = 'dashboard'
        else:
            self.msg_label.text = "Tafadhali weka Username na Password!"

# 2. Skrini ya Dashboard yenye Moduli 25
class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        main_layout.add_widget(Label(text="Willy ClientSync - Moduli 25 za Biashara", font_size=18, bold=True, size_hint_y=0.1))
        
        scroll = ScrollView()
        grid = GridLayout(cols=2, spacing=10, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        
        modules = [
            "1. Wateja", "2. Mauzo", "3. Stoko/Stock", "4. Madeni",
            "5. Miamala", "6. Wagavi", "7. Purchase Orders", "8. Matumizi",
            "9. Faida & Hasara", "10. Ripoti Mauzo", "11. Wafanyakazi", "12. Mahudhurio",
            "13. Mishahara", "14. Invoices", "15. Kodi/VAT", "16. Offa/Discounts",
            "17. Loyalty Points", "18. Matawi", "19. Returns", "20. SMS/Email",
            "21. Offline Sync", "22. Ruhusa/Roles", "23. Activity Logs", "24. Nyaraka",
            "25. Backup Data"
        ]
        
        for mod in modules:
            btn = Button(text=mod, size_hint_y=None, height=60, background_color=(0.2, 0.5, 0.8, 1))
            grid.add_widget(btn)
            
        scroll.add_widget(grid)
        main_layout.add_widget(scroll)
        self.add_widget(main_layout)

class WillyClientSyncApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(DashboardScreen(name='dashboard'))
        return sm

if __name__ == '__main__':
    WillyClientSyncApp().run()
