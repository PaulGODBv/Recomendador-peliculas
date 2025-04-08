from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Task

from .forms import TaskForm

# Create your views here.

def signup(request):
    if request.method == 'GET':
        form = UserCreationForm()
        return render(request, 'signup.html', {"form": form})
    else:
        try:
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('tasks')
            else:
                return render(request, 'signup.html', {"form": form, "error": "Error en el registro. Revisa los datos ingresados."})
        except Exception as e:
            print(f"Error en el registro: {e}")  # Para depuración
            return render(request, 'signup.html', {"form": UserCreationForm(), "error": f"Error inesperado: {e}"})


@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {"tasks": tasks})

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {"tasks": tasks})


@login_required
def create_task(request):
    if request.method == "GET":
        return render(request, 'create_task.html', {"form": TaskForm})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {"form": TaskForm, "error": "Error creating task."})


def home(request):
    # Si el usuario está autenticado, mostrar recomendaciones personalizadas
    if request.user.is_authenticated:
        try:
            # Intentar obtener películas de la base de datos
            peliculas = Pelicula.objects.all()[:3]  # Limitar a 3 películas para la demostración
            
            # Si no hay películas en la base de datos, usar valores predeterminados
            if not peliculas:
                recomendaciones = None  # La plantilla ya tiene películas de muestra
            else:
                # Convertir objetos Pelicula a diccionarios para la plantilla
                recomendaciones = []
                for pelicula in peliculas:
                    recomendaciones.append({
                        'id': pelicula.id,
                        'titulo': pelicula.titulo,
                        'descripcion': pelicula.descripcion,
                        'imagen_url': pelicula.imagen_url
                    })
                
            return render(request, 'home.html', {'recomendaciones': recomendaciones})
        except Exception as e:
            # En caso de error, renderizar sin recomendaciones
            return render(request, 'home.html')
    else:
        # Para usuarios no autenticados, solo mostrar la página de inicio
        return render(request, 'home.html')


@login_required
def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        return render(request, 'signin.html', {"form": form})
    else:
        try:
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('tasks')
            else:
                return render(request, 'signin.html', {"form": form, "error": "Usuario o contraseña incorrectos."})
        except Exception as e:
            print(f"Error en el inicio de sesión: {e}")  # Para depuración
            return render(request, 'signin.html', {"form": AuthenticationForm(), "error": f"Error inesperado: {e}"})

@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task': task, 'form': form, 'error': 'Error updating task.'})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
    
def seleccionar_generos(request):
    return render(request, 'generos.html')

def generos (request):
    
    return render(request, 'generos.html')

@login_required
def recomendaciones (request):
    # Obtener películas de la base de datos o usar valores predeterminados
    try:
        # Intentar obtener películas de la base de datos
        peliculas = Pelicula.objects.all()[:3]  # Limitar a 3 películas para la demostración
        
        # Si no hay películas en la base de datos, crear recomendaciones predeterminadas
        if not peliculas:
            recomendaciones = [
                {
                    'id': 'default-11',
                    'titulo': 'Buscando a Nemo',
                    'descripcion': 'Un pez payaso sobreprotector que, junto a un pez cirujano con pérdida de memoria, busca a su hijo capturado.',
                    'imagen': 'https://m.media-amazon.com/images/I/81montw1gVL._AC_UF1000,1000_QL80_.jpg'
                },
                {
                    'id': 'default-12',
                    'titulo': 'Parasitos',
                    'descripcion': 'Una familia pobre se infiltra en el servicio de una familia rica, con consecuencias inesperadas.',
                    'imagen': 'https://pics.filmaffinity.com/Parasite-406070218-large.jpg'
                },
                {
                    'id': 'default-13',
                    'titulo': 'Spiderman into the Spiderverse',
                    'descripcion': 'Miles Morales se convierte en Spider-Man y conoce a otros Spider-People de diferentes dimensiones.',
                    'imagen': 'https://m.media-amazon.com/images/I/A1GbxGqXCxL._AC_UF1000,1000_QL80_.jpg'
                }
            ]
        else:
            # Convertir objetos Pelicula a diccionarios para la plantilla
            recomendaciones = []
            for pelicula in peliculas:
                recomendaciones.append({
                    'id': pelicula.id,
                    'titulo': pelicula.titulo,
                    'descripcion': pelicula.descripcion,
                    'imagen': pelicula.imagen_url
                })
    except Exception as e:
        # En caso de error, usar recomendaciones predeterminadas
        recomendaciones = [
            {
                'id': 'default-11',
                'titulo': 'Buscando a Nemo',
                'descripcion': 'Un pez payaso sobreprotector que, junto a un pez cirujano con pérdida de memoria, busca a su hijo capturado.',
                'imagen': 'https://m.media-amazon.com/images/I/81montw1gVL._AC_UF1000,1000_QL80_.jpg'
            },
            {
                'id': 'default-12',
                'titulo': 'Parasitos',
                'descripcion': 'Una familia pobre se infiltra en el servicio de una familia rica, con consecuencias inesperadas.',
                'imagen': 'https://pics.filmaffinity.com/Parasite-406070218-large.jpg'
            },
            {
                'id': 'default-13',
                'titulo': 'Spiderman into the Spiderverse',
                'descripcion': 'Miles Morales se convierte en Spider-Man y conoce a otros Spider-People de diferentes dimensiones.',
                'imagen': 'https://m.media-amazon.com/images/I/A1GbxGqXCxL._AC_UF1000,1000_QL80_.jpg'
            }
        ]
    
    return render(request, 'recomendaciones.html', {
        'recomendaciones': recomendaciones
    })

