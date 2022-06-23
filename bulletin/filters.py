from django.db.models import fields
import django_filters

from .models import *


class NoteFilter(django_filters.FilterSet):
    
    class Meta:
        model=Note
        fields=['eleves']

class EleveFilter(django_filters.FilterSet):
    
    class Meta:
        model=Eleve
        fields=['name']
