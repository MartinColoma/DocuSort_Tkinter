import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


class AdminApp:
    def __init__(self, login_root):
        self.login_root = login_root
        self.page = 0
        self.items_per_page = 10

        # Define color scheme for the entire application
        self.bg_dark = "#131f24"
        self.accent_green = "#58cc02"
        self.text_light = "#ffffff"
        self.text_dark = "#131f24"
        self.secondary_bg = "#1c2b33"  # Slightly lighter than main dark for contrast

        self.root = tk.Toplevel(self.login_root)
        self.root.title("Admin Home Page")
        self.root.attributes('-fullscreen', True)
        # Bind Escape key to exit fullscreen
        self.root.bind("<Escape>", self.exit_fullscreen)
        # Bind F or f key to re-enter fullscreen
        self.root.bind("<f>", self.toggle_fullscreen)
        self.root.bind("<F>", self.toggle_fullscreen)
       
        self.root.configure(bg=self.bg_dark)

        # Configure Treeview style
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("Treeview", 
                            background=self.secondary_bg, 
                            foreground=self.text_light, 
                            rowheight=25,
                            fieldbackground=self.secondary_bg)
        self.style.configure("Treeview.Heading", 
                            background=self.accent_green, 
                            foreground=self.text_light,
                            font=("Courier New", 10, "bold"))
        self.style.map("Treeview", 
                      background=[('selected', self.accent_green)],
                      foreground=[('selected', self.text_light)])

        self.login_root.withdraw()  # Hide login window
        self.admin_home_page()
        self.root.protocol("WM_DELETE_WINDOW", self.logout)

    
    def toggle_fullscreen(self, event=None):
        self.root.attributes("-fullscreen", True)

    def exit_fullscreen(self, event=None):
        self.root.attributes("-fullscreen", False)
        
    def admin_home_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=4)

        # Sidebar
        sidebar_frame = tk.Frame(self.root, bg=self.bg_dark, width=200)
        sidebar_frame.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

        tk.Label(sidebar_frame, text="Admin Panel", font=("Courier New", 20, "bold"),
                fg=self.accent_green, bg=self.bg_dark).pack(pady=30)

        # Store buttons here for easy access    
        self.sidebar_buttons = {}

        # Sidebar buttons data
        sidebar_buttons_data = [
            ("Dashboard", self.show_dashboard),
            ("Admin Users", self.show_admin_users),
            ("Log Out", self.logout)
        ]

        for text, command in sidebar_buttons_data:
            button = tk.Button(
                sidebar_frame, text=text, font=("Courier New", 16), fg=self.accent_green, bg=self.bg_dark,
                relief="flat", activebackground=self.accent_green, activeforeground=self.text_light,
                command=lambda cmd=command, btn_text=text: self.switch_page(cmd, btn_text)
            )
            button.pack(fill="x", pady=10, padx=10)
            self.sidebar_buttons[text] = button

        # Main content area
        self.content_frame = tk.Frame(self.root, bg=self.bg_dark)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Start on Dashboard by default
        self.switch_page(self.show_dashboard, "Dashboard")

    def switch_page(self, page_method, button_text):
        # Update the button highlight colors
        for text, btn in self.sidebar_buttons.items():
            if text == button_text:
                # Active button style
                btn.config(bg=self.accent_green, fg=self.bg_dark)
            else:
                # Inactive button style
                btn.config(bg=self.bg_dark, fg=self.accent_green)

        # Clear current content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Call the page method to populate content_frame
        page_method()




    def show_dashboard(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # PENDING DOCUMENTS TABLE
        pending_label = tk.Label(
            self.content_frame,
            text="Pending Documents",
            font=("Courier New", 14, "bold"),
            bg=self.bg_dark,
            fg=self.text_light
        )
        pending_label.pack(pady=(5, 0))

        self.pending_table_frame = tk.Frame(self.content_frame, bg=self.bg_dark)
        self.pending_table_frame.pack(padx=10, pady=10)

        columns = ("first_name", "last_name", "student_number", "course", "doc_type", "datetime")
        column_titles = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "student_number": "Student Number",
            "course": "Course",
            "doc_type": "Process Type",
            "datetime": "Date & Time"
        }
        column_widths = {
            "first_name": 200,
            "last_name": 200,
            "student_number": 160,
            "course": 250,
            "doc_type": 160,
            "datetime": 200
        }

        style = ttk.Style()
        style.configure("Treeview", font=("Courier New", 12), rowheight=30)
        style.configure("Treeview.Heading", font=("Courier New", 12, "bold"))

        self.pending_tree = ttk.Treeview(
            self.pending_table_frame, columns=columns, show="headings", height=10
        )
        for col in columns:
            self.pending_tree.heading(col, text=column_titles[col])
            self.pending_tree.column(col, anchor="center", width=column_widths[col])

        pending_scrollbar = ttk.Scrollbar(
            self.pending_table_frame, orient="vertical", command=self.pending_tree.yview
        )
        self.pending_tree.configure(yscrollcommand=pending_scrollbar.set)
        self.pending_tree.pack(side="left")
        pending_scrollbar.pack(side="right", fill="y")

        pending_nav_frame = tk.Frame(self.content_frame, bg=self.bg_dark)
        pending_nav_frame.pack(pady=5)
        self.pending_prev_button = tk.Button(
            pending_nav_frame, text="← Previous", command=self.pending_prev_page,
            font=("Courier New", 12), bg=self.accent_green, fg=self.text_light,
            activebackground=self.secondary_bg, activeforeground=self.text_light
        )
        self.pending_prev_button.pack(side="left", padx=5)

        self.pending_next_button = tk.Button(
            pending_nav_frame, text="Next →", command=self.pending_next_page,
            font=("Courier New", 12), bg=self.accent_green, fg=self.text_light,
            activebackground=self.secondary_bg, activeforeground=self.text_light
        )
        self.pending_next_button.pack(side="left", padx=5)

        # RECEIVED DOCUMENTS TABLE
        received_label = tk.Label(
            self.content_frame,
            text="Received Documents",
            font=("Courier New", 14, "bold"),
            bg=self.bg_dark,
            fg=self.text_light
        )
        received_label.pack(pady=(20, 0))

        self.received_table_frame = tk.Frame(self.content_frame, bg=self.bg_dark)
        self.received_table_frame.pack(padx=10, pady=10)

        self.received_tree = ttk.Treeview(
            self.received_table_frame, columns=columns, show="headings", height=10
        )
        for col in columns:
            self.received_tree.heading(col, text=column_titles[col])
            self.received_tree.column(col, anchor="center", width=column_widths[col])

        received_scrollbar = ttk.Scrollbar(
            self.received_table_frame, orient="vertical", command=self.received_tree.yview
        )
        self.received_tree.configure(yscrollcommand=received_scrollbar.set)
        self.received_tree.pack(side="left")
        received_scrollbar.pack(side="right", fill="y")

        received_nav_frame = tk.Frame(self.content_frame, bg=self.bg_dark)
        received_nav_frame.pack(pady=5)
        self.received_prev_button = tk.Button(
            received_nav_frame, text="← Previous", command=self.received_prev_page,
            font=("Courier New", 12), bg=self.accent_green, fg=self.text_light,
            activebackground=self.secondary_bg, activeforeground=self.text_light
        )
        self.received_prev_button.pack(side="left", padx=5)

        self.received_next_button = tk.Button(
            received_nav_frame, text="Next →", command=self.received_next_page,
            font=("Courier New", 12), bg=self.accent_green, fg=self.text_light,
            activebackground=self.secondary_bg, activeforeground=self.text_light
        )
        self.received_next_button.pack(side="left", padx=5)

        # Pagination states
        self.pending_page = 0
        self.pending_items_per_page = 10
        self.received_page = 0
        self.received_items_per_page = 10

        self.load_pending_table()
        self.load_received_table()


    def load_pending_table(self):
        for row in self.pending_tree.get_children():
            self.pending_tree.delete(row)

        conn = sqlite3.connect("docusortDB.db")
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM documents WHERE doc_type = 'Pending'")
        total_rows = cursor.fetchone()[0]

        offset = self.pending_page * self.pending_items_per_page

        cursor.execute("""
            SELECT sender_fname, sender_surname, studnum, sender_course, doc_type, datetime
            FROM documents
            WHERE doc_type = 'Pending'
            ORDER BY datetime DESC
            LIMIT ? OFFSET ?
        """, (self.pending_items_per_page, offset))

        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            self.pending_tree.insert("", "end", values=row)

        self.pending_prev_button.config(state="disabled" if self.pending_page == 0 else "normal")
        self.pending_next_button.config(
            state="disabled" if (self.pending_page + 1) * self.pending_items_per_page >= total_rows else "normal"
        )


    def pending_next_page(self):
        self.pending_page += 1
        self.load_pending_table()


    def pending_prev_page(self):
        if self.pending_page > 0:
            self.pending_page -= 1
            self.load_pending_table()


    def load_received_table(self):
        for row in self.received_tree.get_children():
            self.received_tree.delete(row)

        conn = sqlite3.connect("docusortDB.db")
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM documents WHERE doc_type = 'Received'")
        total_rows = cursor.fetchone()[0]

        offset = self.received_page * self.received_items_per_page

        cursor.execute("""
            SELECT sender_fname, sender_surname, studnum, sender_course, doc_type, datetime
            FROM documents
            WHERE doc_type = 'Received'
            ORDER BY datetime DESC
            LIMIT ? OFFSET ?
        """, (self.received_items_per_page, offset))

        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            self.received_tree.insert("", "end", values=row)

        self.received_prev_button.config(state="disabled" if self.received_page == 0 else "normal")
        self.received_next_button.config(
            state="disabled" if (self.received_page + 1) * self.received_items_per_page >= total_rows else "normal"
        )


    def received_next_page(self):
        self.received_page += 1
        self.load_received_table()


    def received_prev_page(self):
        if self.received_page > 0:
            self.received_page -= 1
            self.load_received_table()

    def show_admin_users(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        title_label = tk.Label(
            self.content_frame,
            text="Admin User Management",
            font=("Courier New", 18, "bold"),
            bg=self.bg_dark,
            fg=self.text_light
        )
        title_label.pack(pady=10)

        # Admin users list frame
        users_frame = tk.Frame(self.content_frame, bg=self.bg_dark)
        users_frame.pack(padx=10, pady=10, fill="none", expand=False)

        # Create admin users table
        columns = ("id", "username", "role", "date_created", "last_login")
        self.admin_tree = ttk.Treeview(users_frame, columns=columns, show="headings", height=8)

        for col in columns:
            self.admin_tree.heading(col, text=col.replace("_", " ").title())
            self.admin_tree.column(col, anchor="center", width=140)

        self.admin_tree.pack(pady=10)

        # Load sample or actual admin users
        self.load_admin_users()

        # Button frame
        btn_frame = tk.Frame(self.content_frame, bg=self.bg_dark)
        btn_frame.pack(pady=10)

        add_btn = tk.Button(
            btn_frame, 
            text="Add New Admin", 
            command=self.show_add_admin_form,
            font=("Courier New", 12),
            bg=self.accent_green,
            fg=self.text_light,
            padx=10
        )
        add_btn.pack(side="left", padx=5)

        delete_btn = tk.Button(
            btn_frame, 
            text="Delete Selected", 
            command=self.delete_admin_user,
            font=("Courier New", 12),
            bg="#d9534f",  # Red color for delete
            fg=self.text_light,
            padx=10
        )
        delete_btn.pack(side="left", padx=5)

    def load_admin_users(self):
        # Clear existing items
        for row in self.admin_tree.get_children():
            self.admin_tree.delete(row)

        try:
            # Connect to the database
            conn = sqlite3.connect("docusortDB.db")
            cursor = conn.cursor()
            
            # Check if admin_users table exists
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='admin_users'
            """)
            
            if not cursor.fetchone():
                # Create table if it doesn't exist
                cursor.execute("""
                    CREATE TABLE admin_users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        role TEXT NOT NULL,
                        date_created TEXT NOT NULL,
                        last_login TEXT
                    )
                """)
                conn.commit()
                
                # Insert default admin if table was just created
                cursor.execute("""
                    INSERT INTO admin_users (username, password, role, date_created)
                    VALUES (?, ?, ?, datetime('now'))
                """, ("admin", "admin123", "Super Admin"))
                conn.commit()
            
            # Get admin users
            cursor.execute("""
                SELECT id, username, role, date_created, last_login
                FROM admin_users
                ORDER BY id
            """)
            
            admin_users = cursor.fetchall()
            conn.close()
            
            # Insert into treeview
            for user in admin_users:
                self.admin_tree.insert("", "end", values=user)
                
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to load admin users: {e}")
            
    def delete_admin_user(self):
        selected_item = self.admin_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an admin user to delete.", parent=self.root)
            return
            
        user_id = self.admin_tree.item(selected_item[0], 'values')[0]
        username = self.admin_tree.item(selected_item[0], 'values')[1]
        
        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Delete", 
                                      f"Are you sure you want to delete admin user '{username}'?", 
                                      parent=self.root)
        if not confirm:
            return
            
        try:
            conn = sqlite3.connect("docusortDB.db")
            cursor = conn.cursor()
            
            # Delete user
            cursor.execute("DELETE FROM admin_users WHERE id = ?", (user_id,))
            conn.commit()
            conn.close()
            
            # Refresh the list
            self.load_admin_users()
            messagebox.showinfo("Success", f"Admin user '{username}' has been deleted.", parent=self.root)
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to delete admin user: {e}", parent=self.root)
            
    def show_add_admin_form(self):
        # Create a new top-level window for the form
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Admin User")
        add_window.configure(bg=self.bg_dark)
        add_window.geometry("400x450")
        add_window.resizable(False, False)
        
        # Make it modal
        add_window.transient(self.root)
        add_window.grab_set()
        
        # Form title
        tk.Label(
            add_window,
            text="Register New Admin User",
            font=("Courier New", 16, "bold"),
            bg=self.bg_dark,
            fg=self.accent_green
        ).pack(pady=20)
        
        # Form container
        form_frame = tk.Frame(add_window, bg=self.bg_dark, padx=30, pady=10)
        form_frame.pack(fill="both")
        
        # Username
        tk.Label(
            form_frame,
            text="Username:",
            font=("Courier New", 12),
            bg=self.bg_dark,
            fg=self.text_light,
            anchor="w"
        ).pack(fill="x", pady=(10, 0))
        
        username_var = tk.StringVar()
        username_entry = tk.Entry(
            form_frame,
            font=("Courier New", 12),
            bg=self.secondary_bg,
            fg=self.text_light,
            insertbackground=self.text_light,
            textvariable=username_var
        )
        username_entry.pack(fill="x", pady=(0, 10))
        
        # Password
        tk.Label(
            form_frame,
            text="Password:",
            font=("Courier New", 12),
            bg=self.bg_dark,
            fg=self.text_light,
            anchor="w"
        ).pack(fill="x", pady=(10, 0))
        
        password_var = tk.StringVar()
        password_entry = tk.Entry(
            form_frame,
            font=("Courier New", 12),
            bg=self.secondary_bg,
            fg=self.text_light,
            insertbackground=self.text_light,
            textvariable=password_var,
            show="*"
        )
        password_entry.pack(fill="x", pady=(0, 10))
        
        # Confirm Password
        tk.Label(
            form_frame,
            text="Confirm Password:",
            font=("Courier New", 12),
            bg=self.bg_dark,
            fg=self.text_light,
            anchor="w"
        ).pack(fill="x", pady=(10, 0))
        
        confirm_var = tk.StringVar()
        confirm_entry = tk.Entry(
            form_frame,
            font=("Courier New", 12),
            bg=self.secondary_bg,
            fg=self.text_light,
            insertbackground=self.text_light,
            textvariable=confirm_var,
            show="*"
        )
        confirm_entry.pack(fill="x", pady=(0, 10))
        
        # Role
        tk.Label(
            form_frame,
            text="Role:",
            font=("Courier New", 12),
            bg=self.bg_dark,
            fg=self.text_light,
            anchor="w"
        ).pack(fill="x", pady=(10, 0))
        
        role_var = tk.StringVar(value="Admin")
        roles = ["Admin", "Super Admin", "Viewer"]
        role_dropdown = ttk.Combobox(
            form_frame,
            font=("Courier New", 12),
            textvariable=role_var,
            values=roles,
            state="readonly"
        )
        role_dropdown.pack(fill="x", pady=(0, 20))
        
        # Button frame
        button_frame = tk.Frame(add_window, bg=self.bg_dark, pady=10)
        button_frame.pack()
        
        # Register button
        register_btn = tk.Button(
            button_frame,
            text="Register Admin",
            font=("Courier New", 12, "bold"),
            bg=self.accent_green,
            fg=self.text_light,
            padx=15,
            pady=5,
            command=lambda: self.register_admin(
                username_var.get(),
                password_var.get(),
                confirm_var.get(),
                role_var.get(),
                add_window
            )
        )
        register_btn.pack(side="left", padx=10)
        
        # Cancel button
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            font=("Courier New", 12),
            bg=self.secondary_bg,
            fg=self.text_light,
            padx=15,
            pady=5,
            command=add_window.destroy
        )
        cancel_btn.pack(side="left", padx=10)
        
        # Focus on the first field
        username_entry.focus_set()
        
    def register_admin(self, username, password, confirm, role, window):
        # Validate inputs
        if not username or not password or not confirm:
            messagebox.showerror("Error", "All fields must be filled", parent=window)
            return
            
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match", parent=window)
            return
            
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters", parent=window)
            return
            
        try:
            conn = sqlite3.connect("docusortDB.db")
            cursor = conn.cursor()
            
            # Check if username already exists
            cursor.execute("SELECT id FROM admin_users WHERE username = ?", (username,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Username already exists", parent=window)
                conn.close()
                return
                
            # Insert new admin user
            cursor.execute("""
                INSERT INTO admin_users (username, password, role, date_created)
                VALUES (?, ?, ?, datetime('now'))
            """, (username, password, role))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "New admin user registered successfully", parent=window)
            window.destroy()
            
            # Refresh the admin users list
            self.load_admin_users()
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to register admin: {e}", parent=window)


    def update_content(self, title, message):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        title_label = tk.Label(self.content_frame, text=title,
                               font=("Courier New", 18, "bold"), bg=self.bg_dark, fg=self.text_light)
        title_label.pack(pady=20)

        message_label = tk.Label(self.content_frame, text=message,
                                 font=("Courier New", 14), bg=self.bg_dark, fg=self.text_light)
        message_label.pack(pady=10)

    def logout(self):
        confirm = messagebox.askyesno("Confirm Logout", "Are you sure you want to log out?", 
                                      parent=self.root)
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