@login_required
def peliculasFavoritas(request):
    # Obtener todas las películas para el selector
    todas_peliculas = []
    try:
        todas_peliculas = Pelicula.objects.all()
    except:
        pass  # Si hay error, el selector usará las películas por defecto
    
    # Obtener las películas favoritas del usuario actual
    peliculas_favoritas = []
    
    # Diccionario para mapear IDs por defecto a información de películas
    titulos_muestra = {
        'default-1': 'Interestelar',
        'default-2': 'Titanic',
        'default-3': 'El Padrino',
        'default-4': 'El Diario de Noah',
        'default-5': 'Bajo la misma estrella',
        'default-6': 'El Conjuro',
        'default-7': 'El Resplandor',
        'default-8': 'It',
        'default-9': 'Matrix',
        'default-10': 'Blade Runner 2049',
        'default-11': 'Buscando a Nemo',
        'default-12': 'Parasitos',
        'default-13': 'Spiderman into the Spiderverse'
    }
    
    try:
        # Obtener interacciones de tipo 'guardar' para el usuario actual
        favoritos = Interaccion.objects.filter(
            user=request.user,
            accion='guardar'
        ).order_by('-fecha_creacion')  # Ordenar por fecha, más recientes primero
        
        # Para cada favorito, obtener los detalles de la película
        for favorito in favoritos:
            pelicula_data = {
                'id': favorito.pelicula_id,
                'titulo': 'Película Desconocida',
                'fecha_agregado': favorito.fecha_creacion
            }
            
            # Si es una película por defecto
            if favorito.pelicula_id.startswith('default-'):
                pelicula_data['titulo'] = titulos_muestra.get(favorito.pelicula_id, 'Película Desconocida')
            else:
                # Intentar obtener la película de la base de datos
                try:
                    if favorito.pelicula_id.isdigit():
                        pelicula = Pelicula.objects.get(id=int(favorito.pelicula_id))
                        pelicula_data['titulo'] = pelicula.titulo
                except (Pelicula.DoesNotExist, ValueError):
                    pass  # Mantener el título por defecto
            
            peliculas_favoritas.append(pelicula_data)
    
    except Exception as e:
        messages.error(request, f"Error al cargar favoritos: {str(e)}")
    
    return render(request, 'peliculasFavoritas.html', {
        'peliculas': todas_peliculas,  # Para el selector de películas
        'favoritos': peliculas_favoritas  # Lista de películas favoritas del usuario
    })

# This duplicate home function has been removed to avoid confusion
# The enhanced version at the top of the file is now the only home function

#Aqui empieza la modi
import uuid
from django.shortcuts import render, redirect
from datetime import datetime
from .models import Interaccion, Reseña, Pelicula, Calificacion, Favorito, Favoritos
from django.contrib import messages

