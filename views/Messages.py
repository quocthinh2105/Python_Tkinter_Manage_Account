import tkinter as tk
from tkinter import StringVar
from tkinter import font

class MessageView(tk.Frame):
    def __init__(self, parent, controller, user, contactId):
        super().__init__(parent)
        self.controller = controller
        self.user = user
        self.contactId = contactId

        self.canvas = tk.Canvas(self, width=410, height=375, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.stop_flag = False
        self.is_running = False
        
        if not self.is_running:
            self.run_checking_new_messages()

        self.create_messageview()

    def create_messageview(self):      
        self.label_register = tk.Label(self.canvas, text="Tin Nhắn", font=("Inter", 18, "bold"))
        self.canvas.create_window(205, 30, window=self.label_register)

        buttonFindContact = tk.Button(self.canvas, text="Quay Lại", font=("Arial", 9), command=lambda:self.controller.show_contact_view(), bg="#1492C3")
        self.canvas.create_window(360, 30, window=buttonFindContact)

        self.list_canvas = tk.Canvas(self.canvas, width=380, height=280, bd=0, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.canvas, orient="vertical", command=self.list_canvas.yview)
        self.list_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.image_contact = tk.PhotoImage(file=self.controller.load_asset("contact.png"))

        # Place canvas and scrollbar correctly
        self.canvas.create_window(205, 50, window=self.list_canvas, anchor="n")
        self.canvas.create_window(406, 50, height=280, window=self.scrollbar, anchor="ne")

        # Create frame inside the canvas
        self.list_frame = tk.Frame(self.list_canvas, bg="#F9F9FC")
        self.list_canvas.create_window((0, 0), window=self.list_frame, anchor="nw") 

        self.list_messages(self.controller.get_messages(self.user.username, self.contactId))

        # Select Account
        list_accounts = self.controller.get_list_acc(self.user.username)
        if not list_accounts:
            self.options = ["Vui Lòng Thêm Mới Tài Khoản"]
            self.account_models = []
        else:
            self.options = [f"Ứng dụng: {msg.app_name} - Tài khoản: {msg.acc_name}" for msg in list_accounts]
            self.account_models = list_accounts

        self.selected_message = StringVar(self.canvas,)
        self.selected_message.set(self.options[0])

        custom_font = font.Font(family="Arial", size=10, weight="normal")
        self.option_menu_account = tk.OptionMenu(self.canvas, self.selected_message, *self.options)
        self.option_menu_account.config(font=custom_font, bg="#ffffff", fg="#000000", activebackground="#EFEFEF", activeforeground="#000000")

        self.canvas.create_window(173, 350, width=320, window=self.option_menu_account)

        self.menu = self.option_menu_account.nametowidget(self.option_menu_account.menuname)
        self.menu.config(font=custom_font, bg="#ffffff", fg="#000000", activebackground="#EFEFEF", activeforeground="#000000")

        self.buttonSend = tk.Button(self.canvas, text="Gửi", font=("Inter", 12), bg="#ffffff", fg="#000000", command=self.send_message)
        self.canvas.create_window(360, 350, width=60, window=self.buttonSend)

        # Update the canvas scroll region after adding all account frames
        self.list_frame.update_idletasks()
        self.list_canvas.config(scrollregion=self.list_canvas.bbox("all"))

        # Scroll to the bottom
        self.list_canvas.yview_moveto(1.0)

        # Bind the mouse wheel for scrolling
        self.list_canvas.bind("<Enter>", lambda e: self.list_canvas.bind_all("<MouseWheel>", self._on_mouse_wheel))
        self.list_canvas.bind("<Leave>", lambda e: self.list_canvas.unbind_all("<MouseWheel>"))

    def _on_mouse_wheel(self, event):
        self.list_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def refresh_data(self):
        self.canvas.delete("all")
        self.create_messageview() 

    def list_messages(self, messages):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        for message in messages:
            sender = message.sender_id
            app_name = message.app_name
            acc_name = message.acc_name
            acc_pass = message.acc_pass_enc
            key_enc = message.key_enc
            timestamp = message.created_at.strftime("%d/%m/%Y %H:%M:%S")
            is_user_a = sender == self.contactId

            message_frame = tk.Frame(self.list_frame, bg="#FFFFFF", pady=5, padx=5, relief="solid", bd=0, width=360, height=100)
            message_frame.pack_propagate(False)
            message_frame.pack(fill=tk.X, pady=5, anchor='w' if is_user_a else 'e')

            # Label for the sender's name
            user_label = tk.Label(message_frame, text=sender, font=("Inter", 10, "bold"), bg="#FFFFFF", fg="red" if is_user_a else "blue", anchor='w' if is_user_a else 'e')
            user_label.pack(fill=tk.X, pady=(0, 1), anchor='w' if is_user_a else 'e')

            # Inner frame to hold text and timestamp
            inner_frame = tk.Frame(message_frame, bg="#A5EEFF" if is_user_a else "#D9FFD9", padx=10, pady=3)
            inner_frame.pack(side='left' if is_user_a else 'right', fill=tk.BOTH, expand=True)

            app_label = tk.Label(inner_frame, text=f"Ứng dụng: {app_name}", font=("Inter", 9), bg="#A5EEFF" if is_user_a else "#D9FFD9", anchor='w')
            app_label.pack(fill=tk.BOTH)

            username_label = tk.Label(inner_frame, text=f"Tài khoản: {acc_name}", font=("Inter", 9), bg="#A5EEFF" if is_user_a else "#D9FFD9", anchor='w')
            username_label.pack(fill=tk.BOTH)

            password_frame = tk.Frame(inner_frame, bg="#A5EEFF" if is_user_a else "#D9FFD9")
            password_frame.pack(fill=tk.BOTH)

            password_label = tk.Label(password_frame, text="Mật khẩu: ••••••", font=("Inter", 9), bg="#A5EEFF" if is_user_a else "#D9FFD9", anchor='w')
            password_label.pack(side='left', fill=tk.BOTH, expand=True)

            show_button = tk.Button(password_frame, text="👁", font=("Inter", 9), command=lambda:toggle_password(), bg="#A5EEFF" if is_user_a else "#D9FFD9", relief='flat')
            show_button.pack(side='right')

            # Timestamp for the message
            timestamp_label = tk.Label(message_frame, text=timestamp, font=("Inter", 8), bg="#FFFFFF", fg="gray")
            timestamp_label.pack(side='left' if is_user_a else 'right', padx=5, pady=2)

        def toggle_password():
            if password_label.cget('text') == "Mật khẩu: ••••••":
                password_label.config(text=f"Mật khẩu: {self.controller.decrypt_pass(acc_pass, key_enc)}")
                show_button.config(text="👁")
            else:
                password_label.config(text="Mật khẩu: ••••••")
                show_button.config(text="👁")
    
    def send_message(self):
        selected_value = self.selected_message.get()
        try:
            selected_index = self.options.index(selected_value)
            if selected_index < len(self.account_models):
                selected_data = self.account_models[selected_index]
                self.controller.send_message(self.user.username, self.contactId, selected_data.id)
        except ValueError:
            print("Không tìm thấy tùy chọn trong danh sách.")

    # def update_messages(self):
    #     print("--------------------")
    #     print("username", self.user.username)
    #     print("contactId", self.contactId)
    #     print("--------------------")
    #     self.after(5000, self.update_messages)
        # if is_refesh:
        #     print(self.user.username, self.contactId)
        #     self.list_messages(self.controller.get_messages(self.user.username, self.contactId))

    def run_checking_new_messages(self):
        print("running checking")
        if self.stop_flag:
            return
        if self.is_running:
            return
        self.is_running = True
        if self.controller.checking_new_messages(self.user.username, self.contactId):
            self.refresh_data()
        self.after(10000, self.reset_run_checking)

    def reset_run_checking(self):
        print("reset running checking")
        self.is_running = False
        if not self.stop_flag:
            self.run_checking_new_messages()

    def stop_run_checking(self):
        print("stop run checking")
        self.stop_flag = True

    def start_run_checking(self):
        print("start run checking")
        self.stop_flag = False
        self.run_checking_new_messages()