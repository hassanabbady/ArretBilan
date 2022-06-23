from import_export import fields, resources, widgets

from .models import Classe, Eleve


class EleveResource(resources.ModelResource):
    class meta:
        model = Eleve

