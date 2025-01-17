import tkinter as tk
from tkinter import font
import functools

class ContactView(tk.Frame):
    def __init__(self, parent, controller, user):
        super().__init__(parent)
        self.controller = controller
        self.user = user

        self.canvas = tk.Canvas(self, width=410, height=375, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.create_contactview()

    def create_contactview(self):
        self.label_register = tk.Label(self.canvas, text="Thông Tin Liên Hệ", font=("Inter", 18, "bold"))
        self.canvas.create_window(205, 30, window=self.label_register)

        self.label_search = tk.Label(self.canvas, text="Tìm kiếm", font=("Inter", 10))
        self.canvas.create_window(45, 70, window=self.label_search)

        self.search = tk.Entry(self.canvas, width=25, font=("Arial", 10))
        self.canvas.create_window(150, 70, width=140, height=25, window=self.search)
        self.search.bind("<KeyRelease>", self.filter_contacts)
        self.contacts = self.controller.get_list_contacts(self.user.username)

        self.filtered_contacts = []

        self.sort_option = tk.StringVar()
        self.sort_option.set("Mới Nhất")
        sort_button = tk.Button(self.canvas, text="Sắp xếp", command=self.sort_contacts)
        self.canvas.create_window(250, 70, window=sort_button)

        buttonFindContact = tk.Button(self.canvas, text="Tìm Bạn", font=("Arial", 10), command=lambda:self.controller.call_find_contact_view(), bg="#1492C3", fg="#ffffff")
        self.canvas.create_window(355, 70, window=buttonFindContact)

        self.list_canvas = tk.Canvas(self.canvas, width=380, height=280, bd=0, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.canvas, orient="vertical", command=self.list_canvas.yview)
        self.list_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.image_contact = tk.PhotoImage(file=self.controller.load_asset("contact.png"))

        # Place canvas and scrollbar correctly
        self.canvas.create_window(205, 90, window=self.list_canvas, anchor="n")
        self.canvas.create_window(406, 90, height=280, window=self.scrollbar, anchor="ne")

        # Create frame inside the canvas
        self.list_frame = tk.Frame(self.list_canvas, bg="#F9F9FC")
        self.list_canvas.create_window((0, 0), window=self.list_frame, anchor="nw") 

        self.list_contacts(self.contacts)

        # Update the canvas scroll region after adding all account frames
        self.list_frame.update_idletasks()
        self.list_canvas.config(scrollregion=self.list_canvas.bbox("all"))

        # Bind the mouse wheel for scrolling
        self.list_canvas.bind("<Enter>", lambda e: self.list_canvas.bind_all("<MouseWheel>", self._on_mouse_wheel))
        self.list_canvas.bind("<Leave>", lambda e: self.list_canvas.unbind_all("<MouseWheel>"))

    def _on_mouse_wheel(self, event):
        self.list_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def refresh_data(self):
        self.canvas.delete("all")
        self.create_contactview() 

    def list_contacts(self, contacts):
        self.filtered_contacts = contacts

        if self.filtered_contacts is None:
            self.filtered_contacts = []

        self.filtered_contacts = sorted(self.filtered_contacts, key=lambda x: x.id, reverse=(self.sort_option.get() == "Cũ nhất"))

        for widget in self.list_frame.winfo_children():
            widget.destroy()

        for contact in self.filtered_contacts:
            contact_frame = tk.Frame(self.list_frame, bg="#FFFFFF", pady=5, padx=5, relief="solid", bd=0, width=360, height=60)
            contact_frame.pack_propagate(False)
            contact_frame.pack(fill=tk.X, pady=5)

            image_label = tk.Label(contact_frame, image=self.image_contact, bg="#FFFFFF")
            image_label.place(x=10, y=5)

            contact_name_label = tk.Label(contact_frame, text=contact.contact_name, font=("Inter", 12), bg="#FFFFFF")
            contact_name_label.place(x=70, y=2)

            email_label = tk.Label(contact_frame, text=contact.email, font=("Inter", 11), bg="#FFFFFF")
            email_label.place(x=70, y=26)

            underlined_font = font.Font(family="Inter", size=9, underline=True)
            account_info = tk.Button(contact_frame, text="Tin nhắn", relief="flat", borderwidth=1, fg="#AC1D1F", font=underlined_font , bg="#FFFFFF", 
                                            highlightthickness=0,  command=functools.partial(self.controller.show_message, contact.contact_name))
            account_info.place(x=280, y=10)

    def filter_contacts(self, event=None):
        search_text = self.search.get().lower()
        filtered_contacts = []
        for account in self.contacts:
            if search_text in account.contact_name.lower() or search_text in account.email.lower():
                filtered_contacts.append(account)

        self.filtered_contacts = filtered_contacts
        self.list_contacts(self.filtered_contacts)

    def sort_contacts(self):
        if self.sort_option.get() == "Mới nhất":
            self.sort_option.set("Cũ nhất")
        else:
            self.sort_option.set("Mới nhất")
        self.list_contacts(self.filtered_contacts)