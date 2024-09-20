from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.label = Label(text="Click the button")
        layout.add_widget(self.label)
        button = Button(text="Click Me")
        button.bind(on_press=self.say_hello)
        layout.add_widget(button)
        return layout

    def say_hello(self, instance):
        self.label.text = "Hello, World!"

if __name__ == "__main__":
    MyApp().run()
