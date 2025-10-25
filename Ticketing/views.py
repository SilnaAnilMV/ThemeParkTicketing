from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
import qrcode
from datetime import datetime
import os
from django.conf import settings

# Create your views here.
def index(request):
    return render(request,'frontend/index.html')



def createBooking(request):
    if request.method == "POST":
        persons = request.POST.getlist('person_name[]')
        rides   = request.POST.getlist('person_ride[]')
        guests  = [{"person": name, "ride": ride} for name, ride in zip(persons, rides)]

        # Generate PDF in memory
        buffer  = BytesIO()
        c       = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        for guest in guests:
            name = guest['person']
            ride = guest['ride']

            c.setFont("Helvetica-Bold", 24)
            c.drawCentredString(width/2, height-4*cm, f"Name: {name}")
            c.setFont("Helvetica", 18)
            c.drawCentredString(width/2, height-6*cm, f"Ride: {ride}")

            qr_img = qrcode.make(f"{name} - {ride}")
            c.drawInlineImage(qr_img, width/2 - 4*cm, height/2 - 4*cm, 8*cm, 8*cm)
            c.showPage()

        c.save()
        buffer.seek(0)

        # Save PDF to a temporary file
        filename    = f"booking_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        file_path   = os.path.join(settings.MEDIA_ROOT, 'bookings', filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as f:
            f.write(buffer.getvalue())
        buffer.close()

        # Add success message with download link
        download_url = settings.MEDIA_URL + 'bookings/' + filename
        messages.success(request, f"Booking PDF generated successfully! <a href='{download_url}' target='_blank'>Download here</a>")

        return redirect('index')

    return redirect('index')