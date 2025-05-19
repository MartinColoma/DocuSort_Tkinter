import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk


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
        sidebar_frame = tk.Frame(self.root, bg=self.bg_dark, width=375)
        sidebar_frame.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

        # Load the main image (now above "Admin Panel")
        try:
            image = Image.open("resources/docusort_test.png")
            image = image.resize((64, 64))  # Resize to a small icon
            self.photo = ImageTk.PhotoImage(image)

            img_label = tk.Label(sidebar_frame, image=self.photo, bg=self.bg_dark)
            img_label.pack(pady=(35, 10))  # Top margin and spacing before label
        except Exception as e:
            print(f"Error loading image: {e}")
            fallback_label = tk.Label(sidebar_frame, text="IMAGE NOT FOUND", font=("Courier New", 12),
                                    fg="red", bg=self.bg_dark)
            fallback_label.pack(pady=(20, 10))

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
                command=lambda cmd=command, btn_text=text: self.switch_page(cmd, btn_text), cursor="hand2"
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
        
        # Welcome header
        welcome_frame = tk.Frame(self.content_frame, bg=self.bg_dark)
        welcome_frame.pack(fill="x", pady=(10, 20))
        
        welcome_label = tk.Label(
            welcome_frame,
            text="Welcome to DocuSort - Admin Dashboard",
            font=("Courier New", 32, "bold"),
            bg=self.bg_dark,
            fg=self.text_light
        )
        welcome_label.pack(pady=10)
        
        # Get document counts from database
        conn = sqlite3.connect("docusortDB.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM documents WHERE doc_type = 'Pending'")
        pending_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM documents WHERE doc_type = 'Received'")
        received_count = cursor.fetchone()[0]
        
        conn.close()
        
        # Create frame for statistics cards
        stats_frame = tk.Frame(self.content_frame, bg=self.bg_dark)
        stats_frame.pack(fill="x", padx=20, pady=10)
        
        # Configure grid columns to be equal width
        stats_frame.columnconfigure(0, weight=1)
        stats_frame.columnconfigure(1, weight=1)
        
        # Create container for table content (will hold pending and received tables)
        self.tables_container = tk.Frame(self.content_frame, bg=self.bg_dark)
        self.tables_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Function to switch between tables
        def show_pending_table():
            self.pending_card.config(bg=self.accent_green, relief="raised")
            self.pending_title.config(bg=self.accent_green)
            self.pending_count_label.config(bg=self.accent_green)
            
            self.received_card.config(bg="#4d94ff", relief="flat")
            self.received_title.config(bg="#4d94ff")
            self.received_count_label.config(bg="#4d94ff")
            
            self.pending_table_frame.pack(fill="both", expand=True)
            self.received_table_frame.pack_forget()
            
            # Reload the pending table data
            self.load_pending_table()
        
        def show_received_table():
            self.pending_card.config(bg="#2e7d32", relief="flat")  # Darker green for inactive
            self.pending_title.config(bg="#2e7d32")
            self.pending_count_label.config(bg="#2e7d32")
            
            self.received_card.config(bg="#1976d2", relief="raised")  # Brighter blue for active
            self.received_title.config(bg="#1976d2")
            self.received_count_label.config(bg="#1976d2")
            
            self.pending_table_frame.pack_forget()
            self.received_table_frame.pack(fill="both", expand=True)
            
            # Reload the received table data
            self.load_received_table()
        
        # Pending Documents Card
        self.pending_card = tk.Frame(
            stats_frame,
            bg=self.accent_green,  # Active state color
            padx=15,
            pady=15,
            highlightthickness=1,
            highlightbackground="#ffffff",
            relief="raised",
            cursor="hand2"  # Hand cursor to indicate it's clickable
        )
        self.pending_card.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        self.pending_title = tk.Label(
            self.pending_card,
            text="Pending Documents",
            font=("Courier New", 24, "bold"),
            bg=self.accent_green,
            fg=self.text_dark
        )
        self.pending_title.pack()
        
        self.pending_count_label = tk.Label(
            self.pending_card,
            text=str(pending_count),
            font=("Courier New", 32, "bold"),
            bg=self.accent_green,
            fg=self.text_dark
        )
        self.pending_count_label.pack(pady=5)
        
        # Bind click events to the labels and frame
        self.pending_card.bind("<Button-1>", lambda e: show_pending_table())
        self.pending_title.bind("<Button-1>", lambda e: show_pending_table())
        self.pending_count_label.bind("<Button-1>", lambda e: show_pending_table())
        
        # Received Documents Card
        self.received_card = tk.Frame(
            stats_frame,
            bg="#4d94ff",  # Inactive state color
            padx=15,
            pady=15,
            highlightthickness=1,
            highlightbackground="#ffffff",
            relief="flat",
            cursor="hand2"  # Hand cursor to indicate it's clickable
        )
        self.received_card.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        self.received_title = tk.Label(
            self.received_card,
            text="Received Documents",
            font=("Courier New", 24, "bold"),
            bg="#4d94ff",
            fg=self.text_dark
        )
        self.received_title.pack()
        
        self.received_count_label = tk.Label(
            self.received_card,
            text=str(received_count),
            font=("Courier New", 32, "bold"),
            bg="#4d94ff",
            fg=self.text_dark
        )
        self.received_count_label.pack(pady=5)
        
        # Bind click events to the labels and frame
        self.received_card.bind("<Button-1>", lambda e: show_received_table())
        self.received_title.bind("<Button-1>", lambda e: show_received_table())
        self.received_count_label.bind("<Button-1>", lambda e: show_received_table())
        
        # Define common table properties
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

        # Updated style configuration
        style = ttk.Style()
        style.configure("Treeview", font=("Courier New", 12), rowheight=30)
        style.configure("Treeview.Heading", font=("Courier New", 12, "bold"), anchor="center")  # Center headers
        
        # Create both table frames but only display pending by default
        
        # PENDING DOCUMENTS TABLE
        self.pending_table_frame = tk.LabelFrame(
            self.tables_container,
            text="Pending Documents",
            font=("Courier New", 24, "bold"),
            bg=self.bg_dark,
            fg=self.text_light,
            padx=10, 
            pady=10
        )
        # Don't pack yet - we'll control visibility with show/hide functions
        
        # Add search bar for pending documents
        pending_search_frame = tk.Frame(self.pending_table_frame, bg=self.bg_dark)
        pending_search_frame.pack(fill="x", pady=(5, 10))
        
        search_label = tk.Label(
            pending_search_frame, 
            text="Search:", 
            font=("Courier New", 12),
            bg=self.bg_dark,
            fg=self.text_light
        )
        search_label.pack(side="left", padx=(0, 10))
        
        self.pending_search_var = tk.StringVar()
        self.pending_search_var.trace("w", lambda name, index, mode, sv=self.pending_search_var: self.search_pending_documents(sv))
        
        self.pending_search_entry = tk.Entry(
            pending_search_frame,
            textvariable=self.pending_search_var,
            font=("Courier New", 12),
            bg="#2a2a2a",
            fg=self.text_light,
            insertbackground=self.text_light,  # Cursor color
            relief="flat",
            highlightthickness=1,
            highlightbackground="#555555",
            highlightcolor=self.accent_green,
            width=40
        )
        self.pending_search_entry.pack(side="left", fill="x", expand=True)
        
        search_clear_button = tk.Button(
            pending_search_frame,
            text="✕",
            font=("Courier New", 10),
            bg=self.bg_dark,
            fg=self.text_light,
            activebackground="#444444",
            activeforeground=self.text_light,
            relief="flat",
            borderwidth=0,
            command=lambda: self.clear_search("pending")
        )
        search_clear_button.pack(side="left", padx=(5, 0))
        
        # Create a container for the table and scrollbar
        pending_table_container = tk.Frame(self.pending_table_frame, bg=self.bg_dark)
        pending_table_container.pack(fill="both", expand=True)
        
        # Updated to exactly 10 rows
        self.pending_tree = ttk.Treeview(
            pending_table_container, columns=columns, show="headings", height=10
        )
        for col in columns:
            self.pending_tree.heading(col, text=column_titles[col], anchor="center")  # Center headers
            self.pending_tree.column(col, anchor="w", width=column_widths[col])  # Left-align content

        pending_scrollbar = ttk.Scrollbar(
            pending_table_container, orient="vertical", command=self.pending_tree.yview
        )
        self.pending_tree.configure(yscrollcommand=pending_scrollbar.set)
        self.pending_tree.pack(side="left", fill="both", expand=True)
        pending_scrollbar.pack(side="right", fill="y")

        # Create navigation frame and place it below the table
        pending_nav_frame = tk.Frame(self.pending_table_frame, bg=self.bg_dark)
        pending_nav_frame.pack(fill="x", pady=10)
        
        # Create a left spacer to push the prev button to the left
        tk.Frame(pending_nav_frame, bg=self.bg_dark).pack(side="left", expand=True)
        
        self.pending_next_button = tk.Button(
            pending_nav_frame, text="Next →", command=self.pending_next_page,
            font=("Courier New", 12), bg=self.bg_dark, fg=self.text_light,
            borderwidth=0, highlightthickness=0, relief="flat", cursor="hand2"
        )
        self.pending_next_button.pack(side="right", padx=10)

        self.pending_prev_button = tk.Button(
            pending_nav_frame, text="← Previous", command=self.pending_prev_page,
            font=("Courier New", 12), bg=self.bg_dark, fg=self.text_light,
            borderwidth=0, highlightthickness=0, relief="flat", cursor="hand2"
        )
        self.pending_prev_button.pack(side="right", padx=10)

        # Create a right spacer to push the next button to the right
        tk.Frame(pending_nav_frame, bg=self.bg_dark).pack(side="left", expand=True)

        # RECEIVED DOCUMENTS TABLE
        self.received_table_frame = tk.LabelFrame(
            self.tables_container,
            text="Received Documents",
            font=("Courier New", 24, "bold"),
            bg=self.bg_dark,
            fg=self.text_light,
            padx=10,
            pady=10
        )
        # Don't pack yet - we'll control visibility with show/hide functions
        
        # Add search bar for received documents
        received_search_frame = tk.Frame(self.received_table_frame, bg=self.bg_dark)
        received_search_frame.pack(fill="x", pady=(5, 10))
        
        search_label = tk.Label(
            received_search_frame, 
            text="Search:", 
            font=("Courier New", 12),
            bg=self.bg_dark,
            fg=self.text_light
        )
        search_label.pack(side="left", padx=(0, 10))
        
        self.received_search_var = tk.StringVar()
        self.received_search_var.trace("w", lambda name, index, mode, sv=self.received_search_var: self.search_received_documents(sv))
        
        self.received_search_entry = tk.Entry(
            received_search_frame,
            textvariable=self.received_search_var,
            font=("Courier New", 12),
            bg="#2a2a2a",
            fg=self.text_light,
            insertbackground=self.text_light,  # Cursor color
            relief="flat",
            highlightthickness=1,
            highlightbackground="#555555",
            highlightcolor="#1976d2",
            width=40
        )
        self.received_search_entry.pack(side="left", fill="x", expand=True)
        
        search_clear_button = tk.Button(
            received_search_frame,
            text="✕",
            font=("Courier New", 10),
            bg=self.bg_dark,
            fg=self.text_light,
            activebackground="#444444",
            activeforeground=self.text_light,
            relief="flat",
            borderwidth=0,
            command=lambda: self.clear_search("received")
        )
        search_clear_button.pack(side="left", padx=(5, 0))

        # Create a container for the table and scrollbar
        received_table_container = tk.Frame(self.received_table_frame, bg=self.bg_dark)
        received_table_container.pack(fill="both", expand=True)
        
        # Updated to exactly 10 rows
        self.received_tree = ttk.Treeview(
            received_table_container, columns=columns, show="headings", height=10
        )
        for col in columns:
            self.received_tree.heading(col, text=column_titles[col], anchor="center")  # Center headers
            self.received_tree.column(col, anchor="w", width=column_widths[col])  # Left-align content

        received_scrollbar = ttk.Scrollbar(
            received_table_container, orient="vertical", command=self.received_tree.yview
        )
        self.received_tree.configure(yscrollcommand=received_scrollbar.set)
        self.received_tree.pack(side="left", fill="both", expand=True)
        received_scrollbar.pack(side="right", fill="y")

        # Create navigation frame and place it below the table
        received_nav_frame = tk.Frame(self.received_table_frame, bg=self.bg_dark)
        received_nav_frame.pack(fill="x", pady=10)
        
        # Create a left spacer to push the prev button to the left
        tk.Frame(received_nav_frame, bg=self.bg_dark).pack(side="left", expand=True)
        
        self.received_prev_button = tk.Button(
            received_nav_frame, text="← Previous", command=self.received_prev_page,            
            font=("Courier New", 12), bg=self.bg_dark, fg=self.text_light,
            borderwidth=0, highlightthickness=0, relief="flat", cursor="hand2"
        )
        self.received_prev_button.pack(side="right", padx=10)

        self.received_next_button = tk.Button(
            received_nav_frame, text="Next →", command=self.received_next_page,
            font=("Courier New", 12), bg=self.bg_dark, fg=self.text_light,
            borderwidth=0, highlightthickness=0, relief="flat", cursor="hand2"
        )
        self.received_next_button.pack(side="right", padx=10)
        
        # Create a right spacer to push the next button to the right
        tk.Frame(received_nav_frame, bg=self.bg_dark).pack(side="left", expand=True)

        # Pagination states - set to match table height
        self.pending_page = 0
        self.pending_items_per_page = 10  # Matches table height
        self.received_page = 0
        self.received_items_per_page = 10  # Matches table height
        
        # Search variables
        self.pending_search_active = False
        self.received_search_active = False
        self.pending_all_data = []  # To store all data for searching
        self.received_all_data = []  # To store all data for searching

        # Show pending table by default (initial state)
        show_pending_table()
        
    def load_pending_table(self):
        # Clear the existing table
        for row in self.pending_tree.get_children():
            self.pending_tree.delete(row)

        conn = sqlite3.connect("docusortDB.db")
        cursor = conn.cursor()

        # If search is active, we'll display from our filtered data
        if self.pending_search_active:
            # Display the current page of filtered data
            start_idx = self.pending_page * self.pending_items_per_page
            end_idx = start_idx + self.pending_items_per_page
            page_data = self.pending_filtered_data[start_idx:end_idx]
            
            for row in page_data:
                self.pending_tree.insert("", "end", values=row)
                
            # Update pagination buttons
            total_rows = len(self.pending_filtered_data)
        else:
            # Fetch all data if it's our first load or if search was just cleared
            if not hasattr(self, 'pending_all_data') or not self.pending_all_data:
                cursor.execute("""
                    SELECT sender_fname, sender_surname, studnum, sender_course, doc_type, datetime
                    FROM documents
                    WHERE doc_type = 'Pending'
                    ORDER BY datetime DESC
                """)
                self.pending_all_data = cursor.fetchall()
            
            # Count for pagination
            cursor.execute("SELECT COUNT(*) FROM documents WHERE doc_type = 'Pending'")
            total_rows = cursor.fetchone()[0]
            
            # Get the current page of data
            offset = self.pending_page * self.pending_items_per_page
            
            cursor.execute("""
                SELECT sender_fname, sender_surname, studnum, sender_course, doc_type, datetime
                FROM documents
                WHERE doc_type = 'Pending'
                ORDER BY datetime DESC
                LIMIT ? OFFSET ?
            """, (self.pending_items_per_page, offset))
            
            rows = cursor.fetchall()
            
            for row in rows:
                self.pending_tree.insert("", "end", values=row)

        conn.close()

        # Update pagination buttons
        self.pending_prev_button.config(state="disabled" if self.pending_page == 0 else "normal")
        self.pending_next_button.config(
            state="disabled" if (self.pending_page + 1) * self.pending_items_per_page >= total_rows else "normal"
        )


    def load_received_table(self):
        # Clear the existing table
        for row in self.received_tree.get_children():
            self.received_tree.delete(row)

        conn = sqlite3.connect("docusortDB.db")
        cursor = conn.cursor()

        # If search is active, we'll display from our filtered data
        if self.received_search_active:
            # Display the current page of filtered data
            start_idx = self.received_page * self.received_items_per_page
            end_idx = start_idx + self.received_items_per_page
            page_data = self.received_filtered_data[start_idx:end_idx]
            
            for row in page_data:
                self.received_tree.insert("", "end", values=row)
                
            # Update pagination buttons
            total_rows = len(self.received_filtered_data)
        else:
            # Fetch all data if it's our first load or if search was just cleared
            if not hasattr(self, 'received_all_data') or not self.received_all_data:
                cursor.execute("""
                    SELECT sender_fname, sender_surname, studnum, sender_course, doc_type, datetime
                    FROM documents
                    WHERE doc_type = 'Received'
                    ORDER BY datetime DESC
                """)
                self.received_all_data = cursor.fetchall()
                
            # Count for pagination
            cursor.execute("SELECT COUNT(*) FROM documents WHERE doc_type = 'Received'")
            total_rows = cursor.fetchone()[0]
            
            # Get the current page of data
            offset = self.received_page * self.received_items_per_page
            
            cursor.execute("""
                SELECT sender_fname, sender_surname, studnum, sender_course, doc_type, datetime
                FROM documents
                WHERE doc_type = 'Received'
                ORDER BY datetime DESC
                LIMIT ? OFFSET ?
            """, (self.received_items_per_page, offset))
            
            rows = cursor.fetchall()
            
            for row in rows:
                self.received_tree.insert("", "end", values=row)

        conn.close()

        # Update pagination buttons
        self.received_prev_button.config(state="disabled" if self.received_page == 0 else "normal")
        self.received_next_button.config(
            state="disabled" if (self.received_page + 1) * self.received_items_per_page >= total_rows else "normal"
        )


    def pending_next_page(self):
        self.pending_page += 1
        self.load_pending_table()


    def pending_prev_page(self):
        if self.pending_page > 0:
            self.pending_page -= 1
            self.load_pending_table()

    def received_next_page(self):
        self.received_page += 1
        self.load_received_table()


    def received_prev_page(self):
        if self.received_page > 0:
            self.received_page -= 1
            self.load_received_table()

    def search_pending_documents(self, search_var):
        """Filter pending documents based on search text"""
        search_text = search_var.get().lower()
        
        if not search_text:
            self.pending_search_active = False
            self.pending_page = 0  # Reset to first page
            self.load_pending_table()
            return
        
        # Make sure we have all data to search through
        if not hasattr(self, 'pending_all_data') or not self.pending_all_data:
            conn = sqlite3.connect("docusortDB.db")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT sender_fname, sender_surname, studnum, sender_course, doc_type, datetime
                FROM documents
                WHERE doc_type = 'Pending'
                ORDER BY datetime DESC
            """)
            self.pending_all_data = cursor.fetchall()
            conn.close()
        
        # Filter the data
        self.pending_filtered_data = []
        for row in self.pending_all_data:
            # Convert all fields to strings for searching
            row_string = ' '.join([str(item).lower() for item in row])
            if search_text in row_string:
                self.pending_filtered_data.append(row)
        
        self.pending_search_active = True
        self.pending_page = 0  # Reset to first page
        self.load_pending_table()

    def search_received_documents(self, search_var):
        """Filter received documents based on search text"""
        search_text = search_var.get().lower()
        
        if not search_text:
            self.received_search_active = False
            self.received_page = 0  # Reset to first page
            self.load_received_table()
            return
        
        # Make sure we have all data to search through
        if not hasattr(self, 'received_all_data') or not self.received_all_data:
            conn = sqlite3.connect("docusortDB.db")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT sender_fname, sender_surname, studnum, sender_course, doc_type, datetime
                FROM documents
                WHERE doc_type = 'Received'
                ORDER BY datetime DESC
            """)
            self.received_all_data = cursor.fetchall()
            conn.close()
        
        # Filter the data
        self.received_filtered_data = []
        for row in self.received_all_data:
            # Convert all fields to strings for searching
            row_string = ' '.join([str(item).lower() for item in row])
            if search_text in row_string:
                self.received_filtered_data.append(row)
        
        self.received_search_active = True
        self.received_page = 0  # Reset to first page
        self.load_received_table()

    def clear_search(self, table_type):
        """Clear search and reset to normal table view"""
        if table_type == "pending":
            self.pending_search_var.set("")
            self.pending_search_active = False
            self.pending_page = 0
            self.load_pending_table()
        else:  # received
            self.received_search_var.set("")
            self.received_search_active = False
            self.received_page = 0
            self.load_received_table()

#ADMIN USERS
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
        confirm = messagebox.askyesno("Confirm Logout", "Are you sure you want to log out?", parent=self.root)
        if confirm:
            print("Logging out and going back to login page")
            self.root.destroy()  # Close admin window

            from home_with_db import DocuSortApp
            login_window = tk.Toplevel(self.login_root)
            DocuSortApp(login_window)
        else:
            print("Logout canceled. Returning to Admin Dashboard.")
            messagebox.showinfo("Logout Cancelled", "Returning to Admin Dashboard")
            self.switch_page(self.show_dashboard, "Dashboard")



if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x600")
    app = AdminApp(root)
    root.mainloop()