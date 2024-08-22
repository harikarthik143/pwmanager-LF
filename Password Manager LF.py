import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet 
import sqlite3
import random
import string

# Initialize encryption key
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Connect to the database
conn = sqlite3.connect('passwords.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE IF NOT EXISTS passwords
             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
             website TEXT, 
             username TEXT, 
             password BLOB)''')

class PasswordManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager")
        self.root.configure(bg='#c9bbc8')  # Set background color

        # Configuring the grid to center content
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

        # Labels and Entries
        self.website_label = tk.Label(root, text="Website")
        self.website_label = tk.Label(root, text="Website", font=("Eras Bold ITC", 13), bg='#c9bbc8')
        self.website_label.grid(row=0, column=0, sticky="e", padx=10, pady=5)
        self.website_entry = tk.Entry(root)
        self.website_entry = tk.Entry(root, font=("Eras Bold ITC", 12))
        self.website_entry.grid(row=0, column=1, sticky="w", padx=10, pady=5)

        self.username_label = tk.Label(root, text="Username")
        self.username_label = tk.Label(root, text="Username", font=("Eras Bold ITC", 13), bg='#c9bbc8')
        self.username_label.grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.username_entry = tk.Entry(root, font=("Eras Bold ITC", 12))
        self.username_entry.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        self.password_label = tk.Label(root, text="Password")
        self.password_label = tk.Label(root, text="Password", font=("Eras Bold ITC", 13), bg='#c9bbc8')
        self.password_label.grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.password_entry = tk.Entry(root, font=("Eras Bold ITC", 12))
        self.password_entry.grid(row=2, column=1, sticky="w", padx=10, pady=5)

        # Buttons
        self.add_button = tk.Button(root, text="Add", command=self.add_password, font=("Eras Bold ITC", 11, "bold"), bg='lightgrey')
        self.add_button.grid(row=5, column=0, columnspan=1, padx=10, pady=10)

        self.retrieve_button = tk.Button(root, text="Retrieve", command=self.retrieve_password, font=("Eras Bold ITC", 11, "bold"), bg='lightgrey')
        self.retrieve_button.grid(row=5, column=1, columnspan=2, padx=10, pady=10)

        self.generate_button = tk.Button(root, text="Generate Password", command=self.generate_password, font=("Eras Bold ITC", 11, "bold"))
        self.generate_button.grid(row=4, column=1, columnspan=1, sticky="w, e", padx=10, pady=7)

    def add_password(self):
        website = self.website_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not (website and username and password):
            messagebox.showwarning("Input Error", "All fields must be filled")
            return

        encrypted_password = cipher_suite.encrypt(password.encode())

        c.execute("INSERT INTO passwords (website, username, password) VALUES (?, ?, ?)", 
                  (website, username, encrypted_password))
        conn.commit()
        messagebox.showinfo("Success", "Password saved successfully!")

    def retrieve_password(self):
        website = self.website_entry.get()
        username = self.username_entry.get()

        c.execute("SELECT password FROM passwords WHERE website=? AND username=?", (website, username))
        result = c.fetchone()

        if result:
            decrypted_password = cipher_suite.decrypt(result[0]).decode()
            messagebox.showinfo("Password Retrieved", f"Password: {decrypted_password}")
        else:
            messagebox.showwarning("Error", "No password found for this website and username")

    def generate_password(self):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for i in range(12))
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)

root = tk.Tk()
app = PasswordManager(root)
root.mainloop()

# Close the connection when done
conn.close()
