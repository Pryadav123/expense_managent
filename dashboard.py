import matplotlib.pyplot as plt
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox, filedialog
from database import get_db
from datetime import datetime
import csv


def open_dashboard(root, user_id):

    win = tb.Toplevel(root)
    win.title("Expense Manager – Dashboard")
    win.geometry("1000x600")

    def on_close():
        root.destroy()

    win.protocol("WM_DELETE_WINDOW", on_close)

    # ---------- TOP BAR ----------
    top_bar = tb.Frame(win)
    top_bar.pack(fill=X, padx=10, pady=5)

    tb.Label(
        top_bar,
        text="My Expenses",
        font=("Helvetica", 20, "bold"),
        bootstyle=PRIMARY
    ).pack(side=LEFT)

    def logout():
        win.destroy()
        root.deiconify()

    tb.Button(
        top_bar,
        text="Logout",
        bootstyle=WARNING,
        command=logout
    ).pack(side=RIGHT)

    # ---------- FORM ----------
    form = tb.Frame(win, padding=10)
    form.pack(fill=X)

    date = tb.Entry(form)
    title = tb.Entry(form)
    amount = tb.Entry(form)
    note = tb.Entry(form)

    category = tb.Combobox(
        form,
        values=["Food", "Travel", "Rent", "Shopping"],
        state="readonly"
    )
    category.current(0)

    labels = ["Date (YYYY-MM-DD)", "Title", "Amount", "Category", "Note"]
    widgets = [date, title, amount, category, note]

    for i in range(5):
        tb.Label(form, text=labels[i]).grid(row=0, column=i)
        widgets[i].grid(row=1, column=i, padx=5)

    budget = tb.Entry(form, width=12)
    tb.Label(form, text="Monthly Budget").grid(row=0, column=5)
    budget.grid(row=1, column=5, padx=5)

    # ---------- FUNCTIONS ----------

    def check_budget():
        if not budget.get().isdigit():
            return

        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT SUM(amount)
            FROM expenses
            WHERE user_id=%s
            AND DATE_FORMAT(date,'%Y-%m') = DATE_FORMAT(CURDATE(),'%Y-%m')
        """, (user_id,))
        total = cur.fetchone()[0] or 0
        conn.close()

        if total >= int(budget.get()):
            messagebox.showwarning(
                "Budget Alert",
                f"Budget exceeded!\nSpent: ₹{total}"
            )

    def add_expense():
        if not date.get() or not title.get() or not amount.get():
            messagebox.showerror("Error", "Date, Title and Amount are required")
            return

        if not amount.get().isdigit():
            messagebox.showerror("Error", "Amount must be a number")
            return

        try:
            expense_date = datetime.strptime(date.get(), "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror(
                "Invalid Date",
                "Use YYYY-MM-DD format"
            )
            return

        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO expenses(user_id, date, title, amount, category, note)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, (
            user_id,
            expense_date,
            title.get(),
            int(amount.get()),
            category.get(),
            note.get()
        ))
        conn.commit()
        conn.close()

        show_expenses()
        check_budget()

    tb.Button(
        form,
        text="Add Expense",
        bootstyle=SUCCESS,
        command=add_expense
    ).grid(row=1, column=6, padx=10)

    # ---------- SEARCH ----------
    search = tb.Entry(win)
    search.pack(pady=5)
    search.insert(0, "Search by title...")

    # ---------- TABLE ----------
    cols = ("ID", "Date", "Title", "Amount", "Category", "Note")
    table = tb.Treeview(win, columns=cols, show="headings", height=12)
    table.pack(fill=BOTH, expand=True, padx=10, pady=10)

    for col in cols:
        table.heading(col, text=col)
        table.column(col, anchor=CENTER)

    def show_expenses():
        table.delete(*table.get_children())

        query = """
            SELECT id,date,title,amount,category,note
            FROM expenses
            WHERE user_id=%s
        """
        params = [user_id]

        if search.get() and search.get() != "Search by title...":
            query += " AND title LIKE %s"
            params.append(f"%{search.get()}%")

        conn = get_db()
        cur = conn.cursor()
        cur.execute(query, tuple(params))

        for row in cur.fetchall():
            table.insert("", "end", values=row)

        conn.close()

    search.bind("<KeyRelease>", lambda e: show_expenses())

    def delete_expense():
        selected = table.selection()
        if not selected:
            return
        exp_id = table.item(selected)["values"][0]

        conn = get_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM expenses WHERE id=%s", (exp_id,))
        conn.commit()
        conn.close()

        show_expenses()

    # ---------- EXPORT ----------
    def export_to_csv():
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")]
        )
        if not path:
            return

        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT date,title,amount,category,note
            FROM expenses WHERE user_id=%s
        """, (user_id,))
        rows = cur.fetchall()
        conn.close()

        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Title", "Amount", "Category", "Note"])
            writer.writerows(rows)

        messagebox.showinfo("Exported", "CSV exported successfully")

    # ---------- CHARTS ----------
    def show_category_chart():
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT category, SUM(amount)
            FROM expenses
            WHERE user_id=%s
            GROUP BY category
        """, (user_id,))
        data = cur.fetchall()
        conn.close()

        if not data:
            messagebox.showinfo("No Data", "No expenses to show")
            return

        plt.pie(
            [row[1] for row in data],
            labels=[row[0] for row in data],
            autopct="%1.1f%%"
        )
        plt.title("Expense Distribution")
        plt.show()

    def show_monthly_report():
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT DATE_FORMAT(date,'%Y-%m'), SUM(amount)
            FROM expenses
            WHERE user_id=%s
            GROUP BY 1
            ORDER BY 1
        """, (user_id,))
        data = cur.fetchall()
        conn.close()

        if not data:
            messagebox.showinfo("No Data", "No expenses to show")
            return

        plt.bar([r[0] for r in data], [r[1] for r in data])
        plt.title("Monthly Expense Report")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    # ---------- ACTION BUTTONS ----------
    actions = tb.Frame(win)
    actions.pack(pady=5)

    tb.Button(actions, text="Category Chart", bootstyle=INFO,
              command=show_category_chart).pack(side=LEFT, padx=5)

    tb.Button(actions, text="Monthly Report", bootstyle=PRIMARY,
              command=show_monthly_report).pack(side=LEFT, padx=5)

    tb.Button(actions, text="Export CSV", bootstyle=SUCCESS,
              command=export_to_csv).pack(side=LEFT, padx=5)

    tb.Button(actions, text="Delete Selected", bootstyle=DANGER,
              command=delete_expense).pack(side=LEFT, padx=5)

    show_expenses()
