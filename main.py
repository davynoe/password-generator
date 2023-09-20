import secrets
import string
import re
import pyperclip
import customtkinter as ctk

# Systemwide Settings
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Main Window Settings
        self.title("Quite Simple Password App")
        self.geometry("700x350")
        
        # Adding Tabviews
        self.tabview = ctk.CTkTabview(master=self)
        self.tabview.add("Generator")
        self.tabview.add("Validator")
        self.generator_tab = self.tabview.tab("Generator")
        self.validator_tab = self.tabview.tab("Validator")
        self.tabview.pack(padx=10, pady=12, fill="both", expand=True)

        # Generator Tab Grid Layout Settings (4x4)
        self.generator_tab.columnconfigure((0,1,2,3), weight=1)
        self.generator_tab.rowconfigure((0,1,2,3), weight=1)

        # Validator Tab Grid Layout Settings (3x4)
        self.validator_tab.columnconfigure((0,2), weight=1)
        self.validator_tab.columnconfigure(1, weight=20)
        self.validator_tab.rowconfigure((0,1,2,3), weight=1)
        
        # Generator Tab 1st Row
        self.pwd_len_label = ctk.CTkLabel(self.generator_tab, text="Password Length:", font=("Roboto",18))
        self.pwd_len_entry = ctk.CTkEntry(self.generator_tab, font=("Roboto",18))
        self.pwd_len_label.grid(row=0, column=1, padx=10, pady=12, sticky="e")
        self.pwd_len_entry.grid(row=0, column=2, padx=10, pady=12, sticky="w")

        # Generator Tab 2nd Row
        self.digits_checkbox = ctk.CTkCheckBox(self.generator_tab, text="Digits", font=("Roboto",14))
        self.lowercase_checkbox = ctk.CTkCheckBox(self.generator_tab, text="Lowercase Letters", font=("Roboto",14))
        self.uppercase_checkbox = ctk.CTkCheckBox(self.generator_tab, text="Uppercase Letters", font=("Roboto",14))
        self.symbols_checkbox = ctk.CTkCheckBox(self.generator_tab, text="Symbols", font=("Roboto",14))
        self.digits_checkbox.grid(row=1, column=0, padx=10, pady=10)
        self.lowercase_checkbox.grid(row=1, column=1, padx=10, pady=10)
        self.uppercase_checkbox.grid(row=1, column=2, padx=10, pady=10)
        self.symbols_checkbox.grid(row=1, column=3, padx=10, pady=10)

        # Generator Tab 3rd Row
        self.generate_button = ctk.CTkButton(self.generator_tab, text="GENERATE", font=("Roboto",16), command=self.generate_pwd)
        self.generated_pwd_entry = ctk.CTkEntry(self.generator_tab, font=("Roboto",16))
        self.generate_button.grid(row=2, column=0, padx=10, pady=12)
        self.generated_pwd_entry.grid(row=2, column=1, columnspan=3, padx=10, pady=12, sticky="ew")

        # Generator Tab 4th Row
        self.copy_pwd_button = ctk.CTkButton(self.generator_tab, text="Copy Password", font=("Roboto",16), command=self.copy_pwd)
        self.copy_pwd_button.grid(row=3, column=0, columnspan=4, padx=10, pady=12, sticky="ns")

        # Validator Tab 1st Row
        self.input_pwd_label = ctk.CTkLabel(self.validator_tab, text="Enter your password:", font=("Roboto", 16))
        self.input_pwd_entry = ctk.CTkEntry(self.validator_tab, font=("Roboto",14))
        self.paste_pwd_button = ctk.CTkButton(self.validator_tab, text="Paste Password", font=("Roboto",14), command=self.paste_pwd)
        self.input_pwd_label.grid(row=0, column=0, padx=10, pady=12)
        self.input_pwd_entry.grid(row=0, column=1, padx=10, pady=12, sticky="ew")
        self.paste_pwd_button.grid(row=0, column=2, padx=10, pady=12)

        # Validator Tab 2nd Row
        self.validate_button = ctk.CTkButton(self.validator_tab, text="VALIDATE", font=("Roboto", 16), command=self.validate_pwd)
        self.validate_button.grid(row=1, column=0, columnspan=3, padx=10, pady=12)

        # validator Tab 3rd Row
        self.pwd_strength_bar = ctk.CTkProgressBar(self.validator_tab, progress_color="white")
        self.pwd_strength_bar.set(0)
        self.pwd_strength_bar.grid(row=2, column=0, columnspan=3, padx=50, pady=12, sticky="ew")

        # Validator Tab 4th Row
        self.pwd_strength_text = ctk.CTkLabel(self.validator_tab, text="Your password strength will appear here.", font=("Roboto",18))
        self.pwd_strength_text.grid(row=3, column=0, columnspan=4, padx=10, pady=12)

    
    def check_generator_errors(self):
        pwd_len = self.pwd_len_entry.get()
        has_digits = self.digits_checkbox.get()
        has_lowercase = self.lowercase_checkbox.get()
        has_uppercase = self.uppercase_checkbox.get()
        has_symbols = self.symbols_checkbox.get()

        if not pwd_len.isdigit() or has_digits + has_lowercase + has_uppercase + has_symbols == 0:
            return 1
        return 0

    def generate_pwd(self):
        if self.check_generator_errors(): 
            return
        
        pwd_len = int(self.pwd_len_entry.get())
        has_digits = self.digits_checkbox.get()
        has_lowercase = self.lowercase_checkbox.get()
        has_uppercase = self.uppercase_checkbox.get()
        has_symbols = self.symbols_checkbox.get()

        alphabet = ""
        pwd = ""

        if has_digits: 
            alphabet += string.digits
            pwd += secrets.choice(string.digits)
            pwd_len -= 1
        if has_lowercase: 
            alphabet += string.ascii_lowercase
            pwd += secrets.choice(string.ascii_lowercase)
            pwd_len -= 1
        if has_uppercase: 
            alphabet += string.ascii_uppercase
            pwd += secrets.choice(string.ascii_uppercase)
            pwd_len -= 1
        if has_symbols: 
            alphabet += string.punctuation
            pwd += secrets.choice(string.punctuation)
            pwd_len -= 1

        for _ in range(pwd_len):
            pwd += secrets.choice(alphabet)

        self.generated_pwd_entry.delete(0, "end")
        self.generated_pwd_entry.insert(0, pwd)

    def validate_pwd(self):
        pwd = self.input_pwd_entry.get()
        has_digits = re.search(r'\d', pwd)
        has_lowercase = re.search(r'[a-z]', pwd)
        has_uppercase = re.search(r'[A-Z]', pwd)
        has_symbols = re.search(r'[!@#$%^&*()_+{}\[\]:;<>,.?\'\"\\|]', pwd)
        type_count = int(bool(has_digits)) + int(bool(has_lowercase)) + int(bool(has_uppercase)) + int(bool(has_symbols))

        score = round(int((len(pwd)/8) + type_count - 1)/6, 1)

        match score:
            case 0.0:
                score_text = "MEDIOCRE"
                score_color = "red"
            case 0.2:
                score_text = "VERY LOW"
                score_color = "orange"
            case 0.3:
                score_text = "LOW"
                score_color = "yellow"
            case 0.5:
                score_text = "MEDIUM"
                score_color = "green"
            case 0.7:
                score_text = "HIGH"
                score_color = "blue"
            case 0.8:
                score_text = "VERY HIGH"
                score_color = "aqua"
            case _:
                score_text = "ULTRA HIGH"
                score_color = "pink"

        self.pwd_strength_bar.set(score)
        self.pwd_strength_bar.configure(progress_color=score_color)
        self.pwd_strength_text.configure(text=f"Your password strength is {score_text}", text_color=score_color)

    def copy_pwd(self):
        pyperclip.copy(self.generated_pwd_entry.get())

    def paste_pwd(self):
        self.input_pwd_entry.delete(0, "end")
        self.input_pwd_entry.insert(0, pyperclip.paste())

if __name__ == "__main__":
    app = App()
    app.mainloop()
