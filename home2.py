import tkinter as tk
from tkinter import ttk, messagebox

# Create the main application window
class DocuSortApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DOCUSORT")
        self.root.geometry("1920x1080")
        self.root.state('zoomed')
        self.root.resizable(False,False)
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
        # Clear any previous widgets (if any)
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create a frame to hold the content with the desired background color
        frame = tk.Frame(self.root, bg="#131f24")  # Dark background color
        frame.pack(fill=tk.BOTH, expand=True)

        # Create a frame for the logo to place the labels side by side
        logo_frame = tk.Frame(frame, bg="#131f24")
        logo_frame.pack(pady=(350, 50))

        # Add both parts of the logo in one row
        header_label = tk.Label(logo_frame, text="DOCU", font=("Courier New", 100), fg="white", bg="#131f24")
        header_label.pack(side=tk.LEFT)

        sort_label = tk.Label(logo_frame, text="SORT", font=("Courier New", 100, "bold"), fg="#58cc02", bg="#131f24")
        sort_label.pack(side=tk.LEFT)

        # Add start button below the logo
        start_button = tk.Button(frame, text="START", font=("Courier New", 40), command=self.sender_info_page, bg="#58cc02", fg="#fff")
        start_button.pack(pady=20)

    

    def sender_info_page(self):
        # Clear any previous widgets (if any)
        for widget in self.root.winfo_children():
            widget.destroy()

        # Sender Info Page
        tk.Label(self.root, text="Sender Info", font=("Courier New", 18)).pack(pady=20)

        # Create a frame to hold the form fields and buttons in a grid
        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=20)

        # First Name and Last Name (in the same row)
        tk.Label(form_frame, text="First Name:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.first_name_entry = tk.Entry(form_frame)
        self.first_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

        tk.Label(form_frame, text="Last Name:").grid(row=0, column=2, padx=10, pady=5, sticky=tk.W)
        self.last_name_entry = tk.Entry(form_frame)
        self.last_name_entry.grid(row=0, column=3, padx=10, pady=5, sticky=tk.W)

        # Student ID and Section (in the same row)
        tk.Label(form_frame, text="Student ID #:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.student_id_entry = tk.Entry(form_frame)
        self.student_id_entry.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)

        tk.Label(form_frame, text="Section:").grid(row=1, column=2, padx=10, pady=5, sticky=tk.W)
        self.section_entry = tk.Entry(form_frame)
        self.section_entry.grid(row=1, column=3, padx=10, pady=5, sticky=tk.W)

        # Faculty and Course (in the same row)
        tk.Label(form_frame, text="Faculty:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        self.faculty_combobox = ttk.Combobox(form_frame, values=[ 
            "College of Engineering and Architecture", 
            "Institute of Computer Studies", 
            "Institute of Architecture", 
            "College of Business and Entrepreneurial Technology", 
            "College of Education", 
            "College of Arts and Sciences", 
            "Institute of Human Kinetics"
        ])
        self.faculty_combobox.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)

        tk.Label(form_frame, text="Course:").grid(row=2, column=2, padx=10, pady=5, sticky=tk.W)
        self.course_combobox = ttk.Combobox(form_frame)
        self.course_combobox.grid(row=2, column=3, padx=10, pady=5, sticky=tk.W)

        # Buttons to go back to the landing page or move to the next page
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)

        cancel_button = tk.Button(button_frame, text="Cancel", command=self.go_back_to_landing_page)
        cancel_button.pack(side=tk.LEFT, padx=20)

        next_button = tk.Button(button_frame, text="Next", command=self.save_sender_info)
        next_button.pack(side=tk.RIGHT, padx=20)

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

        # Receiver Info Page
        tk.Label(self.root, text="Receiver Info", font=("Courier New", 18)).pack(pady=20)

        # Create a frame to hold the form fields and buttons in a grid
        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=20)

        # First Name and Last Name (in the same row)
        tk.Label(form_frame, text="First Name:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.receiver_first_name_entry = tk.Entry(form_frame)
        self.receiver_first_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

        tk.Label(form_frame, text="Last Name:").grid(row=0, column=2, padx=10, pady=5, sticky=tk.W)
        self.receiver_last_name_entry = tk.Entry(form_frame)
        self.receiver_last_name_entry.grid(row=0, column=3, padx=10, pady=5, sticky=tk.W)

        # Faculty (in the same row)
        tk.Label(form_frame, text="Faculty:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.receiver_faculty_combobox = ttk.Combobox(form_frame, values=[ 
            "College of Engineering and Architecture", 
            "Institute of Computer Studies", 
            "Institute of Architecture", 
            "College of Business and Entrepreneurial Technology", 
            "College of Education", 
            "College of Arts and Sciences", 
            "Institute of Human Kinetics"
        ])
        self.receiver_faculty_combobox.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)

        # Buttons to cancel or submit
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)

        back_button = tk.Button(button_frame, text="Back", command=self.sender_info_page)
        back_button.pack(side=tk.LEFT, padx=20)

        submit_button = tk.Button(button_frame, text="Submit", command=self.submit_receiver_info)
        submit_button.pack(side=tk.RIGHT, padx=20)

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


# Create the main Tkinter window and pass it to the DocuSortApp
root = tk.Tk()
app = DocuSortApp(root)

# Start the Tkinter event loop
root.mainloop()
