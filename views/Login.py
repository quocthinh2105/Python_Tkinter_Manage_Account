# view/Login_view.py
import tkinter as tk

class LoginView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.canvas = tk.Canvas(self, bg="#ffffff", width=600, height=400, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.create_login()

    def create_login(self):
        self.image_background = tk.PhotoImage(file=self.controller.load_asset("Login.png"))
        self.canvas.create_image(300, 200, image=self.image_background)

        self.username = tk.Entry(self.canvas, width=30, bg="#6EDEFF")
        self.username_placeholder = "Username"
        self.username.insert(0, self.username_placeholder)
        self.username.bind("<FocusIn>", self.on_focus_in_username)
        self.username.bind("<FocusOut>", self.on_focus_out_username)
        self.canvas.create_window(180, 160, window=self.username)

        self.password = tk.Entry(self.canvas, width=30, bg="#6EDEFF", show="*")
        self.password_placeholder = "password"
        self.password.insert(0, self.password_placeholder)
        self.password.bind("<FocusIn>", self.on_focus_in_password)
        self.password.bind("<FocusOut>", self.on_focus_out_password)
        self.canvas.create_window(180, 205, window=self.password)

        self.btnLogin = tk.PhotoImage(file=self.controller.load_asset("btnLogin.png"))
        buttonLogin = tk.Button(self.canvas, image=self.btnLogin, relief="flat", borderwidth=0, background="#0BBEFF",
                            highlightthickness=0, command=self.submit)
        buttonLogin.place(x=125, y=230, width=115, height=35)

        text_register = self.canvas.create_text(105, 280, anchor="nw", text="Đăng ký", fill="#000000", font=("Inter", 10 * -1))
        text_forgot_password = self.canvas.create_text(200, 280, anchor="nw", text="Quên mật khẩu ?", fill="#000000", font=("Inter", 10 * -1))

        self.canvas.tag_bind(text_register, "<Enter>", lambda event: self.on_hover(event, text_register))
        self.canvas.tag_bind(text_register, "<Leave>", lambda event: self.on_leave(event, text_register))
        self.canvas.tag_bind(text_register, "<Button-1>", lambda event: self.controller.show_container("REGISTER"))

        self.canvas.tag_bind(text_forgot_password, "<Enter>", lambda event: self.on_hover(event, text_forgot_password))
        self.canvas.tag_bind(text_forgot_password, "<Leave>", lambda event: self.on_leave(event, text_forgot_password))
        self.canvas.tag_bind(text_forgot_password, "<Button-1>", lambda event: self.controller.show_container("FORGOT"))

    def on_focus_in_username(self, event):
        if self.username.get() == self.username_placeholder:
            self.username.delete(0, tk.END)

    def on_focus_out_username(self, event):
        if self.username.get() == "":
            self.username.insert(0, self.username_placeholder)

    def on_focus_in_password(self, event):
        if self.password.get() == self.password_placeholder:
            self.password.delete(0, tk.END)

    def on_focus_out_password(self, event):
        if self.password.get() == "":
            self.password.insert(0, self.password_placeholder)

    def on_hover(self, event, text_id):
        self.canvas.itemconfig(text_id, fill="#FF0000")

    def on_leave(self, event, text_id):
        self.canvas.itemconfig(text_id, fill="#000000")

    def submit(self):
        self.controller.login(self.username.get(), self.password.get())

    def refresh_data(self):
        self.canvas.delete("all")
        self.create_login() 