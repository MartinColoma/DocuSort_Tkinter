import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


class AdminApp:
    def __init__(self, login_root):
        self.login_root = login_root
        self.page = 0
        self.items_per_page = 10

        self.root = tk.Toplevel(self.login_root)
        self.root.title("Admin Home Page")
        self.root.geometry("1200x700")
        self.root.configure(bg="#131f24")

        self.login_root.withdraw()  # Hide login window
        self.admin_home_page()
        self.root.protocol("WM_DELETE_WINDOW", self.logout)

    def admin_home_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=4)

        # Sidebar
        sidebar_frame = tk.Frame(self.root, bg="#131f24", width=200)
        sidebar_frame.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

        tk.Label(sidebar_frame, text="Admin Panel", font=("Courier New", 20, "bold"),
                 fg="#58cc02", bg="#131f24").pack(pady=30)

        sidebar_buttons = [
            ("Dashboard", self.show_dashboard),
            ("Settings", self.show_settings),
            ("Reports", self.show_reports),
            ("Log Out", self.logout)
        ]

        for text, command in sidebar_buttons:
            button = tk.Button(
                sidebar_frame, text=text, font=("Courier New", 16), fg="white", bg="#58cc02",
                relief="flat", activebackground="#58cc02", activeforeground="white",
                command=command
            )
            button.pack(fill="x", pady=10, padx=10)

        # Main content area
        self.content_frame = tk.Frame(self.root, bg="#f4f4f4")
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.show_dashboard()  # Show dashboard by default

    def show_dashboard(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        title_label = tk.Label(
            self.content_frame,
            text="Dashboard - Recent Documents",
            font=("Courier New", 18, "bold"),
            bg="#131f24",
            fg="#fff"
        )
        title_label.pack(pady=10)

        self.table_frame = tk.Frame(self.content_frame, bg="#f4f4f4")
        self.table_frame.pack(padx=10, pady=10, fill="none", expand=False)

        columns = ("id", "sender", "student_number", "section", "course", "receiver", "datetime")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", height=10)

        for col in columns:
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, anchor="center", width=140)

        self.tree.pack()

        nav_frame = tk.Frame(self.content_frame, bg="#f4f4f4")
        nav_frame.pack(pady=10)

        prev_btn = tk.Button(nav_frame, text="← Previous", command=self.prev_page,
                             font=("Courier New", 12), bg="#58cc02", fg="white")
        prev_btn.pack(side="left", padx=5)

        next_btn = tk.Button(nav_frame, text="Next →", command=self.next_page,
                             font=("Courier New", 12), bg="#58cc02", fg="white")
        next_btn.pack(side="left", padx=5)

        self.load_table_page()

    def load_table_page(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = sqlite3.connect("docusortDB.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM documents")
        total_rows = cursor.fetchone()[0]

        offset = self.page * self.items_per_page
        cursor.execute("""
            SELECT id, sender_fname || ' ' || sender_surname, studnum,
                   sender_section, sender_course,
                   rcvr_fname || ' ' || rcvr_surname, datetime
            FROM documents
            ORDER BY datetime DESC
            LIMIT ? OFFSET ?
        """, (self.items_per_page, offset))
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            self.tree.insert("", "end", values=row)

    def next_page(self):
        self.page += 1
        self.load_table_page()

    def prev_page(self):
        if self.page > 0:
            self.page -= 1
            self.load_table_page()

    def show_settings(self):
        self.update_content("Settings", "Here you can modify settings.")

    def show_reports(self):
        self.update_content("Reports", "Here are the reports.")

    def update_content(self, title, message):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        title_label = tk.Label(self.content_frame, text=title,
                               font=("Courier New", 18, "bold"), bg="#f4f4f4", fg="#131f24")
        title_label.pack(pady=20)

        message_label = tk.Label(self.content_frame, text=message,
                                 font=("Courier New", 14), bg="#f4f4f4", fg="#131f24")
        message_label.pack(pady=10)

    def logout(self):
        confirm = messagebox.askyesno("Confirm Logout", "Are you sure you want to log out?")
        if confirm:
            print("Logging out and going back to login page")
            self.root.destroy()  # Close admin window

            from home_with_db import DocuSortApp
            login_window = tk.Toplevel(self.login_root)
            DocuSortApp(login_window)
        else:
            print("Logout canceled.")




if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x600")
    app = AdminApp(root)
    root.mainloop()
