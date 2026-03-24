from django.db.models.signals import pre_save, pre_delete, post_save, post_delete
from django.dispatch import receiver
from .models import Book
from openai_api.client import get_book_ai_description, get_book_ai_year

@receiver(pre_save, sender=Book)
def book_pre_save(sender, instance, **kwargs):
    if not instance.description:
        print("####### SEM DESCRIÇÃO #########")
        ai_description = get_book_ai_description(instance.title)
        # print("ai_description: ", ai_description)
        instance.description = ai_description
        # print("instance.description: ", instance.description)

    if not instance.year:
        print("####### SEM ANO #########")
        ai_year = get_book_ai_year(instance.title)
        # print("ai_year: ", ai_year)
        instance.year = ai_year
        # print("instance.description: ", instance.description)