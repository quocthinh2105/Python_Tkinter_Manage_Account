import tkinter as tk

class AppView(tk.Frame):
    def __init__(self, parent, controller, user):
        super().__init__(parent)
        self.controller = controller
        self.user = user

        self.canvas = tk.Canvas(self, width=410, height=375, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.create_infoview()

    def create_infoview(self):
        self.label_title = tk.Label(self.canvas, text="THÔNG TIN ỨNG DỤNG", font=("Inter", 18, "bold"))
        self.canvas.create_window(202, 50, window=self.label_title)

        long_text = (
            "Chương Trình Quản Lý Tài Khoản.\n"
            "Version: 0.0.1\n\n"
            "IE221.E13.LT - Kỹ thuật lập trình Python\n"
            "Giảng viên hướng dẫn : Phạm Thế Sơn.\n\n"
            "Thành viên nhóm :\n"
            "   * Hà Quốc Thịnh                - 23410194\n"
            "   * Lê Phan Thanh Bình       - 23410143\n"
            "   * Hà Lê Hùng Cường       - 23410148\n"
        )

        self.long_text_label = tk.Label(self.canvas, text=long_text, font=("Inter", 12), justify="left", wraplength=300)
        self.canvas.create_window(202, 200, width=350, height=200 , window=self.long_text_label)

    def refresh_data(self):
        self.canvas.delete("all")
        self.create_infoview()

