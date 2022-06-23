from django.urls import path 
from . import views 


urlpatterns = [
    path('', views.home , name="home"),
    # path('createEleve', views.createEleve , name="createEleve"),
    path('createEleve/', views.EleveCreateView.as_view(), name='createEleve'),
    path('updateEleve/<str:pk>/', views.updateEleve , name="updateEleve"),
    path('deleteEleve/<str:pk>/', views.deleteEleve , name="deleteEleve"),
    path('Import_csv/', views.Import_csv,name="Import_csv"),  


    path('createClasse', views.createClasse , name="createClasse"),
    path('updateClasse/<str:pk>/', views.updateClasse , name="updateClasse"),
    path('deleteClasse/<str:pk>/', views.deleteClasse , name="deleteClasse"),

    path('AllNotes/', views.AllNotes , name="AllNotes"),
    path('updateNote/<str:pk>/', views.updateNote , name="updateNote"),
    path('deleteNote/<str:pk>/', views.deleteNote , name="deleteNote"),

    path('eleves/<str:pk>/', views.eleves , name="eleves"),
    path('notes/<str:pk>/', views.notes , name="notes"),

    path('print', views.printFinal , name="print"),
    # path('page_pdf', views.page_pdf , name="page_pdf"),

    path('createMatiere', views.createMatiere , name="createMatiere"),
    path('updateMatiere/<str:pk>/', views.updateMatiere , name="updateMatiere"),
    path('deleteMatiere/<str:pk>/', views.deleteMatiere , name="deleteMatiere"),
    
   
]


