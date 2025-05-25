import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
from datetime import datetime
import sys
import smtplib
# import pigpio
# import RPi.GPIO as GPIO
import time
import threading



# Pin Definitions
servo_pin = 17
ir_pin = 27
second_servo_pin = 22

# # Set GPIO mode
# GPIO.setmode(GPIO.BCM)

# # Ultrasonic Sensor Pins
# TRIG = 23
# ECHO = 24
# TRIG2 = 20  # GPIO 18 for trigger
# ECHO2 = 21  # GPIO 25 for echo

# GPIO.setwarnings(False)
# GPIO.cleanup()
# GPIO.setmode(GPIO.BCM)

# # Setup pins
# GPIO.setup(TRIG, GPIO.OUT)
# GPIO.setup(ECHO, GPIO.IN)
# GPIO.setup(TRIG2, GPIO.OUT)
# GPIO.setup(ECHO2, GPIO.IN)

# # Setup
# pi = pigpio.pi()
# if not pi.connected:
#     sys.exit("Could not connect to pigpio daemon")

# # Function to move servo to an angle using pigpio
# def set_angle(angle):
#     pulsewidth = 500 + (angle / 180.0) * 2000  # Maps 0-180 to 500-2500 us
#     pi.set_servo_pulsewidth(servo_pin, pulsewidth)

# def set_angle_second_servo(angle):
#     pulsewidth = 500 + (angle / 180.0) * 2000
#     pi.set_servo_pulsewidth(second_servo_pin, pulsewidth)



# # Track last position
# last_angle = None
# # Set IR pin as input
# pi.set_mode(ir_pin, pigpio.INPUT)

# def monitor_ir():
#     global last_angle
#     print("?? System ready. IR sensor watching...")
#     try:
#         while True:
#             ir_state = GPIO.input(ir_pin)

#             if ir_state == 0:  # Object detected
#                 if last_angle != 180:
#                     print("?? Object detected! Moving to 180ï¿½.")
#                     set_angle(60)
#                     last_angle = 60
#             else:
#                 if last_angle != 0:
#                     print("?? No object. Moving back to 0ï¿½.")
#                     set_angle(0)
#                     last_angle = 0

#             time.sleep(0.2)
#     except Exception as e:
#         print(f"IR Monitoring Error: {e}")

# Create the main application window
class DocuSortApp:
    def only_numbers_and_dash(self, input_text):
    # allow digits and dash, and allow empty input
        return all(c.isdigit() or c == '-' for c in input_text) or input_text == ""

    def only_letters(self, input_text):
        return input_text.isalpha() or input_text == ""
    
    # def wait_for_document_insertion(self, callback=None):
    #     """Wait for document to be inserted via IR sensor detection"""
    #     def check_ir_sensor():
    #         if pi.read(ir_pin) == 0:  # Document detected (LOW signal)
    #             print("[SUBMIT] Document detected by IR sensor!")
    #             if callback:
    #                 callback()  # Call the callback function when document is detected
    #         else:
    #             # Check again after a short delay
    #             self.root.after(100, check_ir_sensor)
        
    #     # Start checking for IR sensor
    #     print("[SUBMIT] Waiting for document insertion...")
    #     check_ir_sensor()
    
    # def move_second_servo_with_ir_detection(self, callback=None):
    #     """
    #     Move second servo to specified angle and wait for IR detection to close it
    #     Optional callback parameter is ignored as it's just to maintain compatibility
    #     """
    #     # Servo should already be at the correct angle by this point
    #     print("[SUBMIT] Second servo is open, waiting for document processing...")
        
    #     def wait_for_ir_and_revert():
    #         # Wait a moment to ensure the document is fully processed
    #         time.sleep(3)
            
    #         # Move back to 0ï¿½ (closed)
    #         set_angle_second_servo(0)
    #         print("[SUBMIT] Second servo (Pin 22): returned to 0ï¿½ (closed)")
            
    #         # Return to landing page and clear form
    #         self.root.after(0, self.go_back_to_landing_page)
    #         self.root.after(0, self.cleartxt_form)
        
    #     # Start background thread for waiting and closing
    #     threading.Thread(target=wait_for_ir_and_revert, daemon=True).start()

