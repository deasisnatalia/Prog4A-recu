from django import forms

class ScraperForm(forms.Form):
    palabra_clave = forms.CharField(
        label="Buscar palabra",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej: Argentina"})
    )
