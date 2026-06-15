import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

# Ensure Kivy version compatibility if needed (optional)
kivy.require("2.0.0")


class Calculator(BoxLayout):
    """Main widget for the calculator application handling UI logic and mathematical operations."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Left for debugging purposes during development
        print(f"Initialized widgets: {self.children}")

    def clear_btn(self):
        """Resets both the primary input expression and the result display."""
        self.ids.input.text = "0"
        self.ids.input2.text = ""

    def button_press(self, value):
        """Appends a digit to the current input string, clearing initial zeros and errors.

        Args:
            value (str/int): The digit or character pressed.
        """
        prev = self.ids.input.text
        ans_box = self.ids.input2.text

        # Clear previous error message if a new number is pressed
        if ans_box == "Error!":
            self.ids.input2.text = ""

        # Overwrite the default initial '0', otherwise append the value
        if prev == "0":
            self.ids.input.text = f"{value}"
        else:
            self.ids.input.text = f"{prev}{value}"

    def maths_sign(self, sign):
        """Appends a mathematical operator (+, -, *, /, %) to the expression.

        Ensures that two consecutive operators cannot be placed back-to-back.

        Args:
            sign (str): The operator sign to append.
        """
        prev = self.ids.input.text

        # Only append if the last character isn't already an operator
        if prev and prev[-1] not in ["+", "-", "*", "/", "%"]:
            self.ids.input.text = f"{prev}{sign}"

    def button_equalto(self):
        """Evaluates the mathematical expression currently in the input field

        using Python's eval() function and displays the result.
        """
        prev = self.ids.input.text
        try:
            # Note: eval handles standard string-based arithmetic
            answer = eval(prev)
        except Exception:
            answer = "Error!"

        self.ids.input2.text = str(answer)

    def dot(self):
        """Inserts a decimal point into the current expression, ensuring that

        the number currently being typed doesn't already contain one.
        """
        prev = self.ids.input.text
        operators = ["+", "-", "*", "/", "%"]
        current_num = ""

        # Read backwards from the end of the string to find the current token
        for char in reversed(prev):
            if char in operators:
                break
            current_num = char + current_num

        # Allow a decimal point only if the current number lacks one
        if "." not in current_num:
            self.ids.input.text = f"{prev}."

    def last_remove(self):
        """Deletes the last character from the input display (Backspace)."""
        prev = self.ids.input.text
        self.ids.input.text = prev[:-1] if prev else "0"

    def change_sign(self):
        """Toggles the sign (positive/negative) of the calculated answer."""
        prev = self.ids.input2.text

        if not prev or prev == "0" or prev == "Error!":
            return

        # If it's already negative, strip the negative symbol
        if prev.startswith("-"):
            self.ids.input2.text = prev[1:]
        else:
            self.ids.input2.text = f"-{prev}"


class CalculatorApp(App):
    """The root Kivy Application instance."""

    def build(self):
        # Set application background color to white
        Window.clearcolor = (1, 1, 1, 1)
        return Calculator()


if __name__ == "__main__":
    CalculatorApp().run()