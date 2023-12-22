import os
import io
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

current_folder = os.path.dirname (__file__)
input_folder = os.path.join (current_folder, "Input")
output_folder = os.path.join (current_folder, "Output")
fonts_folder = os.path.join (current_folder, "Fonts")
font_roboto = os.path.join (fonts_folder, "Roboto-Regular.ttf")
font_roboto_medium = os.path.join (fonts_folder, "Roboto-Medium.ttf")
font_roboto_bold = os.path.join (fonts_folder, "Roboto-Bold.ttf")
original_pdf = os.path.join (input_folder, f"template.pdf")

def generatePDF(name, address, postal_code, city, country, phone, description, value, subtotal, sale_number, date):
    packet = io.BytesIO()

    pdfmetrics.registerFont(TTFont('roboto',font_roboto))
    pdfmetrics.registerFont(TTFont('roboto-medium',font_roboto_medium))
    pdfmetrics.registerFont(TTFont('roboto-bold',font_roboto_bold))

    c = canvas.Canvas(packet, letter)

    #Página 1
    c.setFont('roboto-medium', 12)
    c.drawString(205, 767, sale_number)
    c.drawString(330, 508, name)
    c.drawString(330, 470, address)
    c.drawString(330, 432, postal_code)
    c.drawString(454, 432, city)
    c.drawString(330, 393, country)
    c.drawString(484, 393, phone)
    c.drawString(38, 305, description)
    c.drawString(472, 305, value)
    c.drawString(525, 305, subtotal)

    c.showPage()

    c.setFont('roboto-medium', 12)
    c.drawString(468, 160, date)
    c.showPage()
    
    c.save()

    packet.seek(0)

    new_pdf = PdfFileReader(packet)
    
    existing_pdf = PdfFileReader(open(original_pdf, "rb"))
    output = PdfFileWriter()
    
    page = existing_pdf.pages[0]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)
    page=existing_pdf.pages[1]
    page.merge_page(new_pdf.pages[1])
    output.add_page(page)

    new_pdf = os.path.join (output_folder, f"Invoice {sale_number}.pdf")
    output_stream = open(new_pdf, "wb")
    output.write(output_stream)
    output_stream.close()


  
name = "Ja'waun Jones"
address = "1009 Private Rd 2913" 
postal_code = "65257" 
city = "Higbee" 
country = "USA" 
phone = "6602771577"
description = "Electronic for virtual reality"
value = "302,00 €" 
subtotal = "302,00 €" 
sale_number = "490"
date = "21/12/2023"

generatePDF(name, address, postal_code, city, country, phone, description, value, subtotal, sale_number, date)
