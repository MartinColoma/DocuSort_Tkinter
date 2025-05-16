import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
from datetime import datetime
import sys
import smtplib



# Create the main application window
class DocuSortApp:
    def only_numbers_and_dash(self, input_text):
    # allow digits and dash, and allow empty input
        return all(c.isdigit() or c == '-' for c in input_text) or input_text == ""

    def only_letters(self, input_text):
        return input_text.isalpha() or input_text == ""
    
    def __init__(self, root):
        self.root = root
        self.root.title("DocuSort")
        self.root.resizable(False, False)
        self.root.configure(bg="#131f24")
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}+0+0")

        # Initialize database first!
        self.initialize_database()

        # Initialize data fields
        self.first_name = ""
        self.last_name = ""
        self.student_id = ""
        self.section = ""
        self.faculty = ""
        self.course = ""
        
        # Initialize receiver fields
        self.receiver_first_name = ""
        self.receiver_last_name = ""
        self.receiver_faculty = ""

        # Landing page
        self.landing_page()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.root.destroy()
            sys.exit()  # Ensures the process is completely terminated

    def initialize_database(self):
        conn = sqlite3.connect('docusortDB.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender_fname TEXT NOT NULL,
                sender_surname TEXT NOT NULL,
                studnum TEXT NOT NULL,
                sender_section TEXT NOT NULL,
                sender_fac TEXT NOT NULL,
                sender_course TEXT NOT NULL,
                sender_email TEXT NOT NULL,
                rcvr_fname TEXT NOT NULL,
                rcvr_surname TEXT NOT NULL,
                rcvr_fac TEXT NOT NULL,
                datetime TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
        
    def landing_page(self):
        # Clear previous widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, bg="#131f24")
        frame.pack(fill=tk.BOTH, expand=True)

        # Frame for logo and image
        logo_frame = tk.Frame(frame, bg="#131f24")
        logo_frame.pack(pady=(180, 18))  # Adjust padding as you like
        self.cleartxt_form()

        # Load the top image (this will be placed above the DOCUSORT text)
        try:
            top_image = Image.open("resources/HomeHeader.png")  # Replace with your image path
            top_image = top_image.resize((300, 150))  # Resize as needed
            self.top_photo = ImageTk.PhotoImage(top_image)

            # Place the top image above the text
            top_img_label = tk.Label(logo_frame, image=self.top_photo, bg="#131f24")
            top_img_label.pack(pady=(0, 10))  # Adjust the padding to position it correctly
        except Exception as e:
            print(f"Error loading top image: {e}")
            # Optional: Show a default text label if image loading fails
            fallback_label = tk.Label(logo_frame, text="TOP IMAGE NOT FOUND", font=("Courier New", 18), fg="red", bg="#131f24")
            fallback_label.pack(pady=(0, 10))

        # Load the main image (next to the DOCUSORT text)
        try:
            image = Image.open("resources/docusort_test.png")  # Replace with your image path
            image = image.resize((150, 150))  # Resize if needed
            self.photo = ImageTk.PhotoImage(image)

            # Place the image on the left
            img_label = tk.Label(logo_frame, image=self.photo, bg="#131f24")
            img_label.pack(side=tk.LEFT, padx=18)
        except Exception as e:
            print(f"Error loading image: {e}")
            # Optional: Show a default text label if image loading fails
            fallback_label = tk.Label(logo_frame, text="IMAGE NOT FOUND", font=("Courier New", 18), fg="red", bg="#131f24")
            fallback_label.pack(side=tk.LEFT, padx=18)

        # Text Logo beside the picture
        text_frame = tk.Frame(logo_frame, bg="#131f24")
        text_frame.pack(side=tk.LEFT)

        header_label = tk.Label(text_frame, text="Docu", font=("Courier New", 100, "bold"), fg="white", bg="#131f24")
        header_label.pack(side=tk.LEFT)

        sort_label = tk.Label(text_frame, text="Sort", font=("Courier New", 100, "bold"), fg="#58cc02", bg="#131f24")
        sort_label.pack(side=tk.LEFT)

        # Start Button below
        start_button = tk.Button(frame, text="Let's get sorting", font=("Courier New", 18), command=self.sender_info_page, bg="#58cc02", fg="#131f24", cursor="hand2", relief="flat")
        start_button.pack(pady=30)


        admin_button = tk.Button(
            frame,
            text="Admin Login",
            font=("Courier New", 18),
            command=self.admin_login_page,
            bg="#131f24",
            fg="#58cc02",
            activebackground="#131f24",
            activeforeground="#58cc02",
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            cursor="hand2"
        )

        # Place it in the bottom-right corner with a margin
        admin_button.place(relx=1.0, rely=1.0, anchor="se", x=-30, y=-50)


    def admin_login_page(self):
        # Clear any previous widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        self.cleartxt_form()

        # Create a frame for the login form
        form_frame = tk.Frame(self.root, bg="#131f24")
        form_frame.pack(pady=(150, 18))

        # Header
        tk.Label(form_frame, text="Admin Login", font=("Courier New", 40, "bold"),
                fg="#58cc02", bg="#131f24").grid(row=0, column=0, columnspan=2, pady=30)

        # Username
        tk.Label(form_frame, text="Username:", font=("Courier New", 18),
                fg="white", bg="#131f24").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.username_entry = tk.Entry(form_frame, font=("Courier New", 18),
                                    fg="white", bg="#131f24", width=30)
        self.username_entry.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        # Password
        tk.Label(form_frame, text="Password:", font=("Courier New", 18),
                fg="white", bg="#131f24").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        self.password_entry = tk.Entry(form_frame, font=("Courier New", 18),
                                    fg="white", bg="#131f24", show="*", width=30)
        self.password_entry.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        cancel_button = tk.Button(
            form_frame,
            text="Cancel",
            font=("Courier New", 18),
            command=self.go_back_to_landing_page,
            fg="white",  # Text color is white
            bg=form_frame.cget("bg"),  # Same as the background of the frame
            relief="flat",  # Flat button with no border
            cursor="hand2"
        )
        cancel_button.grid(row=5, column=0, pady=(40, 0), sticky=tk.E, padx=(0,125))

        # Next Button (Custom background color #58cc02, white text)
        admin_loginbtn = tk.Button(
            form_frame,
            text="Login",
            font=("Courier New", 18),
            command=self.validate_login,
            fg="#131f24",  # Text color is white
            bg="#58cc02",  # Custom background color
            relief="flat",  # Flat button with no border
            activebackground="#58cc02",  # Same color when clicked
            activeforeground="white"  # Text color when clicked
        )
        admin_loginbtn.grid(row=5, column=1, pady=(40, 0), sticky=tk.W, padx=(110, 0))

    def validate_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # First check if fields are empty
        if not username or not password:
            messagebox.showerror("Login Failed", "Username and password cannot be empty")
            return  # Exit the function early    
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
                # If the table doesn't exist yet, create it with a default admin user
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
                
                # Insert default admin
                cursor.execute("""
                    INSERT INTO admin_users (username, password, role, date_created)
                    VALUES (?, ?, ?, datetime('now'))
                """, ("admin", "admin123", "Super Admin"))
                conn.commit()
            
            # Check user credentials against the database
            cursor.execute("""
                SELECT id, username, role FROM admin_users 
                WHERE username = ? AND password = ?
            """, (username, password))
            
            user = cursor.fetchone()
                
            if username == "admin" and password == "admin123":
                messagebox.showinfo("Login Successful", "Welcome Admin!")
                self.root.withdraw()
                from admin import AdminApp
                admin_window = tk.Toplevel(self.root)
                AdminApp(admin_window)            
            elif user:
                # Update last login time
                cursor.execute("""
                    UPDATE admin_users 
                    SET last_login = datetime('now') 
                    WHERE id = ?
                """, (user[0],))
                conn.commit()
                
                # Close the database connection
                conn.close()
                
                # Show success message with user role
                messagebox.showinfo("Login Successful", f"Welcome {user[1]}! ({user[2]})")
                
                # Hide the login window
                self.root.withdraw()
                
                # Import here to avoid circular imports
                from admin import AdminApp
                
                admin_window = tk.Toplevel(self.root)
                AdminApp(admin_window)
            else:
                conn.close()
                messagebox.showerror("Login Failed", "Incorrect Username or Password")
                
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to validate login: {e}")
            if conn:
                conn.close()

    def sender_info_page(self):
        # Clear any previous widgets (if any)
        for widget in self.root.winfo_children():
            widget.destroy()
    
        # Create a frame to hold the form fields and buttons
        form_frame = tk.Frame(self.root, bg="#131f24")
        form_frame.pack(pady=(120, 18))  # Adjust top and bottom padding for form_frame

        # Sender Information Header (should occupy all columns, centered)
        tk.Label(form_frame, text="Sender Information", font=("Courier New", 40, "bold"), fg="#58cc02", bg="#131f24").grid(row=0, column=0, columnspan=4, pady=30)

        # First Name and Last Name (in the same row)
        vcmd = (self.root.register(self.only_letters), '%P')
        tk.Label(form_frame, text="First Name:", font=("Courier New", 18), fg="white", bg="#131f24").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.first_name_entry = tk.Entry(form_frame, font=("Courier New", 18), fg="white", bg="#131f24", width=18, validate="key", validatecommand=vcmd)
        self.first_name_entry.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        self.first_name_entry.insert(0, self.first_name)
        self.first_name_entry.focus_set()
        
        tk.Label(form_frame, text="Last Name:", font=("Courier New", 18), fg="white", bg="#131f24").grid(row=1, column=2, padx=10, pady=5, sticky=tk.W)
        self.last_name_entry = tk.Entry(form_frame, font=("Courier New", 18), fg="white", bg="#131f24", width=18, validate="key", validatecommand=vcmd)
        self.last_name_entry.grid(row=2, column=2, padx=10, pady=5, sticky=tk.W)
        self.last_name_entry.insert(0, self.last_name)

        # Student ID and Section (in the next row)
        vcmd_student_no = (self.root.register(self.only_numbers_and_dash), '%P')
        tk.Label(form_frame, text="Student ID #:", font=("Courier New", 18), fg="white", bg="#131f24").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        self.student_id_entry = tk.Entry(form_frame, font=("Courier New", 18), fg="white", bg="#131f24", width=18,
                                        validate="key", validatecommand=vcmd_student_no)
        self.student_id_entry.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
        self.student_id_entry.insert(0, self.student_id)

        tk.Label(form_frame, text="Section:", font=("Courier New", 18), fg="white", bg="#131f24").grid(row=3, column=2, padx=10, pady=5, sticky=tk.W)
        self.section_entry = tk.Entry(form_frame, font=("Courier New", 18), fg="white", bg="#131f24", width=18)
        self.section_entry.grid(row=4, column=2, padx=10, pady=5, sticky=tk.W)
        self.section_entry.insert(0, self.section)

        # Faculty and Course (in the next row)
# Faculty and Course (in the next row)
        tk.Label(form_frame, text="Faculty:", font=("Courier New", 18), fg="white", bg="#131f24").grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)

        faculty_options = [
            "Select Student's Faculty",  # <-- Placeholder
            "College of Engineering", 
            "College of Business, Entrepreneurial and Accountancy",
            "Institute of Computer Studies",
            "Institute of Architecture",
            "College of Education",
            "College of Arts and Sciences",
            "Institute of Human Kinetics"
        ]

        self.faculty_combobox = ttk.Combobox(
            form_frame,
            font=("Courier New", 18),
            width=39,
            state="readonly",
            values=faculty_options
        )
        self.faculty_combobox.grid(row=6, column=0, columnspan=4, padx=10, pady=5, sticky=tk.W)

        # Set placeholder or a previously saved value
        if hasattr(self, "faculty") and self.faculty in faculty_options:
            self.faculty_combobox.set(self.faculty)
        else:
            self.faculty_combobox.set(faculty_options[0])  # Set placeholder

        tk.Label(form_frame, text="Course:", font=("Courier New", 18), fg="white", bg="#131f24").grid(row=7, column=0, padx=10, pady=5, sticky=tk.W)

        self.course_combobox = ttk.Combobox(
            form_frame,
            font=("Courier New", 18),
            width=39,
            state="disabled"
        )
        self.course_combobox.grid(row=8, column=0, columnspan=4, padx=10, pady=5, sticky=tk.W)

        # Set course placeholder or value if available
        if hasattr(self, "course") and self.course:
            self.course_combobox.set(self.course)
        else:
            self.course_combobox.set("Select Student's Course")  # Optional placeholder


        tk.Label(form_frame, text="Course:", font=("Courier New", 18), fg="white", bg="#131f24").grid(row=7, column=0, padx=10, pady=5, sticky=tk.W)
        self.course_combobox = ttk.Combobox(form_frame, font=("Courier New", 18), width=39, state="readonly")
        self.course_combobox.grid(row=8, column=0, columnspan=4, padx=10, pady=5, sticky=tk.W)
        self.course_combobox.set(self.course)
        

        # Cancel Button (Transparent background, white text)
        cancel_button = tk.Button(
            form_frame,
            text="Cancel",
            font=("Courier New", 18),
            command=self.go_back_to_landing_page,
            fg="white",  # Text color is white
            bg=form_frame.cget("bg"),  # Same as the background of the frame
            relief="flat",  # Flat button with no border
            activebackground=form_frame.cget("bg"),  # Same color when clicked
            activeforeground="white"  # Text color when clicked
        )
        cancel_button.grid(row=9, column=0, columnspan=2, pady=(40, 0), sticky=tk.E, padx=(0, 200))

        # Next Button (Custom background color #58cc02, white text)
        next_button = tk.Button(
            form_frame,
            text="Next",
            font=("Courier New", 18),
            command=self.save_sender_info,
            fg="white",  # Text color is white
            bg="#58cc02",  # Custom background color
            relief="flat",  # Flat button with no border
            activebackground="#58cc02",  # Same color when clicked
            activeforeground="white"  # Text color when clicked
        )
        next_button.grid(row=9, column=2, columnspan=2, pady=(40, 0), sticky=tk.W, padx=(200, 0))

        # Bind faculty selection to update courses
        self.faculty_combobox.bind("<<ComboboxSelected>>", self.update_courses)  
        self.student_id_entry.bind('<KeyRelease>', self.format_student_id)


    def go_back_to_landing_page(self):
        # Clears all widgets on the current page and returns to the landing page
        self.landing_page()

    def format_student_id(self, event):
        entry = self.student_id_entry
        current_text = entry.get().replace("-", "")  # Remove existing dash if any
        if len(current_text) > 4:
            formatted = current_text[:4] + '-' + current_text[4:10]
        else:
            formatted = current_text
        entry.delete(0, tk.END)
        entry.insert(0, formatted)
        entry.icursor(tk.END)  # Keep cursor at the end

    def update_courses(self, event=None):
        faculty = self.faculty_combobox.get()
        course_list = []

        # Mapping of faculty to respective courses
        faculty_degrees = {
            "College of Engineering": [
                "B.S. in Mechanical Engineering", "B.S. in Civil Engineering", "B.S. in Electrical Engineering",
                "B.S. in Electronics Engineering", "B.S. in Computer Engineering", "B.S. in Industrial Engineering",
                "B.S. in Instrumentation and Control Engineering", "B.S. in Mechatronics"
            ],
            "Institute of Computer Studies": ["B.S. in Information Technology"],
            "Institute of Architecture": ["B.S. in Architecture"],
            "College of Business, Entrepreneurial and Accountancy": [
                "B.S. in Accountancy", "B.S. in Business Administration", "B.S. in Entrepreneurship",
                "B.S. in Hospitality Management"
            ],
            "College of Education": [
                "B.S. in Secondary Education", "B.S. in Elementary Education", "B.S. in Early Childhood Education",
                "B.S. in Physical Education"
            ],
            "College of Arts and Sciences": [
                "A.B. in Political Science", "A.B. in Communication", "B.S. in Psychology", "B.S. in Biology", "B.S. in Mathematics"
            ],
            "Institute of Human Kinetics": ["B.S. in Exercise and Sports Sciences", "B.S. in Physical Education"]
        }

        # Clear the previous course options and add new ones
        self.course_combobox.set('')
        course_list = faculty_degrees.get(faculty, [])
        self.course_combobox['values'] = course_list

    def save_sender_info(self):
        # Store the entered information in the class variables
        self.first_name = self.first_name_entry.get()
        self.last_name = self.last_name_entry.get()
        self.student_id = self.student_id_entry.get()
        self.section = self.section_entry.get()
        self.faculty = self.faculty_combobox.get()
        self.course = self.course_combobox.get()
        
        # Check if any field is empty
        if not all([self.first_name, self.last_name, self.student_id, self.section, self.faculty, self.course]):
            messagebox.showerror("Missing Information", "Please fill in all the fields before proceeding.")
            return  # Stop the function if any field is empty
        if self.faculty_combobox.get() == "Select Student's Faculty":
            messagebox.showerror("Input Error", "Please select a valid faculty.")

        # Proceed to next page if all fields are filled
        self.receiver_info_page()

    def receiver_info_page(self):
        # Clear any previous widgets (if any)
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create a frame to hold the form fields and buttons
        form_frame = tk.Frame(self.root, bg="#131f24")
        form_frame.pack(pady=(175, 18))  # Adjust top and bottom padding for form_frame

        # Receiver Information Header (should occupy all columns, centered)
        tk.Label(form_frame, text="Receiver Information", font=("Courier New", 32, "bold"), fg="#58cc02", bg="#131f24").grid(row=0, column=0, columnspan=4, pady=50)

        # First Name and Last Name (in the same row)
        vcmd = (self.root.register(self.only_letters), '%P')
        tk.Label(form_frame, text="First Name:", font=("Courier New", 18), fg="white", bg="#131f24").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.receiver_first_name_entry = tk.Entry(form_frame, font=("Courier New", 18), fg="white", bg="#131f24", width=18, validate="key", validatecommand=vcmd)
        self.receiver_first_name_entry.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        self.receiver_first_name_entry.insert(0, self.receiver_first_name)
        self.receiver_first_name_entry.focus_set()
        
        tk.Label(form_frame, text="Last Name:", font=("Courier New", 18), fg="white", bg="#131f24").grid(row=1, column=2, padx=10, pady=5, sticky=tk.W)
        self.receiver_last_name_entry = tk.Entry(form_frame, font=("Courier New", 18), fg="white", bg="#131f24", width=18, validate="key", validatecommand=vcmd)
        self.receiver_last_name_entry.grid(row=2, column=2, padx=10, pady=5, sticky=tk.W)
        self.receiver_last_name_entry.insert(0, self.receiver_last_name)

        # Faculty (in the same row)
        tk.Label(form_frame, text="Faculty:", font=("Courier New", 18), fg="white", bg="#131f24").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        self.receiver_faculty_combobox = ttk.Combobox(form_frame, font=("Courier New", 18), width=38, state="readonly", values=[ 
            "College of Engineering", 
            "College of Business, Entrepreneurial and Accountancy"
        ])
        self.receiver_faculty_combobox.grid(row=4, column=0, columnspan=4, padx=10, pady=5, sticky=tk.W)
        self.receiver_faculty_combobox.set(self.receiver_faculty)


        # Buttons (Back and Next)
        back_button = tk.Button(
            form_frame,
            text="Back",
            font=("Courier New", 18),
            command=self.sender_info_page,
            fg="white",  # Text color is white
            bg=form_frame.cget("bg"),  # Same as the background of the frame
            relief="flat",  # Flat button with no border
            activebackground=form_frame.cget("bg"),  # Same color when clicked
            activeforeground="white"  # Text color when clicked
        )
        back_button.grid(row=5, column=0, columnspan=2, pady=(40, 0), sticky=tk.E, padx=(0, 200))

        # Changed from Submit to Next
        next_button = tk.Button(
            form_frame,
            text="Next",
            font=("Courier New", 18),
            command=self.save_receiver_info,
            fg="white",  # Text color is white
            bg="#58cc02",  # Custom background color
            relief="flat",  # Flat button with no border
            activebackground="#58cc02",  # Same color when clicked
            activeforeground="white"  # Text color when clicked
        )
        next_button.grid(row=5, column=2, columnspan=2, pady=(40, 0), sticky=tk.W, padx=(200, 0))

    def save_receiver_info(self):
        # Store the receiver information in the class variables
        self.receiver_first_name = self.receiver_first_name_entry.get()
        self.receiver_last_name = self.receiver_last_name_entry.get()
        self.receiver_faculty = self.receiver_faculty_combobox.get()
        
        # Check if any field is empty
        if not all([self.receiver_first_name, self.receiver_last_name, self.receiver_faculty]):
            messagebox.showerror("Missing Information", "Please fill in all the fields before proceeding.")
            return  # Stop the function if any field is empty

        # Proceed to preview page
        self.preview_page()

    def preview_page(self):
        # Clear any previous widgets
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Create a frame to hold the preview information
        preview_frame = tk.Frame(self.root, bg="#131f24")
        preview_frame.pack(pady=(100, 18))
        
        # Preview Header
        tk.Label(preview_frame, text="Document Information Preview", font=("Courier New", 32, "bold"), 
                fg="#58cc02", bg="#131f24").grid(row=0, column=0, columnspan=2, pady=30)
        
        # Create a frame for the information with a slightly different background for better visibility
        info_frame = tk.Frame(preview_frame, bg="#1a2a30", padx=20, pady=20)
        info_frame.grid(row=1, column=0, columnspan=2)
        
        # Sender Information Section
        tk.Label(info_frame, text="SENDER INFORMATION", font=("Courier New", 18, "bold"), 
                fg="#58cc02", bg="#1a2a30").grid(row=0, column=0, columnspan=4, sticky=tk.W, pady=(0, 10))
        
        # Create two columns for better organization
        left_col = 0
        right_col = 2
        
        # Sender details - left column
        tk.Label(info_frame, text="First Name:", font=("Courier New", 14), 
                fg="white", bg="#1a2a30").grid(row=1, column=left_col, sticky=tk.W, pady=5)
        tk.Label(info_frame, text=self.first_name, font=("Courier New", 14, "bold"), 
                fg="white", bg="#1a2a30").grid(row=1, column=left_col+1, sticky=tk.W, pady=5)
        
        tk.Label(info_frame, text="Last Name:", font=("Courier New", 14), 
                fg="white", bg="#1a2a30").grid(row=2, column=left_col, sticky=tk.W, pady=5)
        tk.Label(info_frame, text=self.last_name, font=("Courier New", 14, "bold"), 
                fg="white", bg="#1a2a30").grid(row=2, column=left_col+1, sticky=tk.W, pady=5)
        
        tk.Label(info_frame, text="Student ID:", font=("Courier New", 14), 
                fg="white", bg="#1a2a30").grid(row=3, column=left_col, sticky=tk.W, pady=5)
        tk.Label(info_frame, text=self.student_id, font=("Courier New", 14, "bold"), 
                fg="white", bg="#1a2a30").grid(row=3, column=left_col+1, sticky=tk.W, pady=5)
        
        # Sender details - right column
        tk.Label(info_frame, text="Section:", font=("Courier New", 14), 
                fg="white", bg="#1a2a30").grid(row=1, column=right_col, sticky=tk.W, pady=5, padx=(20, 0))
        tk.Label(info_frame, text=self.section, font=("Courier New", 14, "bold"), 
                fg="white", bg="#1a2a30").grid(row=1, column=right_col+1, sticky=tk.W, pady=5)
        
        tk.Label(info_frame, text="Faculty:", font=("Courier New", 14), 
                fg="white", bg="#1a2a30").grid(row=2, column=right_col, sticky=tk.W, pady=5, padx=(20, 0))
        tk.Label(info_frame, text=self.faculty, font=("Courier New", 14, "bold"), 
                fg="white", bg="#1a2a30").grid(row=2, column=right_col+1, sticky=tk.W, pady=5)
        
        tk.Label(info_frame, text="Course:", font=("Courier New", 14), 
                fg="white", bg="#1a2a30").grid(row=3, column=right_col, sticky=tk.W, pady=5, padx=(20, 0))
        tk.Label(info_frame, text=self.course, font=("Courier New", 14, "bold"), 
                fg="white", bg="#1a2a30").grid(row=3, column=right_col+1, sticky=tk.W, pady=5)
        
        # Separator (a horizontal line)
        separator = tk.Frame(info_frame, height=2, bg="#58cc02")
        separator.grid(row=4, column=0, columnspan=4, sticky="ew", pady=15)
        
        # Receiver Information Section
        tk.Label(info_frame, text="RECEIVER INFORMATION", font=("Courier New", 18, "bold"), 
                fg="#58cc02", bg="#1a2a30").grid(row=5, column=0, columnspan=4, sticky=tk.W, pady=(10, 10))
        
        # Receiver details
        tk.Label(info_frame, text="First Name:", font=("Courier New", 14), 
                fg="white", bg="#1a2a30").grid(row=6, column=left_col, sticky=tk.W, pady=5)
        tk.Label(info_frame, text=self.receiver_first_name, font=("Courier New", 14, "bold"), 
                fg="white", bg="#1a2a30").grid(row=6, column=left_col+1, sticky=tk.W, pady=5)
        
        tk.Label(info_frame, text="Last Name:", font=("Courier New", 14), 
                fg="white", bg="#1a2a30").grid(row=7, column=left_col, sticky=tk.W, pady=5)
        tk.Label(info_frame, text=self.receiver_last_name, font=("Courier New", 14, "bold"), 
                fg="white", bg="#1a2a30").grid(row=7, column=left_col+1, sticky=tk.W, pady=5)
        
        tk.Label(info_frame, text="Faculty:", font=("Courier New", 14), 
                fg="white", bg="#1a2a30").grid(row=6, column=right_col, sticky=tk.W, pady=5, padx=(20, 0))
        tk.Label(info_frame, text=self.receiver_faculty, font=("Courier New", 14, "bold"), 
                fg="white", bg="#1a2a30").grid(row=6, column=right_col+1, sticky=tk.W, pady=5)
        
        # Timestamp information
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Separator (a horizontal line)
        separator2 = tk.Frame(info_frame, height=2, bg="#58cc02")
        separator2.grid(row=8, column=0, columnspan=4, sticky="ew", pady=15)
        
        # Timestamp section
        tk.Label(info_frame, text="TIMESTAMP", font=("Courier New", 18, "bold"), 
                fg="#58cc02", bg="#1a2a30").grid(row=9, column=0, columnspan=4, sticky=tk.W, pady=(10, 10))
                
        tk.Label(info_frame, text="Date and Time:", font=("Courier New", 14), 
                fg="white", bg="#1a2a30").grid(row=10, column=left_col, sticky=tk.W, pady=5)
        tk.Label(info_frame, text=current_time, font=("Courier New", 14, "bold"), 
                fg="white", bg="#1a2a30").grid(row=10, column=left_col+1, columnspan=3, sticky=tk.W, pady=5)
        
        # Create a button frame for better positioning
        button_frame = tk.Frame(preview_frame, bg="#131f24")
        button_frame.grid(row=2, column=0, columnspan=2, pady=30)
        
        # Back Button
        back_button = tk.Button(
            button_frame,
            text="Back",
            font=("Courier New", 18),
            command=self.receiver_info_page,
            fg="white",
            bg="#131f24",
            relief="flat",
            activebackground="#131f24",
            activeforeground="white",
            cursor="hand2"
        )
        back_button.pack(side=tk.LEFT, padx=30)
        
        # Edit Button
        edit_button = tk.Button(
            button_frame,
            text="Edit",
            font=("Courier New", 18),
            command=self.sender_info_page,
            fg="white",
            bg="#131f24",
            relief="flat",
            activebackground="#131f24",
            activeforeground="white",
            cursor="hand2"
        )
        edit_button.pack(side=tk.LEFT, padx=30)
        
        # Submit Button
        submit_button = tk.Button(
            button_frame,
            text="Submit",
            font=("Courier New", 18),
            command=self.submit_document,
            fg="#131f24",
            bg="#58cc02",
            relief="flat",
            activebackground="#58cc02",
            activeforeground="#131f24",
            cursor="hand2"
        )
        submit_button.pack(side=tk.LEFT, padx=30)


    def submit_document(self):
                    # Construct the recipient email address
        student_email = f"{self.student_id}@rtu.edu.ph"

        try:
            # Connect to the database
            conn = sqlite3.connect('docusortDB.db')
            cursor = conn.cursor()

            # Current timestamp
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Insert the document information into the database
            cursor.execute('''
                INSERT INTO documents 
                (sender_fname, sender_surname, studnum, sender_section, sender_fac, sender_course,sender_email, 
                rcvr_fname, rcvr_surname, rcvr_fac, datetime)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                self.first_name, self.last_name, self.student_id, self.section, self.faculty, self.course, student_email,
                self.receiver_first_name, self.receiver_last_name, self.receiver_faculty, current_time
            ))

            conn.commit()
            conn.close()

            
            # Function to verify email existence
            def verify_email(email):
                import socket
                import re
                
                # Basic format validation
                if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                    return False, "Invalid email format"
                    
                # Split email into user and domain parts
                try:
                    domain = email.split('@')[1]
                except IndexError:
                    return False, "Invalid email format"
                    
                # Try to get the MX record for domain
                try:
                    # Instead of using dns.resolver, we'll use socket to check if domain exists
                    socket.gethostbyname(domain)
                    return True, "Email domain exists"
                except socket.gaierror:
                    return False, f"Domain '{domain}' does not exist"
                    
            # Verify the email
            email_is_valid, email_status = verify_email(student_email)
            
            if not email_is_valid:
                messagebox.showwarning("Email Warning", f"Email verification issue: {email_status}\n\nThe submission has been saved, but the receipt may not be delivered.")
            
            # Construct the email
            email_sender = "docusort@gmail.com"  # Your Gmail address
            email_password = "kpgc hbzr kfyb ojiu"  # App Password
            email_subject = "Document Submission Receipt"
            email_body = f"""Hello {self.first_name} {self.last_name},

    Your document has been successfully submitted on {current_time}.
    Here are the details of your submission:

    - Name: {self.first_name} {self.last_name}
    - Student ID: {self.student_id}
    - Section: {self.section}
    - Course: {self.course}
    - Faculty: {self.faculty}
    - Receiver: {self.receiver_first_name} {self.receiver_last_name} ({self.receiver_faculty})
    - Timestamp: {current_time}

    Thank you for using our document submission service!

    Best regards,
    Docusort System
    """

            # Create proper email format with headers
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart

            message = MIMEMultipart()
            message["From"] = email_sender
            message["To"] = student_email
            message["Subject"] = email_subject
            message.attach(MIMEText(email_body, "plain"))

            # Send the email
            try:
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(email_sender, email_password)
                server.send_message(message)
                server.quit()
                email_sent = True
            except Exception as e:
                email_sent = False
                print(f"Email error: {e}")

            # Show success message
            if email_sent:
                messagebox.showinfo("Success", f"Document successfully submitted!\nEmail receipt sent to {student_email}")
            else:
                messagebox.showinfo("Success", f"Document successfully submitted!\nNote: Could not send email receipt to {student_email}")

            # Reset form and go back to landing page
            self.landing_page()
            self.cleartxt_form()

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to submit document: {e}")
            if 'conn' in locals() and conn:
                conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def cleartxt_form(self):
        # Reset the instance variables to empty strings
        self.first_name = ""
        self.last_name = ""
        self.student_id = ""
        self.section = ""
        self.faculty = ""
        self.course = ""
        self.receiver_first_name = ""
        self.receiver_last_name = ""
        self.receiver_faculty = ""                
                                
if __name__ == "__main__":
    root = tk.Tk()
    app = DocuSortApp(root)
    root.mainloop()