def guardar_interaccion(request):
    if request.method == 'POST':
        pelicula_id = request.POST.get('pelicula')
        accion = request.POST.get('accion')
        usuario_id = request.user.id  # Get the logged in user
        
        try:
            # Verificar si es un ID por defecto (default-1, default-2, etc.)
            if pelicula_id.startswith('default-'):
                # Usar películas de muestra
                titulos_muestra = {
                    'default-1': 'Interestelar',
                    'default-2': 'Titanic',
                    'default-3': 'El Padrino',
                    'default-4': 'El Diario de Noah',
                    'default-5': 'Bajo la misma estrella',
                    'default-6': 'El Conjuro',
                    'default-7': 'El Resplandor',
                    'default-8': 'It',
                    'default-9': 'Matrix',
                    'default-10': 'Blade Runner 2049',
                    'default-11': 'Buscando a Nemo',
                    'default-12': 'Parasitos',
                    'default-13': 'Spiderman into the Spiderverse'
                }
                titulo_pelicula = titulos_muestra.get(pelicula_id, 'Película Desconocida')
                
                # Registrar directamente en la tabla de interacciones
                nueva_interaccion = Interaccion(
                    user=request.user,
                    pelicula_id=pelicula_id,
                    accion=accion,
                    reseña=request.POST.get('reseña', ''),
                    calificacion=request.POST.get('calificacion', None)
                )
                nueva_interaccion.save()
            else:
                # Intentar obtener la película de la base de datos
                try:
                    pelicula = Pelicula.objects.get(id=pelicula_id)
                    
                    if accion == 'reseñar':
                        # Guardar reseña
                        comentario = request.POST.get('reseña')
                        nueva_reseña = Reseña(
                            pelicula_id=pelicula.id,
                            comentario=comentario,
                            fecha_creacion=datetime.now()
                        )
                        nueva_reseña.save()
                        
                    elif accion == 'calificar':
                        # Guardar calificación
                        calificacion_valor = request.POST.get('calificacion')
                        nueva_calificacion = Calificacion(
                            pelicula_id=pelicula.id,
                            calificacion=calificacion_valor
                        )
                        nueva_calificacion.save()
                        
                    elif accion == 'guardar':
                        # Guardar como favorito
                        nuevo_favorito = Favoritos(
                            pelicula_id=pelicula.id,
                            usuario_id=usuario_id,
                            fecha_agregado=datetime.now()
                        )
                        nuevo_favorito.save()
                    
                    # También registrar en la tabla de interacciones
                    nueva_interaccion = Interaccion(
                        user=request.user,
                        pelicula_id=pelicula_id,
                        accion=accion,
                        reseña=request.POST.get('reseña', ''),
                        calificacion=request.POST.get('calificacion', None)
                    )
                    nueva_interaccion.save()
                
                except Pelicula.DoesNotExist:
                    # Si la película no existe, solo guardar la interacción
                    nueva_interaccion = Interaccion(
                        user=request.user,
                        pelicula_id=pelicula_id,
                        accion=accion,
                        reseña=request.POST.get('reseña', ''),
                        calificacion=request.POST.get('calificacion', None)
                    )
                    nueva_interaccion.save()
            
            # Redirigir con parámetros para mostrar confirmación
            return redirect(f'/peliculasFavoritas?success=true&action={accion}&movie={pelicula_id}')
            
        except Exception as e:
            # Manejar errores
            messages.error(request, f"Error al guardar: {str(e)}")
            return redirect('peliculasFavoritas')
    
    # Si no es POST, redirigir a la página de favoritos
    return redirect('peliculasFavoritas')


