import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
from database import get_db
from dashboard import open_dashboard
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_window():
    app = tb.Window(themename="flatly")
    app.title("Expense Manager – Login")
    app.geometry("350x420")
    app.resizable(False, False)

    tb.Label(
        app,
        text="Expense Manager",
        font=("Helvetica", 18, "bold"),
        bootstyle=PRIMARY
    ).pack(pady=20)

    frame = tb.Frame(app, padding=20)
    frame.pack()

    tb.Label(frame, text="Username").pack(anchor=W)
    username = tb.Entry(frame, width=30)
    username.pack(pady=5)

    tb.Label(frame, text="Password").pack(anchor=W)
    password = tb.Entry(frame, show="*", width=30)
    password.pack(pady=5)

    def login():
        hashed_pwd = hash_password(password.get())

        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, username FROM users WHERE username=%s AND password=%s",
            (username.get(), hashed_pwd)
        )

        user = cur.fetchone()
        print("LOGIN QUERY RESULT:", user)   # 🔥 IMPORTANT
        conn.close()

        if user:
            app.withdraw()
            open_dashboard(app, user[0])
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")


    def signup():
        if not username.get() or not password.get():
            messagebox.showerror("Error", "Username and Password required")
            return

        try:
            hashed_pwd = hash_password(password.get())
            conn = get_db()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO users(username, password) VALUES (%s, %s)",
                (username.get(), hashed_pwd)
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Signup successful")
        except Exception as e:
            messagebox.showerror("Signup Error", str(e))


    tb.Button(frame, text="Login", bootstyle=SUCCESS,
              width=25, command=login).pack(pady=10)

    tb.Button(frame, text="Signup", bootstyle=INFO,
              width=25, command=signup).pack()

    app.mainloop()
