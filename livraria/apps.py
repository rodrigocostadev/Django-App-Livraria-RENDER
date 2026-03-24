from django.apps import AppConfig


class LivrariaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'livraria'

    # Função ready ativa o signals no app 
    def ready(self):
        import livraria.signals
