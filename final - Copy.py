import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io
from datetime import datetime, timedelta
import os
import sys
from datetime import datetime
import os
from dateutil.relativedelta import relativedelta

if getattr(sys, 'frozen', False):
    # Running in a PyInstaller bundle
    base_path = sys._MEIPASS
else:
    # Running in a normal Python environment
    base_path = os.path.dirname(__file__)

# Register Arial and Arial Narrow fonts
pdfmetrics.registerFont(TTFont('Arial', os.path.join(base_path, 'Arial.ttf')))
pdfmetrics.registerFont(TTFont('ArialNarrow', os.path.join(base_path, 'arialnarrow.ttf')))
pdfmetrics.registerFont(TTFont('ArialNarrowBold', os.path.join(base_path, 'arialnarrow_bold.ttf')))

# Function to create a new PDF overlay with specific text, position, font, and size
def create_overlay_single(text, x, y, font_name="Arial", font_size=11):
    packet = io.BytesIO()   
    can = canvas.Canvas(packet, pagesize=letter, invariant=1)
    can.setFont(font_name, font_size)
    can.drawString(x, y, text)
    can.save()
    packet.seek(0)
    return PdfReader(packet)

import os
import subprocess

import os
import subprocess

import os
import subprocess
import pikepdf

# Main function to create the modified PDF based on user inputs
def create_pdf(title, first_name, second_name, address_line, user_input_code, user_birthday, user_input_value):
    try:
        # Determine PDF path based on title
        input_pdf_path = "dry3.pdf" if title == "Mme" else "dry2.pdf"

        output_pdf_path = f"{first_name} {second_name}.pdf"
        reader = PdfReader(input_pdf_path)
        writer = PdfWriter()
        current_datetime = datetime.now().strftime("D:%Y%m%d%H%M%S")
        writer.add_metadata({
                    "/Title": "driver_out.pdf",
                    "/Author": "Open Print",
                    "/Subject": "Driver PDF",
                    "/Keywords": "HCS Runtime PDF driver",
                    "/Producer": "Open Print Backstage VERSION 1.1.4.1(7)",
                    "/Creator": "HCS Runtime - Copyright (c) 2015 Sefas Innovation. All Rights Reserved",
                    "/CreationDate": current_datetime,
                    "/ModDate": current_datetime
                })

        # Prepare full name and overlay positions
        full_name = f"{title} {first_name} {second_name}"
        x1, y1 = 300.50     , letter[1] - 143.47
        lines1 = [full_name, address_line, user_input_value +" PARIS"]
        line_height = 12

        # Create the first overlay with Arial
        packet1 = io.BytesIO()
        can1 = canvas.Canvas(packet1, pagesize=letter, invariant=1)
        can1.setFont("Arial", 11)
        for i, line in enumerate(lines1):
            can1.drawString(x1, y1 - i * line_height, line)
        can1.save()
        packet1.seek(0)
        overlay_pdf1 = PdfReader(packet1)
        print(reader.pages[0].mediabox.width)
        print(reader.pages[0].mediabox.height)    
        # Second overlay for formatted name using Arial Narrow
        x2, y2 = 45.6, float(reader.pages[0].mediabox.height) - 158.4
        overlay_pdf2 = create_overlay_single(first_name + " " + second_name, x2, y2, font_name="ArialNarrow", font_size=10)

        # Format code as "1 91 09 99 213 167 82"
        formatted_code = format_code(user_input_code)
      
        x3, y3 = 98.55, float(reader.pages[0].mediabox.height) - 135.85
        overlay_pdf3 = create_overlay_single(formatted_code, x3, y3, font_name="ArialNarrow", font_size=10)

        x4, y4 = 501, float(reader.pages[0].mediabox.height) - 277.9
        today_date = datetime.today().strftime("%d/%m/%Y")
        overlay_pdf4 = create_overlay_single(f"Le {today_date}", x4, y4, font_name="ArialNarrow", font_size=10)

        # Additional overlays for page 2
        x5, y5 =98.55, float(reader.pages[1].mediabox.height) -  135.85
        overlay_pdf5 = create_overlay_single(formatted_code, x5, y5, font_name="ArialNarrow", font_size=10)

        x6, y6 = 45.6, float(reader.pages[1].mediabox.height) - 158.4
        overlay_pdf6 = create_overlay_single(first_name + " " + second_name, x6, y6, font_name="ArialNarrow", font_size=10)

        x7, y7 = 308.83, float(reader.pages[1].mediabox.height) - 374.62
        overlay_pdf7 = create_overlay_single(formatted_code, x7, y7, font_name="ArialNarrow", font_size=11)

        x8, y8 = 47.5, float(reader.pages[1].mediabox.height) - 523.99999
        overlay_pdf8 = create_overlay_single(first_name, x8, y8, font_name="ArialNarrow", font_size=10)

        x9, y9 = 47.5, float(reader.pages[1].mediabox.height) - 535.31
        overlay_pdf9 = create_overlay_single(second_name, x9, y9, font_name="ArialNarrow", font_size=10)

       
        
        x10, y10 = 227.08, float(reader.pages[1].mediabox.height) - 509.05
        overlay_pdf10 = create_overlay_single(formatted_code, x10, y10, font_name="ArialNarrow", font_size=10)

        # Birthday overlay
        x11, y11 = 318.35, float(reader.pages[1].mediabox.height) - 509.3
        overlay_pdf11 = create_overlay_single(user_birthday, x11, y11, font_name="ArialNarrow", font_size=10)

        input_date = datetime.today()
        start_date, end_datee = get_date_range(input_date)
    	
        x12, y12 = 452.4, float(reader.pages[1].mediabox.height) - 509.3
        x13, y13 = 514.4, float(reader.pages[1].mediabox.height) - 509.3

        overlay_pdf12 = create_overlay_single(start_date, x12, y12, font_name="ArialNarrow", font_size=10)
        overlay_pdf13 = create_overlay_single(end_datee, x13, y13, font_name="ArialNarrow", font_size=10)
        # Additional type number overlays
        # x11_over, y11_over = 367.9, float(reader.pages[1].mediabox.height) - 509.3
        # overlay_pdf11_over = create_overlay_single("1", x11_over, y11_over, font_name="ArialNarrow", font_size=10)

        # x11_over2, y11_over2 = 407.8, float(reader.pages[1].mediabox.height) - 509.3
        # overlay_pdf11_over2 = create_overlay_single("1", x11_over2, y11_over2, font_name="ArialNarrow", font_size=10)

        # Date overlays
        

        # Set start and end dates
        
   
        overlay_text = today_date
        x14, y14 = 92.15, float(reader.pages[1].mediabox.height) - 283.69
        overlay_pdf14 = create_overlay_single(overlay_text, x14, y14, font_name="ArialNarrowBold", font_size=11)

        end_date_full = (datetime.today() + timedelta(days=364)).strftime("%d/%m/%Y")
        overlay_textend = end_date_full
        x14end, y14end = 152.90, float(reader.pages[1].mediabox.height) - 283.69
        overlay_pdf14end = create_overlay_single(overlay_textend, x14end, y14end, font_name="ArialNarrowBold", font_size=11)
        
        input_date = datetime.today() 
        start_date, end_date = get_date_range(input_date)
        xlstse, ylstse = 184.31, float(reader.pages[1].mediabox.height) - 562.63
        overlay_pasdadad = create_overlay_single(start_date, xlstse, ylstse, font_name="ArialNarrow", font_size=10)
        
        xlstsae, ylstsae = 239.52, float(reader.pages[1].mediabox.height) - 562.63
        overlay_pasdadade = create_overlay_single(end_date, xlstsae, ylstsae, font_name="ArialNarrow", font_size=10)
        # Merge overlays and save final PDF
        first_page = reader.pages[0]
        first_page.merge_page(overlay_pdf1.pages[0])
        first_page.merge_page(overlay_pdf2.pages[0])
        first_page.merge_page(overlay_pdf3.pages[0])
        first_page.merge_page(overlay_pdf4.pages[0])

        secound_page = reader.pages[1]
        secound_page.merge_page(overlay_pdf5.pages[0])
        secound_page.merge_page(overlay_pdf6.pages[0])  
        secound_page.merge_page(overlay_pdf7.pages[0])
        secound_page.merge_page(overlay_pdf8.pages[0])
        secound_page.merge_page(overlay_pdf9.pages[0])
        secound_page.merge_page(overlay_pdf10.pages[0])
        secound_page.merge_page(overlay_pdf11.pages[0])
        # secound_page.merge_page(overlay_pdf11_over.pages[0])
        # secound_page.merge_page(overlay_pdf11_over2.pages[0])
        secound_page.merge_page(overlay_pdf12.pages[0])
        secound_page.merge_page(overlay_pdf13.pages[0])
        secound_page.merge_page(overlay_pdf14.pages[0])
        secound_page.merge_page(overlay_pdf14end.pages[0])
        secound_page.merge_page(overlay_pasdadad.pages[0])
        secound_page.merge_page(overlay_pasdadade.pages[0])


        writer.add_page(first_page)
        writer.add_page(secound_page)

        with open(output_pdf_path, "wb") as temp_pdf:
            writer.write(output_pdf_path)
        
        messagebox.showinfo("Success", f" PDF saved as {output_pdf_path}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to create PDF: {e}")