#start
    # Unified method that checks faculty and uses appropriate sensor
    # def check_distance_and_proceed(self):
    #     """Check distance based on selected faculty and proceed accordingly"""
    #     try:
    #         # Get the selected faculty from combobox
    #         selected_faculty = self.receiver_faculty_combobox.get()
            
    #         if selected_faculty == "College of Engineering":
    #             # Use 2nd sensor for College of Engineering
    #             distance = self.get_single_distance_2()
    #             sensor_name = "2nd sensor"
    #             max_distance = 45  # College of Engineering uses 50cm as max
                
    #         elif selected_faculty == "College of Business, Entrepreneurial and Accountancy":
    #             # Use 1st sensor for College of Business
    #             distance = self.get_single_distance()
    #             sensor_name = "1st sensor"
    #             max_distance = 30  # College of Business uses 30cm as max

    #         else:
    #             # Default case or no selection
    #             messagebox.showerror("Selection Error", "Please select a valid faculty")
    #             return
            
    #         # Check if sensor failed to read
    #         maxultradistance = 0
    #         if distance is None:
    #             messagebox.showerror("Sensor Error", f"Unable to read distance from {sensor_name}")
    #             return
    #         if selected_faculty == "College of Engineering":
    #             maxultradistance = 27
    #         else:
    #             maxultradistance = 18
            
    #         # Check distance conditions
    #         if distance < maxultradistance:
    #             messagebox.showerror("Bin Full", "Oooops. The bin is at full capacity. Please contact your local admin for support")
    #             # self.landing_page()
    #             return
    #         elif maxultradistance <= distance <= max_distance:
    #             # Distance is in acceptable range, proceed without showing messagebox
    #             self.update_receiver_names()
    #         else:  # distance > max_distance
    #             messagebox.showerror("Bin Full", "Oooops. The bin is at full capacity. Please contact your local admin for support")
    #             # self.landing_page()
    #             return
                
    #     except Exception as e:
    #         messagebox.showerror("Error", f"Sensor error: {str(e)}")
    
    # #CBEA
    # def get_single_distance(self, timeout=0.02):
    #     GPIO.output(TRIG, False)
    #     time.sleep(0.000000001)
    #     GPIO.output(TRIG, True)
    #     time.sleep(0.000000001)
    #     GPIO.output(TRIG, False)
        
    #     start_time = time.perf_counter()
    #     while GPIO.input(ECHO) == 0:
    #         if time.perf_counter() - start_time > timeout:
    #             return None
    #     pulse_start = time.perf_counter()
        
    #     while GPIO.input(ECHO) == 1:
    #         if time.perf_counter() - pulse_start > timeout:
    #             return None
    #     pulse_end = time.perf_counter()
        
    #     pulse_duration = pulse_end - pulse_start
    #     distance = pulse_duration * 17150
    #     return round(distance, 2)
    # #CEng
    # def get_single_distance_2(self, timeout=0.02):
    #     GPIO.output(TRIG2, False)
    #     time.sleep(0.000000001)
    #     GPIO.output(TRIG2, True)
    #     time.sleep(0.000000001)
    #     GPIO.output(TRIG2, False)
        
    #     start_time = time.perf_counter()
    #     while GPIO.input(ECHO2) == 0:
    #         if time.perf_counter() - start_time > timeout:
    #             return None
    #     pulse_start = time.perf_counter()
        
    #     while GPIO.input(ECHO2) == 1:
    #         if time.perf_counter() - pulse_start > timeout:
    #             return None
    #     pulse_end = time.perf_counter()
        
    #     pulse_duration = pulse_end - pulse_start
    #     distance = pulse_duration * 17150
    #     return round(distance, 2)
    
    def __init__(self, root):
        self.root = root
        self.root.title("DocuSort")
        # self.root.resizable(False, False)
        self.root.configure(bg="#131f24")
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Key>", self.press_to_start)

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
    def toggle_fullscreen(self, event=None):
        self.root.attributes("-fullscreen", True)

    def exit_fullscreen(self, event=None):
        self.root.attributes("-fullscreen", False)
    def press_to_start(self, event=None):
        excluded_keys = {
            "Alt_L", "Alt_R", "Tab", "F", "f",
            "F1", "F2", "F3", "F4", "F5", "F6",
            "F7", "F8", "F9", "F10", "F11", "F12"
        }

        # If this was triggered by a keypress, check if the key is excluded
        if event is not None and event.keysym in excluded_keys:
            return

        self.root.unbind("<Key>")  # Unbind the key event to prevent multiple triggers
        self.root.bind("<Escape>", self.exit_fullscreen)
        self.root.bind("<f>", self.toggle_fullscreen)
        self.root.bind("<F>", self.toggle_fullscreen)
        self.sender_info_page()



            
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
                datetime TEXT NOT NULL,
                doc_type TEXT NOT NULL
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

        # Modified Start Button
        start_button = tk.Button(frame, text="Press Any Key to Start...", 
                                font=("Courier New", 20), 
                                command=lambda: self.press_to_start(), 
                                bg="#131f24", fg="#fff", cursor="hand2", relief="flat")
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
        self.root.unbind("<Key>")  # Unbind the key event to prevent multiple triggers

        # Create a frame for the login form
        form_frame = tk.Frame(self.root, bg="#1a2a30")
        form_frame.pack(pady=(175, 18))

        inner_form_frame = tk.Frame(form_frame, bg="#1a2a30")
        inner_form_frame.pack(padx=70, pady=50)  # This creates the internal padding
        
        # Header
        tk.Label(inner_form_frame, text="Admin Login", font=("Courier New", 40, "bold"),
                fg="#58cc02", bg="#1a2a30").grid(row=0, column=0, columnspan=2, pady=30)

        # Username
        tk.Label(inner_form_frame, text="Username:", font=("Courier New", 18),
                fg="white", bg="#1a2a30").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.username_entry = tk.Entry(inner_form_frame, font=("Courier New", 18),
                                    fg="white", bg="#1a2a30", width=30)
        self.username_entry.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
        self.username_entry.focus_set()

        # Password
        tk.Label(inner_form_frame, text="Password:", font=("Courier New", 18),
                fg="white", bg="#1a2a30").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        self.password_entry = tk.Entry(inner_form_frame, font=("Courier New", 18),
                                    fg="white", bg="#1a2a30", show="*", width=30)
        self.password_entry.grid(row=4, column=0, columnspan=2, padx=10, pady=5)
        self.password_entry.bind('<KeyRelease>', self.check_enter_key)

        cancel_button = tk.Button(
            inner_form_frame,
            text="Cancel",
            font=("Courier New", 18),
            command=self.go_back_to_landing_page,
            fg="white",  # Text color is white
            bg=inner_form_frame.cget("bg"),  # Same as the background of the frame
            relief="flat",  # Flat button with no border
            cursor="hand2"
        )
        cancel_button.grid(row=5, column=0, pady=(40, 0), sticky=tk.E, padx=(0,125))

        # Next Button (Custom background color #58cc02, white text)
        admin_loginbtn = tk.Button(
            inner_form_frame,
            text="Login",
            font=("Courier New", 18, "bold"),
            command=self.validate_login,
            fg="#131f24",  # Text color is white
            bg="#58cc02",  # Custom background color
            relief="flat",  # Flat button with no border
            activebackground="#58cc02",  # Same color when clicked
            activeforeground="white"  # Text color when clicked
        )
        admin_loginbtn.grid(row=5, column=1, pady=(40, 0), sticky=tk.W, padx=(110, 0))

    def check_enter_key(self, event):
        if event.keysym == 'Return':
            self.root.focus_set()
            self.validate_login()
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
            
            if user:
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
                    # Print login info to the terminal
                print(f"User '{user[1]}' has logged in successfully.")
                
                # Hide the login window
                self.root.withdraw()
                
                # Import here to avoid circular imports
                from admin import AdminApp
                
                admin_window = tk.Toplevel(self.root)
                AdminApp(admin_window, current_user=user[1])


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
    
        # Outer frame with border
        form_frame = tk.Frame(self.root, bg="#1a2a30")
        form_frame.pack(pady=(120, 18))

        # Inner frame to simulate "padding" inside the bordered frame
        inner_form_frame = tk.Frame(form_frame, bg="#1a2a30")
        inner_form_frame.pack(padx=70, pady=50)  # This creates the internal padding


        # Sender Information Header (should occupy all columns, centered)
        tk.Label(inner_form_frame, text="Sender Information", font=("Courier New", 40, "bold"), fg="#58cc02", bg="#1a2a30").grid(row=0, column=0, columnspan=4, pady=30)

        # First Name and Last Name (in the same row)
        vcmd = (self.root.register(self.only_letters), '%P')
        tk.Label(inner_form_frame, text="First Name:", font=("Courier New", 18), fg="white", bg="#1a2a30").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.first_name_entry = tk.Entry(inner_form_frame, font=("Courier New", 18), fg="white", bg="#1a2a30", width=18, validate="key", validatecommand=vcmd)
        self.first_name_entry.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        self.first_name_entry.insert(0, self.first_name)
        self.first_name_entry.focus_set()
        
        tk.Label(inner_form_frame, text="Last Name:", font=("Courier New", 18), fg="white", bg="#1a2a30").grid(row=1, column=2, padx=10, pady=5, sticky=tk.W)
        self.last_name_entry = tk.Entry(inner_form_frame, font=("Courier New", 18), fg="white", bg="#1a2a30", width=18, validate="key", validatecommand=vcmd)
        self.last_name_entry.grid(row=2, column=2, padx=10, pady=5, sticky=tk.W)
        self.last_name_entry.insert(0, self.last_name)

        # Student ID and Section (in the next row)
        vcmd_student_no = (self.root.register(self.only_numbers_and_dash), '%P')
        tk.Label(inner_form_frame, text="Student ID #:", font=("Courier New", 18), fg="white", bg="#1a2a30").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        self.student_id_entry = tk.Entry(inner_form_frame, font=("Courier New", 18), fg="white", bg="#1a2a30", width=18,
                                        validate="key", validatecommand=vcmd_student_no)
        self.student_id_entry.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
        self.student_id_entry.insert(0, self.student_id)

        tk.Label(inner_form_frame, text="Section:", font=("Courier New", 18), fg="white", bg="#1a2a30").grid(row=3, column=2, padx=10, pady=5, sticky=tk.W)
        self.section_entry = tk.Entry(inner_form_frame, font=("Courier New", 18), fg="white", bg="#1a2a30", width=18)
        self.section_entry.grid(row=4, column=2, padx=10, pady=5, sticky=tk.W)
        self.section_entry.insert(0, self.section)

        # Faculty and Course (in the next row)
