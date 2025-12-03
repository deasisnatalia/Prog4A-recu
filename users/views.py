from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from .forms import RegistroForm

def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            send_mail(
                "Bienvenido",
                "Gracias por registrarte!",
                "admin@example.com",
                [user.email],
                fail_silently=True
            )

            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, "users/registro.html", {'form': form})
