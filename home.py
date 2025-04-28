import tkinter as tk
from tkinter import ttk, messagebox

current_step = 1

def show_step(step):
    for i, frame in enumerate(steps, 1):
        frame.pack_forget()
        if i == step:
            frame.pack(pady=20)

    update_nav_buttons()

def next_step():
    global current_step
    if current_step < len(steps):
        current_step += 1
        update_progress()
        show_step(current_step)

def prev_step():
    global current_step
    if current_step > 1:
        current_step -= 1
        update_progress()
        show_step(current_step)

def cancel():
    student_frame.pack_forget()
    landing_frame.pack(pady=50)

def update_progress():
    for i, dot in enumerate(progress_dots, 1):
        if i <= current_step:
            dot.configure(fg="#4CAF50")  # Green progress
        else:
            dot.configure(fg="lightgray")

def update_nav_buttons():
    if current_step == 1:
        back_btn.grid_remove()
        cancel_btn.grid(row=0, column=0, padx=10, pady=10)  # Place cancel button below
    else:
        cancel_btn.grid_remove()
        back_btn.grid(row=0, column=0, padx=10, pady=10)  # Place back button below

def student_info():
    global steps, progress_dots, back_btn, next_btn, cancel_btn, student_frame

    landing_frame.pack_forget()

    student_frame = tk.Frame(root, bg="#f9f9f9")
    student_frame.pack(fill="both", expand=True)

    # Progress Bar
    progress_frame = tk.Frame(student_frame, bg="#f9f9f9")
    progress_frame.pack(pady=10)

    progress_dots = []
    for i in range(5):
        dot = tk.Label(progress_frame, text="●", font=("Arial", 16), fg="lightgray", bg="#f9f9f9")
        dot.pack(side="left", padx=5)
        progress_dots.append(dot)

    # Steps
    steps = []

    def create_label_entry(parent, label_text):
        frame = tk.Frame(parent, bg="#f9f9f9")
        label = tk.Label(frame, text=label_text, font=("Helvetica", 12), bg="#f9f9f9")
        label.pack(anchor="w")
        entry = ttk.Entry(frame, width=40)
        entry.pack(pady=5)
        frame.pack(pady=5)
        return entry

    # Step 1: First & Last Name
    step1 = tk.Frame(student_frame, bg="#f9f9f9")
    create_label_entry(step1, "First Name:")
    create_label_entry(step1, "Last Name:")
    steps.append(step1)

    # Step 2: ID and Section
    step2 = tk.Frame(student_frame, bg="#f9f9f9")
    create_label_entry(step2, "ID number:")
    create_label_entry(step2, "Section:")
    steps.append(step2)

    # Step 3: Faculty & Degree
    step3 = tk.Frame(student_frame, bg="#f9f9f9")
    tk.Label(step3, text="Faculty:", font=("Helvetica", 12), bg="#f9f9f9").pack(anchor="w")
    faculty_entry = ttk.Combobox(step3, values=[
        "College of Engineering and Architecture",
        "Institute of Computer Studies",
        "Institute of Architecture",
        "College of Business and Entrepreneurial Technology",
        "College of Education",
        "College of Arts and Sciences",
        "Institute of Human Kinetics"
    ], width=38)
    faculty_entry.pack(pady=5)

    create_label_entry(step3, "Undergraduate Degree:")
    steps.append(step3)

    # Step 4: Receiver's First & Last Name
    step4 = tk.Frame(student_frame, bg="#f9f9f9")
    create_label_entry(step4, "Receiver First Name (optional):")
    create_label_entry(step4, "Receiver Last Name (optional):")
    steps.append(step4)

    # Step 5: Receiver's Faculty
    step5 = tk.Frame(student_frame, bg="#f9f9f9")
    tk.Label(step5, text="Receiver Faculty:", font=("Helvetica", 12), bg="#f9f9f9").pack(anchor="w")
    receiver_faculty = ttk.Combobox(step5, values=[
        "College of Engineering and Architecture",
        "Institute of Computer Studies",
        "Institute of Architecture",
        "College of Business and Entrepreneurial Technology",
        "College of Education",
        "College of Arts and Sciences",
        "Institute of Human Kinetics"
    ], width=38)
    receiver_faculty.pack(pady=5)
    steps.append(step5)

    # Navigation Buttons
    nav_frame = tk.Frame(student_frame, bg="#f9f9f9")
    nav_frame.pack(pady=20)

    back_btn = ttk.Button(nav_frame, text="← Back", command=prev_step)
    back_btn.grid(row=0, column=0, padx=10)

    next_btn = ttk.Button(nav_frame, text="Next →", command=next_step)
    next_btn.grid(row=0, column=1, padx=10)

    cancel_btn = ttk.Button(nav_frame, text="Cancel", command=cancel)
    cancel_btn.grid(row=0, column=2, padx=10)

    update_progress()
    show_step(current_step)

def main():
    global root, landing_frame
    root = tk.Tk()
    root.title("DocuSort")
    root.geometry("600x500")
    root.configure(bg="#131f24")

    landing_frame = tk.Frame(root, bg="white")
    landing_frame.pack(pady=50)

    header_label = tk.Label(landing_frame, text="DOCU", font=("Helvetica", 32), bg="white")
    header_label.pack()
    sort_label = tk.Label(landing_frame, text="SORT", font=("Helvetica", 32, "bold"), fg="#ff6600", bg="white")
    sort_label.pack()

    get_sorting_btn = ttk.Button(landing_frame, text="Let's get Sorting →", command=student_info)
    get_sorting_btn.pack(pady=20)

    admin_login_btn = ttk.Button(landing_frame, text="Admin Login", command=lambda: messagebox.showinfo("Admin Login", "Redirecting to Admin Login..."))
    admin_login_btn.place(x=500, y=10)

    root.mainloop()

if __name__ == "__main__":
    main()
