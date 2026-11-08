import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import json
import os

FILE_NAME = "students.txt"

#THEME

BG = "#F4F3FA"
CARD = "#FFFFFF"
DARK = "#24213D"
PRIMARY = "#6D5AA8"
PRIMARY_HOVER = "#58478F"
TEXT = "#34304F"
MUTED = "#85819B"
BORDER = "#E2DEEF"
SUCCESS = "#477B72"


# MAIN WINDOW 

root = tk.Tk()
root.title("Student Scholarship Management System")
root.geometry("850x560")
root.resizable(False, False)
root.configure(bg=BG)


# FILE HANDLING

def load_students():
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            data = json.load(file)

            if not isinstance(data, list):
                raise json.JSONDecodeError(
                    "Student data must be a list.", "", 0
                )

            return data

    except (json.JSONDecodeError, OSError):
        messagebox.showerror(
            "File Error",
            "Could not read student records.\n"
            "Please check students.txt."
        )
        return []


def save_students(students):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(students, file, indent=4)


# STUDENT REGISTRATION 

def student_registration():
    registration = tk.Toplevel(root)
    registration.title("Student Registration")
    registration.geometry("540x720")
    registration.resizable(False, False)
    registration.configure(bg=BG)

    # Center registration
    registration.transient(root)
    registration.grab_set()

    # Header

    header = tk.Frame(registration, bg=DARK, height=125)
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="Create Your Account",
        font=("Segoe UI", 21, "bold"),
        bg=DARK,
        fg="#FFFFFF"
    ).pack(anchor="w", padx=34, pady=(23, 5))

    tk.Label(
        header,
        text="Join the student scholarship portal",
        font=("Segoe UI", 10),
        bg=DARK,
        fg="#D0CBEA"
    ).pack(anchor="w", padx=36)

    # Small line
    tk.Frame(
        header,
        bg="#A89ADD",
        height=3
    ).place(x=35, y=105, width=65)

    # Form Container 

    form = tk.Frame(registration, bg=BG)
    form.pack(fill="both", expand=True, padx=42, pady=(14, 5))

    fields = {}

    field_names = [
        ("Name", "Enter your full name"),
        ("Age", "Enter your age"),
        ("Marks", "Enter marks (0–100)"),
        ("Annual Family Income (₹)", "Enter annual income in rupees"),
        ("Username", "Choose a unique username"),
        ("Password", "Create a password")
    ]

    for field, placeholder in field_names:
        tk.Label(
            form,
            text=field,
            font=("Segoe UI", 10, "bold"),
            bg=BG,
            fg=TEXT
        ).pack(anchor="w", pady=(5, 4))

        entry = tk.Entry(
            form,
            font=("Segoe UI", 10),
            relief="flat",
            bd=0,
            bg=CARD,
            fg=TEXT,
            insertbackground=PRIMARY,
            highlightthickness=1,
            highlightbackground=BORDER,
            highlightcolor=PRIMARY,
            show="*" if field == "Password" else ""
        )
        entry.pack(fill="x", ipady=7, pady=(0, 3))

        # Store the entry 
        fields[field] = entry

        # Placeholder

    # Show Password 
    show_password = tk.BooleanVar(value=False)

    def toggle_password():
        fields["Password"].configure(
            show="" if show_password.get() else "*"
        )

    tk.Checkbutton(
        form,
        text="Show password",
        variable=show_password,
        command=toggle_password,
        font=("Segoe UI", 9),
        bg=BG,
        fg=MUTED,
        activebackground=BG,
        activeforeground=TEXT,
        selectcolor=BG,
        cursor="hand2",
        bd=0,
        highlightthickness=0
    ).pack(anchor="w", pady=(3, 0))

    # Registration Logic 

    def submit_registration():
        name = fields["Name"].get().strip()
        username = fields["Username"].get().strip()
        password = fields["Password"].get()
        age_text = fields["Age"].get().strip()
        marks_text = fields["Marks"].get().strip()
        income_text = fields["Annual Family Income (₹)"].get().strip()

        if not all([
            name, username, password,
            age_text, marks_text, income_text
        ]):
            messagebox.showerror(
                "Missing Information",
                "Please fill in all fields.",
                parent=registration
            )
            return

        if any(char in username for char in "\r\n\t"):
            messagebox.showerror(
                "Invalid Username",
                "Please enter a valid username.",
                parent=registration
            )
            return

        try:
            age = int(age_text)
            marks = float(marks_text)
            income = float(income_text)

            if age <= 0 or not 0 <= marks <= 100 or income < 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Enter a positive age, marks from 0 to 100, "
                "and non-negative income.",
                parent=registration
            )
            return

        students = load_students()

        if any(
            student["username"].casefold() == username.casefold()
            for student in students
            if isinstance(student, dict) and "username" in student
        ):
            messagebox.showerror(
                "Username Already Exists",
                "Please choose another username.",
                parent=registration
            )
            return

        student = {
            "name": name,
            "age": age,
            "marks": marks,
            "income": income,
            "username": username,
            "password": password,
            "status": "Pending"
        }

        try:
            students.append(student)
            save_students(students)

        except OSError:
            messagebox.showerror(
                "File Error",
                "Could not save your registration.\n"
                "Please check file permissions.",
                parent=registration
            )
            return

        messagebox.showinfo(
            "Registration Successful",
            "Your account has been created successfully!\n\n"
            "You can now log in using your credentials.",
            parent=registration
        )

        registration.destroy()

    # Create Account Button 

    tk.Button(
        form,
        text="CREATE ACCOUNT   →",
        command=submit_registration,
        font=("Segoe UI", 11, "bold"),
        bg=PRIMARY,
        fg="#FFFFFF",
        activebackground=PRIMARY_HOVER,
        activeforeground="#FFFFFF",
        relief="flat",
        bd=0,
        cursor="hand2"
    ).pack(fill="x", ipady=10, pady=(12, 5))

    # Footer 

    tk.Label(
        registration,
        text="STUDENT SCHOLARSHIP MANAGEMENT SYSTEM",
        font=("Segoe UI", 8, "bold"),
        bg=BG,
        fg=MUTED
    ).pack(pady=(0, 12))



# STUDENT LOGIN 

