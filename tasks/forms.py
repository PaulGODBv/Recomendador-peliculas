from django.forms import ModelForm
from .models import Task

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']

        #Aqui empieza la modi
from django import forms
from .models import Reseña

class ReseñaForm(forms.ModelForm):
    class Meta:
        model = Reseña
        fields = ['pelicula', 'comentario']  # ❌ Eliminamos 'calificacion'
        widgets = {
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe tu reseña aquí...'}),
        }

        #Aqui acaba