import telebot
from telebot import types
import os
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
from io import BytesIO
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
import io
import logging

logging.basicConfig(level=logging.DEBUG, filename="bot_debug.log", filemode="w", format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize the bot with your token
BOT_TOKEN = "7718033282:AAGFpbL5R70qISG2aWS5FtcMBuHeCGXnhSY"
bot = telebot.TeleBot(BOT_TOKEN)

# Register fonts
base_path = os.path.dirname(__file__)
pdfmetrics.registerFont(TTFont('Arial', os.path.join(base_path, 'Arial.ttf')))
pdfmetrics.registerFont(TTFont('ArialNarrow', os.path.join(base_path, 'arialnarrow.ttf')))
pdfmetrics.registerFont(TTFont('ArialNarrowBold', os.path.join(base_path, 'arialnarrow_bold.ttf')))

# Store user data temporarily
user_data = {}
def create_overlay_single(text, x, y, font_name="Arial", font_size=11):
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=letter, invariant=1)
    can.setFont(font_name, font_size)
    can.drawString(x, y, text)
    can.save()
    packet.seek(0)
    return PdfReader(packet)
# Function to validate and format date
def create_pdf(title, first_name, second_name, address_line, user_input_code, user_birthday, user_input_value):
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
        
        return output_pdf_path

# Function to format the code
def format_code(code):
    digits_only = ''.join(filter(str.isdigit, code))
    if len(digits_only) < 15:
        raise ValueError("Code is too short or invalid. Please enter a valid 15-digit code.")
    return f"{digits_only[0]} {digits_only[1:3]} {digits_only[3:5]} {digits_only[5:7]} {digits_only[7:10]} {digits_only[10:13]} {digits_only[13:15]}"
from dateutil.relativedelta import relativedelta
def validate_date(date_str):
    try:
        parsed_date = datetime.strptime(date_str, "%d/%m/%Y")
        return parsed_date
    except ValueError:
        return None
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

# Bot Handlers
@bot.message_handler(commands=['start'])
def start_command(message):
    chat_id = message.chat.id
    logging.debug(f"Starting interaction with chat_id: {chat_id}")
    if chat_id not in user_data:
        logging.debug(f"Initializing user_data for chat_id: {chat_id}")
        user_data[chat_id] = {}
    bot.send_message(chat_id, "Welcome! Let's create your PDF. Please enter your title (M or Mme):")
    bot.register_next_step_handler(message, validate_title)

@bot.message_handler(func=lambda message: message.chat.id in user_data)
@bot.message_handler(func=lambda message: message.chat.id in user_data)
def handle_user_input(message):
    chat_id = message.chat.id
    if chat_id not in user_data:  # Fallback initialization
        user_data[chat_id] = {}
    data = user_data[chat_id]
    text = message.text.strip()

    if 'Title' not in data:
        validate_title(message)
    elif 'First Name' not in data:
        validate_first_name(message)
    elif 'Second Name' not in data:
        validate_second_name(message)
    elif 'Birthday' not in data:
        validate_birthday(message)
    elif 'Code' not in data:
        validate_code(message)
    elif 'Address' not in data:
        validate_address(message)
    elif 'Type Number' not in data:
        validate_type_number(message)


# Validation for title
def validate_title(message):
    chat_id = message.chat.id
    text = message.text.strip()

    if text in ["M", "Mme"]:
        user_data[chat_id]['Title'] = text
        bot.send_message(chat_id, "Enter your First Name:")
    else:
        bot.send_message(chat_id, "Invalid title. Please enter 'M.' or 'Mme' (exactly):")

# Validation for first name
def validate_first_name(message):
    chat_id = message.chat.id
    text = message.text.strip()

    if text.isalpha():
        user_data[chat_id]['First Name'] = text
        bot.send_message(chat_id, "Enter your Second Name:")
    else:
        bot.send_message(chat_id, "Invalid name. Please enter alphabetic characters only.")

