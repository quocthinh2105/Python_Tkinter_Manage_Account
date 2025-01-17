# view/dashboard_view.py
import tkinter as tk

class DashboardView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.canvas = tk.Canvas(self, bg="#ffffff", width=600, height=400, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.container = tk.Frame(self.canvas, bg="#D9D9D9", width=410, height=375)
        self.container.place(x=179, y=13)

        self.inner_container = tk.Canvas(self.container, bg="#D9D9D9", width=410, height=375, bd=0, highlightthickness=0, relief="ridge")
        self.inner_container.pack(fill=tk.BOTH, expand=True)

        self.current_button = None 

        self.create_dashboard()

    def create_dashboard(self):

        self.image_background = tk.PhotoImage(file=self.controller.load_asset("background.png"))
        self.canvas.create_image(300, 200, image=self.image_background)

        self.image_frame_menu = tk.PhotoImage(file=self.controller.load_asset("frame_menu_dashb.png"))
        self.canvas.create_image(89, 199, image=self.image_frame_menu)

        self.image_welcome = tk.PhotoImage(file=self.controller.load_asset("welcome.png"))
        self.inner_container.create_image(205, 188, image=self.image_welcome)

        text = self.controller.get_username()
        font = ("Inter", 14 * -1)
        text_width = self.canvas.bbox(self.canvas.create_text(0, 0, text=text, font=font))[2]
        text_x = 80 - (text_width / 2)
        self.canvas.create_text(text_x, 134, anchor="nw", text=text, fill="#000000", font=("Inter", 14 * -1))

        self.image_avatar = tk.PhotoImage(file=self.controller.load_asset("avatar.png"))
        self.canvas.create_image(89, 78, image=self.image_avatar)

        self.create_button("Người Dùng", 9, 165, 160, 40,"USER")
        self.create_button("Tài Khoản", 9, 220, 160, 40, "ACCOUNT")
        self.create_button("Bạn Bè", 9, 275, 160, 40, "CONTACT")
        self.create_button("Ứng Dụng", 9, 330, 160, 40, "INFO")

    def create_button(self, name, x, y, width, height, command):
        button = tk.Button(self.canvas, text=name, relief="flat", borderwidth=0, background="#1492C3", font=("Arial", 13),
                            highlightthickness=0, command=lambda:self.on_button_click(button, command))
        button.place(x=x, y=y, width=width, height=height)
        return button

    def on_button_click(self, button, screen_name):
        if self.current_button:
            self.current_button.configure(background="#1492C3", fg="#000000")
        button.configure(background="#E7090C", fg="#ffffff")
        self.current_button = button
        self.controller.show_screen(screen_name)