from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
import csv

# ================= STYLES =================
PRIMARY = "#1f4e79"
SECONDARY = "#3a6ea5"
DANGER = "#a83232"
GRAY = "#6c757d"

FONT_LABEL = ("Segoe UI", 10)
FONT_ENTRY = ("Segoe UI", 10)
FONT_TITLE = ("Segoe UI", 12, "bold")
FONT_HEADER = ("Segoe UI", 20, "bold")
FONT_SUB = ("Segoe UI", 18, "bold")


class EmployeeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NanoPulse Database Engine")
        self.root.geometry("1550x850")
        self.root.configure(bg="white")
        self.root.resizable(False, False)

        # Login vars
        self.username = StringVar()
        self.password = StringVar()

        # Employee vars
        self.var_name = StringVar()
        self.var_designation = StringVar()
        self.var_dep = StringVar()
        self.var_email = StringVar()
        self.var_address = StringVar()
        self.var_married = StringVar()
        self.var_dob = StringVar()
        self.var_idproof = StringVar()
        self.var_idnum = StringVar()
        self.var_gender = StringVar()
        self.var_country = StringVar()
        self.var_doj = StringVar()
        self.var_salary = StringVar()
        self.var_phone = StringVar()
        self.var_search_by = StringVar()
        self.var_search_txt = StringVar()

        self.show_login()

    def search_data(self):
        if self.var_search_by.get() == "" or self.var_search_txt.get() == "":
            messagebox.showerror("Error", "Please select search option and enter value")
            return

        try:
            conn = self.connect()
            cur = conn.cursor()

            query = f"""
                   SELECT * FROM employee3
                   WHERE {self.var_search_by.get()} LIKE %s
                   """
            value = (f"%{self.var_search_txt.get()}%",)

            cur.execute(query, value)
            rows = cur.fetchall()

            self.table.delete(*self.table.get_children())

            if rows:
                for row in rows:
                    self.table.insert("", END, values=row)
            else:
                messagebox.showinfo("No Result", "No matching record found")

            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred:\n{str(e)}")


    # ================= PLACEHOLDER =================
    def add_placeholder(self, entry, text, is_password=False):
        entry.insert(0, text)
        entry.config(fg="gray", show="" if is_password else None)

        def focus_in(e):
            if entry.get() == text:
                entry.delete(0, END)
                entry.config(fg="black")
                if is_password:
                    entry.config(show="*")

        def focus_out(e):
            if not entry.get():
                entry.insert(0, text)
                entry.config(fg="gray")
                if is_password:
                    entry.config(show="")

        entry.bind("<FocusIn>", focus_in)
        entry.bind("<FocusOut>", focus_out)

    # ================= LOGIN =================
    def show_login(self):
        self.login_frame = Frame(self.root, bg="white")
        self.login_frame.place(relwidth=1, relheight=1)

        Label(self.login_frame, text="NanoPulse Login",
              font=FONT_HEADER, bg="white").pack(pady=40)

        user = Entry(self.login_frame, textvariable=self.username,
                     font=FONT_ENTRY, width=35)
        user.pack(pady=10)
        self.add_placeholder(user, "Enter your username")

        pwd = Entry(self.login_frame, textvariable=self.password,
                    font=FONT_ENTRY, width=35)
        pwd.pack(pady=10)
        self.add_placeholder(pwd, "Enter your password", True)

        Button(self.login_frame, text="Login",
               bg=PRIMARY, fg="white",
               width=18, font=FONT_TITLE,
               command=self.login).pack(pady=20)

    def login(self):
        if self.username.get() == "admin" and self.password.get() == "admin":
            self.login_frame.destroy()
            self.build_main_ui()
        else:
            messagebox.showerror("Error", "Invalid Credentials")

    # ================= MAIN UI =================
    def build_main_ui(self):

        # ===== HEADER (PERFECT CENTER ALIGNMENT) =====
        header = Frame(self.root, bg="white", height=120)
        header.pack(fill=X)

        header_center = Frame(header, bg="white")
        header_center.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Logo icon
        icon = Image.open("assets/nanopulse_icon.png").resize((210, 150))
        self.icon_img = ImageTk.PhotoImage(icon)
        Label(header_center, image=self.icon_img,
              bg="white").grid(row=0, column=0, rowspan=2, padx=(0, 20))

        # Company name
        name_img = Image.open("assets/nanopulse_name.png").resize((455, 385))
        self.name_img = ImageTk.PhotoImage(name_img)
        Label(header_center, image=self.name_img,
              bg="white").grid(row=0, column=1, sticky=W)


        # Divider
        Label(header_center, text="│",
              font=("Segoe UI", 44),
              fg="#c0c0c0", bg="white").grid(row=0, column=2, rowspan=2, padx=25)

        # Engine title
        Label(header_center, text="DATA MANAGEMENT\nENGINE",
              font=("Segoe UI", 28, "bold"), fg="#0c2b4d",
              bg="white", justify=LEFT).grid(row=0, column=3, rowspan=2)

        # ===== EMPLOYEE FORM =====
        upper = LabelFrame(self.root, text="EMPLOYEE INFORMATION",
                           font=FONT_TITLE, bg="white")
        upper.place(x=20, y=130, width=1500, height=260)

        self.make_field(upper, "Name", self.var_name, 0, 0)
        self.make_field(upper, "Designation", self.var_designation, 1, 0)
        self.make_field(upper, "Department", self.var_dep, 2, 0)
        self.make_field(upper, "Email", self.var_email, 3, 0)
        self.make_field(upper, "Address", self.var_address, 4, 0, 40)

        self.make_combo(upper, "Marriage Status", self.var_married,
                        ("Select", "Married", "Unmarried"), 0, 2)
        self.make_field(upper, "Date of Birth", self.var_dob, 1, 2)
        self.make_combo(upper, "ID Proof", self.var_idproof,
                        ("Select ID Proof", "Aadhar", "PAN", "Passport"), 2, 2)
        self.make_combo(upper, "Gender", self.var_gender,
                        ("Select", "Male", "Female", "Other"), 3, 2)
        self.make_field(upper, "Country", self.var_country, 4, 2)

        self.make_field(upper, "Date of Join", self.var_doj, 0, 4)
        self.make_field(upper, "Salary (CTC)", self.var_salary, 1, 4)
        self.make_field(upper, "Phone Number", self.var_phone, 2, 4)
        self.make_field(upper, "ID Number", self.var_idnum, 3, 4)

        btn = Frame(upper, bg="white")
        btn.place(x=1300, y=40)

        self.make_button(btn, "Save", self.add_data, PRIMARY, 0)
        self.make_button(btn, "Update", self.update_data, SECONDARY, 1)
        self.make_button(btn, "Delete", self.delete_data, DANGER, 2)
        self.make_button(btn, "Clear", self.reset_data, GRAY, 3)

        # ===== TABLE & SEARCH =====
        lower = LabelFrame(self.root, text="EMPLOYEE INFORMATION TABLE",
                           font=("Segoe UI", 17, "bold"), bg="white")
        lower.place(x=20, y=400, width=1500, height=400)

        search = LabelFrame(lower, text="SEARCH EMPLOYEE INFORMATION",
                    font=("Segoe UI", 17, "bold"), bg="#f7f9fb")
        search.place(x=10, y=10, width=1500, height=100)

        Label(search, text="Search By",
             bg="#c0392b", fg="white",
             font=("Segoe UI", 12, "bold")) \
             .grid(row=0, column=0, padx=(25, 10), pady=10, sticky=W)

        combo = ttk.Combobox(search, textvariable=self.var_search_by,
                             values=("ID_Number", "Phone"),
                             state="readonly", width=18)
        combo.grid(row=0, column=1, padx=(10, 20), pady=10)

        Entry(search, textvariable=self.var_search_txt,
              font=FONT_ENTRY, width=35) \
             .grid(row=0, column=2, padx=(0, 25), pady=10)

        Button(search, text="Search", width=14,
               command=self.search_data) \
              .grid(row=0, column=3, padx=(0, 15), pady=10)

        Button(search, text="Show All", width=14,
               command=self.fetch_data) \
              .grid(row=0, column=4, padx=(0, 20), pady=10)


        table_frame = Frame(lower)
        table_frame.place(x=10, y=90, width=1480, height=280)

        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(table_frame, orient=VERTICAL)

        self.table = ttk.Treeview(
            table_frame,
            columns=("name","desg","dept","email","address","marriage",
                     "dob","idproof","idnum","gender","country",
                     "doj","salary","phone"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set
        )

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.table.xview)
        scroll_y.config(command=self.table.yview)

        for col in self.table["columns"]:
            self.table.heading(col, text=col.upper())
            self.table.column(col, width=110)

        self.table["show"] = "headings"
        self.table.pack(fill=BOTH, expand=1)
        self.table.bind("<ButtonRelease-1>", self.get_cursor)

        self.fetch_data()

    # ================= HELPERS =================
    def make_field(self, parent, text, var, r, c, w=25):
        Label(parent, text=text, font=FONT_LABEL,
              bg="white").grid(row=r, column=c, padx=18, pady=6, sticky=W)
        Entry(parent, textvariable=var,
              font=FONT_ENTRY, width=w).grid(row=r, column=c+1, padx=18)

    def make_combo(self, parent, text, var, values, r, c):
        Label(parent, text=text, font=FONT_LABEL,
              bg="white").grid(row=r, column=c, padx=18, pady=6, sticky=W)
        cb = ttk.Combobox(parent, textvariable=var,
                          values=values, state="readonly", width=24)
        cb.grid(row=r, column=c+1, padx=18)
        cb.current(0)

    def make_button(self, parent, text, cmd, color, r):
        btn = Button(parent, text=text, width=14,
                     bg=color, fg="white",
                     font=("Segoe UI", 10, "bold"),
                     relief=FLAT, cursor="hand2",
                     command=cmd)
        btn.grid(row=r, column=0, pady=8)
        btn.bind("<Enter>", lambda e: btn.config(bg="#163b5c"))
        btn.bind("<Leave>", lambda e: btn.config(bg=color))

    # ================= DATABASE =================

    import csv
    import mysql.connector

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",#ENTER YOUR PASSWORD
        database="nanopulse"
        )
    cursor = conn.cursor()


    create_table_query = """
                          CREATE TABLE IF NOT EXISTS employee3 (
                          ID_Number VARCHAR(20) PRIMARY KEY,
                          Name VARCHAR(100),
                          Designation VARCHAR(100),
                          Department VARCHAR(100),
                          Email VARCHAR(150),
                          Address VARCHAR(255),
                          Marriage VARCHAR(20),
                          DOB DATE,
                          ID_Proof VARCHAR(50),
                          Gender VARCHAR(20),
                          Country VARCHAR(50),
                          DOJ DATE,
                          Salary INT,
                          Phone VARCHAR(15)
                          );
                        """
    cursor.execute(create_table_query)


    insert_query = """
                  INSERT INTO employee3
                  (ID_Number, Name, Designation, Department, Email, Address,
                  Marriage, DOB, ID_Proof, Gender, Country, DOJ, Salary, Phone)
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                  """
    with open("employee_data.csv", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # skip header
        for row in reader:
            cursor.execute(insert_query, (
                row[8],  # ID_Number
                row[0],  # Name
                row[1],  # Designation
                row[2],  # Department
                row[3],  # Email
                row[4],  # Address
                row[5],  # Marriage
                row[6],  # DOB
                row[7],  # ID_Proof
                row[9],  # Gender
                row[10], # Country
                row[11], # DOJ
                row[12], # Salary
                row[13]  # Phone
                ))
    conn.commit()
    cursor.close()
    conn.close()

    print("✅ Table checked/created and CSV data inserted successfully.")

    conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password"
    )#ENTER YOUR PASSWORD
    cursor = conn.cursor()


    cursor.execute("CREATE DATABASE IF NOT EXISTS nanopulse")


    cursor.execute("USE nanopulse")


    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS employee3 (
                   ID_Number VARCHAR(20) PRIMARY KEY,
                   Name VARCHAR(100),
                   Designation VARCHAR(100),
                   Department VARCHAR(100),
                   Email VARCHAR(150),
                   Address VARCHAR(255),
                   Marriage VARCHAR(20),
                   DOB DATE,
                   ID_Proof VARCHAR(50),
                   Gender VARCHAR(20),
                   Country VARCHAR(50),
                   DOJ DATE,
                   Salary INT,
                   Phone VARCHAR(15)
                   );
                   """)
    conn.commit()
    cursor.close()
    conn.close()

    print("✅ Database and table ready")

    
    conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",#ENTER YOUR PASSWORD        
    database="nanopulse"     
    )

    def connect(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",#ENTER YOUR PASSWORD
            database="nanopulse"
        )

    def add_data(self):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("INSERT INTO employee3 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (
            self.var_name.get(), self.var_designation.get(), self.var_dep.get(),
            self.var_email.get(), self.var_address.get(), self.var_married.get(),
            self.var_dob.get(), self.var_idproof.get(), self.var_idnum.get(),
            self.var_gender.get(), self.var_country.get(), self.var_doj.get(),
            self.var_salary.get(), self.var_phone.get()
        ))
        conn.commit()
        conn.close()
        self.fetch_data()

    def fetch_data(self):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM employee3")
        rows = cur.fetchall()
        self.table.delete(*self.table.get_children())
        for r in rows:
            self.table.insert("", END, values=r)
        conn.close()

    def get_cursor(self, event=""):
        data = self.table.item(self.table.focus())["values"]
        if data:
            (self.var_name.set(data[0]), self.var_designation.set(data[1]),
             self.var_dep.set(data[2]), self.var_email.set(data[3]),
             self.var_address.set(data[4]), self.var_married.set(data[5]),
             self.var_dob.set(data[6]), self.var_idproof.set(data[7]),
             self.var_idnum.set(data[8]), self.var_gender.set(data[9]),
             self.var_country.set(data[10]), self.var_doj.set(data[11]),
             self.var_salary.set(data[12]), self.var_phone.set(data[13]))

    def update_data(self):
        if self.var_idnum.get() == "":
            messagebox.showerror("Error", "Please select an employee to update")
            return

        confirm = messagebox.askyesno(
                                      "Confirm Update",
                                      "⚠️ Do you really want to update this employee's information?"
                                      )

        if not confirm:
            return  # User clicked NO → cancel update

        try:
            conn = self.connect()
            cur = conn.cursor()
            cur.execute("""
                       UPDATE employee3 SET 
                       Name=%s,
                       Designation=%s,
                       Department=%s,
                       Email=%s,
                       Address=%s,
                       Marriage=%s,
                       DOB=%s,
                       ID_Proof=%s,
                       Gender=%s,
                       Country=%s,
                       DOJ=%s,
                       Salary=%s,
                       Phone=%s
                       WHERE ID_Number=%s
                       """, (
                           self.var_name.get(),
                           self.var_designation.get(),
                           self.var_dep.get(),
                           self.var_email.get(),
                           self.var_address.get(),
                           self.var_married.get(),
                           self.var_dob.get(),
                           self.var_idproof.get(),
                           self.var_gender.get(),
                           self.var_country.get(),
                           self.var_doj.get(),
                           self.var_salary.get(),
                           self.var_phone.get(),
                           self.var_idnum.get()))
            conn.commit()
            conn.close()

            self.fetch_data()
            messagebox.showinfo("Success", "Employee information updated successfully")
           
        except Exception as e:
            messagebox.showerror("Error", f"Update failed:\n{str(e)}")


    def delete_data(self):
        if self.var_idnum.get() == "":
            messagebox.showerror("Error", "Please select an employee to delete")
            return

        confirm = messagebox.askyesno(
                                      "Confirm Delete",
                                      "⚠️ Are you sure you want to delete this employee?"
                                      )

        if not confirm:
            return  # User clicked NO → cancel delete

        try:
            conn = self.connect()
            cur = conn.cursor()

            cur.execute(
                        "DELETE FROM employee3 WHERE ID_Number=%s",
                        (self.var_idnum.get(),)
                        )

            conn.commit()
            conn.close()

            self.fetch_data()
            self.reset_data()

            messagebox.showinfo("Success", "Employee deleted successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Delete failed:\n{str(e)}")


    def reset_data(self):
        for v in [self.var_name, self.var_designation, self.var_dep,
                  self.var_email, self.var_address, self.var_married,
                  self.var_dob, self.var_idproof, self.var_idnum,
                  self.var_gender, self.var_country, self.var_doj,
                  self.var_salary, self.var_phone]:
            v.set("")


# ================= RUN =================
if __name__ == "__main__":
    root = Tk()
    app = EmployeeApp(root)
    root.mainloop()