# Validation for second name
def validate_second_name(message):
    chat_id = message.chat.id
    text = message.text.strip()

    if text.isalpha():
        user_data[chat_id]['Second Name'] = text
        bot.send_message(chat_id, "Enter your Birthday (DD/MM/YYYY):")
    else:
        bot.send_message(chat_id, "Invalid name. Please enter alphabetic characters only.")

# Validation for birthday
def validate_birthday(message):
    chat_id = message.chat.id
    text = message.text.strip()
    parsed_birthday = validate_date(text)

    if parsed_birthday:
        user_data[chat_id]['Birthday'] = parsed_birthday.strftime("%d/%m/%Y")
        bot.send_message(chat_id, "Enter your Code:")
    else:
        bot.send_message(chat_id, "Invalid date format. Please use DD/MM/YYYY.")

# Validation for code (must be 15 digits)
def validate_code(message):
    chat_id = message.chat.id
    text = message.text.strip()

    if text.isdigit() and len(text) == 15:
        user_data[chat_id]['Code'] = text
        bot.send_message(chat_id, "Enter your Address:")
    else:
        bot.send_message(chat_id, "Invalid code. Please enter exactly 15 digits.")

# Validation for address
def validate_address(message):
    chat_id = message.chat.id
    text = message.text.strip()

    if len(text) > 0:  # Allow any non-empty address
        user_data[chat_id]['Address'] = text
        bot.send_message(chat_id, "Enter your Type Number:")
    else:
        bot.send_message(chat_id, "Invalid address. Please enter a valid address.")

# Validation for type number
def validate_type_number(message):
    chat_id = message.chat.id
    if chat_id not in user_data:
        logging.warning(f"chat_id {chat_id} not found in user_data during validate_type_number.")
        user_data[chat_id] = {}  # Fallback initialization
    data = user_data[chat_id]
    text = message.text.strip()

    if len(text) > 0:  # Allow any non-empty type number
        data['Type Number'] = text
        bot.send_message(chat_id, "Generating your PDF, please wait...")
        generate_pdf_and_send(chat_id)
    else:
        bot.send_message(chat_id, "Invalid type number. Please enter a valid type number.")



 

    if 'Title' not in data:
        data['Title'] = text
        bot.send_message(chat_id, "Enter your First Name:")
    elif 'First Name' not in data:
        data['First Name'] = text
        bot.send_message(chat_id, "Enter your Second Name:")
    elif 'Second Name' not in data:
        data['Second Name'] = text
        bot.send_message(chat_id, "Enter your Birthday (DD/MM/YYYY):")
    elif 'Birthday' not in data:
        parsed_birthday = validate_date(text)
        if parsed_birthday:
            data['Birthday'] = parsed_birthday.strftime("%d/%m/%Y")
            bot.send_message(chat_id, "Enter your Code:")
        else:
            bot.send_message(chat_id, "Invalid date format. Please use DD/MM/YYYY.")
    elif 'Code' not in data:
        data['Code'] = text
        bot.send_message(chat_id, "Enter your Address:")
    elif 'Address' not in data:
        data['Address'] = text
        bot.send_message(chat_id, "Enter your Type Number:")
    elif 'Type Number' not in data:
        data['Type Number'] = text
        bot.send_message(chat_id, "Generating your PDF, please wait...")
        generate_pdf_and_send(chat_id)

def generate_pdf_and_send(chat_id):
    try:
        data = user_data[chat_id]
        pdf_path = create_pdf(
            title=data['Title'],
            first_name=data['First Name'],
            second_name=data['Second Name'],
            address_line=data['Address'],
            user_input_code=data['Code'],
            user_birthday=data['Birthday'],
            user_input_value=data['Type Number']
        )
        with open(pdf_path, 'rb') as pdf_file:
            bot.send_document(chat_id, pdf_file)
        os.remove(pdf_path)
    except Exception as e:
        bot.send_message(chat_id, f"Error: {e}")
    finally:
        # Ensure user data is deleted even if an error occurs
        if chat_id in user_data:
            del user_data[chat_id]


# Start the bot
if __name__ == "__main__":
    bot.polling()
