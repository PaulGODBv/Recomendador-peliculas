from django.db import models
from django.contrib.auth.models import User
#Aqui empieza la modi
from django.db import models
import uuid

class Pelicula(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(null=True, blank=True)
    imagen = models.URLField(default="https://via.placeholder.com/150")  # Agrega un valor por defecto


class Reseña(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # ID aleatorio único
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    comentario = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Fecha automática al crear


class Calificacion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # ID aleatorio único
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    calificacion = models.IntegerField(choices=[(i, str(i)) for i in range(1, 11)])

class Favorito(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # ID aleatorio único
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    from django.db import models

class Interaccion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # Referencia al usuario de Django
    pelicula_id = models.CharField(max_length=100)  # Ahora puede ser un ID de la BD o un UUID
    accion = models.CharField(max_length=20, choices=[("reseñar", "Reseñar"), ("calificar", "Calificar"), ("guardar", "Guardar")])
    reseña = models.TextField(blank=True, null=True)
    calificacion = models.IntegerField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)  # Fecha automática al crear

    def __str__(self):
        username = self.user.username if self.user else "Usuario desconocido"
        return f"{username} - {self.pelicula_id} - {self.accion}"



#Aqui acaba
class Task(models.Model):
  title = models.CharField(max_length=200)
  description = models.TextField(max_length=1000)
  created = models.DateTimeField(auto_now_add=True)
  datecompleted = models.DateTimeField(null=True, blank=True)
  important = models.BooleanField(default=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.title + ' - ' + self.user.username
  
class Usuario(models.Model):
    nombre = models.CharField(max_length=255)
    correo = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=255)
    generos_favoritos = models.ManyToManyField('Genero', blank=True)

    def __str__(self):
        return self.nombre

class Genero(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.nombre


class HistorialBusqueda(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    termino_busqueda = models.CharField(max_length=255)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.nombre} - {self.termino_busqueda}"

class Favoritos(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.nombre} - {self.pelicula.titulo}"

class Recomendacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    fecha_generada = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.nombre} - {self.pelicula.titulo}"

