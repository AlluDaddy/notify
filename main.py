from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from plyer import notification

class NotifyApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        self.message_input = TextInput(hint_text="Enter notification message", size_hint=(1, 0.2))
        self.time_input = TextInput(hint_text="Interval (minutes)", input_filter='int', size_hint=(1, 0.2))
        self.status_label = Label(text="Set your notification!", size_hint=(1, 0.2))
        
        self.start_btn = Button(text="Start Notification", size_hint=(1, 0.2))
        self.start_btn.bind(on_press=self.start_notifications)
        
        self.layout.add_widget(self.message_input)
        self.layout.add_widget(self.time_input)
        self.layout.add_widget(self.start_btn)
        self.layout.add_widget(self.status_label)
        
        return self.layout

    def start_notifications(self, instance):
        message = self.message_input.text.strip()
        interval = self.time_input.text.strip()

        if not message or not interval:
            self.status_label.text = "Please fill both fields!"
            return

        minutes = int(interval)
        self.status_label.text = f"Notifications every {minutes} minutes set!"
        Clock.schedule_interval(lambda dt: self.send_notification(message), minutes * 60)

    def send_notification(self, message):
        notification.notify(
            title="Reminder!",
            message=message,
            timeout=5
        )

if __name__ == '__main__':
    NotifyApp().run()
