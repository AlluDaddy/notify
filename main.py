import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, BorderImage
from plyer import notification
from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty, NumericProperty


# 1. Load the Kivy Design File
# We use Builder.load_file to load the design from solo.kv
Builder.load_file('solo.kv')


class ReminderItem(BoxLayout):
    """
    A custom widget for an individual reminder item.
    The design is primarily handled in solo.kv, but the logic remains here.
    """
    name = StringProperty("")
    active = BooleanProperty(False)
    
    # Use properties to dynamically display the input value
    # value_display is what is shown next to the activate button
    value_display = StringProperty("")

    # Internal logic variables
    interval = NumericProperty(0) # Interval in minutes
    time = StringProperty(None, allownone=True) # Specific time HH:MM
    event = None

    def __init__(self, name, interval=None, time=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name

        if time:
            self.time = time
            self.value_display = f"@{time}"
        elif interval:
            self.interval = interval
            self.value_display = f"{interval} min"
        
        # Link the button press to the toggle function
        self.ids.start_btn.bind(on_press=self.toggle)


    def toggle(self, instance):
        if not self.active:
            # 1. Activation Logic
            if self.interval > 0:
                # Interval reminder: schedule to alert every 'interval' minutes
                # self.interval is in minutes, so we multiply by 60 for seconds
                self.event = Clock.schedule_interval(lambda dt: self.alert(), self.interval * 60)
                # Run the alert immediately on activation for interval reminders
                self.alert() 
            elif self.time:
                # Time reminder: schedule a check every 60 seconds (1 minute)
                self.event = Clock.schedule_interval(self.check_time, 60)
                
            self.active = True
        else:
            # 2. Deactivation Logic
            if self.event:
                self.event.cancel()
            
            self.active = False
            
        # The button text is updated automatically via the Kivy language file 
        # based on the 'active' BooleanProperty.


    def alert(self):
        """Triggers a desktop notification."""
        # Use the custom notification icon
        notification.notify(
            title=f"Shadow Monarch's Quest: {self.name}", 
            message="Arise! It's time to level up!", 
            timeout=4,
            # app_icon="C:\\Python\\notify\\notify_icon.png" 
        )

    def check_time(self, dt):
        """Checks if the current time matches the scheduled time."""
        now = datetime.datetime.now().strftime("%H:%M")
        if now == self.time:
            self.alert()


class SoloLevelingLayout(BoxLayout):
    """
    The main layout for the application. 
    Design and structure defined in solo.kv.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Clear the initial status message
        self.status_label = self.ids.status_label
        self.status_label.text = ""

    def add_reminder(self, instance):
        name = self.ids.name_input.text.strip()
        value = self.ids.time_input.text.strip()

        if not name or not value:
            self.status_label.text = "Error: Task Name and Time/Interval required!"
            return

        try:
            # Clear previous error
            self.status_label.text = ""
            reminder = None

            # Case 1: Specific time format like 14:00 or 09:30 (HH:MM)
            if ":" in value:
                hours, minutes = map(int, value.split(":"))
                if not (0 <= hours < 24 and 0 <= minutes < 60):
                    raise ValueError("Invalid time format")
                reminder = ReminderItem(name, time=value)

            # Case 2: Interval in minutes (must be a positive integer)
            else:
                minutes = int(value)
                if minutes <= 0:
                    raise ValueError("Interval must be positive")
                reminder = ReminderItem(name, interval=minutes)

            # Add the new reminder item
            self.ids.reminder_box.add_widget(reminder)
            # Clear input fields
            self.ids.name_input.text = ""
            self.ids.time_input.text = ""

        except ValueError:
            self.status_label.text = "Error: Use positive number for interval or HH:MM for time."


class SoloLevelingApp(App):
    def build(self):
        from kivy.core.window import Window
        # Set a standard mobile/portrait size for better demonstration
        Window.size = (480, 850) 
        # The background will be handled by the layout's background image
        Window.clearcolor = (0, 0, 0, 1) 
        return SoloLevelingLayout()


if __name__ == "__main__":
    SoloLevelingApp().run()

# from kivy.app import App
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.button import Button
# from kivy.uix.label import Label
# from kivy.uix.textinput import TextInput
# from kivy.clock import Clock
# from plyer import notification

# class NotifyApp(App):
#     def build(self):
#         self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
#         self.message_input = TextInput(hint_text="Enter notification message", size_hint=(1, 0.2))
#         self.time_input = TextInput(hint_text="Interval (minutes)", input_filter='int', size_hint=(1, 0.2))
#         self.status_label = Label(text="Set your notification!", size_hint=(1, 0.2))
        
#         self.start_btn = Button(text="Start Notification", size_hint=(1, 0.2))
#         self.start_btn.bind(on_press=self.start_notifications)
        
#         self.layout.add_widget(self.message_input)
#         self.layout.add_widget(self.time_input)
#         self.layout.add_widget(self.start_btn)
#         self.layout.add_widget(self.status_label)
        
#         return self.layout

#     def start_notifications(self, instance):
#         message = self.message_input.text.strip()
#         interval = self.time_input.text.strip()

#         if not message or not interval:
#             self.status_label.text = "Please fill both fields!"
#             return

#         minutes = int(interval)
#         self.status_label.text = f"Notifications every {minutes} minutes set!"
#         Clock.schedule_interval(lambda dt: self.send_notification(message), minutes * 60)

#     def send_notification(self, message):
#         notification.notify(
#             title="Reminder!",
#             message=message,
#             timeout=5
#         )

# if __name__ == '__main__':
#     NotifyApp().run()
