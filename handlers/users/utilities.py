import qrcode
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
import io

async def generate_modern_qr_pdf(link, output_filename="qr_code.pdf"):

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=15,
        border=2,
    )
    qr.add_data(link)
    qr.make(fit=True)
    
    # QR code rasmini yaratish (oq-qora)
    qr_img = qr.make_image(fill_color="#1a1a2e", back_color="white")
    
    # Yangi rasm yaratish (zamonaviy dizayn uchun)
    width, height = 800, 1000
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Gradient background (yuqoridan pastga)
    for i in range(height):
        # Och ko'k dan oq rangga gradient
        ratio = i / height
        r = int(240 + (255 - 240) * ratio)
        g = int(248 + (255 - 248) * ratio)
        b = int(255)
        draw.rectangle([(0, i), (width, i + 1)], fill=(r, g, b))
    
    # QR code ni markazga joylashtirish
    qr_size = 500
    qr_img = qr_img.resize((qr_size, qr_size))
    qr_position = ((width - qr_size) // 2, 200)
    
    # Oq fon bilan QR code uchun joy
    padding = 30
    shadow_offset = 8
    
    # Shadow effekt
    draw.rounded_rectangle(
        [qr_position[0] - padding + shadow_offset, 
         qr_position[1] - padding + shadow_offset,
         qr_position[0] + qr_size + padding + shadow_offset,
         qr_position[1] + qr_size + padding + shadow_offset],
        radius=20,
        fill=(200, 200, 200, 100)
    )
    
    # Oq fon
    draw.rounded_rectangle(
        [qr_position[0] - padding, 
         qr_position[1] - padding,
         qr_position[0] + qr_size + padding,
         qr_position[1] + qr_size + padding],
        radius=20,
        fill='white'
    )
    
    # QR code ni joylashtirish
    img.paste(qr_img, qr_position)
    
    # Matn qo'shish
    try:
        # Katta shrift uchun
        font_large = ImageFont.truetype("arial.ttf", 60)
        font_small = ImageFont.truetype("arial.ttf", 30)
    except:
        # Agar arial topilmasa, default font
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # "SCAN ME" matni
    scan_text = "SCAN ME"
    bbox = draw.textbbox((0, 0), scan_text, font=font_large)
    text_width = bbox[2] - bbox[0]
    text_x = (width - text_width) // 2
    
    # Matn uchun gradient effekt (qo'shimcha bezak)
    draw.text((text_x, 100), scan_text, fill='#1a1a2e', font=font_large)
    
    # Pastda qo'shimcha matn
    instruction_text = "Point your camera at the QR code"
    bbox = draw.textbbox((0, 0), instruction_text, font=font_small)
    text_width = bbox[2] - bbox[0]
    text_x = (width - text_width) // 2
    draw.text((text_x, 750), instruction_text, fill='#555555', font=font_small)
    
    # Dekorativ elementlar
    # Yuqori chap burchakda kichik doira
    draw.ellipse([30, 30, 80, 80], fill='#6c5ce7', outline='#a29bfe', width=3)
    # Yuqori o'ng burchakda
    draw.ellipse([width-80, 30, width-30, 80], fill='#00b894', outline='#55efc4', width=3)
    # Pastki chap
    draw.ellipse([30, height-80, 80, height-30], fill='#fd79a8', outline='#fdcb6e', width=3)
    # Pastki o'ng
    draw.ellipse([width-80, height-80, width-30, height-30], fill='#74b9ff', outline='#a29bfe', width=3)
    
  
    pdf_canvas = canvas.Canvas(output_filename, pagesize=A4)
    a4_width, a4_height = A4
    
    # Rasmni BytesIO ga saqlash
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    
    # Rasmni PDF ga markazlashtirish
    img_reader = ImageReader(img_buffer)
    
    # A4 ga mos ravishda o'lchamini sozlash
    aspect = width / height
    if aspect > 1:
        img_width = a4_width * 0.8
        img_height = img_width / aspect
    else:
        img_height = a4_height * 0.9
        img_width = img_height * aspect
    
    x = (a4_width - img_width) / 2
    y = (a4_height - img_height) / 2
    
    pdf_canvas.drawImage(img_reader, x, y, width=img_width, height=img_height)
    pdf_canvas.save()
    
    print(f"✅ QR code muvaffaqiyatli yaratildi: {output_filename}")
    print(f"📱 Link: {link}")
    return output_filename


