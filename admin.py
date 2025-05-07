import tkinter as tk
from tkinter import messagebox

class AdminHomePage:
    def __init__(self, login_root):
        self.login_root = login_root  # The original login window
        self.root = tk.Toplevel(self.login_root)  # Create a new top-level window for admin panel
        self.root.resizable(False, False)
        self.root.configure(bg="#131f24")
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}+0+0")
        self.root.title("Admin Home Page")        
        self.admin_home_page()

        # Hide the login window when admin panel opens
        self.login_root.withdraw()

    def admin_home_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=4)
        
        sidebar_frame = tk.Frame(self.root, bg="#131f24", width=200)
        sidebar_frame.grid(row=0, column=0, rowspan=1, sticky="ns", padx=10, pady=10)

        tk.Label(sidebar_frame, text="Admin Panel", font=("Courier New", 20, "bold"), fg="#58cc02", bg="#131f24").pack(pady=30)

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

        content_frame = tk.Frame(self.root, bg="#f4f4f4")
        content_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.content_label = tk.Label(
            content_frame,
            text="Welcome to the Admin Panel\nClick a button from the sidebar to view content.",
            font=("Courier New", 18), fg="#131f24", bg="#f4f4f4"
        )
        self.content_label.pack(padx=20, pady=20)

    def show_dashboard(self):
        self.update_content("Dashboard", "Here is the dashboard content...")

    def show_settings(self):
        self.update_content("Settings", "Here you can modify settings.")

    def show_reports(self):
        self.update_content("Reports", "Here are the reports.")

    def logout(self):
        messagebox.showinfo("Logged Out", "You have logged out.")
        print("Logging out and going back to login page")

        self.root.destroy()  # Close the admin window

        # Bring the login window back
        from home_with_db import DocuSortApp
    
        login_window = tk.Toplevel(self.login_root)
        DocuSortApp(login_window)        
    
    def update_content(self, title, content):
        self.content_label.config(text=f"{title}\n\n{content}")


# Main application
def main():
    root = tk.Tk()
    app = AdminHomePage(root)
    root.mainloop()


if __name__ == "__main__":
    main()
