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
from .models import *


# Create your views here.
def index(request):
    return render(request,'frontend/index.html')



def createBooking(request):
    if request.method == "POST":
        # Booking info
        booking_name = request.POST.get('booking_name')
        phone        = request.POST.get('phone')
        location     = request.POST.get('location')
        date         = request.POST.get('date')

        # Guests info
        persons = request.POST.getlist('person_name[]')
        rides   = request.POST.getlist('person_ride[]')

        if not booking_name or not phone or not location or not date:
            messages.error(request, "Booking details missing!")
            return redirect('index')
        if not persons or not rides:
            messages.error(request, "No guests added!")
            return redirect('index')

        # Create Booking record
        booking = Booking.objects.create(
            booking_name=booking_name,
            phone=phone,
            location=location,
            date=date
        )

        # Create Guest records
        guests  = []
        for name, ride in zip(persons, rides):
            guest = Guest.objects.create(
                booking=booking,
                person_name=name,
                ride=ride
            )
            guests.append(guest)

        # Generate PDF
        buffer  = BytesIO()
        c       = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        for guest in guests:
            c.setFont("Helvetica-Bold", 24)
            c.drawCentredString(width/2, height-4*cm, f"Booking: {booking.booking_name}")
            c.setFont("Helvetica", 18)
            c.drawCentredString(width/2, height-5*cm, f"Name: {guest.person_name}")
            c.drawCentredString(width/2, height-6*cm, f"Ride: {guest.ride}")
            c.drawCentredString(width/2, height-7*cm, f"Phone: {booking.phone}")
            c.drawCentredString(width/2, height-8*cm, f"Location: {booking.location}")
            c.drawCentredString(width/2, height-9*cm, f"Date: {booking.date}")

            qr_img = qrcode.make(f"{booking.booking_name} - {guest.person_name} - {guest.ride}")
            c.drawInlineImage(qr_img, width/2 - 4*cm, height/2 - 4*cm, 8*cm, 8*cm)
            c.showPage()

        c.save()
        buffer.seek(0)

        # Save PDF
        filename  = f"booking_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        file_path = os.path.join(settings.MEDIA_ROOT, 'bookings', filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as f:
            f.write(buffer.getvalue())
        buffer.close()

        download_url    = settings.MEDIA_URL + 'bookings/' + filename
        messages.success(request, f"Booking PDF generated successfully! <a href='{download_url}' target='_blank'>Download here</a>")

        return redirect('index')

    return redirect('index')