# Function to format the code
def format_code(code):
    digits_only = ''.join(filter(str.isdigit, code))
    if len(digits_only) < 15:
        raise ValueError("Code is too short or invalid. Please enter a valid 15-digit code.")
    return f"{digits_only[0]} {digits_only[1:3]} {digits_only[3:5]} {digits_only[5:7]} {digits_only[7:10]} {digits_only[10:13]} {digits_only[13:15]}"
from dateutil.relativedelta import relativedelta

def get_date_range(input_date):
    # Adjust the start date to the 1st of the previous month if day < 15
    if input_date.day < 15:
        input_date -= relativedelta(months=1)
    start_date = input_date.replace(day=1)

    # Set end date to one year later
    end_date = start_date + relativedelta(years=1, days=-1)

    # Convert dates to strings
    start_date_str = start_date.strftime("%d/%m/%Y")
    end_date_str = end_date.strftime("%d/%m/%Y")
    return start_date_str, end_date_str

# GUI Application using Tkinter
root = tk.Tk()
root.title("PDF Modifier")
root.geometry("400x600")
root.configure(bg="#f0f0f0")

# Title Frame
title_frame = tk.LabelFrame(root, text="PDF Information", padx=10, pady=10, bg="#f0f0f0")
title_frame.pack(pady=10, padx=20, fill="both")

