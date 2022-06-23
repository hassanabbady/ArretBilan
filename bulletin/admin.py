from django.contrib import admin
from .models import *
# Register your models here.
from import_export.admin import ImportExportModelAdmin



@admin.register(Eleve)
class Eleve(ImportExportModelAdmin):
    pass



@admin.register(Matiere)
class Matiere(ImportExportModelAdmin):
    pass

@admin.register(Classe)
class Classe(ImportExportModelAdmin):
    pass

@admin.register(Note)
class Note(ImportExportModelAdmin):
    list_display=['eleves','classes','matieres','semestre','lanote']
    # list_display_links=['semestre']
    
    list_editable=['classes','matieres','semestre','lanote']
    # # autocomplete_fields = ['service']
    search_fields=['semestre','lanote']
    
    # list_filter = (('name', DropdownFilter),('age'))
    # # fields=['name','surname']

    # search_fields = ['name']
    list_per_page=10