def student_login():
    login = tk.Toplevel(root)
    login.title("Student Login")
    login.geometry("480x510")
    login.configure(bg=BG)
    login.resizable(False, False)
    login.transient(root)
    login.grab_set()

    header = tk.Frame(login, bg=DARK, height=145)
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="STUDENT PORTAL",
        font=("Segoe UI", 10, "bold"),
        bg=DARK,
        fg="#BEB2EE"
    ).pack(anchor="w", padx=34, pady=(22, 4))

    tk.Label(
        header,
        text="Welcome back!",
        font=("Segoe UI", 23, "bold"),
        bg=DARK,
        fg="white"
    ).pack(anchor="w", padx=32, pady=(0, 4))

    tk.Label(
        header,
        text="Sign in to manage your scholarship applications.",
        font=("Segoe UI", 9),
        bg=DARK,
        fg="#D8D3F0"
    ).pack(anchor="w", padx=34)

    form = tk.Frame(login, bg=BG)
    form.pack(fill="both", expand=True, padx=38, pady=(25, 10))

    tk.Label(
        form,
        text="Username",
        font=("Segoe UI", 10, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(anchor="w", pady=(0, 6))

    username_entry = tk.Entry(
        form,
        font=("Segoe UI", 11),
        relief="flat",
        bg="white",
        fg=TEXT,
        insertbackground=PRIMARY,
        highlightthickness=1,
        highlightbackground=BORDER,
        highlightcolor=PRIMARY
    )
    username_entry.pack(fill="x", ipady=9, pady=(0, 17))

    tk.Label(
        form,
        text="Password",
        font=("Segoe UI", 10, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(anchor="w", pady=(0, 6))

    password_entry = tk.Entry(
        form,
        font=("Segoe UI", 11),
        relief="flat",
        bg="white",
        fg=TEXT,
        insertbackground=PRIMARY,
        show="*",
        highlightthickness=1,
        highlightbackground=BORDER,
        highlightcolor=PRIMARY
    )
    password_entry.pack(fill="x", ipady=9)

    show_password = tk.BooleanVar(value=False)

    def toggle_password():
        password_entry.configure(
            show="" if show_password.get() else "*"
        )

    tk.Checkbutton(
        form,
        text="Show password",
        variable=show_password,
        command=toggle_password,
        font=("Segoe UI", 9),
        bg=BG,
        fg=MUTED,
        activebackground=BG,
        selectcolor=BG,
        cursor="hand2",
        bd=0,
        highlightthickness=0
    ).pack(anchor="w", pady=(7, 0))

    def check_login():
        username = username_entry.get().strip()
        password = password_entry.get()

        if not username or not password:
            messagebox.showerror(
                "Missing Information",
                "Please enter your username and password.",
                parent=login
            )
            return

        students = load_students()

        for student in students:
            if (
                isinstance(student, dict)
                and student.get("username", "").casefold()
                == username.casefold()
                and student.get("password") == password
            ):
                login.destroy()
                student_dashboard(student)
                return

        messagebox.showerror(
            "Login Failed",
            "Incorrect username or password.",
            parent=login
        )

    tk.Button(
        form,
        text="SIGN IN   →",
        command=check_login,
        font=("Segoe UI", 11, "bold"),
        bg=PRIMARY,
        fg="white",
        activebackground=PRIMARY_HOVER,
        activeforeground="white",
        relief="flat",
        bd=0,
        cursor="hand2"
    ).pack(fill="x", ipady=10, pady=(22, 0))

    tk.Label(
        login,
        text="STUDENT SCHOLARSHIP MANAGEMENT SYSTEM",
        font=("Segoe UI", 8, "bold"),
        bg=BG,
        fg=MUTED
    ).pack(pady=(0, 13))

    username_entry.focus_set()
    login.bind("<Return>", lambda event: check_login())


# STUDENT DASHBOARD 

def student_dashboard(student):
    dashboard = tk.Toplevel(root)
    dashboard.title("Student Dashboard")
    dashboard.geometry("850x650")
    dashboard.configure(bg=BG)
    dashboard.resizable(False, False)

    username = student.get("username", "")

    scholarships = [
        {
            "name": "Merit Scholarship",
            "description": "For students with strong academic performance.",
            "tag": "ACADEMIC"
        },
        {
            "name": "Need-Based Scholarship",
            "description": "For students who need financial assistance.",
            "tag": "FINANCIAL SUPPORT"
        },
        {
            "name": "Minority Scholarship",
            "description": "For eligible students applying under this category.",
            "tag": "SPECIAL CATEGORY"
        }
    ]

    # Header 

    header = tk.Frame(dashboard, bg=DARK, height=100)
    header.pack(fill="x")
    header.pack_propagate(False)

    header_left = tk.Frame(header, bg=DARK)
    header_left.pack(side="left", padx=27, pady=18)

    tk.Label(
        header_left,
        text="STUDENT PORTAL",
        font=("Segoe UI", 9, "bold"),
        bg=DARK,
        fg="#BEB2EE"
    ).pack(anchor="w")

    tk.Label(
        header_left,
        text="Your Scholarship Dashboard",
        font=("Segoe UI", 19, "bold"),
        bg=DARK,
        fg="white"
    ).pack(anchor="w", pady=(2, 0))

    header_right = tk.Frame(header, bg=DARK)
    header_right.pack(side="right", padx=25)

    tk.Label(
        header_right,
        text=f"Welcome, {student.get('name', 'Student')}",
        font=("Segoe UI", 10, "bold"),
        bg=DARK,
        fg="white"
    ).pack(anchor="e")

    tk.Label(
        header_right,
        text=f"@{username}",
        font=("Segoe UI", 9),
        bg=DARK,
        fg="#D8D3F0"
    ).pack(anchor="e", pady=(3, 0))

    # Main Content

    content = tk.Frame(dashboard, bg=BG)
    content.pack(fill="both", expand=True, padx=25, pady=17)

    # Profile Card 

    profile = tk.Frame(
        content,
        bg="white",
        highlightbackground=BORDER,
        highlightthickness=1
    )
    profile.pack(fill="x", pady=(0, 17))

    profile_top = tk.Frame(profile, bg="white")
    profile_top.pack(fill="x", padx=18, pady=(13, 5))

    tk.Label(
        profile_top,
        text="YOUR PROFILE",
        font=("Segoe UI", 10, "bold"),
        bg="white",
        fg=PRIMARY
    ).pack(side="left")

    tk.Label(
        profile_top,
        text="Registered Student",
        font=("Segoe UI", 9),
        bg="white",
        fg=MUTED
    ).pack(side="right")

    profile_details = tk.Frame(profile, bg="white")
    profile_details.pack(fill="x", padx=18, pady=(4, 14))

    profile_items = [
        ("FULL NAME", student.get("name", "")),
        ("AGE", str(student.get("age", ""))),
        ("MARKS", f"{student.get('marks', '')}%"),
        ("ANNUAL INCOME", f"₹{student.get('income', '')}")
    ]

    for label_text, value_text in profile_items:
        item = tk.Frame(profile_details, bg="white")
        item.pack(side="left", fill="x", expand=True, padx=(0, 8))

        tk.Label(
            item,
            text=label_text,
            font=("Segoe UI", 8, "bold"),
            bg="white",
            fg=MUTED
        ).pack(anchor="w")

        tk.Label(
            item,
            text=value_text,
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg=TEXT
        ).pack(anchor="w", pady=(4, 0))

    # Scholarship Section Heading 

    section_heading = tk.Frame(content, bg=BG)
    section_heading.pack(fill="x", pady=(0, 9))

    tk.Label(
        section_heading,
        text="Available Scholarships",
        font=("Segoe UI", 16, "bold"),
        bg=BG,
        fg=DARK
    ).pack(side="left")

    tk.Label(
        section_heading,
        text="Apply to multiple scholarships",
        font=("Segoe UI", 9),
        bg=BG,
        fg=MUTED
    ).pack(side="right", pady=(5, 0))

    scholarship_frame = tk.Frame(content, bg=BG)
    scholarship_frame.pack(fill="both", expand=True)

    # Application 

    def get_applications(current_student):
        applications = current_student.get("applications", [])

        old_scholarship = current_student.get("applied_scholarship")

        if old_scholarship and not applications:
            applications = [{
                "scholarship": old_scholarship,
                "status": current_student.get("status", "Pending")
            }]

        return applications

    def get_current_student():
        students = load_students()

        for record in students:
            if record.get("username", "") == username:
                return students, record

        messagebox.showerror(
            "Account Not Found",
            "Your student record could not be found.",
            parent=dashboard
        )
        return None, None

    # Refresh Cards 

    def refresh_applications():
        for widget in scholarship_frame.winfo_children():
            widget.destroy()

        students, current_student = get_current_student()

        if current_student is None:
            return

        applications = get_applications(current_student)

        for scholarship in scholarships:
            scholarship_name = scholarship["name"]

            existing = next(
                (
                    application
                    for application in applications
                    if application.get("scholarship", "").casefold()
                    == scholarship_name.casefold()
                ),
                None
            )

            card = tk.Frame(
                scholarship_frame,
                bg="white",
                highlightbackground=BORDER,
                highlightthickness=1
            )
            card.pack(fill="x", pady=5)

            # Accent strip
            tk.Frame(
                card,
                bg=PRIMARY if existing else "#D9D2EE",
                width=5
            ).pack(side="left", fill="y")

            details = tk.Frame(card, bg="white")
            details.pack(
                side="left",
                fill="both",
                expand=True,
                padx=14,
                pady=10
            )

            title_row = tk.Frame(details, bg="white")
            title_row.pack(fill="x")

            tk.Label(
                title_row,
                text=scholarship_name,
                font=("Segoe UI", 11, "bold"),
                bg="white",
                fg=DARK
            ).pack(side="left")

            tk.Label(
                title_row,
                text=scholarship["tag"],
                font=("Segoe UI", 7, "bold"),
                bg="#F0ECFA",
                fg=PRIMARY,
                padx=7,
                pady=3
            ).pack(side="left", padx=(9, 0))

            tk.Label(
                details,
                text=scholarship["description"],
                font=("Segoe UI", 9),
                bg="white",
                fg=MUTED,
                wraplength=470,
                justify="left"
            ).pack(anchor="w", pady=(5, 0))

            if existing:
                status = existing.get("status", "Pending")

                status_styles = {
                    "Approved": ("#E5F5EB", "#237A48"),
                    "Rejected": ("#FCE9EA", "#B42332"),
                    "Pending": ("#FFF2D6", "#946200")
                }

                status_bg, status_fg = status_styles.get(
                    status,
                    ("#EEEAF5", "#6D5AA8")
                )

                tk.Label(
                    details,
                    text=f"  {status.upper()}  ",
                    font=("Segoe UI", 8, "bold"),
                    bg=status_bg,
                    fg=status_fg,
                    padx=5,
                    pady=3
                ).pack(anchor="w", pady=(7, 0))

                tk.Button(
                    card,
                    text="APPLIED ✓",
                    state="disabled",
                    font=("Segoe UI", 9, "bold"),
                    disabledforeground=SUCCESS,
                    relief="flat",
                    padx=12,
                    pady=7
                ).pack(side="right", padx=15, pady=10)

            else:
                tk.Button(
                    card,
                    text="APPLY NOW  →",
                    command=lambda name=scholarship_name: (
                        apply_scholarship(name)
                    ),
                    font=("Segoe UI", 9, "bold"),
                    bg=PRIMARY,
                    fg="white",
                    activebackground=PRIMARY_HOVER,
                    activeforeground="white",
                    relief="flat",
                    bd=0,
                    cursor="hand2",
                    padx=13,
                    pady=8
                ).pack(side="right", padx=15, pady=10)

    # Apply for Scholarship 

    def apply_scholarship(scholarship_name):
        students, current_student = get_current_student()

        if current_student is None:
            return

        applications = get_applications(current_student)

        already_applied = any(
            application.get("scholarship", "").casefold()
            == scholarship_name.casefold()
            for application in applications
        )

        if already_applied:
            messagebox.showwarning(
                "Already Applied",
                f"You have already applied for {scholarship_name}.",
                parent=dashboard
            )
            refresh_applications()
            return

        confirm = messagebox.askyesno(
            "Confirm Application",
            f"Submit your application for:\n\n{scholarship_name}?",
            parent=dashboard
        )

        if not confirm:
            return

        applications.append({
            "scholarship": scholarship_name,
            "status": "Pending"
        })

        current_student["applications"] = applications
        current_student["applied_scholarship"] = scholarship_name

        try:
            save_students(students)
        except OSError:
            messagebox.showerror(
                "File Error",
                "Your application could not be saved.",
                parent=dashboard
            )
            return

        messagebox.showinfo(
            "Application Submitted",
            f"Your application for {scholarship_name} has been submitted.\n\n"
            "Current status: Pending",
            parent=dashboard
        )

        refresh_applications()

    # Footer Actions 

    footer = tk.Frame(content, bg=BG)
    footer.pack(fill="x", pady=(12, 0))

    tk.Button(
        footer,
        text="↻  Refresh Applications",
        command=refresh_applications,
        font=("Segoe UI", 9, "bold"),
        bg="#E9E4F5",
        fg=PRIMARY,
        activebackground="#DCD4EF",
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=13,
        pady=9
    ).pack(side="left")

    tk.Button(
        footer,
        text="LOG OUT",
        command=dashboard.destroy,
        font=("Segoe UI", 9, "bold"),
        bg=DARK,
        fg="white",
        activebackground="#393455",
        activeforeground="white",
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=19,
        pady=9
    ).pack(side="right")

    refresh_applications()



def admin_login():
    login_window = tk.Toplevel(root)
    login_window.title("Admin Login")
    login_window.geometry("430x460")
    login_window.resizable(False, False)
    login_window.configure(bg=BG)
    login_window.transient(root)
    login_window.grab_set()

    card = tk.Frame(
        login_window, bg=CARD,
        highlightbackground=BORDER, highlightthickness=1
    )
    card.place(relx=0.5, rely=0.5, anchor="center",
               width=350, height=400)

    tk.Label(
        card, text="ADMIN LOGIN",
        font=("Segoe UI", 10, "bold"),
        bg=CARD, fg=PRIMARY
    ).pack(pady=(25, 5))

    tk.Label(
        card, text="Welcome Back",
        font=("Segoe UI", 22, "bold"),
        bg=CARD, fg=DARK
    ).pack()

    tk.Label(
        card, text="Sign in to manage scholarship applications",
        font=("Segoe UI", 9), bg=CARD, fg=MUTED,
        wraplength=280
    ).pack(pady=(5, 22))

    tk.Label(
        card, text="Username",
        font=("Segoe UI", 10, "bold"),
        bg=CARD, fg=TEXT
    ).pack(anchor="w", padx=30)

    username_entry = tk.Entry(
        card, font=("Segoe UI", 11), bg="#FAF9FD",
        fg=TEXT, relief="flat", highlightthickness=1,
        highlightbackground=BORDER, highlightcolor=PRIMARY
    )
    username_entry.pack(fill="x", padx=30, ipady=8, pady=(5, 14))

    tk.Label(
        card, text="Password",
        font=("Segoe UI", 10, "bold"),
        bg=CARD, fg=TEXT
    ).pack(anchor="w", padx=30)

    password_entry = tk.Entry(
        card, font=("Segoe UI", 11), bg="#FAF9FD",
        fg=TEXT, show="*", relief="flat",
        highlightthickness=1, highlightbackground=BORDER,
        highlightcolor=PRIMARY
    )
    password_entry.pack(fill="x", padx=30, ipady=8, pady=(5, 7))

    show_password = tk.BooleanVar(value=False)

    def toggle_password():
        password_entry.configure(
            show="" if show_password.get() else "*"
        )

    tk.Checkbutton(
        card, text="Show password",
        variable=show_password, command=toggle_password,
        font=("Segoe UI", 9), bg=CARD, fg=MUTED,
        activebackground=CARD, selectcolor=CARD,
        cursor="hand2"
    ).pack(anchor="w", padx=27, pady=(0, 12))

    def login():
        if (username_entry.get().strip() == "admin"
                and password_entry.get() == "admin123"):
            login_window.grab_release()
            login_window.destroy()
            admin_dashboard()
        else:
            messagebox.showerror(
                "Login Failed",
                "Incorrect username or password.",
                parent=login_window
            )
            password_entry.delete(0, tk.END)
            password_entry.focus_set()

    tk.Button(
        card, text="LOGIN", command=login,
        font=("Segoe UI", 11, "bold"),
        bg=PRIMARY, fg="white",
        activebackground=PRIMARY_HOVER,
        activeforeground="white",
        relief="flat", bd=0, cursor="hand2"
    ).pack(fill="x", padx=30, ipady=9)

    username_entry.focus_set()
    login_window.bind("<Return>", lambda event: login())


def check_eligibility(student):
    reasons = []

    try:
        age = int(student.get("age", 0))
        marks = float(student.get("marks", 0))
        income = float(student.get("income", 0))
    except (ValueError, TypeError):
        return False, ["Student details contain invalid numeric values."]

    if age < 18:
        reasons.append("Age must be at least 18 years.")

    if marks < 60:
        reasons.append("Marks must be at least 60%.")

    if income > 250000:
        reasons.append("Annual family income must not exceed ₹2,50,000.")

    return len(reasons) == 0, reasons



def admin_dashboard():
    dashboard = tk.Toplevel(root)
    dashboard.title("Student Scholarship Management - Admin")
    dashboard.geometry("1100x740")
    dashboard.minsize(950, 650)
    dashboard.configure(bg=BG)

    GREEN = "#2E8B57"
    GREEN_HOVER = "#246E45"
    RED = "#C74450"
    RED_HOVER = "#A93440"
    BLUE = "#3978C5"
    BLUE_HOVER = "#285FA0"
    BLACK = "#292638"
    BLACK_HOVER = "#171521"

    # ---------- Styles ----------

    style = ttk.Style(dashboard)
    style.configure(
        "Admin.Treeview",
        background=CARD,
        foreground=TEXT,
        fieldbackground=CARD,
        rowheight=28,
        font=("Segoe UI", 9)
    )
    style.configure(
        "Admin.Treeview.Heading",
        background="#EAE6F5",
        foreground=DARK,
        font=("Segoe UI", 9, "bold"),
        padding=6
    )
    style.map(
        "Admin.Treeview",
        background=[("selected", "#DCD4F1")],
        foreground=[("selected", DARK)]
    )

    def make_button(parent, text, command, color, hover):
        return tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 9, "bold"),
            bg=color,
            fg="white",
            activebackground=hover,
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=10,
            pady=8
        )

    def get_apps(student):
        apps = student.get("applications", [])

        if not isinstance(apps, list):
            apps = []

        # Support records 
        if not apps and student.get("applied_scholarship"):
            apps = [{
                "scholarship": student["applied_scholarship"],
                "status": student.get("status", "Pending")
            }]
            student["applications"] = apps

        return apps

    def app_status(app):
        return str(app.get("status", "Pending")).title()

    def save_records(students):
        try:
            save_students(students)
            return True
        except (OSError, TypeError) as error:
            messagebox.showerror(
                "Save Error",
                f"Could not save changes:\n{error}",
                parent=dashboard
            )
            return False

    # Header 

    header = tk.Frame(dashboard, bg=DARK, height=72)
    header.pack(side="top", fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="Admin Dashboard",
        font=("Segoe UI", 19, "bold"),
        bg=DARK,
        fg="white"
    ).pack(side="left", padx=22, pady=15)

    tk.Label(
        header,
        text="STUDENT SCHOLARSHIP MANAGEMENT SYSTEM",
        font=("Segoe UI", 9),
        bg=DARK,
        fg="#D8D2EB"
    ).pack(side="left", padx=5, pady=20)

    tk.Label(
        header,
        text="ADMIN",
        font=("Segoe UI", 10, "bold"),
        bg="#49415F",
        fg="white",
        padx=14,
        pady=6
    ).pack(side="right", padx=20)


    action_bar = tk.Frame(
        dashboard,
        bg="#FFFFFF",
        highlightbackground=BORDER,
        highlightthickness=1
    )
    action_bar.pack(side="bottom", fill="x")

    # ---------- Main Content ----------

    content = tk.Frame(dashboard, bg=BG)
    content.pack(side="top", fill="both", expand=True, padx=16, pady=10)

    # Statistics 

    stats_frame = tk.Frame(content, bg=BG)
    stats_frame.pack(fill="x", pady=(0, 9))

    stat_labels = {}

    stats = [
        ("Students", "students", BLUE),
        ("Applications", "applications", PRIMARY),
        ("Pending", "pending", "#B78335"),
        ("Approved", "approved", GREEN),
        ("Rejected", "rejected", RED)
    ]

    for title, key, accent in stats:
        box = tk.Frame(
            stats_frame,
            bg=CARD,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        box.pack(side="left", fill="x", expand=True, padx=(0, 6))

        tk.Frame(box, bg=accent, height=3).pack(fill="x")

        tk.Label(
            box,
            text=title,
            font=("Segoe UI", 9),
            bg=CARD,
            fg=MUTED
        ).pack(anchor="w", padx=9, pady=(5, 0))

        stat_labels[key] = tk.Label(
            box,
            text="0",
            font=("Segoe UI", 17, "bold"),
            bg=CARD,
            fg=DARK
        )
        stat_labels[key].pack(anchor="w", padx=9, pady=(0, 5))

    # Search and Eligibility Panel

    search_card = tk.Frame(
        content,
        bg=CARD,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    search_card.pack(fill="x", pady=(0, 9))

    tk.Label(
        search_card,
        text="Search Student & Check Eligibility",
        font=("Segoe UI", 11, "bold"),
        bg=CARD,
        fg=DARK
    ).pack(anchor="w", padx=11, pady=(7, 5))

    search_row = tk.Frame(search_card, bg=CARD)
    search_row.pack(fill="x", padx=11, pady=(0, 8))

    search_entry = tk.Entry(
        search_row,
        font=("Segoe UI", 10),
        bg="#FAF9FD",
        fg=TEXT,
        relief="flat",
        highlightthickness=1,
        highlightbackground=BORDER,
        highlightcolor=PRIMARY
    )
    search_entry.pack(
        side="left", fill="x", expand=True, ipady=7
    )

    # Eligibility panel 
    eligibility_panel = tk.Frame(
        search_card,
        bg="#F0EDF8",
        highlightbackground=BORDER,
        highlightthickness=1
    )
    eligibility_panel.pack(fill="x", padx=11, pady=(0, 9))

    eligibility_title = tk.Label(
        eligibility_panel,
        text="ELIGIBILITY RESULT",
        font=("Segoe UI", 9, "bold"),
        bg="#F0EDF8",
        fg=DARK
    )
    eligibility_title.pack(anchor="w", padx=9, pady=(5, 1))

    eligibility_text = tk.Label(
        eligibility_panel,
        text="Enter a student name or username, then check eligibility.",
        font=("Segoe UI", 9),
        bg="#F0EDF8",
        fg=MUTED,
        justify="left",
        anchor="w",
        wraplength=1000
    )
    eligibility_text.pack(fill="x", padx=9, pady=(0, 6))

    # Application Table 

    table_card = tk.Frame(
        content,
        bg=CARD,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    table_card.pack(fill="both", expand=True)

    table_heading = tk.Frame(table_card, bg=CARD)
    table_heading.pack(fill="x", padx=10, pady=(6, 4))

    tk.Label(
        table_heading,
        text="Scholarship Applications",
        font=("Segoe UI", 11, "bold"),
        bg=CARD,
        fg=DARK
    ).pack(side="left")

    result_count = tk.Label(
        table_heading,
        text="0 records",
        font=("Segoe UI", 9),
        bg=CARD,
        fg=MUTED
    )
    result_count.pack(side="right")

    tree_frame = tk.Frame(table_card, bg=CARD)
    tree_frame.pack(fill="both", expand=True, padx=9, pady=(0, 8))

    columns = (
        "name", "username", "scholarship",
        "age", "marks", "income", "status"
    )

    tree = ttk.Treeview(
        tree_frame,
        columns=columns,
        show="headings",
        style="Admin.Treeview",
        selectmode="browse"
    )

    column_info = [
        ("name", "Applicant Name", 140),
        ("username", "Username", 100),
        ("scholarship", "Scholarship", 180),
        ("age", "Age", 45),
        ("marks", "Marks (%)", 70),
        ("income", "Annual Income (₹)", 125),
        ("status", "Status", 85)
    ]

    for col, title, width in column_info:
        tree.heading(col, text=title)
        tree.column(col, width=width, minwidth=40, anchor="center")

    tree.tag_configure("Pending", foreground="#9A6B1F")
    tree.tag_configure("Approved", foreground=GREEN)
    tree.tag_configure("Rejected", foreground=RED)
    tree.tag_configure("NoApplication", foreground=MUTED)

    scrollbar = ttk.Scrollbar(
        tree_frame,
        orient="vertical",
        command=tree.yview
    )
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    current_rows = []

    # Eligibility Display 

    def display_eligibility(student, app=None):
        eligible, reasons = check_eligibility(student)

        scholarship = (
            app.get("scholarship", "Unnamed Scholarship")
            if app else "No application"
        )

        if eligible:
            result = "ELIGIBLE"
            explanation = "Meets all eligibility criteria."
            panel_color = "#E2F3E8"
            text_color = "#216B42"
        else:
            result = "NOT ELIGIBLE"
            explanation = " ".join(reasons)
            panel_color = "#FBE5E7"
            text_color = "#A62F3B"

        status = app_status(app) if app else "No application"

        eligibility_panel.configure(bg=panel_color)
        eligibility_title.configure(
            text=f"ELIGIBILITY RESULT: {result}",
            bg=panel_color,
            fg=text_color
        )
        eligibility_text.configure(
            text=(
                f"Name: {student.get('name', 'N/A')}  |  "
                f"Username: {student.get('username', 'N/A')}  |  "
                f"Scholarship: {scholarship}\n"
                f"Age: {student.get('age', 'N/A')}  |  "
                f"Marks: {student.get('marks', 'N/A')}%  |  "
                f"Income: ₹{student.get('income', 'N/A')}\n"
                f"{explanation}  |  Status: {status}"
            ),
            bg=panel_color,
            fg=text_color
        )

        return eligible

    def clear_eligibility():
        eligibility_panel.configure(bg="#F0EDF8")
        eligibility_title.configure(
            text="ELIGIBILITY RESULT",
            bg="#F0EDF8",
            fg=DARK
        )
        eligibility_text.configure(
            text="Enter a student name or username, then check eligibility.",
            bg="#F0EDF8",
            fg=MUTED
        )

    # Refresh Table 

    def refresh_table():
        current_rows.clear()
        students = load_students()

        query = search_entry.get().strip().casefold()
        all_applications = []

        for student in students:
            all_applications.extend(get_apps(student))

        stat_labels["students"].configure(text=str(len(students)))
        stat_labels["applications"].configure(
            text=str(len(all_applications))
        )

        statuses = [app_status(app) for app in all_applications]

        stat_labels["pending"].configure(
            text=str(statuses.count("Pending"))
        )
        stat_labels["approved"].configure(
            text=str(statuses.count("Approved"))
        )
        stat_labels["rejected"].configure(
            text=str(statuses.count("Rejected"))
        )

        tree.delete(*tree.get_children())

        for student in students:
            name = str(student.get("name", ""))
            username = str(student.get("username", ""))

            if query and query not in name.casefold() and query not in username.casefold():
                continue

            apps = get_apps(student)

            if not apps:
                row = {
                    "student": student,
                    "application": None,
                    "scholarship": "No application"
                }
                current_rows.append(row)
                row_id = str(len(current_rows) - 1)

                tree.insert(
                    "", "end", iid=row_id,
                    values=(
                        name, username, "No application",
                        student.get("age", ""),
                        student.get("marks", ""),
                        student.get("income", ""),
                        student.get("status", "Pending")
                    ),
                    tags=("NoApplication",)
                )
                continue

            for app in apps:
                status = app_status(app)
                row = {
                    "student": student,
                    "application": app,
                    "scholarship": app.get(
                        "scholarship", "Unnamed Scholarship"
                    )
                }
                current_rows.append(row)
                row_id = str(len(current_rows) - 1)

                tree.insert(
                    "", "end", iid=row_id,
                    values=(
                        name, username, row["scholarship"],
                        student.get("age", ""),
                        student.get("marks", ""),
                        student.get("income", ""),
                        status
                    ),
                    tags=(status,)
                )

        result_count.configure(
            text=f"{len(tree.get_children())} record(s)"
        )
        clear_eligibility()

    def selected_row():
        selection = tree.selection()

        if not selection:
            messagebox.showwarning(
                "No Selection",
                "Select an application from the table first.",
                parent=dashboard
            )
            return None

        try:
            return current_rows[int(selection[0])]
        except (ValueError, IndexError):
            return None

    # Save a Status Change 

    def update_application(row, new_status, confirm=True):
        if row is None or row["application"] is None:
            messagebox.showwarning(
                "No Application",
                "Select a student who has a scholarship application.",
                parent=dashboard
            )
            return False

        student = row["student"]
        scholarship = row["scholarship"]

        if new_status == "Approved":
            eligible, reasons = check_eligibility(student)
            if not eligible:
                display_eligibility(student, row["application"])
                messagebox.showwarning(
                    "Cannot Accept Application",
                    "This student does not meet the eligibility criteria:\n\n"
                    + "\n".join(reasons),
                    parent=dashboard
                )
                return False

        if confirm and not messagebox.askyesno(
            f"{new_status} Application",
            f"{new_status} this application?\n\n"
            f"Student: {student.get('name', '')}\n"
            f"Scholarship: {scholarship}",
            parent=dashboard
        ):
            return False

        students = load_students()
        saved_student = next(
            (
                item for item in students
                if item.get("username") == student.get("username")
            ),
            None
        )

        if saved_student is None:
            messagebox.showerror(
                "Not Found", "Student record was not found.",
                parent=dashboard
            )
            return False

        saved_app = next(
            (
                app for app in get_apps(saved_student)
                if app.get("scholarship") == scholarship
            ),
            None
        )

        if saved_app is None:
            messagebox.showerror(
                "Not Found", "Application was not found.",
                parent=dashboard
            )
            return False

        saved_app["status"] = new_status

        if save_records(students):
            refresh_table()
            return True

        return False

    # Check Eligibility

    def check_student(student):
        apps = get_apps(student)

        if not apps:
            display_eligibility(student, None)
            messagebox.showinfo(
                "No Application",
                "This student has not applied for a scholarship.",
                parent=dashboard
            )
            return

        # Check the first application for this student.
        app = apps[0]
        eligible = check_eligibility(student)[0]
        new_status = "Approved" if eligible else "Rejected"

        students = load_students()
        saved_student = next(
            (
                item for item in students
                if item.get("username") == student.get("username")
            ),
            None
        )

        if saved_student:
            saved_app = next(
                (
                    item for item in get_apps(saved_student)
                    if item.get("scholarship") == app.get("scholarship")
                ),
                None
            )

            if saved_app:
                saved_app["status"] = new_status

                if save_records(students):
                    refresh_table()

                    # Show the updated result after refreshing.
                    updated_student = next(
                        (
                            item for item in load_students()
                            if item.get("username") == student.get("username")
                        ),
                        student
                    )
                    updated_app = next(
                        (
                            item for item in get_apps(updated_student)
                            if item.get("scholarship") == app.get("scholarship")
                        ),
                        None
                    )
                    display_eligibility(updated_student, updated_app)

                    messagebox.showinfo(
                        "Eligibility Checked",
                        f"{updated_student.get('name', 'Student')}: "
                        f"{new_status}\n\n"
                        "The application status has been updated.",
                        parent=dashboard
                    )

    def check_search_result():
        query = search_entry.get().strip().casefold()

        if not query:
            row = selected_row()
            if row:
                check_student(row["student"])
            return

        students = load_students()

        matches = [
            student for student in students
            if query in str(student.get("name", "")).casefold()
            or query in str(student.get("username", "")).casefold()
        ]

        if not matches:
            messagebox.showinfo(
                "No Results",
                "No student matched that name or username.",
                parent=dashboard
            )
            clear_eligibility()
            return

        exact_username = [
            student for student in matches
            if str(student.get("username", "")).casefold() == query
        ]

        if exact_username:
            check_student(exact_username[0])
        elif len(matches) == 1:
            check_student(matches[0])
        else:
            chooser = tk.Toplevel(dashboard)
            chooser.title("Choose Applicant")
            chooser.geometry("420x300")
            chooser.configure(bg=BG)
            chooser.transient(dashboard)
            chooser.grab_set()

            tk.Label(
                chooser,
                text="Multiple students found",
                font=("Segoe UI", 14, "bold"),
                bg=BG,
                fg=DARK
            ).pack(anchor="w", padx=14, pady=(14, 5))

            tk.Label(
                chooser,
                text="Choose the correct username.",
                font=("Segoe UI", 9),
                bg=BG,
                fg=MUTED
            ).pack(anchor="w", padx=14, pady=(0, 8))

            listbox = tk.Listbox(
                chooser,
                font=("Segoe UI", 10),
                bg=CARD,
                fg=TEXT,
                relief="flat",
                selectbackground=PRIMARY,
                selectforeground="white"
            )
            listbox.pack(fill="both", expand=True, padx=14, pady=(0, 8))

            for student in matches:
                listbox.insert(
                    tk.END,
                    f"{student.get('name', '')} (@{student.get('username', '')})"
                )

            def choose_student():
                selection = listbox.curselection()
                if not selection:
                    messagebox.showwarning(
                        "Select Student",
                        "Choose a student from the list.",
                        parent=chooser
                    )
                    return

                chosen = matches[selection[0]]
                chooser.destroy()
                check_student(chosen)

            make_button(
                chooser,
                "Check Selected Student",
                choose_student,
                BLUE,
                BLUE_HOVER
            ).pack(pady=(0, 12))

            listbox.bind(
                "<Double-1>",
                lambda event: choose_student()
            )

    def check_selected_eligibility():
        row = selected_row()
        if row:
            check_student(row["student"])

    def delete_application(row=None):
        if row is None:
            row = selected_row()

        if row is None or row["application"] is None:
            messagebox.showwarning(
                "No Application",
                "Select a scholarship application to delete.",
                parent=dashboard
            )
            return False

        student = row["student"]
        scholarship = row["scholarship"]

        if not messagebox.askyesno(
            "Delete Application",
            f"Delete this application permanently?\n\n"
            f"Student: {student.get('name', '')}\n"
            f"Scholarship: {scholarship}",
            parent=dashboard
        ):
            return False

        students = load_students()
        saved_student = next(
            (
                item for item in students
                if item.get("username") == student.get("username")
            ),
            None
        )

        if not saved_student:
            messagebox.showerror(
                "Not Found", "Student record was not found.",
                parent=dashboard
            )
            return False

        saved_student["applications"] = [
            app for app in get_apps(saved_student)
            if app.get("scholarship") != scholarship
        ]

        if save_records(students):
            refresh_table()
            return True

        return False

    # Applicant Popup 

    def view_applicants():
        popup = tk.Toplevel(dashboard)
        popup.title("Applicant Management")
        popup.geometry("850x510")
        popup.minsize(700, 430)
        popup.configure(bg=BG)
        popup.transient(dashboard)

        tk.Label(
            popup,
            text="Applicant Management",
            font=("Segoe UI", 18, "bold"),
            bg=BG,
            fg=DARK
        ).pack(anchor="w", padx=16, pady=(13, 3))

        tk.Label(
            popup,
            text="Select an application, then use the action buttons below.",
            font=("Segoe UI", 9),
            bg=BG,
            fg=MUTED
        ).pack(anchor="w", padx=16, pady=(0, 9))

        popup_frame = tk.Frame(popup, bg=BG)
        popup_frame.pack(fill="both", expand=True, padx=16)

        popup_tree = ttk.Treeview(
            popup_frame,
            columns=("name", "username", "scholarship", "status"),
            show="headings",
            style="Admin.Treeview",
            selectmode="browse"
        )

        for col, title, width in [
            ("name", "Applicant Name", 175),
            ("username", "Username", 130),
            ("scholarship", "Scholarship", 260),
            ("status", "Status", 100)
        ]:
            popup_tree.heading(col, text=title)
            popup_tree.column(col, width=width, anchor="center")

        popup_tree.tag_configure("Pending", foreground="#9A6B1F")
        popup_tree.tag_configure("Approved", foreground=GREEN)
        popup_tree.tag_configure("Rejected", foreground=RED)

        popup_scroll = ttk.Scrollbar(
            popup_frame,
            orient="vertical",
            command=popup_tree.yview
        )
        popup_tree.configure(yscrollcommand=popup_scroll.set)
        popup_tree.pack(side="left", fill="both", expand=True)
        popup_scroll.pack(side="right", fill="y")

        popup_rows = []

        def refresh_popup():
            popup_rows.clear()
            popup_tree.delete(*popup_tree.get_children())

            for student in load_students():
                for app in get_apps(student):
                    row = {
                        "student": student,
                        "application": app,
                        "scholarship": app.get(
                            "scholarship", "Unnamed Scholarship"
                        )
                    }
                    popup_rows.append(row)

                    popup_tree.insert(
                        "",
                        "end",
                        iid=str(len(popup_rows) - 1),
                        values=(
                            student.get("name", ""),
                            student.get("username", ""),
                            row["scholarship"],
                            app_status(app)
                        ),
                        tags=(app_status(app),)
                    )

        def popup_selected():
            selection = popup_tree.selection()

            if not selection:
                messagebox.showwarning(
                    "No Selection",
                    "Select an applicant from the popup list.",
                    parent=popup
                )
                return None

            try:
                return popup_rows[int(selection[0])]
            except (ValueError, IndexError):
                return None

        def popup_check():
            row = popup_selected()
            if row is None:
                return

            # Show the result and update the application.
            student = row["student"]
            app = row["application"]
            eligible, reasons = check_eligibility(student)
            new_status = "Approved" if eligible else "Rejected"

            students = load_students()
            saved_student = next(
                (
                    item for item in students
                    if item.get("username") == student.get("username")
                ),
                None
            )

            if saved_student:
                saved_app = next(
                    (
                        item for item in get_apps(saved_student)
                        if item.get("scholarship") == row["scholarship"]
                    ),
                    None
                )

                if saved_app:
                    saved_app["status"] = new_status

                    if save_records(students):
                        refresh_table()
                        refresh_popup()

                        if eligible:
                            result_message = (
                                "Eligible. Application automatically approved."
                            )
                        else:
                            result_message = (
                                "Not eligible. Application automatically rejected.\n\n"
                                + "\n".join(reasons)
                            )

                        messagebox.showinfo(
                            "Eligibility Result",
                            f"Student: {student.get('name', '')}\n"
                            f"Scholarship: {row['scholarship']}\n\n"
                            f"{result_message}",
                            parent=popup
                        )

        def popup_accept():
            row = popup_selected()
            if row and update_application("Approved", row):
                refresh_popup()

        def popup_reject():
            row = popup_selected()
            if row and update_application("Rejected", row):
                refresh_popup()

        def popup_delete():
            row = popup_selected()
            if row and delete_application(row):
                refresh_popup()

        popup_actions = tk.Frame(
            popup,
            bg="#FFFFFF",
            highlightbackground=BORDER,
            highlightthickness=1
        )
        popup_actions.pack(side="bottom", fill="x", pady=(10, 0))

        make_button(
            popup_actions,
            "Check Eligibility",
            popup_check,
            BLUE,
            BLUE_HOVER
        ).pack(side="left", padx=(10, 5), pady=10)

        make_button(
            popup_actions,
            "Accept Application",
            popup_accept,
            GREEN,
            GREEN_HOVER
        ).pack(side="left", padx=5, pady=10)

        make_button(
            popup_actions,
            "Reject Application",
            popup_reject,
            RED,
            RED_HOVER
        ).pack(side="left", padx=5, pady=10)

        make_button(
            popup_actions,
            "Delete Application",
            popup_delete,
            RED,
            RED_HOVER
        ).pack(side="left", padx=5, pady=10)

        make_button(
            popup_actions,
            "Close",
            popup.destroy,
            BLACK,
            BLACK_HOVER
        ).pack(side="right", padx=10, pady=10)

        popup_tree.bind("<Double-1>", lambda event: popup_check())
        refresh_popup()

    # View All Students 

    def view_all_students():
        popup = tk.Toplevel(dashboard)
        popup.title("Registered Students")
        popup.geometry("760x430")
        popup.configure(bg=BG)

        tk.Label(
            popup,
            text="Registered Students",
            font=("Segoe UI", 16, "bold"),
            bg=BG,
            fg=DARK
        ).pack(anchor="w", padx=15, pady=12)

        frame = tk.Frame(popup, bg=BG)
        frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        cols = ("name", "username", "age", "marks", "income")

        student_tree = ttk.Treeview(
            frame,
            columns=cols,
            show="headings",
            style="Admin.Treeview"
        )

        for col, title, width in [
            ("name", "Name", 160),
            ("username", "Username", 130),
            ("age", "Age", 70),
            ("marks", "Marks (%)", 100),
            ("income", "Annual Income (₹)", 170)
        ]:
            student_tree.heading(col, text=title)
            student_tree.column(col, width=width, anchor="center")

        student_scroll = ttk.Scrollbar(
            frame, orient="vertical", command=student_tree.yview
        )
        student_tree.configure(yscrollcommand=student_scroll.set)
        student_tree.pack(side="left", fill="both", expand=True)
        student_scroll.pack(side="right", fill="y")

        for student in load_students():
            student_tree.insert(
                "",
                "end",
                values=(
                    student.get("name", ""),
                    student.get("username", ""),
                    student.get("age", ""),
                    student.get("marks", ""),
                    student.get("income", "")
                )
            )

    # Search Buttons 

    make_button(
        search_row,
        "Check Eligibility",
        check_search_result,
        BLUE,
        BLUE_HOVER
    ).pack(side="left", padx=(7, 0))

    make_button(
        search_row,
        "Search",
        refresh_table,
        PRIMARY,
        PRIMARY_HOVER
    ).pack(side="left", padx=(6, 0))

    search_entry.bind(
        "<Return>",
        lambda event: check_search_result()
    )

    tree.bind(
        "<Double-1>",
        lambda event: check_selected_eligibility()
    )

    make_button(
        action_bar,
        "Add / Register Student",
        student_registration,
        GREEN,
        GREEN_HOVER
    ).pack(side="left", padx=(10, 5), pady=10)

    make_button(
        action_bar,
        "View Applicants",
        view_applicants,
        BLUE,
        BLUE_HOVER
    ).pack(side="left", padx=5, pady=10)

    make_button(
        action_bar,
        "View All Students",
        view_all_students,
        BLUE,
        BLUE_HOVER
    ).pack(side="left", padx=5, pady=10)

    make_button(
        action_bar,
        "Refresh",
        refresh_table,
        PRIMARY,
        PRIMARY_HOVER
    ).pack(side="left", padx=5, pady=10)

    make_button(
        action_bar,
        "Exit Admin Panel",
        dashboard.destroy,
        BLACK,
        BLACK_HOVER
    ).pack(side="right", padx=10, pady=10)

    refresh_table()

# HOME WINDOW

# Main layout
sidebar = tk.Frame(root, bg="#24213D", width=245, height=560)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

content = tk.Frame(root, bg="#F4F3FA")
content.pack(side="right", fill="both", expand=True)

tk.Label(
    sidebar,
    text="✦",
    font=("Arial", 38, "bold"),
    bg="#24213D",
    fg="#C4B5FD"
).pack(pady=(32, 3))

tk.Label(
    sidebar,
    text="SCHOLARSHIP",
    font=("Arial", 17, "bold"),
    bg="#24213D",
    fg="white"
).pack()

tk.Label(
    sidebar,
    text="MANAGEMENT SYSTEM",
    font=("Arial", 9, "bold"),
    bg="#24213D",
    fg="#C4B5FD"
).pack(pady=(3, 25))

tk.Frame(
    sidebar,
    bg="#484365",
    height=2
).pack(fill="x", padx=25, pady=5)

tk.Label(
    sidebar,
    text="YOUR FUTURE,\nYOUR OPPORTUNITY.",
    font=("Arial", 15, "bold"),
    bg="#24213D",
    fg="white",
    justify="left"
).pack(anchor="w", padx=25, pady=(28, 10))

tk.Label(
    sidebar,
    text="Discover opportunities.\nApply for scholarships.\nTrack your progress.",
    font=("Arial", 10),
    bg="#24213D",
    fg="#C7C4D9",
    justify="left"
).pack(anchor="w", padx=25)

# Sidebar information
tk.Label(
    sidebar,
    text="STUDENT PORTAL  •  ADMIN PORTAL",
    font=("Arial", 8, "bold"),
    bg="#24213D",
    fg="#A8A3C7",
    wraplength=195,
    justify="left"
).pack(side="bottom", anchor="w", padx=20, pady=20)

# MAIN CONTENT HEADER

tk.Label(
    content,
    text="STUDENT SCHOLARSHIP PORTAL",
    font=("Arial", 9, "bold"),
    bg="#F4F3FA",
    fg="#7667A8"
).pack(anchor="w", padx=35, pady=(25, 5))

tk.Label(
    content,
    text="Welcome!",
    font=("Arial", 28, "bold"),
    bg="#F4F3FA",
    fg="#24213D"
).pack(anchor="w", padx=35)

tk.Label(
    content,
    text="Your next opportunity starts here.",
    font=("Arial", 11),
    bg="#F4F3FA",
    fg="#77748B"
).pack(anchor="w", padx=37, pady=(3, 15))

# WELCOME CARD

welcome_card = tk.Frame(
    content,
    bg="#FFFFFF",
    highlightbackground="#E2DEEF",
    highlightthickness=1
)
welcome_card.pack(fill="x", padx=32, pady=(0, 16))

tk.Label(
    welcome_card,
    text="ONE STEP CLOSER TO YOUR GOALS",
    font=("Arial", 9, "bold"),
    bg="#FFFFFF",
    fg="#6D5AA8"
).pack(anchor="w", padx=18, pady=(14, 4))

tk.Label(
    welcome_card,
    text="Register. Apply. Track.",
    font=("Arial", 17, "bold"),
    bg="#FFFFFF",
    fg="#24213D"
).pack(anchor="w", padx=18)

tk.Label(
    welcome_card,
    text="Create an account, explore scholarships, and track\n"
         "your application status from one place.",
    font=("Arial", 10),
    bg="#FFFFFF",
    fg="#77748B",
    justify="left"
).pack(anchor="w", padx=18, pady=(4, 14))

# ACTION BUTTONS

tk.Label(
    content,
    text="GET STARTED",
    font=("Arial", 10, "bold"),
    bg="#F4F3FA",
    fg="#4D4965"
).pack(anchor="w", padx=35, pady=(0, 6))


def make_action_button(parent, text, command, color, hover_color):
    button = tk.Button(
        parent,
        text=text,
        command=command,
        font=("Arial", 10, "bold"),
        bg=color,
        fg="white",
        activebackground=hover_color,
        activeforeground="white",
        relief="flat",
        bd=0,
        cursor="hand2",
        height=2,
        anchor="w",
        padx=16
    )

    button.pack(fill="x", padx=32, pady=4)

    # Hover effect
    button.bind(
        "<Enter>",
        lambda event: button.config(bg=hover_color)
    )
    button.bind(
        "<Leave>",
        lambda event: button.config(bg=color)
    )

    return button


# registration / add
make_action_button(
    content,
    "✚   Student Registration",
    student_registration,
    "#477B72",
    "#35665E"
)

# student login
make_action_button(
    content,
    "↗   Student Login",
    student_login,
    "#6D5AA8",
    "#58478F"
)

# admin login
make_action_button(
    content,
    "⚙   Admin Login",
    admin_login,
    "#4267A9",
    "#31518B"
)

# FOOTER

tk.Label(
    content,
    text="STUDENT SCHOLARSHIP MANAGEMENT SYSTEM  |  VERSION 1.0",
    font=("Arial", 8),
    bg="#F4F3FA",
    fg="#9995AD"
).pack(side="bottom", pady=10)

# RUN APPLICATION

root.mainloop()