# Faculty and Course (in the next row)
        tk.Label(inner_form_frame, text="Faculty:", font=("Courier New", 18), fg="white", bg="#1a2a30").grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)

        faculty_options = [
            "Select Student's Faculty",  # <-- Placeholder
            "College of Engineering", 
            "College of Business, Entrepreneurial and Accountancy",
        ]

        self.faculty_combobox = ttk.Combobox(
            inner_form_frame,
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

        tk.Label(inner_form_frame, text="Course:", font=("Courier New", 18), fg="white", bg="#1a2a30").grid(row=7, column=0, padx=10, pady=5, sticky=tk.W)

        self.course_combobox = ttk.Combobox(
            inner_form_frame,
            font=("Courier New", 18),
            width=39,
            state="disabled",
        )
        self.course_combobox.grid(row=8, column=0, columnspan=4, padx=10, pady=5, sticky=tk.W)

        # Set course placeholder or value if available
        if hasattr(self, "course") and self.course:
            self.course_combobox.set(self.course)

        else:
            self.course_combobox.set("Select Student's Course")  # Optional placeholder
        

        # Cancel Button (Transparent background, white text)
        cancel_button = tk.Button(
            inner_form_frame,
            text="Cancel",
            font=("Courier New", 18),
            command=self.go_back_to_landing_page,
            fg="white",  # Text color is white
            bg=inner_form_frame.cget("bg"),  # Same as the background of the frame
            relief="flat",  # Flat button with no border
            activebackground=inner_form_frame.cget("bg"),  # Same color when clicked
            activeforeground="white",  # Text color when clicked
            cursor="hand2"
        )
        cancel_button.grid(row=9, column=0, columnspan=2, pady=(40, 0), sticky=tk.E, padx=(0, 200))

        # Next Button (Custom background color #58cc02, white text)
        next_button = tk.Button(
            inner_form_frame,
            text="Next",
            font=("Courier New", 18),
            command=self.save_sender_info,
            fg="#131f24",  # Text color is white
            bg="#58cc02",  # Custom background color
            relief="flat",  # Flat button with no border
            activebackground="#58cc02",  # Same color when clicked
            activeforeground="white",  # Text color when clicked
            cursor="hand2"
        )
        next_button.grid(row=9, column=2, columnspan=2, pady=(40, 0), sticky=tk.W, padx=(200, 0))

        # Bind faculty selection to update courses
        self.faculty_combobox.bind("<<ComboboxSelected>>", self.update_courses)  
        self.student_id_entry.bind('<KeyRelease>', self.format_student_id)


    def go_back_to_landing_page(self):
        self.root.focus_set()
        self.landing_page()
        self.root.bind("<Key>", self.press_to_start)

        

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
            "College of Business, Entrepreneurial and Accountancy": [
                "B.S. in Accountancy", "B.S. in Business Administration", "B.S. in Entrepreneurship",
                "B.S. in Hospitality Management"
            ]
        }


        # Update course combobox
        if faculty in faculty_degrees:
            course_list = faculty_degrees[faculty]
            self.course_combobox['state'] = 'readonly'
            self.course_combobox.set("Select Student's Course")
            self.course_combobox['values'] = course_list
        else:
            self.course_combobox['state'] = 'disabled'
            self.course_combobox.set("Select Student's Course")

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
            return

        # Proceed to next page if all fields are filled
        self.receiver_info_page()

    def receiver_info_page(self):
        # Clear any previous widgets (if any)
        for widget in self.root.winfo_children():
            widget.destroy()

        # Optional: set fixed window size (ensure enough space)
        self.root.geometry("1000x800")

        form_frame = tk.Frame(self.root, bg="#1a2a30")
        form_frame.pack(pady=(100, 18))

        # Inner frame to simulate "padding" inside the bordered frame
        inner_form_frame = tk.Frame(form_frame, bg="#1a2a30")
        inner_form_frame.pack(padx=40, pady=40)

        # Receiver Information Header (should occupy all columns, centered)
        tk.Label(inner_form_frame, text="Receiver Information", font=("Courier New", 32, "bold"),
                fg="#58cc02", bg="#1a2a30").grid(row=0, column=0, columnspan=4, pady=50)

        # Faculty Dropdown
        rcvr_faculty_option = [
            "Select Receiver's Faculty",
            "College of Engineering",
            "College of Business, Entrepreneurial and Accountancy"
        ]
        tk.Label(inner_form_frame, text="Faculty:", font=("Courier New", 18), fg="white", bg="#1a2a30")\
            .grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.receiver_faculty_combobox = ttk.Combobox(
            inner_form_frame, font=("Courier New", 18), width=45, state="readonly", values=rcvr_faculty_option
        )
        self.receiver_faculty_combobox.grid(row=2, column=0, columnspan=4, padx=10, pady=5, sticky=tk.W)
        
        # Handle case where self.receiver_faculty might not exist
        default_faculty = getattr(self, 'receiver_faculty', None) or rcvr_faculty_option[0]
        self.receiver_faculty_combobox.set(default_faculty)
        self.receiver_faculty_combobox.bind("<<ComboboxSelected>>", self.on_combobox_change)

        # Receiver Name Dropdown
        tk.Label(inner_form_frame, text="Receiver Name:", font=("Courier New", 18), fg="white", bg="#1a2a30")\
            .grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        self.receiver_name_combobox = ttk.Combobox(
            inner_form_frame, font=("Courier New", 18), width=45, state="disabled", values=["Select Faculty First"]
        )
        self.receiver_name_combobox.grid(row=4, column=0, columnspan=4, padx=10, pady=5, sticky=tk.W)

        # Set receiver name placeholder or value if available
        if hasattr(self, "receiver_name") and self.receiver_name:
            self.receiver_name_combobox.set(self.receiver_name)
        else:
            self.receiver_name_combobox.set("Select Receiver Name")  # Optional placeholder

        # Document Description Label
        tk.Label(inner_form_frame, text="Document Description:", font=("Courier New", 18),
                fg="white", bg="#1a2a30").grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)

        # Multi-line Text Box for Document Description
        self.document_description_text = tk.Text(
            inner_form_frame,
            font=("Courier New", 18),
            fg="#cccccc",  # Changed to lighter gray for better readability
            bg="#2d3e45",  # Slightly lighter background for the text area
            insertbackground="white",  # White cursor
            selectbackground="#58cc02",  # Green selection background
            selectforeground="white",  # White selected text
            width=45,
            height=5,
            wrap="word",
            relief="solid",
            bd=1
        )
        self.document_description_text.grid(row=6, column=0, columnspan=4, padx=10, pady=5, sticky=tk.W)
        
        # Add placeholder text with better handling
        placeholder_text = "Enter your notes or description here..."
        self.document_description_text.insert("1.0", placeholder_text)
        self.document_description_text.config(fg="#888888")  # Gray placeholder text
        
        # Add focus events to handle placeholder text
        def on_focus_in(event):
            if self.document_description_text.get("1.0", tk.END).strip() == placeholder_text:
                self.document_description_text.delete("1.0", tk.END)
                self.document_description_text.config(fg="#cccccc")
        
        def on_focus_out(event):
            if not self.document_description_text.get("1.0", tk.END).strip():
                self.document_description_text.insert("1.0", placeholder_text)
                self.document_description_text.config(fg="#888888")
        
        self.document_description_text.bind("<FocusIn>", on_focus_in)
        self.document_description_text.bind("<FocusOut>", on_focus_out)
        
        # Add scrollbar for the text widget
        scrollbar = tk.Scrollbar(inner_form_frame, orient="vertical", command=self.document_description_text.yview)
        scrollbar.grid(row=6, column=4, sticky="ns", pady=5)
        self.document_description_text.config(yscrollcommand=scrollbar.set)

        # Buttons (Back and Next)
        back_button = tk.Button(
            inner_form_frame,
            text="Back",
            font=("Courier New", 18),
            command=self.sender_info_page,
            fg="white",  # Text color is white
            bg=inner_form_frame.cget("bg"),  # Same as the background of the frame
            relief="flat",  # Flat button with no border
            activebackground=inner_form_frame.cget("bg"),  # Same color when clicked
            activeforeground="white"  # Text color when clicked
        )
        back_button.grid(row=7, column=0, columnspan=2, pady=(40, 0), sticky=tk.E, padx=(0, 260))

        # Changed from Submit to Next
        next_button = tk.Button(
            inner_form_frame,
            text="Next",
            font=("Courier New", 18),
            command=self.save_receiver_info,
            fg="#131f24",  # Text color is white
            bg="#58cc02",  # Custom background color
            relief="flat",  # Flat button with no border
            activebackground="#58cc02",  # Same color when clicked
            activeforeground="white"  # Text color when clicked
        )
        next_button.grid(row=7, column=2, columnspan=2, pady=(40, 0), sticky=tk.W, padx=(260, 0))


    def update_receiver_names(self, event=None):
        faculty = self.receiver_faculty_combobox.get()

        # Mapping of faculty to receiver names and their emails
        self.faculty_receivers = {
            "College of Engineering": {
                "Engr. Ezekiel Nequit": "colomamartinlaurence@gmail.com" # "ecnequit@rtu.edu.ph"
            },
            "College of Business, Entrepreneurial and Accountancy": {
                "Engr. Joben Guevarra": "cmartinlaurence@gmail.com" #"jguevara@rtu.edu.ph"
            }
        }

        if faculty in self.faculty_receivers:
            name_list = list(self.faculty_receivers[faculty].keys())
            self.receiver_name_combobox['state'] = 'readonly'
            self.receiver_name_combobox.set("Select Receiver Name")
            self.receiver_name_combobox['values'] = name_list
        else:
            self.receiver_name_combobox['state'] = 'disabled'
            self.receiver_name_combobox.set("Select Faculty First")

            
    def on_combobox_change(self, event=None):
        self.update_receiver_names()
