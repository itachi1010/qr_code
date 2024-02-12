from django.shortcuts import render, HttpResponse
from .models import QRCode, AccessRecord
import qrcode
from PIL import Image
from io import BytesIO

def get_client_ip(request):
    """Utility function to get the client IP address from Django request object."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def generate_qr(request):
    if request.method == "POST":
        content = request.POST.get('content')
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(content)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buf = BytesIO()
        img.save(buf, format="PNG")
        image_stream = buf.getvalue()

        response = HttpResponse(image_stream, content_type="image/png")

        # Assuming you're creating an AccessRecord instance somewhere here
        ip_address = get_client_ip(request)
        qr_code_instance = QRCode(content=content)  # Assuming you have a QRCode model instance
        qr_code_instance.save()

        # Create AccessRecord with IP address
        AccessRecord.objects.create(qr_code=qr_code_instance, ip_address=ip_address, user_agent=request.META['HTTP_USER_AGENT'])

        return response
    else:
        return render(request, 'qr_generator/generate_qr.html')
