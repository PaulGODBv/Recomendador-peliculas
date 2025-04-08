"""djangocrud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views
from django.conf import settings
from django.conf.urls.static import static


from django.conf import settings
from django.conf.urls.static import static
from tasks.views import reviews_list, delete_review
from django.contrib.auth.views import LoginView


from tasks.views import reviews_list, delete_review, update_review, eliminar_favorito

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('tasks/', views.tasks, name='tasks'),
    path('tasks_completed/', views.tasks_completed, name='tasks_completed'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('create_task/', views.create_task, name='create_task'),
    path('tasks/<int:task_id>', views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/complete', views.complete_task, name='complete_task'),  
    path('tasks/<int:task_id>/delete', views.delete_task, name='delete_task'),
    
    path('reviews/', reviews_list, name='reviews_list'),
    path('reviews/delete/<str:review_id>/', delete_review, name='delete_review'),
    path('generos/', views.generos, name='generos'),
    path('recomendaciones/', views.recomendaciones, name='recomendaciones'),
    path('peliculasFavoritas/', views.peliculasFavoritas, name='peliculasFavoritas'),
    path("guardar-interaccion/", views.guardar_interaccion, name="guardar_interaccion"),
    path('reviews/update/<str:review_id>/', update_review, name='update_review'),
    path('pelicula/<str:pelicula_id>/', views.detalle_pelicula, name='detalle_pelicula'),
    path('favoritos/eliminar/<str:pelicula_id>/', eliminar_favorito, name='eliminar_favorito'),
]

if settings.DEBUG:  # Solo en modo desarrollo
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