#Aqui acaba
@login_required
def reviews_list(request):
    # Obtener las reseñas del usuario actual (interacciones con reseña no vacía)
    reviews = Interaccion.objects.filter(user=request.user).exclude(reseña__isnull=True).exclude(reseña="")
    
    # Crear una lista para almacenar las reseñas con información adicional
    enhanced_reviews = []
    
    # Diccionario para mapear IDs por defecto a títulos de películas
    titulos_muestra = {
        'default-1': 'Interestelar',
        'default-2': 'Titanic',
        'default-3': 'El Padrino',
        'default-4': 'El Diario de Noah',
        'default-5': 'Bajo la misma estrella',
        'default-6': 'El Conjuro',
        'default-7': 'El Resplandor',
        'default-8': 'It',
        'default-9': 'Matrix',
        'default-10': 'Blade Runner 2049',
        'default-11': 'Buscando a Nemo',
        'default-12': 'Parasitos',
        'default-13': 'Spiderman into the Spiderverse'
    }
    
    # Para cada reseña, intentar obtener el título de la película
    for review in reviews:
        # Crear un diccionario con la información de la reseña
        review_data = {
            'id': review.id,
            'pelicula_id': review.pelicula_id,
            'accion': review.accion,
            'reseña': review.reseña,
            'calificacion': review.calificacion,
            'titulo_pelicula': 'Película Desconocida'  # Valor por defecto
        }
        
        # Intentar obtener el título de la película
        if review.pelicula_id.startswith('default-'):
            # Es una película de muestra
            review_data['titulo_pelicula'] = titulos_muestra.get(review.pelicula_id, 'Película Desconocida')
        else:
            # Intentar obtener la película de la base de datos
            try:
                # Solo intentar obtener de la base de datos si no es un ID por defecto
                # y si parece ser un número válido
                if not review.pelicula_id.startswith('default-') and review.pelicula_id.isdigit():
                    pelicula = Pelicula.objects.get(id=int(review.pelicula_id))
                    review_data['titulo_pelicula'] = pelicula.titulo
            except (Pelicula.DoesNotExist, ValueError):
                # Si la película no existe o el ID no es válido, dejar el valor por defecto
                pass
        
        enhanced_reviews.append(review_data)
    
    return render(request, 'reviews_list.html', {'reviews': enhanced_reviews})

@login_required
def delete_review(request, review_id):
    # Asegurar que solo el propietario pueda eliminar la reseña
    review = get_object_or_404(Interaccion, id=review_id, user=request.user)
    review.delete()
    messages.success(request, "Reseña eliminada correctamente.")
    return redirect('reviews_list')


