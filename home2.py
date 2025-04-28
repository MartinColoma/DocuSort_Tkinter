import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

# Create the main application window
class DocuSortApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DOCUSORT")
        self.root.geometry("1718x1080")
        self.root.state('zoomed')
        self.root.resizable(False,False)
        self.root.configure(bg="#131f24")

        # Initialize data fields
        self.first_name = ""
        self.last_name = ""
        self.student_id = ""
        self.section = ""
        self.faculty = ""
        self.course = ""

        # Landing page
        self.landing_page()

    def landing_page(self):
        # Clear previous widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, bg="#131f24")
        frame.pack(fill=tk.BOTH, expand=True)

        # Frame for logo and image
        logo_frame = tk.Frame(frame, bg="#131f24")
        logo_frame.pack(pady=(180, 18))  # Adjust padding as you like

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

        header_label = tk.Label(text_frame, text="DOCU", font=("Courier New", 100, "bold"), fg="white", bg="#131f24")
        header_label.pack(side=tk.LEFT)

        sort_label = tk.Label(text_frame, text="SORT", font=("Courier New", 100, "bold"), fg="#58cc02", bg="#131f24")
        sort_label.pack(side=tk.LEFT)

        # Start Button below
        start_button = tk.Button(frame, text="Let's get sorting", font=("Courier New", 18), command=self.sender_info_page, bg="#58cc02", fg="#fff")
        start_button.pack(pady=30)

    

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
        tk.Label(form_frame, text="First Name:", font=("Courier New", 18), fg="white", bg="#131f24").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.first_name_entry = tk.Entry(form_frame, font=("Courier New", 18), fg="white", bg="#131f24", width=18)
        self.first_name_entry.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

        tk.Label(form_frame, text="Last Name:", font=("Courier New", 18), fg="white", bg="#131f24").grid(row=1, column=2, padx=10, pady=5, sticky=tk.W)
        self.last_name_entry = tk.Entry(form_frame, font=("Courier New", 18), fg="white", bg="#131f24", width=18)
        self.last_name_entry.grid(row=2, column=2, padx=10, pady=5, sticky=tk.W)

        # Student ID and Section (in the next row)
        tk.Label(form_frame, text="Student ID #:", font=("Courier New", 18), fg="white", bg="#131f24").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        self.student_id_entry = tk.Entry(form_frame, font=("Courier New", 18), fg="white", bg="#131f24", width=18)
        self.student_id_entry.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)

        tk.Label(form_frame, text="Section:", font=("Courier New", 18), fg="white", bg="#131f24").grid(row=3, column=2, padx=10, pady=5, sticky=tk.W)
        self.section_entry = tk.Entry(form_frame, font=("Courier New", 18), fg="white", bg="#131f24", width=18)
        self.section_entry.grid(row=4, column=2, padx=10, pady=5, sticky=tk.W)

        # Faculty and Course (in the next row)
        tk.Label(form_frame, text="Faculty:", font=("Courier New", 18), fg="white", bg="#131f24").grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)
        self.faculty_combobox = ttk.Combobox(form_frame, font=("Courier New", 18), width=39 , state="readonly", values=[
            "College of Engineering and Architecture",
            "Institute of Computer Studies",
            "Institute of Architecture",
            "College of Business and Entrepreneurial Technology",
            "College of Education",
            "College of Arts and Sciences",
            "Institute of Human Kinetics"
        ])
        self.faculty_combobox.grid(row=6, column=0, columnspan=4, padx=10, pady=5, sticky=tk.W)

        tk.Label(form_frame, text="Course:", font=("Courier New", 18), fg="white", bg="#131f24").grid(row=7, column=0, padx=10, pady=5, sticky=tk.W)
        self.course_combobox = ttk.Combobox(form_frame, font=("Courier New", 18), width=39, state="readonly")
        self.course_combobox.grid(row=8, column=0, columnspan=4, padx=10, pady=5, sticky=tk.W)

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



    def go_back_to_landing_page(self):
        # Clears all widgets on the current page and returns to the landing page
        self.landing_page()

    def update_courses(self, event=None):
        faculty = self.faculty_combobox.get()
        course_list = []

        # Mapping of faculty to respective courses
        faculty_degrees = {
            "College of Engineering and Architecture": [
                "B.S. in Mechanical Engineering", "B.S. in Civil Engineering", "B.S. in Electrical Engineering",
                "B.S. in Electronics Engineering", "B.S. in Computer Engineering", "B.S. in Industrial Engineering",
                "B.S. in Instrumentation and Control Engineering", "B.S. in Mechatronics"
            ],
            "Institute of Computer Studies": ["B.S. in Information Technology"],
            "Institute of Architecture": ["B.S. in Architecture"],
            "College of Business and Entrepreneurial Technology": [
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

        # Print the entered information (for now)
        print(f"First Name: {self.first_name}")
        print(f"Last Name: {self.last_name}")
        print(f"Student ID: {self.student_id}")
        print(f"Section: {self.section}")
        print(f"Faculty: {self.faculty}")
        print(f"Course: {self.course}")
        
        # Proceed to receiver info page
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
        tk.Label(form_frame, text="First Name:", font=("Courier New", 18), fg="white", bg="#131f24").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.receiver_first_name_entry = tk.Entry(form_frame, font=("Courier New", 18), fg="white", bg="#131f24", width=18)
        self.receiver_first_name_entry.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

        tk.Label(form_frame, text="Last Name:", font=("Courier New", 18), fg="white", bg="#131f24").grid(row=1, column=2, padx=10, pady=5, sticky=tk.W)
        self.receiver_last_name_entry = tk.Entry(form_frame, font=("Courier New", 18), fg="white", bg="#131f24", width=18)
        self.receiver_last_name_entry.grid(row=2, column=2, padx=10, pady=5, sticky=tk.W)

        # Faculty (in the same row)
        tk.Label(form_frame, text="Faculty:", font=("Courier New", 18), fg="white", bg="#131f24").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        self.receiver_faculty_combobox = ttk.Combobox(form_frame, font=("Courier New", 18), width=40, state="readonly", values=[ 
            "College of Engineering and Architecture", 
            "Institute of Computer Studies", 
            "Institute of Architecture", 
            "College of Business and Entrepreneurial Technology", 
            "College of Education", 
            "College of Arts and Sciences", 
            "Institute of Human Kinetics"
        ])
        self.receiver_faculty_combobox.grid(row=4, column=0, columnspan=4, padx=10, pady=5, sticky=tk.W)


        # Buttons (Cancel and Submit)
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

        submit_button = tk.Button(
            form_frame,
            text="Submit",
            font=("Courier New", 18),
            command=self.submit_receiver_info,
            fg="white",  # Text color is white
            bg="#58cc02",  # Custom background color
            relief="flat",  # Flat button with no border
            activebackground="#58cc02",  # Same color when clicked
            activeforeground="white"  # Text color when clicked
        )
        submit_button.grid(row=5, column=2, columnspan=2, pady=(40, 0), sticky=tk.W, padx=(200, 0))

        # Bind faculty selection to update courses (optional, if needed)
        self.receiver_faculty_combobox.bind("<<ComboboxSelected>>", self.update_receiver_courses)


    def submit_receiver_info(self):
        # Gather the sender's information
        sender_info = {
            "Sender First Name": self.first_name,
            "Sender Last Name": self.last_name,
            "Sender Student ID": self.student_id,
            "Sender Section": self.section,
            "Sender Faculty": self.faculty,
            "Sender Course": self.course,
        }

        # Gather the receiver's information
        receiver_info = {
            "Receiver First Name": self.receiver_first_name_entry.get(),
            "Receiver Last Name": self.receiver_last_name_entry.get(),
            "Receiver Faculty": self.receiver_faculty_combobox.get(),
        }

        # Combine both sender and receiver information into one string
        all_info = "\n".join([f"{key}: {value}" for key, value in {**sender_info, **receiver_info}.items()])

        # Show a popup with both sender and receiver information
        messagebox.showinfo("Submitted Information", all_info)
        self.go_back_to_landing_page()


# Create the main Tkinter window and pass it to the DocuSortApp
root = tk.Tk()
app = DocuSortApp(root)

# Start the Tkinter event loop
root.mainloop()
