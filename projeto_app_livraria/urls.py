
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.conf.urls.static import static
from django.conf import settings

# def teste(request):
#     return HttpResponse('Hello World')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('livraria.urls')), # Pega o arquivo URLS.py da pasta do app livraria
    # path('teste/',teste),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

