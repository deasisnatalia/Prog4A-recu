from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Alumno
from django.http import HttpResponse
import csv
from io import BytesIO
from reportlab.pdfgen import canvas
from django.core.mail import EmailMessage

@login_required
def dashboard(request):
    alumnos = Alumno.objects.filter(user=request.user)
    return render(request, "alumnos/dashboard.html", {'alumnos': alumnos})

@login_required
def crear_alumno(request):
    if request.method == "POST":
        Alumno.objects.create(
            user=request.user,
            nombre=request.POST["nombre"],
            apellido=request.POST["apellido"],
            nota=request.POST["nota"],
        )
        return redirect("dashboard")
    return render(request, "alumnos/crear.html")

@login_required
def generar_pdf(request, alumno_id):
    alumno = Alumno.objects.get(id=alumno_id, user=request.user)

    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 800, f"Alumno: {alumno.nombre} {alumno.apellido}")
    p.drawString(100, 780, f"Nota: {alumno.nota}")
    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()

    email = EmailMessage(
        "PDF Alumno",
        "Adjunto el PDF del alumno",
        "admin@example.com",
        [request.user.email],
    )
    email.attach("alumno.pdf", pdf, "application/pdf")
    try:
        email.send()
        return HttpResponse("PDF enviado correctamente")
    except:
        response = HttpResponse(pdf, content_type="application/pdf")
        response['Content-Disposition'] = 'attachment; filename="alumno.pdf"'
        return response
    
@login_required
def exportar_csv(request):
    alumnos = Alumno.objects.filter(user=request.user)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="alumnos.csv"'

    writer = csv.writer(response)
    writer.writerow(['nombre', 'apellido', 'nota'])

    for a in alumnos:
        writer.writerow([a.nombre, a.apellido, a.nota])

    return response