def detalle_pelicula(request, pelicula_id):
    """
    Vista para mostrar los detalles de una película específica.
    """
    # Diccionario para mapear IDs por defecto a información de películas
    peliculas_muestra = {
        'default-1': {
            'titulo': 'Interestelar',
            'descripcion': 'Un grupo de exploradores emprende la misión más importante de la historia: viajar más allá de nuestra galaxia para descubrir si la humanidad tiene un futuro entre las estrellas.',
            'imagen': 'https://pics.filmaffinity.com/Interstellar-366875261-large.jpg',
            'genero': 'Ciencia Ficción',
            'director': 'Christopher Nolan',
            'año': '2014',
            'duracion': '169 min',
            'calificacion': '8.6/10'
        },
        'default-2': {
            'titulo': 'Titanic',
            'descripcion': 'Un aristócrata y una joven de clase baja se enamoran a bordo del Titanic en su viaje inaugural. Su romance se ve afectado cuando el transatlántico choca con un iceberg.',
            'imagen': 'https://es.web.img3.acsta.net/pictures/16/02/04/15/49/599815.jpg',
            'genero': 'Romance',
            'director': 'James Cameron',
            'año': '1997',
            'duracion': '195 min',
            'calificacion': '7.9/10'
        },
        'default-3': {
            'titulo': 'El Padrino',
            'descripcion': 'El patriarca de una dinastía del crimen organizado transfiere el control de su imperio clandestino a su reacio hijo.',
            'imagen': 'https://pics.filmaffinity.com/El_padrino-488102675-large.jpg',
            'genero': 'Drama',
            'director': 'Francis Ford Coppola',
            'año': '1972',
            'duracion': '175 min',
            'calificacion': '9.2/10'
        },
        'default-4': {
            'titulo': 'El Diario de Noah',
            'descripcion': 'Una anciana con demencia escucha la historia de un amor perdido y reencontrado a través de las páginas de un antiguo diario.',
            'imagen': 'https://m.media-amazon.com/images/I/81rXTNAr+TL._AC_UF1000,1000_QL80_.jpg',
            'genero': 'Romance',
            'director': 'Nick Cassavetes',
            'año': '2004',
            'duracion': '123 min',
            'calificacion': '7.8/10'
        },
        'default-5': {
            'titulo': 'Bajo la misma estrella',
            'descripcion': 'Dos adolescentes con cáncer se conocen en un grupo de apoyo y desarrollan una profunda conexión mientras enfrentan sus enfermedades.',
            'imagen': 'https://pics.filmaffinity.com/the_fault_in_our_stars-259624288-large.jpg',
            'genero': 'Romance',
            'director': 'Josh Boone',
            'año': '2014',
            'duracion': '126 min',
            'calificacion': '7.7/10'
        },
        'default-6': {
            'titulo': 'El Conjuro',
            'descripcion': 'Basada en un caso real, los investigadores paranormales Ed y Lorraine Warren ayudan a una familia aterrorizada por una presencia oscura en su casa.',
            'imagen': 'https://pics.filmaffinity.com/Expediente_Warren_The_Conjuring-153245956-large.jpg',
            'genero': 'Terror',
            'director': 'James Wan',
            'año': '2013',
            'duracion': '112 min',
            'calificacion': '7.5/10'
        },
        'default-7': {
            'titulo': 'El Resplandor',
            'descripcion': 'Un escritor acepta un trabajo como cuidador de un hotel aislado durante el invierno, donde una siniestra presencia influye en él y aterroriza a su familia.',
            'imagen': 'https://pics.filmaffinity.com/El_resplandor-526136262-large.jpg',
            'genero': 'Terror',
            'director': 'Stanley Kubrick',
            'año': '1980',
            'duracion': '146 min',
            'calificacion': '8.4/10'
        },
        'default-8': {
            'titulo': 'It',
            'descripcion': 'En un pequeño pueblo, un grupo de niños debe enfrentarse a sus mayores miedos cuando un malvado payaso resurge, responsable de la desaparición de varios niños.',
            'imagen': 'https://pics.filmaffinity.com/It-844355670-large.jpg',
            'genero': 'Terror',
            'director': 'Andy Muschietti',
            'año': '2017',
            'duracion': '135 min',
            'calificacion': '7.3/10'
        },
        'default-9': {
            'titulo': 'Matrix',
            'descripcion': 'Un programador informático descubre que el mundo en el que vive es una simulación digital controlada por máquinas que han esclavizado a la humanidad.',
            'imagen': 'https://pics.filmaffinity.com/The_Matrix-155050517-large.jpg',
            'genero': 'Ciencia Ficción',
            'director': 'Lana y Lilly Wachowski',
            'año': '1999',
            'duracion': '136 min',
            'calificacion': '8.7/10'
        },
        'default-10': {
            'titulo': 'Blade Runner 2049',
            'descripcion': 'Un blade runner descubre un secreto que podría desestabilizar la sociedad, lo que lo lleva a buscar a Rick Deckard, quien ha estado desaparecido por 30 años.',
            'imagen': 'https://pics.filmaffinity.com/Blade_Runner_2049-202270567-large.jpg',
            'genero': 'Ciencia Ficción',
            'director': 'Denis Villeneuve',
            'año': '2017',
            'duracion': '163 min',
            'calificacion': '8.0/10'
        },
        'default-11': {
            'titulo': 'Buscando a Nemo',
            'descripcion': 'Un pez payaso sobreprotector que, junto a un pez cirujano con pérdida de memoria, busca a su hijo capturado.',
            'imagen': 'https://m.media-amazon.com/images/I/81montw1gVL._AC_UF1000,1000_QL80_.jpg',
            'genero': 'Animación',
            'director': 'Andrew Stanton',
            'año': '2003',
            'duracion': '100 min',
            'calificacion': '8.2/10'
        },
        'default-12': {
            'titulo': 'Parasitos',
            'descripcion': 'Una familia pobre se infiltra en el servicio de una familia rica, con consecuencias inesperadas.',
            'imagen': 'https://pics.filmaffinity.com/Parasite-406070218-large.jpg',
            'genero': 'Drama',
            'director': 'Bong Joon-ho',
            'año': '2019',
            'duracion': '132 min',
            'calificacion': '8.6/10'
        },
        'default-13': {
            'titulo': 'Spiderman into the Spiderverse',
            'descripcion': 'Miles Morales se convierte en Spider-Man y conoce a otros Spider-People de diferentes dimensiones.',
            'imagen': 'https://m.media-amazon.com/images/I/A1GbxGqXCxL._AC_UF1000,1000_QL80_.jpg',
            'genero': 'Animación',
            'director': 'Bob Persichetti, Peter Ramsey, Rodney Rothman',
            'año': '2018',
            'duracion': '117 min',
            'calificacion': '8.4/10'
        }
    }
    
    try:
        # Verificar si es un ID por defecto
        if str(pelicula_id).startswith('default-'):
            # Obtener información de la película de muestra
            pelicula = peliculas_muestra.get(str(pelicula_id))
            if not pelicula:
                # Si no se encuentra la película de muestra, mostrar mensaje de error
                messages.error(request, "Película no encontrada.")
                return redirect('home')
        else:
            # Intentar obtener la película de la base de datos
            try:
                pelicula_obj = Pelicula.objects.get(id=pelicula_id)
                # Convertir objeto Pelicula a diccionario para la plantilla
                pelicula = {
                    'titulo': pelicula_obj.titulo,
                    'descripcion': pelicula_obj.descripcion,
                    'imagen': pelicula_obj.imagen_url,
                    # Otros campos que pueda tener el modelo Pelicula
                }
            except Pelicula.DoesNotExist:
                # Si no se encuentra la película en la base de datos, mostrar mensaje de error
                messages.error(request, "Película no encontrada.")
                return redirect('home')
        
        # Obtener reseñas de la película
        reseñas = Interaccion.objects.filter(pelicula_id=str(pelicula_id), accion='reseñar').exclude(reseña__isnull=True).exclude(reseña="")
        
        # Obtener calificaciones de la película
        calificaciones = Interaccion.objects.filter(pelicula_id=str(pelicula_id), accion='calificar').exclude(calificacion__isnull=True)
        
        # Calcular calificación promedio
        calificacion_promedio = None
        if calificaciones.exists():
            total = 0
            count = 0
            for cal in calificaciones:
                if cal.calificacion:
                    try:
                        total += int(cal.calificacion)
                        count += 1
                    except (ValueError, TypeError):
                        pass
            if count > 0:
                calificacion_promedio = round(total / count, 1)
        
        # Renderizar plantilla con la información de la película
        return render(request, 'detalle_pelicula.html', {
            'pelicula': pelicula,
            'pelicula_id': pelicula_id,
            'reseñas': reseñas,
            'calificacion_promedio': calificacion_promedio
        })
        
    except Exception as e:
        # En caso de error, mostrar mensaje y redirigir a la página de inicio
        messages.error(request, f"Error al cargar la película: {str(e)}")
        return redirect('home')


@login_required
def update_review(request, review_id):
    # Asegurar que solo el propietario pueda actualizar la reseña
    review = get_object_or_404(Interaccion, id=review_id, user=request.user)
    if request.method == 'POST':
        nueva_resena = request.POST.get('reseña', '').strip()
        if nueva_resena:
            review.reseña = nueva_resena
            review.save()
            messages.success(request, "Reseña actualizada correctamente.")
        else:
            messages.error(request, "La reseña no puede estar vacía.")
    return redirect('reviews_list')

@login_required
def eliminar_favorito(request, pelicula_id):
    """
    Elimina una película de la lista de favoritos del usuario.
    """
    if request.method == 'POST':
        try:
            # Buscar la interacción de tipo 'guardar' para esta película y este usuario
            favorito = Interaccion.objects.filter(
                user=request.user,
                pelicula_id=pelicula_id,
                accion='guardar'
            ).first()
            
            if favorito:
                favorito.delete()
                messages.success(request, "Película eliminada de favoritos correctamente.")
            else:
                messages.warning(request, "Esta película no estaba en tu lista de favoritos.")
                
        except Exception as e:
            messages.error(request, f"Error al eliminar de favoritos: {str(e)}")
            
    return redirect('peliculasFavoritas')