from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from bs4 import BeautifulSoup
import requests
from urllib.parse import quote_plus
from .forms import ScraperForm


@login_required
def buscar(request):
    form = ScraperForm()
    resultados = None
    error = None

    if request.method == "POST" and "buscar" in request.POST:
        form = ScraperForm(request.POST)

        if form.is_valid():
            termino = form.cleaned_data["palabra_clave"].strip()

            try:
                termino_url = quote_plus(termino)
                url = f"https://es.wikipedia.org/wiki/{termino_url}"

                page = requests.get(url)
                soup = BeautifulSoup(page.text, "html.parser")

                first_para = None
                for p in soup.select("p"):
                    texto = p.get_text(strip=True)
                    if texto:
                        first_para = texto
                        break

                if not first_para:
                    first_para = "No se encontró contenido."

                secciones = [h.text.strip() for h in soup.select("h2 span.mw-headline")]

                resultados = {
                    "termino": termino,
                    "url": url,
                    "first_para": first_para,
                    "secciones": secciones,
                }

            except Exception as e:
                error = f"Error al obtener resultados: {e}"

    return render(request, "scraper/buscar.html", {
        "form": form,
        "resultados": resultados,
        "error": error,
    })


@login_required
def enviar_resultados(request):
    if request.method == "POST":
        termino = request.POST.get("termino")
        first_para = request.POST.get("first_para")
        secciones = request.POST.getlist("secciones")

        contenido = f"""
Resultados para: {termino}

Primer párrafo:
{first_para}

Secciones:
- """ + "\n- ".join(secciones)

        send_mail(
            subject=f"Resultados del scraping: {termino}",
            message=contenido,
            from_email="no-reply@miapp.com",
            recipient_list=[request.user.email],
        )

        return render(request, "scraper/buscar.html", {
            "form": ScraperForm(),
            "mensaje": "Correo enviado correctamente.",
        })

    return redirect("buscar")
