from django.db.models import fields
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import *
from bootstrap_modal_forms.forms import BSModalModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm

class EleveForm(BSModalModelForm):
    class Meta:
        model=Eleve
        fields =[ 'name','classe'] 

class ClasseForm(forms.ModelForm):
    
    class Meta:
        model=Classe
        fields="__all__"

class MatiereForm(ModelForm):
    class Meta:
        model=Matiere
        fields = "__all__"

class NoteForm(ModelForm):
    class Meta:
        model=Note
        fields=['classes','eleves','semestre','matieres','lanote']