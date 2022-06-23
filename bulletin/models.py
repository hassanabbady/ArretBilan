from django.db import models
from typing import DefaultDict
from django.db.models.enums import Choices
# Create your models here.

class Matiere(models.Model):
    name = models.CharField(max_length=190, null=True)
    
    
        #fonction de costumer pour afficher le nom sur admin
    def __str__(self):
        return self.name


class Classe(models.Model):
    nomClasse = models.CharField(max_length=190, null=True,unique=True)
    def __str__(self):
        return self.nomClasse

class Eleve(models.Model):
    name = models.CharField(max_length=190, null=True)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, null=True)
        #fonction de costumer pour afficher le nom sur admin
    def __str__(self):
        return self.name



class Note(models.Model):
    SEMESTRE= (
        ('semestre1','Semestre 1'),
        ('semestre2','Semestre 2')
    )  

    lanote = models.FloatField(null=True)
    semestre= models.CharField(max_length=100, null=True, choices=SEMESTRE)
    
    eleves = models.ForeignKey(Eleve, on_delete=models.CASCADE, null=True)

    matieres = models.ForeignKey(Matiere, on_delete=models.CASCADE, null=True)
    classes = models.ForeignKey(Classe, on_delete=models.CASCADE, null=True)

    # def __str__(self):
    #     return self.eleves