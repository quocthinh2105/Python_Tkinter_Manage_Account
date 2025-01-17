import tkinter as tk
import functools

class FindContactView(tk.Frame):
    def __init__(self, parent, controller, user):
        super().__init__(parent)
        self.controller = controller
        self.user = user

        self.canvas = tk.Canvas(self, width=410, height=375, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.create_contactview()

    def create_contactview(self):
        self.label_register = tk.Label(self.canvas, text="Thêm Bạn", font=("Inter", 18, "bold"))
        self.canvas.create_window(205, 30, window=self.label_register)

        self.label_search = tk.Label(self.canvas, text="Tìm kiếm", font=("Inter", 13))
        self.canvas.create_window(100, 80, window=self.label_search)

        self.search = tk.Entry(self.canvas, width=25, font=("Arial", 13))
        self.canvas.create_window(250, 80, width=160, height=25, window=self.search)
        self.search.bind("<KeyRelease>", self.search_contacts)
        self.contacts = self.controller.find_contacts(self.user.username, "")

        self.filtered_contacts=[]

        self.list_canvas = tk.Canvas(self.canvas, width=380, height=200, bd=0, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.canvas, orient="vertical", command=self.list_canvas.yview)
        self.list_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.image_contact = tk.PhotoImage(file=self.controller.load_asset("contact.png"))

        # Place canvas and scrollbar correctly
        self.canvas.create_window(205, 100, window=self.list_canvas, anchor="n")
        self.canvas.create_window(406, 100, height=200, window=self.scrollbar, anchor="ne")

        # Create frame inside the canvas
        self.list_frame = tk.Frame(self.list_canvas, bg="#F9F9FC")
        self.list_canvas.create_window((0, 0), window=self.list_frame, anchor="nw") 

        self.list_contacts(self.contacts)

        buttonFindContact = tk.Button(self.canvas, text="Quay Lại", font=("Arial", 13), command=lambda:self.controller.show_contact_view(), bg="#1492C3", fg="#ffffff")
        self.canvas.create_window(205, 335, window=buttonFindContact)

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
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        for contact in self.filtered_contacts:
            contact_name = contact.contact_name
            email = contact.email
            phone = contact.phone

            contact_frame = tk.Frame(self.list_frame, bg="#FFFFFF", pady=5, padx=5, relief="solid", bd=0, width=360, height=60)
            contact_frame.pack_propagate(False)
            contact_frame.pack(fill=tk.X, pady=5)

            image_label = tk.Label(contact_frame, image=self.image_contact, bg="#FFFFFF")
            image_label.place(x=10, y=5)

            contact_name_label = tk.Label(contact_frame, text=contact_name, font=("Inter", 12), bg="#FFFFFF")
            contact_name_label.place(x=70, y=2)

            email_label = tk.Label(contact_frame, text=email, font=("Inter", 11), bg="#FFFFFF")
            email_label.place(x=70, y=26)

            account_info = tk.Button(contact_frame, text="Thêm Bạn", relief="flat", borderwidth=1, fg="#ffffff", font=("Inter", 10) , bg="#1492C3",
                                             highlightthickness=0,  command=functools.partial(self.controller.add_contact, self.user.username, contact_name, email, phone))
            account_info.place(x=260, y=10)

    def search_contacts(self, event=None):
        search_text = self.search.get().lower()
        filtered_contacts = []
        for contact in self.contacts:
            if search_text in contact.contact_name.lower() or search_text in contact.email.lower():
                filtered_contacts.append(contact)
        self.filtered_contacts = filtered_contacts
        self.list_contacts(self.filtered_contacts)