# Title Dropdown
tk.Label(title_frame, text="Title (M./Mme):", bg="#f0f0f0").grid(row=0, column=0, sticky="w", pady=5)
title_var = tk.StringVar()
title_combo = ttk.Combobox(title_frame, textvariable=title_var, state="readonly", width=10)
title_combo['values'] = ("M.", "Mme")
title_combo.current(0)
title_combo.grid(row=0, column=1, sticky="w", pady=5)

# Input Fields
tk.Label(title_frame, text="First Name:", bg="#f0f0f0").grid(row=1, column=0, sticky="w", pady=5)
first_name_entry = tk.Entry(title_frame, width=30) 
first_name_entry.grid(row=1, column=1, sticky="w", pady=5)

tk.Label(title_frame, text="Second Name:", bg="#f0f0f0").grid(row=2, column=0, sticky="w", pady=5)
second_name_entry = tk.Entry(title_frame, width=30) 
second_name_entry.grid(row=2, column=1, sticky="w", pady=5)

tk.Label(title_frame, text="Birthday (DD/MM/YYYY):", bg="#f0f0f0").grid(row=3, column=0, sticky="w", pady=5)
birthday_entry = tk.Entry(title_frame, width=30) 
birthday_entry.grid(row=3, column=1, sticky="w", pady=5)
tk.Label(title_frame, text="Code:", bg="#f0f0f0").grid(row=4, column=0, sticky="w", pady=5)
code_entry = tk.Entry(title_frame, width=30) 
code_entry.grid(row=4, column=1, sticky="w", pady=5)

tk.Label(title_frame, text="Address:", bg="#f0f0f0").grid(row=5, column=0, sticky="w", pady=5)
address_entry = tk.Entry(title_frame, width=30)  # Adjust the width as needed
address_entry.grid(row=5, column=1, sticky="w", pady=5)


tk.Label(title_frame, text="Type Number:", bg="#f0f0f0").grid(row=6, column=0, sticky="w", pady=5)
type_number_entry = tk.Entry(title_frame, width=30) 
type_number_entry.grid(row=6, column=1, sticky="w", pady=5)

# Generate PDF Button=
def validate_date(date_str):
    try:
        parsed_date = datetime.strptime(date_str, "%d/%m/%Y")
        return parsed_date
    except ValueError:
        return None

def on_submit():
    title = title_var.get().strip()
    first_name = first_name_entry.get()
    second_name = second_name_entry.get()
    user_birthday = birthday_entry.get().strip()
    address = address_entry.get()
    user_input_code = code_entry.get().strip()
    type_number = type_number_entry.get().strip()

    # Validate birthday
    parsed_birthday = validate_date(user_birthday)
    if not parsed_birthday:
        messagebox.showerror("Invalid Input", "Invalid birthday format. Please use DD/MM/YYYY.")
        return

    # Pass parsed birthday as `datetime` to avoid further parsing issues
    create_pdf(title, first_name, second_name, address, user_input_code, parsed_birthday.strftime("%d/%m/%Y"), type_number)


generate_button = tk.Button(root, text="Generate PDF", command=on_submit, bg="#4CAF50", fg="white", padx=10, pady=5)
generate_button.pack(pady=10)

root.mainloop()