#        self.check_distance_and_proceed()  # Or whatever other method you want to run
        
    def save_receiver_info(self):
        self.receiver_name = self.receiver_name_combobox.get()
        self.receiver_faculty = self.receiver_faculty_combobox.get()

        # Get and clean document description
        placeholder_text = "Enter your notes or description here..."
        description_content = self.document_description_text.get("1.0", tk.END).strip()
        self.document_description = "" if description_content == placeholder_text or not description_content else description_content

        if not self.receiver_name or self.receiver_name == "Select Receiver Name":
            messagebox.showerror("Missing Information", "Please select a receiver name.")
            return

        if not self.receiver_faculty or self.receiver_faculty == "Select Receiver's Faculty":
            messagebox.showerror("Input Error", "Please select a valid faculty.")
            return

        # 📩 Get receiver email from faculty_receivers
        self.receiver_email = self.faculty_receivers.get(self.receiver_faculty, {}).get(self.receiver_name, "")
        print(f"Receiver Email: {self.receiver_email}")  # Debugging line
        # Servo movement simulation
        try:
            if self.receiver_faculty == "College of Engineering":
                print("[NEXT BUTTON] Servo: Moving to 180° for Engineering")
            elif self.receiver_faculty == "College of Business, Entrepreneurial and Accountancy":
                print("[NEXT BUTTON] Servo: Moving to 0° for CBEA")
        except Exception as e:
            print(f"Servo movement error on next: {e}")

        # Proceed to preview
        self.preview_page()

    def preview_page(self):
        # Clear any previous widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create a frame to hold the preview information
        preview_frame = tk.Frame(self.root, bg="#131f24")
        preview_frame.pack(pady=(50, 18))

        # Preview Header
        tk.Label(preview_frame, text="Document Information Preview", font=("Courier New", 32, "bold"),
                fg="#58cc02", bg="#131f24").grid(row=0, column=0, columnspan=2, pady=30)

        # Info frame
        info_frame = tk.Frame(preview_frame, bg="#1a2a30", padx=20, pady=20)
        info_frame.grid(row=1, column=0, columnspan=2)

        # Sender Information Section
        tk.Label(info_frame, text="SENDER INFORMATION", font=("Courier New", 18, "bold"),
                fg="#58cc02", bg="#1a2a30").grid(row=0, column=0, columnspan=4, sticky=tk.W, pady=(0, 10))

        left_col = 0
        spacer_col = 2
        right_col = 3

        # First Name / Last Name
        tk.Label(info_frame, text="First Name:", font=("Courier New", 14), fg="white", bg="#1a2a30").grid(row=1, column=left_col, sticky=tk.W, pady=5)
        tk.Label(info_frame, text=self.first_name, font=("Courier New", 14, "bold"), fg="white", bg="#1a2a30").grid(row=1, column=left_col+1, sticky=tk.W, pady=5)

        tk.Label(info_frame, text="    ", font=("Courier New", 14), fg="white", bg="#1a2a30").grid(row=1, column=spacer_col, sticky=tk.W, pady=5)

        tk.Label(info_frame, text="Last Name:", font=("Courier New", 14), fg="white", bg="#1a2a30").grid(row=1, column=right_col, sticky=tk.W, pady=5)
        tk.Label(info_frame, text=self.last_name, font=("Courier New", 14, "bold"), fg="white", bg="#1a2a30").grid(row=1, column=right_col+1, sticky=tk.W, pady=5)

        # Student ID / Section
        tk.Label(info_frame, text="Student ID:", font=("Courier New", 14), fg="white", bg="#1a2a30").grid(row=2, column=left_col, sticky=tk.W, pady=5)
        tk.Label(info_frame, text=self.student_id, font=("Courier New", 14, "bold"), fg="white", bg="#1a2a30").grid(row=2, column=left_col+1, sticky=tk.W, pady=5)

        tk.Label(info_frame, text="Section:", font=("Courier New", 14), fg="white", bg="#1a2a30").grid(row=2, column=right_col, sticky=tk.W, pady=5)
        tk.Label(info_frame, text=self.section, font=("Courier New", 14, "bold"), fg="white", bg="#1a2a30").grid(row=2, column=right_col+1, sticky=tk.W, pady=5)

        # Faculty / Course
        tk.Label(info_frame, text="Faculty:", font=("Courier New", 14), fg="white", bg="#1a2a30").grid(row=3, column=left_col, sticky=tk.W, pady=5)
        tk.Label(info_frame, text=self.faculty, font=("Courier New", 14, "bold"), fg="white", bg="#1a2a30", justify="left", wraplength=400).grid(row=3, column=left_col+1, sticky=tk.W, pady=5)

        tk.Label(info_frame, text="Course:", font=("Courier New", 14), fg="white", bg="#1a2a30").grid(row=3, column=right_col, sticky=tk.W, pady=5)
        tk.Label(info_frame, text=self.course, font=("Courier New", 14, "bold"), fg="white", bg="#1a2a30", justify="left", wraplength=400).grid(row=3, column=right_col+1, sticky=tk.W, pady=5)

        # Separator
        separator = tk.Frame(info_frame, height=2, bg="#58cc02")
        separator.grid(row=4, column=0, columnspan=5, sticky="ew", pady=15)

        # Receiver Information Section
        tk.Label(info_frame, text="RECEIVER INFORMATION", font=("Courier New", 18, "bold"),
                fg="#58cc02", bg="#1a2a30").grid(row=5, column=0, columnspan=4, sticky=tk.W, pady=(10, 10))

        # Receiver Name / Faculty
        tk.Label(info_frame, text="Receiver Name:", font=("Courier New", 14), fg="white", bg="#1a2a30").grid(row=6, column=left_col, sticky=tk.W, pady=5)
        tk.Label(info_frame, text=self.receiver_name, font=("Courier New", 14, "bold"), fg="white", bg="#1a2a30").grid(row=6, column=left_col+1, sticky=tk.W, pady=5)

        tk.Label(info_frame, text="Faculty:", font=("Courier New", 14), fg="white", bg="#1a2a30").grid(row=6, column=right_col, sticky=tk.W, pady=5)
        tk.Label(info_frame, text=self.receiver_faculty, font=("Courier New", 14, "bold"), fg="white", bg="#1a2a30", justify="left", wraplength=400).grid(row=6, column=right_col+1, sticky=tk.W, pady=5)

        # Receiver Email (new row)
        tk.Label(info_frame, text="Email:", font=("Courier New", 14), fg="white", bg="#1a2a30").grid(row=7, column=left_col, sticky=tk.W, pady=5)
        tk.Label(info_frame, text=self.receiver_email, font=("Courier New", 14, "bold"), fg="white", bg="#1a2a30").grid(row=7, column=left_col+1, columnspan=3, sticky=tk.W, pady=5)

        # Document Description
        if hasattr(self, 'document_description') and self.document_description:
            tk.Label(info_frame, text="Description:", font=("Courier New", 14), fg="white", bg="#1a2a30").grid(row=8, column=left_col, sticky=tk.NW, pady=5)

            desc_text = tk.Text(info_frame, font=("Courier New", 12), fg="white", bg="#1a2a30",
                                height=3, width=50, wrap="word", relief="flat", bd=0)
            desc_text.grid(row=8, column=left_col+1, columnspan=4, sticky=tk.W, pady=5)
            desc_text.insert("1.0", self.document_description)
            desc_text.config(state="disabled")

        # Separator
        separator2 = tk.Frame(info_frame, height=2, bg="#58cc02")
        separator2.grid(row=9, column=0, columnspan=5, sticky="ew", pady=15)

        # Timestamp section
        tk.Label(info_frame, text="TIMESTAMP", font=("Courier New", 18, "bold"),
                fg="#58cc02", bg="#1a2a30").grid(row=10, column=0, columnspan=4, sticky=tk.W, pady=(10, 10))

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tk.Label(info_frame, text="Date and Time:", font=("Courier New", 14),
                fg="white", bg="#1a2a30").grid(row=11, column=left_col, sticky=tk.W, pady=5)
        tk.Label(info_frame, text=current_time, font=("Courier New", 14, "bold"),
                fg="white", bg="#1a2a30").grid(row=11, column=left_col+1, columnspan=3, sticky=tk.W, pady=5)

        # Button frame
        button_frame = tk.Frame(preview_frame, bg="#131f24")
        button_frame.grid(row=2, column=0, columnspan=2, pady=30)

        tk.Button(button_frame, text="Back", font=("Courier New", 18), command=self.receiver_info_page,
                fg="white", bg="#131f24", relief="flat", activebackground="#131f24",
                activeforeground="white", cursor="hand2").pack(side=tk.LEFT, padx=30)

        tk.Button(button_frame, text="Edit", font=("Courier New", 18), command=self.sender_info_page,
                fg="white", bg="#131f24", relief="flat", activebackground="#131f24",
                activeforeground="white", cursor="hand2").pack(side=tk.LEFT, padx=30)

        tk.Button(button_frame, text="Submit", font=("Courier New", 18), command=self.submit_document,
                fg="#131f24", bg="#58cc02", relief="flat", activebackground="#58cc02",
                activeforeground="#131f24", cursor="hand2").pack(side=tk.LEFT, padx=30)


    def submit_document(self):
        try:
            student_email = f"{self.student_id}@rtu.edu.ph"
            receiver_email = self.receiver_email  # Ensure this is set from combobox
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Only send emails if not in testing mode
            email_sent = False
            receiver_notified = False
            if not getattr(self, 'testing_mode', False):  # You can add a testing_mode flag
                email_sent = self.send_receipt_email(student_email, current_time)
                receiver_notified = self.send_receiver_email(receiver_email, current_time)

            # Submit to database regardless of email status
            self.submit_to_database()

            # Give feedback to user
            if email_sent and receiver_notified:
                messagebox.showinfo(
                    "Success",
                    f"Document successfully submitted!\n"
                    f"Email receipt sent to {student_email}.\n"
                    f"Receiver notified at {receiver_email}."
                    
                )
                self.go_back_to_landing_page()
            elif email_sent and not receiver_notified:
                messagebox.showinfo(
                    "Partial Success",
                    f"Document submitted.\n"
                    f"Email receipt sent to {student_email}, "
                    f"but failed to notify the receiver."
                )
                self.go_back_to_landing_page()
            elif not email_sent and receiver_notified:
                messagebox.showinfo(
                    "Partial Success",
                    f"Document submitted.\n"
                    f"Receiver notified at {receiver_email}, "
                    f"but failed to send email receipt to {student_email}."
                )
                self.go_back_to_landing_page()
            else:
                messagebox.showinfo(
                    "Success",
                    f"Document successfully submitted!\n"
                    f"Note: Could not send any email notifications."
                )
                self.go_back_to_landing_page()

        except Exception as e:
            messagebox.showerror("Error", f"Submission failed: {e}")

                
            #messagebox.showinfo("Insert Document", "Please insert your document into the slot now.")
            # Open the servo to receive the document
            #set_angle_second_servo(35)

            # Define a callback function to handle document detection and completion
            # def on_document_inserted():
            #     # Show success message
            #     if email_sent:
            #         messagebox.showinfo("Success", f"Document successfully submitted!\nEmail receipt sent to {student_email}")
            #         self.submit_to_database()
            #     else:
            #         messagebox.showinfo("Success", f"Document successfully submitted!\nNote: Could not send email receipt to {student_email}")
            #         self.submit_to_database()
            #     # Call the method to wait for IR detection and return servo to closed position
            #     self.move_second_servo_with_ir_detection(callback=on_document_inserted)

            # # Start the IR detection in a way that calls our callback when document is detected
            # self.wait_for_document_insertion(callback=on_document_inserted)



 
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def send_receipt_email(self, student_email, submission_time):
        """
        Sends a receipt email to the student with submission details
        
        Args:
            student_email (str): The email address to send the receipt to
            submission_time (str): The timestamp when the document was submitted
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        try:
            # Construct the email
            email_sender = "docusort@gmail.com"  # Your Gmail address
            email_password = "kpgc hbzr kfyb ojiu"  # App Password
            email_subject = "Document Submission Receipt"
            email_body = f"""Hello {self.first_name} {self.last_name},

    Your document has been successfully submitted on {submission_time}.
    Here are the details of your submission:

    - Name: {self.first_name} {self.last_name}
    - Student ID: {self.student_id}
    - Section: {self.section}
    - Course: {self.course}
    - Faculty: {self.faculty}
    - Receiver: {self.receiver_first_name} {self.receiver_last_name} ({self.receiver_faculty})
    - Timestamp: {submission_time}

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
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(email_sender, email_password)
            server.send_message(message)
            server.quit()
            
            return True
            
        except Exception as e:
            print(f"Email error: {e}")
            return False

    def send_receiver_email(self, receiver_email, submission_time):
        """
        Sends a notification email to the faculty receiver

        Args:
            receiver_email (str): The faculty's email address
            submission_time (str): The timestamp when the document was submitted

        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        try:
            email_sender = "docusort@gmail.com"
            email_password = "kpgc hbzr kfyb ojiu"
            email_subject = "New Document Pending for You"
            email_body = f"""Good day {self.receiver_name},

    You have received a new document from a student on {submission_time}.
    Here are the submission details:

    - Sender: {self.first_name} {self.last_name}
    - Student ID: {self.student_id}
    - Section: {self.section}
    - Course: {self.course}
    - Faculty: {self.faculty}
    - Document Status: Pending
    - Document Description: {self.document_description if self.document_description else "No description provided"}
    - Timestamp: {submission_time}

    Please contact a Docusort representative to collect the document.

    Regards,  
    Docusort System
    """

            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart

            message = MIMEMultipart()
            message["From"] = email_sender
            message["To"] = receiver_email
            message["Subject"] = email_subject
            message.attach(MIMEText(email_body, "plain"))

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(email_sender, email_password)
            server.send_message(message)
            server.quit()

            return True

        except Exception as e:
            print(f"Receiver email error: {e}")
            return False


    def submit_to_database(self):
        try:
            student_email = f"{self.student_id}@rtu.edu.ph"

            # Connect to the database
            conn = sqlite3.connect('docusortDB.db')
            cursor = conn.cursor()

            # Current timestamp and document status
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            doc_type = "Pending"

            # Insert into the updated 'documents' table structure
            cursor.execute('''
                INSERT INTO documents 
                (sender_fname, sender_surname, studnum, sender_section, sender_fac, sender_course, sender_email, 
                rcvr_fac, rcvr_name, rcvr_email, doc_description, datetime, doc_type)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                self.first_name,
                self.last_name,
                self.student_id,
                self.section,
                self.faculty,
                self.course,
                student_email,
                self.receiver_faculty,
                self.receiver_name,       # From Combobox
                self.receiver_email,
                self.document_description,
                current_time,
                doc_type
            ))

            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to submit document: {e}")
            if 'conn' in locals() and conn:
                conn.close()
   

    def cleartxt_form(self):
        # Reset the instance variables to empty strings
        self.first_name = ""
        self.last_name = ""
        self.student_id = ""
        self.section = ""
        self.faculty = ""
        self.course = ""
        self.receiver_faculty = ""
        self.receiver_name = ""
        self.document_description = ""              
                                
if __name__ == "__main__":
    root = tk.Tk()
    app = DocuSortApp(root)
    root.mainloop()