import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk
from datetime import datetime  
import os
import sys


class AdminApp:
    def __init__(self, login_root, current_user=None):
        self.login_root = login_root
        self.current_user_username = current_user  
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
                            foreground=self.text_dark,
                            font=("Courier New", 10, "bold"))
        self.style.map("Treeview", 
                      background=[('selected', self.accent_green)],
                      foreground=[('selected', self.text_dark)])

        self.login_root.withdraw()  # Hide login window
        self.admin_home_page()
        self.root.protocol("WM_DELETE_WINDOW", self.logout)

    def resource_path(self, relative_path):
        """ Get absolute path to resource (for dev and PyInstaller .exe) """
        try:
            # PyInstaller stores temp path in _MEIPASS
            base_path = sys._MEIPASS
        except AttributeError:
            # Running in development mode
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
    
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
            image_path = self.resource_path("resources/docusort_test.png")
            image = Image.open(image_path)
            image = image.resize((64, 64))  # Resize to a small icon
            self.photo = ImageTk.PhotoImage(image)

            img_label = tk.Label(sidebar_frame, image=self.photo, bg=self.bg_dark)
            img_label.pack(pady=(35, 10))  # Top margin and spacing before label
        except Exception as e:
            print(f"Error loading image: {e}")
            fallback_label = tk.Label(sidebar_frame, text="IMAGE NOT FOUND", font=("Courier New", 12),
                                    fg="red", bg=self.bg_dark)
            fallback_label.pack(pady=(20, 10))
        
        admin_name = tk.Label(
            sidebar_frame,
            text=f"Hello, {self.current_user_username}",
            font=("Courier New", 16, "bold"),
            bg=self.bg_dark,
            fg=self.accent_green,
            anchor="w",  # Align text to the left inside the label
            justify="left"
        )
        admin_name.pack(pady=10, padx=10, anchor="w", fill="x")
        
        # Add separator after admin name label
        separator_after_label = tk.Frame(sidebar_frame, height=1, bg="white")
        separator_after_label.pack(fill="x", pady=(10, 20), padx=10)
        
        # Store buttons here for easy access    
        self.sidebar_buttons = {}

        # Sidebar buttons data
        sidebar_buttons_data = [
            ("Dashboard", self.show_dashboard),
            ("Admin Users", self.show_admin_users),
            ("Log Out", self.logout)
        ]

        for i, (text, command) in enumerate(sidebar_buttons_data):
            # Add separator before logout button
            if text == "Log Out":
                separator = tk.Frame(sidebar_frame, height=1, bg="white")
                separator.pack(fill="x", pady=(20, 10), padx=10)

            button = tk.Button(
                sidebar_frame, 
                text=text, 
                font=("Courier New", 16), 
                fg="white",  # Changed from self.accent_green to white
                bg=self.bg_dark,
                relief="flat", 
                activebackground=self.accent_green, 
                activeforeground=self.text_light,
                command=lambda cmd=command, btn_text=text: self.switch_page(cmd, btn_text), 
                cursor="hand2",
                anchor="w"  # Align button text to the left
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
            text="DocuSort Admin Dashboard",
            font=("Courier New", 32, "bold"),
            bg=self.bg_dark,
            fg=self.text_light
        )
        welcome_label.pack(pady=10)
        
        # Get document counts from database
        conn = sqlite3.connect(self.resource_path("docusortDB.db"))
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
            self.clear_search("pending")
        
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
            self.clear_search("received ")
        
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
        columns = ("first_name", "last_name", "student_number", "sender_fac","doc_type")
        column_titles = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "student_number": "Student Number",
            "sender_fac": "Faculty",
            "doc_type": "Status"
        }
        column_widths = {
            "first_name": 200,
            "last_name": 200,
            "student_number": 160,
            "sender_fac": 400,
            "doc_type": 160
        }

        # Updated style configuration
        style = ttk.Style()
        style.configure("Treeview", font=("Courier New", 12), rowheight=30)
        style.configure("Treeview.Heading", font=("Courier New", 12, "bold"), anchor="center", foreground=self.text_dark)  # Center headers
        
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
        
        # Add combined frame for search bar and quick action button
        pending_search_frame = tk.Frame(self.pending_table_frame, bg=self.bg_dark)
        pending_search_frame.pack(fill="x", pady=(5, 10), padx=10)

        # Search Label
        search_label = tk.Label(
            pending_search_frame, 
            text="Search:", 
            font=("Courier New", 12),
            bg=self.bg_dark,
            fg=self.text_light
        )
        search_label.pack(side="left", padx=(0, 5))

        # Container to overlap Entry + Clear Button
        pending_entry_container = tk.Frame(pending_search_frame, bg=self.bg_dark)
        pending_entry_container.pack(side="left")

        # Search Variable and Entry
        self.pending_search_var = tk.StringVar()
        self.pending_search_var.trace("w", lambda name, index, mode, sv=self.pending_search_var: self.search_pending_documents(sv))

        self.pending_search_entry = tk.Entry(
            pending_entry_container,
            textvariable=self.pending_search_var,
            font=("Courier New", 12),
            bg="#2a2a2a",
            fg=self.text_light,
            insertbackground=self.text_light,
            relief="flat",
            highlightthickness=1,
            highlightbackground="#555555",
            highlightcolor=self.accent_green,
            width=30  # Reduced width for compact layout
        )
        self.pending_search_entry.pack()

        # Clear Search Button (positioned over entry)
        search_clear_button = tk.Button(
            pending_entry_container,
            text="✕",
            font=("Courier New", 10),
            bg="#2a2a2a",  # Same as entry background for seamless look
            fg=self.text_light,
            activebackground="#3a3a3a",
            activeforeground=self.text_light,
            relief="flat",
            borderwidth=0,
            command=lambda: self.clear_search("pending"),
            cursor="hand2"
        )
        search_clear_button.place(relx=1.0, rely=0.5, x=-3, y=-1, anchor="e", width=20, height=20)

        # Convert All Button
        convert_all_btn = tk.Button(
            pending_search_frame,
            text="Mark ALL Pending as Received",
            font=("Courier New", 12, "bold"),
            bg="#1976d2",  # Blue
            fg=self.text_light,
            padx=15,
            pady=3,
            relief="flat",
            cursor="hand2",
            command=self.convert_all_pending_to_received
        )
        convert_all_btn.pack(side="right")
                
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
        
        # Create spacers and containers for better layout
        tk.Frame(pending_nav_frame, bg=self.bg_dark).pack(side="left", expand=True)
        
        # Previous button
        self.pending_prev_button = tk.Button(
            pending_nav_frame, text="← Prev", command=self.pending_prev_page,
            font=("Courier New", 12), bg=self.bg_dark, fg=self.text_light,
            borderwidth=0, highlightthickness=0, relief="flat", cursor="hand2"
        )
        self.pending_prev_button.pack(side="left", padx=10)
        
        # Page number indicators container
        self.pending_page_indicator_frame = tk.Frame(pending_nav_frame, bg=self.bg_dark)
        self.pending_page_indicator_frame.pack(side="left")
        
        # Page number labels - will be updated dynamically
        self.pending_page_prev = tk.Label(
            self.pending_page_indicator_frame, text="", 
            font=("Courier New", 12), bg=self.bg_dark, fg=self.text_light
        )
        self.pending_page_prev.pack(side="left", padx=5)
        
        self.pending_page_separator1 = tk.Label(
            self.pending_page_indicator_frame, text="-", 
            font=("Courier New", 12), bg=self.bg_dark, fg=self.text_light
        )
        self.pending_page_separator1.pack(side="left")
        
        self.pending_page_current = tk.Label(
            self.pending_page_indicator_frame, text="1", 
            font=("Courier New", 14, "bold"), bg=self.bg_dark, fg=self.accent_green
        )
        self.pending_page_current.pack(side="left", padx=5)
        
        self.pending_page_separator2 = tk.Label(
            self.pending_page_indicator_frame, text="-", 
            font=("Courier New", 12), bg=self.bg_dark, fg=self.text_light
        )
        self.pending_page_separator2.pack(side="left")
        
        self.pending_page_next = tk.Label(
            self.pending_page_indicator_frame, text="", 
            font=("Courier New", 12), bg=self.bg_dark, fg=self.text_light
        )
        self.pending_page_next.pack(side="left", padx=5)
        
        # Next button
        self.pending_next_button = tk.Button(
            pending_nav_frame, text="Next →", command=self.pending_next_page,
            font=("Courier New", 12), bg=self.bg_dark, fg=self.text_light,
            borderwidth=0, highlightthickness=0, relief="flat", cursor="hand2"
        )
        self.pending_next_button.pack(side="left", padx=10)
        
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
        received_search_frame.pack(fill="x", pady=(5, 10), padx=10)

        # Label
        search_label = tk.Label(
            received_search_frame, 
            text="Search:", 
            font=("Courier New", 12),
            bg=self.bg_dark,
            fg=self.text_light
        )
        search_label.pack(side="left", padx=(0, 5))

        # Entry container for input and button
        entry_container = tk.Frame(received_search_frame, bg=self.bg_dark)
        entry_container.pack(side="left")

        # StringVar and Entry field (narrower width)
        self.received_search_var = tk.StringVar()
        self.received_search_var.trace("w", lambda name, index, mode, sv=self.received_search_var: self.search_received_documents(sv))

        self.received_search_entry = tk.Entry(
            entry_container,
            textvariable=self.received_search_var,
            font=("Courier New", 12),
            bg="#2a2a2a",
            fg=self.text_light,
            insertbackground=self.text_light,
            relief="flat",
            highlightthickness=1,
            highlightbackground="#555555",
            highlightcolor="#1976d2",
            width=30  # 👈 Reduce width (adjust as needed)
        )
        self.received_search_entry.pack()

        # Clear Button (✕) placed inside the container
        search_clear_button = tk.Button(
            entry_container,
            text="✕",
            font=("Courier New", 10),
            bg="#2a2a2a",
            fg=self.text_light,
            activebackground="#3a3a3a",
            activeforeground=self.text_light,
            relief="flat",
            borderwidth=0,
            command=lambda: self.clear_search("received"),
            cursor="hand2"
        )
        # Position over Entry (tightly aligned to right)
        search_clear_button.place(relx=1.0, rely=0.5, x=-3, y=-1, anchor="e", width=20, height=20)


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
        # Update the navigation frame for the received table
        received_nav_frame = tk.Frame(self.received_table_frame, bg=self.bg_dark)
        received_nav_frame.pack(fill="x", pady=10)
        
        # Create spacers and containers for better layout
        tk.Frame(received_nav_frame, bg=self.bg_dark).pack(side="left", expand=True)
        
        # Previous button
        self.received_prev_button = tk.Button(
            received_nav_frame, text="← Prev", command=self.received_prev_page,
            font=("Courier New", 12), bg=self.bg_dark, fg=self.text_light,
            borderwidth=0, highlightthickness=0, relief="flat", cursor="hand2"
        )
        self.received_prev_button.pack(side="left", padx=10)
        
        # Page number indicators container
        self.received_page_indicator_frame = tk.Frame(received_nav_frame, bg=self.bg_dark)
        self.received_page_indicator_frame.pack(side="left")
        
        # Page number labels - will be updated dynamically
        self.received_page_prev = tk.Label(
            self.received_page_indicator_frame, text="", 
            font=("Courier New", 12), bg=self.bg_dark, fg=self.text_light
        )
        self.received_page_prev.pack(side="left", padx=5)
        
        self.received_page_separator1 = tk.Label(
            self.received_page_indicator_frame, text="-", 
            font=("Courier New", 12), bg=self.bg_dark, fg=self.text_light
        )
        self.received_page_separator1.pack(side="left")
        
        self.received_page_current = tk.Label(
            self.received_page_indicator_frame, text="1", 
            font=("Courier New", 14, "bold"), bg=self.bg_dark, fg="#1976d2"  # Blue color for received
        )
        self.received_page_current.pack(side="left", padx=5)
        
        self.received_page_separator2 = tk.Label(
            self.received_page_indicator_frame, text="-", 
            font=("Courier New", 12), bg=self.bg_dark, fg=self.text_light
        )
        self.received_page_separator2.pack(side="left")
        
        self.received_page_next = tk.Label(
            self.received_page_indicator_frame, text="", 
            font=("Courier New", 12), bg=self.bg_dark, fg=self.text_light
        )
        self.received_page_next.pack(side="left", padx=5)
        
        # Next button
        self.received_next_button = tk.Button(
            received_nav_frame, text="Next →", command=self.received_next_page,
            font=("Courier New", 12), bg=self.bg_dark, fg=self.text_light,
            borderwidth=0, highlightthickness=0, relief="flat", cursor="hand2"
        )
        self.received_next_button.pack(side="left", padx=10)
        
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
        
                # In the show_dashboard method, after creating the pending_tree:
        self.pending_tree.bind("<Double-1>", lambda event: self.show_document_details("pending"))

        # In the show_dashboard method, after creating the received_tree:
        self.received_tree.bind("<Double-1>", lambda event: self.show_document_details("received"))
        
        self.create_table_context_menu()


    def convert_all_pending_to_received(self):
        """Convert all pending documents to received status"""
        try:
            # First, count how many documents will be affected
            conn = sqlite3.connect(self.resource_path("docusortDB.db"))
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM documents WHERE doc_type = 'Pending'")
            pending_count = cursor.fetchone()[0]
            
            if pending_count == 0:
                messagebox.showinfo("No Documents", "There are no pending documents to convert.", parent=self.root)
                conn.close()
                return
            
            # Confirm before proceeding with bulk update
            confirm = messagebox.askyesno(
                "Confirm Action", 
                f"Are you sure you want to mark ALL {pending_count} pending documents as received?", 
                parent=self.root
            )
            
            if not confirm:
                conn.close()
                return
            
            # Update all pending documents
            cursor.execute("UPDATE documents SET doc_type = 'Received' WHERE doc_type = 'Pending'")
            conn.commit()
            
            # Get new counts
            cursor.execute("SELECT COUNT(*) FROM documents WHERE doc_type = 'Pending'")
            new_pending_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM documents WHERE doc_type = 'Received'")
            new_received_count = cursor.fetchone()[0]
            
            conn.close()
            
            # Show success message
            messagebox.showinfo(
                "Success", 
                f"All pending documents have been marked as received. \n\nDocuments processed: {pending_count}", 
                parent=self.root
            )
            
            # Refresh both tables
            self.pending_page = 0  # Reset to first page
            self.received_page = 0  # Reset to first page
            self.load_pending_table()
            self.load_received_table()
            
            # Update the count labels
            self.pending_count_label.config(text=str(new_pending_count))
            self.received_count_label.config(text=str(new_received_count))
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to update documents: {e}", parent=self.root)  
        
    def update_pending_page_indicators(self):
        """Update the pending page number indicators based on current page"""
        # Calculate total pages
        total_data = len(self.pending_all_data if self.pending_search_active else self.get_all_pending_data())
        total_pages = max((total_data - 1) // self.pending_items_per_page + 1, 1)
        
        # Current page number (1-based for display)
        current_page = self.pending_page + 1
        
        # Update current page display
        self.pending_page_current.config(text=str(current_page))
        
        # Calculate previous and next page numbers
        prev_page = current_page - 1
        next_page = current_page + 1
        
        # Only show previous page if it exists
        if prev_page >= 1:
            self.pending_page_prev.config(text=str(prev_page))
            self.pending_page_separator1.config(text="-")
        else:
            self.pending_page_prev.config(text="")
            self.pending_page_separator1.config(text="")
        
        # Only show next page if it exists
        if next_page <= total_pages:
            self.pending_page_next.config(text=str(next_page))
            self.pending_page_separator2.config(text="-")
        else:
            self.pending_page_next.config(text="")
            self.pending_page_separator2.config(text="")
        
        # Enable/disable navigation buttons based on page position
        self.pending_prev_button.config(state="normal" if current_page > 1 else "disabled")
        self.pending_next_button.config(state="normal" if current_page < total_pages else "disabled")

    def update_received_page_indicators(self):
        """Update the received page number indicators based on current page"""
        # Calculate total pages
        total_data = len(self.received_all_data if self.received_search_active else self.get_all_received_data())
        total_pages = max((total_data - 1) // self.received_items_per_page + 1, 1)
        
        # Current page number (1-based for display)
        current_page = self.received_page + 1
        
        # Update current page display
        self.received_page_current.config(text=str(current_page))
        
        # Calculate previous and next page numbers
        prev_page = current_page - 1
        next_page = current_page + 1
        
        # Only show previous page if it exists
        if prev_page >= 1:
            self.received_page_prev.config(text=str(prev_page))
            self.received_page_separator1.config(text="-")
        else:
            self.received_page_prev.config(text="")
            self.received_page_separator1.config(text="")
        
        # Only show next page if it exists
        if next_page <= total_pages:
            self.received_page_next.config(text=str(next_page))
            self.received_page_separator2.config(text="-")
        else:
            self.received_page_next.config(text="")
            self.received_page_separator2.config(text="")
        
        # Enable/disable navigation buttons based on page position
        self.received_prev_button.config(state="normal" if current_page > 1 else "disabled")
        self.received_next_button.config(state="normal" if current_page < total_pages else "disabled")

    # ------------------ GET ALL PENDING DATA ------------------
    def get_all_pending_data(self):
        conn = sqlite3.connect(self.resource_path("docusortDB.db"))
        cursor = conn.cursor()
        cursor.execute("""
            SELECT sender_fname, sender_surname, studnum, sender_fac, doc_type, datetime, id
            FROM documents 
            WHERE doc_type = 'Pending'
        """)
        result = cursor.fetchall()
        conn.close()
        return result

    # ------------------ LOAD PENDING TABLE ------------------
    def load_pending_table(self):
        for item in self.pending_tree.get_children():
            self.pending_tree.delete(item)

        if self.pending_search_active:
            data = self.pending_all_data
        else:
            data = self.get_all_pending_data()
            self.pending_all_data = data

        def get_datetime(row):
            dt_str = row[5]  # datetime is index 5
            try:
                return datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
            except (ValueError, TypeError):
                return datetime.min

        sorted_data = sorted(data, key=get_datetime, reverse=True)

        start = self.pending_page * self.pending_items_per_page
        end = start + self.pending_items_per_page
        page_data = sorted_data[start:end]

        for row in page_data:
            self.pending_tree.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4]), tags=(str(row[6]),))

        self.update_pending_page_indicators()

    # ------------------ GET ALL RECEIVED DATA ------------------
    def get_all_received_data(self):
        conn = sqlite3.connect(self.resource_path("docusortDB.db"))
        cursor = conn.cursor()
        cursor.execute("""
            SELECT sender_fname, sender_surname, studnum, sender_fac, doc_type, datetime, id
            FROM documents 
            WHERE doc_type = 'Received'
        """)
        result = cursor.fetchall()
        conn.close()
        return result

    # ------------------ LOAD RECEIVED TABLE ------------------
    def load_received_table(self):
        for item in self.received_tree.get_children():
            self.received_tree.delete(item)

        if self.received_search_active:
            data = self.received_all_data
        else:
            data = self.get_all_received_data()
            self.received_all_data = data

        def get_datetime(row):
            dt_str = row[5]  # datetime is index 5
            try:
                return datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
            except (ValueError, TypeError):
                return datetime.min

        sorted_data = sorted(data, key=get_datetime, reverse=True)

        start = self.received_page * self.received_items_per_page
        end = start + self.received_items_per_page
        page_data = sorted_data[start:end]

        for row in page_data:
            self.received_tree.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4]), tags=(str(row[6]),))

        self.update_received_page_indicators()


          
    def pending_prev_page(self):
        """Navigate to the previous page of pending documents"""
        if self.pending_page > 0:
            self.pending_page -= 1
            self.load_pending_table()

    def pending_next_page(self):
        """Navigate to the next page of pending documents"""
        # Calculate total pages
        total_data = len(self.pending_all_data if self.pending_search_active else self.get_all_pending_data())
        total_pages = (total_data - 1) // self.pending_items_per_page + 1
        
        # Check if there's a next page available
        if self.pending_page + 1 < total_pages:
            self.pending_page += 1
            self.load_pending_table()

    def received_prev_page(self):
        """Navigate to the previous page of received documents"""
        if self.received_page > 0:
            self.received_page -= 1
            self.load_received_table()

    def received_next_page(self):
        """Navigate to the next page of received documents"""
        # Calculate total pages
        total_data = len(self.received_all_data if self.received_search_active else self.get_all_received_data())
        total_pages = (total_data - 1) // self.received_items_per_page + 1
        
        # Check if there's a next page available
        if self.received_page + 1 < total_pages:
            self.received_page += 1
            self.load_received_table()

    def search_pending_documents(self, search_var):
        """Search within pending documents"""
        search_text = search_var.get().lower()
        
        if search_text.strip() == "":
            # If search is empty, clear search mode
            self.pending_search_active = False
            self.pending_page = 0  # Reset to first page
            self.load_pending_table()
            return
            
        # Set search mode active
        self.pending_search_active = True
        
        # Get all data if not already fetched
        if not self.pending_all_data:
            self.pending_all_data = self.get_all_pending_data()
        
        # Filter data based on search text
        filtered_data = []
        for row in self.pending_all_data:
            # Search in sender first name, sender surname, student number, and faculty
            if (search_text in str(row[0]).lower() or  # sender_fname
                search_text in str(row[1]).lower() or  # sender_surname
                search_text in str(row[2]).lower() or  # studnum
                search_text in str(row[3]).lower()):   # sender_fac
                filtered_data.append(row)
        
        # Update filtered data and reset to first page
        self.pending_all_data = filtered_data
        self.pending_page = 0
        self.load_pending_table()

    def search_received_documents(self, search_var):
        """Search within received documents"""
        search_text = search_var.get().lower()
        
        if search_text.strip() == "":
            # If search is empty, clear search mode
            self.received_search_active = False
            self.received_page = 0  # Reset to first page
            self.load_received_table()
            return
            
        # Set search mode active
        self.received_search_active = True
        
        # Get all data if not already fetched
        if not self.received_all_data:
            self.received_all_data = self.get_all_received_data()
        
        # Filter data based on search text
        filtered_data = []
        for row in self.received_all_data:
            # Search in sender first name, sender surname, student number, and faculty
            if (search_text in str(row[0]).lower() or  # sender_fname
                search_text in str(row[1]).lower() or  # sender_surname
                search_text in str(row[2]).lower() or  # studnum
                search_text in str(row[3]).lower()):   # sender_fac
                filtered_data.append(row)
        
        # Update filtered data and reset to first page
        self.received_all_data = filtered_data
        self.received_page = 0
        self.load_received_table()

    def clear_search(self, table_type):
        """Clear search field and reset table view"""
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

    # Add this method to update the status of a document
    def update_document_status(self, studnum, datetime_val, new_status):
        """Update a document's status and refresh all related data"""
        conn = sqlite3.connect(self.resource_path("docusortDB.db"))
        cursor = conn.cursor()
        
        # Update the document status
        cursor.execute("""
            UPDATE documents
            SET doc_type = ?
            WHERE studnum = ? AND datetime = ?
        """, (new_status, studnum, datetime_val))
        
        conn.commit()
        conn.close()
        
        # Refresh both pending and received data caches
        self.pending_all_data = None
        self.received_all_data = None
        
        # Reload the tables
        self.load_pending_table()
        self.load_received_table()

    # Step 1: Add these functions to your AdminApp class

    def show_document_details(self, table_type):
        """Show detailed information for the selected document with dark theme UI design"""
        if table_type == "pending":
            selected_item = self.pending_tree.selection()
            if not selected_item:
                messagebox.showwarning("No Selection", "Please select a document to view details.", parent=self.root)
                return
            student_number = self.pending_tree.item(selected_item[0], 'values')[2]
            doc_type = "Pending"
        else:  # received
            selected_item = self.received_tree.selection()
            if not selected_item:
                messagebox.showwarning("No Selection", "Please select a document to view details.", parent=self.root)
                return
            student_number = self.received_tree.item(selected_item[0], 'values')[2]
            doc_type = "Received"

        # Fetch detailed information from database
        try:
            conn = sqlite3.connect(self.resource_path("docusortDB.db"))
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, sender_fname, sender_surname, studnum, sender_section, sender_fac, 
                    sender_course, sender_email, rcvr_fac, rcvr_name, rcvr_email, 
                    doc_description, datetime, doc_type
                FROM documents
                WHERE studnum = ? AND doc_type = ?
            """, (student_number, doc_type))

            document = cursor.fetchone()
            conn.close()

            if not document:
                messagebox.showerror("Error", "Document not found in database.", parent=self.root)
                return

            # Dark theme color scheme (from second snippet)
            colors = {
                'bg_primary': '#131f24',
                'bg_secondary': '#1a2a30',
                'text_primary': 'white',
                'text_secondary': 'white',
                'accent_green': '#58cc02',
                'button_bg': '#131f24',
                'button_active': '#58cc02'
            }

            # Create popup window with dark theme
            detail_window = tk.Toplevel(self.root)
            detail_window.title("Document Details")
            detail_window.configure(bg=colors['bg_primary'])
            detail_window.geometry("1100x700")
            detail_window.resizable(True, True)
            
            # Center the window
            detail_window.transient(self.root)
            detail_window.wait_visibility()
            detail_window.grab_set()

            # Main container with padding
            main_container = tk.Frame(detail_window, bg=colors['bg_primary'])
            main_container.pack(fill="both", expand=True, padx=24, pady=24)

            # Header section with title and status
            header_frame = tk.Frame(main_container, bg=colors['bg_primary'])
            header_frame.pack(pady=(0, 24))

            # Document title (centered like in second snippet)
            title_label = tk.Label(
                header_frame,
                text=f"Document #{document[0]} - Information Details",
                font=("Courier New", 24, "bold"),
                bg=colors['bg_primary'],
                fg=colors['accent_green']
            )
            title_label.pack()

            # Scrollable content area
            canvas = tk.Canvas(main_container, bg=colors['bg_primary'], highlightthickness=0)
            scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y", padx=(8, 0))

            # Content frame
            content_frame = tk.Frame(canvas, bg=colors['bg_primary'])
            canvas.create_window((0, 0), window=content_frame, anchor="nw")

            # Info frame with dark background
            info_frame = tk.Frame(content_frame, bg=colors['bg_secondary'], padx=20, pady=20)
            info_frame.pack(fill="x", pady=(0, 16), padx=4)

            # Status section
            tk.Label(info_frame, text="DOCUMENT STATUS", font=("Courier New", 18, "bold"),
                    fg=colors['accent_green'], bg=colors['bg_secondary']).grid(row=0, column=0, columnspan=4, sticky=tk.W, pady=(0, 10))

            tk.Label(info_frame, text="Current Status:", font=("Courier New", 14), 
                    fg=colors['text_primary'], bg=colors['bg_secondary']).grid(row=1, column=0, sticky=tk.W, pady=5)
            tk.Label(info_frame, text=document[13], font=("Courier New", 14, "bold"), 
                    fg=colors['text_primary'], bg=colors['bg_secondary']).grid(row=1, column=1, sticky=tk.W, pady=5)

            tk.Label(info_frame, text="Document ID:", font=("Courier New", 14), 
                    fg=colors['text_primary'], bg=colors['bg_secondary']).grid(row=1, column=3, sticky=tk.W, pady=5)
            tk.Label(info_frame, text=str(document[0]), font=("Courier New", 14, "bold"), 
                    fg=colors['text_primary'], bg=colors['bg_secondary']).grid(row=1, column=4, sticky=tk.W, pady=5)

            # Separator
            separator = tk.Frame(info_frame, height=2, bg=colors['accent_green'])
            separator.grid(row=2, column=0, columnspan=5, sticky="ew", pady=15)

            # Sender Information Section
            tk.Label(info_frame, text="SENDER INFORMATION", font=("Courier New", 18, "bold"),
                    fg=colors['accent_green'], bg=colors['bg_secondary']).grid(row=3, column=0, columnspan=4, sticky=tk.W, pady=(10, 10))

            left_col = 0
            spacer_col = 2
            right_col = 3

            # First Name / Last Name
            tk.Label(info_frame, text="First Name:", font=("Courier New", 14), 
                    fg=colors['text_primary'], bg=colors['bg_secondary']).grid(row=4, column=left_col, sticky=tk.W, pady=5)
            tk.Label(info_frame, text=document[1], font=("Courier New", 14, "bold"), 
                    fg=colors['text_primary'], bg=colors['bg_secondary']).grid(row=4, column=left_col+1, sticky=tk.W, pady=5)

            tk.Label(info_frame, text="    ", font=("Courier New", 14), 
                    fg=colors['text_primary'], bg=colors['bg_secondary']).grid(row=4, column=spacer_col, sticky=tk.W, pady=5)

            tk.Label(info_frame, text="Last Name:", font=("Courier New", 14), 
                    fg=colors['text_primary'], bg=colors['bg_secondary']).grid(row=4, column=right_col, sticky=tk.W, pady=5)
            tk.Label(info_frame, text=document[2], font=("Courier New", 14, "bold"), 
                    fg=colors['text_primary'], bg=colors['bg_secondary']).grid(row=4, column=right_col+1, sticky=tk.W, pady=5)

            # Student ID / Section
            tk.Label(info_frame, text="Student ID:", font=("Courier New", 14), 
                    fg=colors['text_primary'], bg=colors['bg_secondary']).grid(row=5, column=left_col, sticky=tk.W, pady=5)
            tk.Label(info_frame, text=document[3], font=("Courier New", 14, "bold"), 
                    fg=colors['text_primary'], bg=colors['bg_secondary']).grid(row=5, column=left_col+1, sticky=tk.W, pady=5)

            tk.Label(info_frame, text="Section:", font=("Courier New", 14), 
                    fg=colors['text_primary'], bg=colors['bg_secondary']).grid(row=5, column=right_col, sticky=tk.W, pady=5)
            tk.Label(info_frame, text=document[4], font=("Courier New", 14, "bold"), 
                    fg=colors['text_primary'], bg=colors['bg_secondary']).grid(row=5, column=right_col+1, sticky=tk.W, pady=5)

            # Faculty / Course
            tk.Label(info_frame, text="Faculty:", font=("Courier New", 14), 
                    fg=colors['text_primary'], bg=colors['bg_secondary']).grid(row=6, column=left_col, sticky=tk.W, pady=5)
            tk.Label(info_frame, text=document[5], font=("Courier New", 14, "bold"), 
                    fg=colors['text_primary'], bg=colors['bg_secondary'], justify="left", wraplength=400).grid(row=6, column=left_col+1, sticky=tk.W, pady=5)

            tk.Label(info_frame, text="Course:", font=("Courier New", 14), 
                    fg=colors['text_primary'], bg=colors['bg_secondary']).grid(row=6, column=right_col, sticky=tk.W, pady=5)
            tk.Label(info_frame, text=document[6], font=("Courier New", 14, "bold"), 
                    fg=colors['text_primary'], bg=colors['bg_secondary'], justify="left", wraplength=400).grid(row=6, column=right_col+1, sticky=tk.W, pady=5)

            # Sender Email
            tk.Label(info_frame, text="Email:", font=("Courier New", 14), 
                    fg=colors['text_primary'], bg=colors['bg_secondary']).grid(row=7, column=left_col, sticky=tk.W, pady=5)
            tk.Label(info_frame, text=document[7], font=("Courier New", 14, "bold"), 
                    fg=colors['text_primary'], bg=colors['bg_secondary']).grid(row=7, column=left_col+1, columnspan=3, sticky=tk.W, pady=5)

            # Separator
            separator2 = tk.Frame(info_frame, height=2, bg=colors['accent_green'])
            separator2.grid(row=8, column=0, columnspan=5, sticky="ew", pady=15)

            # Receiver Information Section
            tk.Label(info_frame, text="RECEIVER INFORMATION", font=("Courier New", 18, "bold"),
                    fg=colors['accent_green'], bg=colors['bg_secondary']).grid(row=9, column=0, columnspan=4, sticky=tk.W, pady=(10, 10))

            # Receiver Name / Faculty
            tk.Label(info_frame, text="Receiver Name:", font=("Courier New", 14), 
                    fg=colors['text_primary'], bg=colors['bg_secondary']).grid(row=10, column=left_col, sticky=tk.W, pady=5)
            tk.Label(info_frame, text=document[9], font=("Courier New", 14, "bold"), 
                    fg=colors['text_primary'], bg=colors['bg_secondary']).grid(row=10, column=left_col+1, sticky=tk.W, pady=5)

            tk.Label(info_frame, text="Faculty:", font=("Courier New", 14), 
                    fg=colors['text_primary'], bg=colors['bg_secondary']).grid(row=10, column=right_col, sticky=tk.W, pady=5)
            tk.Label(info_frame, text=document[8], font=("Courier New", 14, "bold"), 
                    fg=colors['text_primary'], bg=colors['bg_secondary'], justify="left", wraplength=400).grid(row=10, column=right_col+1, sticky=tk.W, pady=5)

            # Receiver Email
            tk.Label(info_frame, text="Email:", font=("Courier New", 14), 
                    fg=colors['text_primary'], bg=colors['bg_secondary']).grid(row=11, column=left_col, sticky=tk.W, pady=5)
            tk.Label(info_frame, text=document[10], font=("Courier New", 14, "bold"), 
                    fg=colors['text_primary'], bg=colors['bg_secondary']).grid(row=11, column=left_col+1, columnspan=3, sticky=tk.W, pady=5)

            # Document Description
            if document[11]:
                tk.Label(info_frame, text="Description:", font=("Courier New", 14), 
                        fg=colors['text_primary'], bg=colors['bg_secondary']).grid(row=12, column=left_col, sticky=tk.NW, pady=5)

                desc_text = tk.Text(info_frame, font=("Courier New", 12), fg=colors['text_primary'], bg=colors['bg_secondary'],
                                    height=3, width=50, wrap="word", relief="flat", bd=0)
                desc_text.grid(row=12, column=left_col+1, columnspan=4, sticky=tk.W, pady=5)
                desc_text.insert("1.0", document[11])
                desc_text.config(state="disabled")

            # Separator
            separator3 = tk.Frame(info_frame, height=2, bg=colors['accent_green'])
            separator3.grid(row=13, column=0, columnspan=5, sticky="ew", pady=15)

            # Timestamp section
            tk.Label(info_frame, text="TIMESTAMP", font=("Courier New", 18, "bold"),
                    fg=colors['accent_green'], bg=colors['bg_secondary']).grid(row=14, column=0, columnspan=4, sticky=tk.W, pady=(10, 10))

            tk.Label(info_frame, text="Date and Time:", font=("Courier New", 14),
                    fg=colors['text_primary'], bg=colors['bg_secondary']).grid(row=15, column=left_col, sticky=tk.W, pady=5)
            tk.Label(info_frame, text=document[12], font=("Courier New", 14, "bold"),
                    fg=colors['text_primary'], bg=colors['bg_secondary']).grid(row=15, column=left_col+1, columnspan=3, sticky=tk.W, pady=5)

            # Button frame
            button_frame = tk.Frame(content_frame, bg=colors['bg_primary'])
            button_frame.pack(pady=30)

            # Close button
            close_btn = tk.Button(
                button_frame,
                text="Close",
                font=("Courier New", 18),
                fg=colors['text_primary'],
                bg=colors['button_bg'],
                relief="flat",
                activebackground=colors['button_bg'],
                activeforeground=colors['text_primary'],
                cursor="hand2",
                command=detail_window.destroy
            )
            close_btn.pack(side=tk.LEFT, padx=30)

            # Mark as Received button (only for pending documents)
            if doc_type == "Pending":
                receive_btn = tk.Button(
                    button_frame,
                    text="✓ Mark as Received",
                    font=("Courier New", 18),
                    fg=colors['bg_primary'],
                    bg=colors['accent_green'],
                    relief="flat",
                    activebackground=colors['accent_green'],
                    activeforeground=colors['bg_primary'],
                    cursor="hand2",
                    command=lambda: self.mark_as_received(document[0], detail_window)
                )
                receive_btn.pack(side=tk.LEFT, padx=30)

            # Configure scrolling
            def configure_scroll_region(event=None):
                canvas.configure(scrollregion=canvas.bbox("all"))
                
            content_frame.bind('<Configure>', configure_scroll_region)
            
            # Mouse wheel scrolling
            def on_mousewheel(event):
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            
            canvas.bind("<MouseWheel>", on_mousewheel)
            detail_window.bind("<MouseWheel>", on_mousewheel)

            # Initial scroll region configuration
            detail_window.after(100, configure_scroll_region)

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to load document details:\n{str(e)}", parent=self.root)

    def mark_as_received(self, doc_id, window):
        """Mark a pending document as received"""
        try:
            conn = sqlite3.connect(self.resource_path("docusortDB.db"))
            cursor = conn.cursor()
            
            # Update document status
            cursor.execute("""
                UPDATE documents 
                SET doc_type = 'Received'
                WHERE id = ?
            """, (doc_id,))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Document has been marked as received.", parent=window)
            window.destroy()
            
            # Refresh both tables
            self.pending_page = 0  # Reset to first page
            self.received_page = 0  # Reset to first page
            self.load_pending_table()
            self.load_received_table()
            
            # Update dashboard counts
            conn = sqlite3.connect(self.resource_path("docusortDB.db"))
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM documents WHERE doc_type = 'Pending'")
            pending_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM documents WHERE doc_type = 'Received'")
            received_count = cursor.fetchone()[0]
            
            conn.close()
            
            # Update the count labels
            self.pending_count_label.config(text=str(pending_count))
            self.received_count_label.config(text=str(received_count))
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to update document: {e}", parent=window)

        # Step 2: Add double-click bindings to the tables in the show_dashboard method
        # Add these lines after creating the pending_tree and received_tree



        # Step 3: Add context menu for right-click functionality (optional enhancement)
    def create_table_context_menu(self):
        """Create right-click context menus for tables"""
        # Pending table context menu
        self.pending_context_menu = tk.Menu(self.root, tearoff=0, bg=self.secondary_bg, fg=self.text_light)
        self.pending_context_menu.add_command(label="View Details", 
                                            command=lambda: self.show_document_details("pending"))
        self.pending_context_menu.add_command(label="Mark as Received", 
                                            command=self.mark_selected_as_received)
        
        # Received table context menu
        self.received_context_menu = tk.Menu(self.root, tearoff=0, bg=self.secondary_bg, fg=self.text_light)
        self.received_context_menu.add_command(label="View Details", 
                                            command=lambda: self.show_document_details("received"))
        
        # Bind right-click events
        self.pending_tree.bind("<Button-3>", self.show_pending_context_menu)
        self.received_tree.bind("<Button-3>", self.show_received_context_menu)

    def show_pending_context_menu(self, event):
        """Show context menu on right-click for pending table"""
        # Select the row under cursor
        iid = self.pending_tree.identify_row(event.y)
        if iid:
            self.pending_tree.selection_set(iid)
            self.pending_context_menu.tk_popup(event.x_root, event.y_root)
        
    def show_received_context_menu(self, event):
        """Show context menu on right-click for received table"""
        # Select the row under cursor
        iid = self.received_tree.identify_row(event.y)
        if iid:
            self.received_tree.selection_set(iid)
            self.received_context_menu.tk_popup(event.x_root, event.y_root)

    def mark_selected_as_received(self):
        """Mark the selected pending document as received from context menu"""
        selected_item = self.pending_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a document to mark as received.", parent=self.root)
            return
        
        student_number = self.pending_tree.item(selected_item[0], 'values')[2]
        
        try:
            conn = sqlite3.connect(self.resource_path("docusortDB.db"))
            cursor = conn.cursor()
            
            # Get the document ID based on student number
            cursor.execute("SELECT id FROM documents WHERE studnum = ? AND doc_type = 'Pending'", (student_number,))
            doc_id = cursor.fetchone()
            
            if doc_id:
                # Call existing method to mark as received
                conn.close()
                self.mark_as_received(doc_id[0], self.root)
            else:
                conn.close()
                messagebox.showerror("Error", "Document not found in database.", parent=self.root)
        
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to process document: {e}", parent=self.root)

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

        # Create admin users table with additional columns for Full Name and Email
        columns = ("id", "fullname", "admin_email", "username", "role", "date_created", "last_login")
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
            conn = sqlite3.connect(self.resource_path("docusortDB.db"))
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
                        fullname TEXT UNIQUE NOT NULL,
                        admin_email TEXT UNIQUE NOT NULL,
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
                    INSERT INTO admin_users (fullname, admin_email, username, password, role, date_created)
                    VALUES (?, ?, ?, ?, ?, datetime('now'))
                """, ("Administrator", "admin@example.com", "admin", "admin123", "Super Admin"))
                conn.commit()

            # Get admin users (include fullname and admin_email)
            cursor.execute("""
                SELECT id, fullname, admin_email, username, role, date_created, last_login
                FROM admin_users
                ORDER BY id
            """)

            admin_users = cursor.fetchall()
            conn.close()

            # Insert into Treeview
            for user in admin_users:
                self.admin_tree.insert("", "end", values=user)

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to load admin users: {e}")

            

    def delete_admin_user(self):
        from tkinter.simpledialog import askstring
        selected_item = self.admin_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an admin user to delete.", parent=self.root)
            return

        user_id = self.admin_tree.item(selected_item[0], 'values')[0]
        username = self.admin_tree.item(selected_item[0], 'values')[1]
    

        # Prompt for password
        password_input = askstring("Password Required", "Enter your password to confirm deletion:", show="*", parent=self.root)
        if not password_input:
            messagebox.showwarning("Cancelled", "Deletion cancelled.", parent=self.root)
            return

        try:
            # Check password of the currently logged-in user
            conn = sqlite3.connect(self.resource_path("docusortDB.db"))
            cursor = conn.cursor()

            cursor.execute("SELECT password FROM admin_users WHERE username = ?", (self.current_user_username,))
            result = cursor.fetchone()

            if result is None:
                messagebox.showerror("Error", "Your account was not found.", parent=self.root)
                conn.close()
                return

            correct_password = result[0]
            if password_input != correct_password:
                messagebox.showerror("Authentication Failed", "Incorrect password. Deletion cancelled.", parent=self.root)
                conn.close()
                return

            # Confirm deletion
            confirm = messagebox.askyesno("Confirm Delete", 
                                        f"Are you sure you want to delete admin user '{username}'?", 
                                        parent=self.root)
            if not confirm:
                conn.close()
                return

            # Delete user
            cursor.execute("DELETE FROM admin_users WHERE id = ?", (user_id,))
            conn.commit()
            conn.close()

            # Refresh list
            self.load_admin_users()
            messagebox.showinfo("Success", f"Admin user '{username}' has been deleted.", parent=self.root)

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to delete admin user: {e}", parent=self.root)
            
    def show_add_admin_form(self):
        # Create a new top-level window for the form
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Admin User")
        add_window.configure(bg=self.bg_dark)
        add_window.geometry("400x575")
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

        # First and Last Name
        tk.Label(
            form_frame,
            text="Full Name:",
            font=("Courier New", 12),
            bg=self.bg_dark,
            fg=self.text_light,
            anchor="w"
        ).pack(fill="x", pady=(10, 0))
        
        fullname_var = tk.StringVar()
        fullname_entry = tk.Entry(
            form_frame,
            font=("Courier New", 12),
            bg=self.secondary_bg,
            fg=self.text_light,
            insertbackground=self.text_light,
            textvariable=fullname_var
        )
        fullname_entry.pack(fill="x", pady=(0, 10))
        fullname_entry.focus_set()
        
        # Email
        tk.Label(
            form_frame,
            text="Email:",
            font=("Courier New", 12),
            bg=self.bg_dark,
            fg=self.text_light,
            anchor="w"
        ).pack(fill="x", pady=(10, 0))
                
        
        admin_email_var = tk.StringVar()
        admin_email_entry = tk.Entry(
            form_frame,
            font=("Courier New", 12),
            bg=self.secondary_bg,
            fg=self.text_light,
            insertbackground=self.text_light,
            textvariable=admin_email_var
        )
        admin_email_entry.pack(fill="x", pady=(0, 10))
        
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
                fullname_var.get(),
                admin_email_var.get(),
                username_var.get(),
                password_var.get(),
                confirm_var.get(),
                role_var.get(),
                add_window
            )
        )
        register_btn.pack(side="left", padx=10)
        

        

        
    def register_admin(self, fullname, admin_email, username, password, confirm, role, window):
        # Validate inputs
        if not fullname or not admin_email or not username or not password or not confirm:
            messagebox.showerror("Error", "All fields must be filled", parent=window)
            return

        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match", parent=window)
            return

        if len(password) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters", parent=window)
            return

        try:
            conn = sqlite3.connect(self.resource_path("docusortDB.db"))
            cursor = conn.cursor()

            # Check if FULL NAME already exists
            cursor.execute("SELECT id FROM admin_users WHERE fullname = ?", (fullname,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Full Name already exists", parent=window)
                conn.close()
                return

            # Check if USERNAME already exists
            cursor.execute("SELECT id FROM admin_users WHERE username = ?", (username,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Username already exists", parent=window)
                conn.close()
                return

            # Insert new admin user
            cursor.execute("""
                INSERT INTO admin_users (fullname, admin_email, username, password, role, date_created)
                VALUES (?, ?, ?, ?, ?, datetime('now'))
            """, (fullname, admin_email, username, password, role))

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

            from DocuSort import DocuSortApp
            login_window = tk.Toplevel(self.login_root)
            app_instance = DocuSortApp(login_window)
            app_instance.go_back_to_landing_page()
        else:
            print("Logout canceled. Returning to Admin Dashboard.")
            messagebox.showinfo("Logout Cancelled", "Returning to Admin Dashboard")
            self.switch_page(self.show_dashboard, "Dashboard")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x600")
    app = AdminApp(root)
    root.mainloop()