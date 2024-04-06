

import tkinter as tk
from tkinter import ttk, messagebox
import csv

class InvoiceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Invoice Management System")
        self.root.geometry("800x600")
        
        self.side_panel = tk.Frame(self.root, width=200, bg='lightgrey', padx=10, pady=10)
        self.side_panel.grid(row=0, column=0, sticky='ns')
        self.create_side_panel_buttons()
        
        self.current_page = None
    
    def create_side_panel_buttons(self):
        create_home_btn = tk.Button(self.side_panel, text="Home", command=self.home_page)
        create_home_btn.pack(pady=5, fill='x')
        create_invoice_btn = tk.Button(self.side_panel, text="Create Invoice", command=self.create_invoice_page)
        create_invoice_btn.pack(pady=5, fill='x')
        product_details_btn = tk.Button(self.side_panel, text="Product Details", command=self.product_details_page)
        product_details_btn.pack(pady=5, fill='x')
        view_details_btn = tk.Button(self.side_panel, text="View Details", command=self.view_details_page)
        view_details_btn.pack(pady=5, fill='x')

    def home_page(self):
        self.clear_page()
        home_frame = tk.Frame(self.root, padx=20, pady=20)
        home_frame.grid(row=0, column=1)
        self.current_page = home_frame
        tk.Label(home_frame, text="Raj Patel Company", font=("Arial", 20)).grid(row=0, column=0, columnspan=2, pady=10)
        tk.Label(home_frame, text="Welcome to Invoice Management System", font=("Arial", 16)).grid(row=1, column=0, columnspan=2)

    def create_invoice_page(self):
        self.clear_page()
        invoice_frame = tk.Frame(self.root, padx=20, pady=20)
        invoice_frame.grid(row=0, column=1)
        self.current_page = invoice_frame
        tk.Label(invoice_frame, text="Generate Invoice", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)
         # Fields
        style = ttk.Style()
        style.configure("TLabel", padding=5)
        style.configure("TButton", padding=5)

        # Labels and Entries
        tk.Label(invoice_frame, text="Name:").grid(row=1, column=0, sticky='w')
        self.name_entry = tk.Entry(invoice_frame, relief=tk.RIDGE)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(invoice_frame, text="Address:").grid(row=2, column=0, sticky='w')
        self.address_entry = tk.Entry(invoice_frame, relief=tk.RIDGE)
        self.address_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(invoice_frame, text="Phone:").grid(row=3, column=0, sticky='w')
        self.phone_entry = tk.Entry(invoice_frame, relief=tk.RIDGE)
        self.phone_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(invoice_frame, text="Product Name:").grid(row=4, column=0, sticky='w')
        self.product_combo = ttk.Combobox(invoice_frame, state='readonly')
        self.product_combo['values'] = self.fetch_product_names()
        self.product_combo.grid(row=4, column=1, padx=5, pady=5)
        self.product_combo.bind("<<ComboboxSelected>>", self.update_product_details)

        tk.Label(invoice_frame, text="Product Description:").grid(row=5, column=0, sticky='w')
        self.product_desc_label = tk.Label(invoice_frame, text="", relief=tk.RIDGE, height=5, width=30,wraplength=200)
        self.product_desc_label.grid(row=5, column=1, padx=5, pady=5)


        tk.Label(invoice_frame, text="Unit Price:").grid(row=6, column=0, sticky='w')
        self.unit_price_label = tk.Label(invoice_frame, text="", relief=tk.RIDGE,height=1, width=20)
        self.unit_price_label.grid(row=6, column=1, padx=5, pady=5)

        tk.Label(invoice_frame, text="Quantity:").grid(row=7, column=0, sticky='w')
        self.quantity_entry = tk.Entry(invoice_frame, relief=tk.RIDGE)
        self.quantity_entry.grid(row=7, column=1, padx=5, pady=5)
        self.quantity_entry.bind("<KeyRelease>", self.calculate_total_amount)

        tk.Label(invoice_frame, text="Total Amount:").grid(row=8, column=0, sticky='w')
        self.total_amount_label = tk.Label(invoice_frame, text="", relief=tk.RIDGE,height=1, width=20)
        self.total_amount_label.grid(row=8, column=1, padx=5, pady=5)

        # Buttons
        tk.Button(invoice_frame, text="Save", command=self.save_invoice, relief=tk.RIDGE).grid(row=9, column=0, pady=10)
        tk.Button(invoice_frame, text="Reset", command=self.reset_invoice_form, relief=tk.RIDGE).grid(row=9, column=1, pady=10)

    def fetch_product_names(self):
        try:
            with open("products.csv", "r") as file:
                reader = csv.reader(file)
                products = [row[0] for row in reader]
            return products
        except FileNotFoundError:
            return []
    
    def update_product_details(self, event=None):
        product_name = self.product_combo.get()
        try:
            with open("products.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == product_name:
                        self.product_desc_label.config(text=row[1])
                        self.unit_price_label.config(text=row[2])
                        break
        except FileNotFoundError:
            pass
    
    def calculate_total_amount(self, event=None):
        try:
            unit_price = float(self.unit_price_label.cget("text"))
            quantity = int(self.quantity_entry.get())
            total_amount = unit_price * quantity
            self.total_amount_label.config(text=total_amount)
        except ValueError:
            self.total_amount_label.config(text="")
    
    def save_invoice(self):
        name = self.name_entry.get()
        address = self.address_entry.get()
        phone = self.phone_entry.get()
        product_name = self.product_combo.get()
        quantity = self.quantity_entry.get()
        total_amount = self.total_amount_label.cget("text")
        
        if name and address and phone and product_name and quantity and total_amount:
            with open("invoices.csv", "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([name, address, phone, product_name, quantity, total_amount])
            
            messagebox.showinfo("Success", "Invoice saved successfully!")
            self.reset_invoice_form()
        else:
            messagebox.showerror("Error", "Please fill in all fields.")
    
    def reset_invoice_form(self):
        self.name_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.product_combo.set('')
        self.product_desc_label.config(text="")
        self.unit_price_label.config(text="")
        self.quantity_entry.delete(0, tk.END)
        self.total_amount_label.config(text="")

    def product_details_page(self):
        self.clear_page()
        product_details_frame = tk.Frame(self.root, padx=20, pady=20)
        product_details_frame.grid(row=0, column=1)
        self.current_page = product_details_frame
        
        # Labels and Entries for Product Details
        tk.Label(product_details_frame, text="Product Details", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)
        tk.Label(product_details_frame, text="Product Name:").grid(row=1, column=0, sticky='w')
        self.product_name_entry = tk.Entry(product_details_frame)
        self.product_name_entry.grid(row=1, column=1, padx=5)
        
        tk.Label(product_details_frame, text="Product Description:").grid(row=2, column=0, sticky='w')
        self.product_desc_entry = tk.Entry(product_details_frame)
        self.product_desc_entry.grid(row=2, column=1, padx=5)
        
        tk.Label(product_details_frame, text="Unit Price:").grid(row=3, column=0, sticky='w')
        self.unit_price_entry = tk.Entry(product_details_frame)
        self.unit_price_entry.grid(row=3, column=1, padx=5)
        
        tk.Label(product_details_frame, text="Inventory:").grid(row=4, column=0, sticky='w')
        self.inventory_entry = tk.Entry(product_details_frame)
        self.inventory_entry.grid(row=4, column=1, padx=5)
        
        # Buttons for Product Details
        tk.Button(product_details_frame, text="Save", command=self.save_product_details).grid(row=5, column=0, pady=10)
        tk.Button(product_details_frame, text="Reset", command=self.reset_product_details_form).grid(row=5, column=1, pady=10)
        
        # List of product names
        product_names = self.fetch_product_names()
        
        tk.Label(product_details_frame, text="Product List", font=("Arial", 16)).grid(row=6, column=0, columnspan=2, pady=10)
        
        self.product_listbox = tk.Listbox(product_details_frame)
        self.product_listbox.grid(row=7, column=0, padx=5, columnspan=2)
        
        scrollbar = ttk.Scrollbar(product_details_frame, orient="vertical", command=self.product_listbox.yview)
        scrollbar.grid(row=7, column=2, sticky='ns')
        self.product_listbox.config(yscrollcommand=scrollbar.set)
        
        for product_name in product_names:
            self.product_listbox.insert(tk.END, product_name)
        
        self.product_listbox.bind("<<ListboxSelect>>", self.fill_product_details)
        
    def save_product_details(self):
        product_name = self.product_name_entry.get()
        product_desc = self.product_desc_entry.get()
        unit_price = self.unit_price_entry.get()
        inventory = self.inventory_entry.get()
        
        if product_name and product_desc and unit_price and inventory:
            with open("products.csv", "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([product_name, product_desc, unit_price, inventory])
            
            messagebox.showinfo("Success", "Product details saved successfully!")
            self.reset_product_details_form()
            self.update_product_listbox(product_name)
        else:
            messagebox.showerror("Error", "Please fill in all fields.")
    
    def reset_product_details_form(self):
        self.product_name_entry.delete(0, tk.END)
        self.product_desc_entry.delete(0, tk.END)
        self.unit_price_entry.delete(0, tk.END)
        self.inventory_entry.delete(0, tk.END)
    
    def fill_product_details(self, event=None):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            product_name = event.widget.get(index)
            try:
                with open("products.csv", "r") as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if row[0] == product_name:
                            self.product_name_entry.delete(0, tk.END)
                            self.product_desc_entry.delete(0, tk.END)
                            self.unit_price_entry.delete(0, tk.END)
                            self.inventory_entry.delete(0, tk.END)
                            
                            self.product_name_entry.insert(tk.END, row[0])
                            self.product_desc_entry.insert(tk.END, row[1])
                            self.unit_price_entry.insert(tk.END, row[2])
                            self.inventory_entry.insert(tk.END, row[3])
                            break
            except FileNotFoundError:
                pass
    
    def update_product_listbox(self, product_name):
        self.product_listbox.insert(tk.END, product_name)
    
    
    def view_details_page(self):
        self.clear_page()
        view_details_frame = tk.Frame(self.root, padx=20, pady=20)
        view_details_frame.grid(row=0, column=1)
        self.current_page = view_details_frame
    
        tk.Label(view_details_frame, text="View Details", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Display data in table view
        headers = ["Name", "Address", "Phone", "Product Name", "Quantity", "Total Amount"]
        self.treeview = ttk.Treeview(view_details_frame, columns=headers, show='headings')
        column_widths = [200, 300, 100, 200, 100, 100]  # Adjust these values as needed
        for header, width in zip(headers, column_widths):
            self.treeview.heading(header, text=header)
            self.treeview.column(header, width=width)
        
        self.treeview.grid(row=1, column=0)
        
        # Populate data from invoices.csv
        file_path = "invoices.csv" 
        try:
            with open(file_path, newline='') as csvfile:
                csv_reader = csv.reader(csvfile)
                for row in csv_reader:
                    self.treeview.insert("", "end", values=row)
        except Exception as e:
            self.text_output.insert(tk.END, f"Error: {e}")
    def clear_page(self):
        if self.current_page:
            self.current_page.destroy()

root = tk.Tk()
app = InvoiceApp(root)
app.home_page()  # Display home page initially
root.mainloop()

