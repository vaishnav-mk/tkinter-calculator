import tkinter as tk

BIG_FONT = ("Calibri", 40, "bold")
ERROR_FONT = ("Calibri", 20, "bold")
SMALL_FONT = ("Calibri", 16)
DIGITS_FONT = ("Calibri", 24, "bold")
DEFAULT_FONT = ("Calibri", 20)

SPECIAL_COLOUR = "#323232"
DIGIT_COLOURS = "#3B3B3B"
EQUAL_COLOUR = "#4CC2FF"
SCREEN_COLOUR = "#202020"
EQUAL_LABEL_COLOR = "#25265E"
TEXT_COLOR = "#F0F0F0"

class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("400x600")
        self.window.title("Calculator")

        self.error = False

        self.total_expression = ""
        self.current_expression = ""
        self.display_frame = self.display_frame_gen()

        self.total_label, self.label = self.display_gen()

        self.digit_pos = {
            7: (1, 1), 
            8: (1, 2), 
            9: (1, 3),
            4: (2, 1), 
            5: (2, 2), 
            6: (2, 3),
            1: (3, 1), 
            2: (3, 2), 
            3: (3, 3),
            0: (4, 2), 
            '.': (4, 1),
        }
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}
        self.errors = {
            "division by zero": "Cannot divide by zero",
            "invalid syntax": "Invalid Syntax",
            "unknown error": "Unknown Error"
        }
        self.buttons_frame = self.create_buttons_frame()

        self.buttons_frame.rowconfigure(0, weight=1)

        
        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)

            
        self.create_digit_but()
        self.create_op_but()
        self.create_sp_but()
        self.bind_keys()

    def bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())
        self.window.bind("<BackSpace>", lambda event: self.backspace())
        self.window.bind("<Escape>", lambda event: self.clear())
        
        for key in self.digit_pos:
            self.window.bind(str(key), lambda event, digit=key: self.manipulate_expression(digit))

        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.handle_operator(operator))
        
        self.window.bind("c", lambda event: self.clear())

        for child in self.buttons_frame.winfo_children():
            if child['text'] != '=':
                child.bind("<Enter>", lambda event, child=child: child.config(bg=DIGIT_COLOURS if child['bg'] == SPECIAL_COLOUR else SPECIAL_COLOUR))
                child.bind("<Leave>", lambda event, child=child: child.config(bg= DIGIT_COLOURS if child['text'] in '0123456789.' else SPECIAL_COLOUR))

    def create_sp_but(self):
        self.c_but()
        self.equal_but()
        self.square_but()
        self.sqrt_but()

    def display_gen(self):
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E, bg=SCREEN_COLOUR, fg=TEXT_COLOR, padx=24, font=SMALL_FONT)
        total_label.pack(expand=True, fill='both')

        label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E, bg=SCREEN_COLOUR,
                         fg=TEXT_COLOR if not self.error else "red", padx=24, font=BIG_FONT)
        label.pack(expand=True, fill='both')

        return total_label, label

    def display_frame_gen(self):
        frame = tk.Frame(self.window, height=221, bg=SCREEN_COLOUR)
        frame.pack(expand=True, fill="both")
        return frame

    def manipulate_expression(self, value):
        if self.error:
            self.clear()
            self.error = False
        self.current_expression += str(value)
        self.update_label()

    def create_digit_but(self):
        for digit, grid_value in self.digit_pos.items():
            button = tk.Button(self.buttons_frame, text=str(digit), bg=DIGIT_COLOURS, fg=TEXT_COLOR, font=DIGITS_FONT,
                               borderwidth=0, command=lambda x=digit: self.manipulate_expression(x))            
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW, padx=1, pady=1)

    def handle_operator(self, operator):
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.update_label()

    def create_op_but(self):
        i = 0
        for operator, symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=symbol, bg=SPECIAL_COLOUR, fg=TEXT_COLOR, font=DEFAULT_FONT,
                               borderwidth=0, command=lambda x=operator: self.handle_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW, padx=1, pady=1)
            i += 1

    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()

    def c_but(self):
        button = tk.Button(self.buttons_frame, text="C", bg=SPECIAL_COLOUR, fg=TEXT_COLOR, font=DEFAULT_FONT,
                           borderwidth=0, command=self.clear)
        button.grid(row=0, column=1, sticky=tk.NSEW, padx=1, pady=1)

    def square(self):
        self.current_expression = str(eval(f"{self.current_expression or 0}**2"))
        self.update_label()

    def square_but(self):
        button = tk.Button(self.buttons_frame, text="x\u00b2", bg=SPECIAL_COLOUR, fg=TEXT_COLOR, font=DEFAULT_FONT,
                           borderwidth=0, command=self.square)
        button.grid(row=0, column=2, sticky=tk.NSEW, padx=1, pady=1)

    def sqrt(self):
        self.current_expression = str(eval(f"{self.current_expression or 0}**0.5"))
        self.update_label()

    def sqrt_but(self):
        button = tk.Button(self.buttons_frame, text="\u221ax", bg=SPECIAL_COLOUR, fg=TEXT_COLOR, font=DEFAULT_FONT,
                           borderwidth=0, command=self.sqrt)
        button.grid(row=0, column=3, sticky=tk.NSEW, padx=1, pady=1)

    def evaluate(self):
        if self.current_expression == "":
            self.current_expression = "0"
        self.total_expression += self.current_expression
        self.update_total_label()
        try:
            self.current_expression = str(eval(self.total_expression))
            self.total_expression = ""
        except Exception as e:
            print(str(e))
            self.error = True
            if (any(error in str(e) for error in self.errors)):
                self.current_expression = self.errors[str(e)] 
            else:
                self.current_expression = "Error"
            self.total_expression = ""

        self.update_label(True)
        self.update_total_label()
        
    def equal_but(self):
        button = tk.Button(self.buttons_frame, text="=", bg=EQUAL_COLOUR, fg=EQUAL_LABEL_COLOR, font=DEFAULT_FONT,
                           borderwidth=0, command=self.evaluate)
        
        button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW, padx=1, pady=1)

    def create_buttons_frame(self):
        frame = tk.Frame(self.window, bg="black")
        frame.pack(expand=True, fill="both")
        return frame

    def update_total_label(self):
        expression = self.total_expression

        if expression.startswith("0"):
            expression = expression[1:]
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')
        self.total_label.config(text=expression)

    def update_label(self, error=False):
        if error:
            self.label.config(text=self.current_expression, font=ERROR_FONT)
        else:
            self.label.config(text=self.current_expression[:11], font=BIG_FONT)

    def backspace(self):
        self.current_expression = self.current_expression[:-1]
        self.update_label()
            
    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    Calculator().run()
