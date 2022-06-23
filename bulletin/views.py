from django.forms.models import inlineformset_factory
from django.shortcuts import render,redirect
from django.http import HttpResponse
from bulletin.forms import *
from .models import *
from .filters import NoteFilter,EleveFilter
from django.template.loader import render_to_string
from django.forms import inlineformset_factory, modelformset_factory
from django.urls import reverse_lazy
from django.contrib import messages
from bootstrap_modal_forms.generic import BSModalCreateView
from .resources import EleveResource
from tablib import Dataset
#pdf
from django.http import FileResponse,JsonResponse
import io
from fpdf import FPDF

class EleveCreateView(BSModalCreateView):
    template_name = 'bulletin/eleve_form.html'
    form_class = EleveForm
    success_message = 'Success: Eleve was created.'
    success_url = reverse_lazy('createClasse')

# Create your views here.
def home(request):
    
    context={}

    return render(request, 'bulletin/dashboard.html', context)


#Eleve
def eleves(request, pk):
    
    classes = Classe.objects.get(id=pk)
    eleves = classes.eleve_set.all()
    searchFilter = EleveFilter(request.GET , queryset=eleves)
    eleves = searchFilter.qs
    context={'classes':classes , 'eleves': eleves ,'searchFilter':searchFilter , } 
    return render(request, 'bulletin/eleve.html', context)

def AllNotes(request):
    if 'eleves' in request.GET:
        eleves=request.GET['eleves']
        notes=Note.objects.filter(eleves_id=eleves)    
    else:    
        notes=Note.objects.all()
 
    eleves = notes.all()
    searchFilter = NoteFilter(request.GET , queryset=eleves)
    eleves = searchFilter.qs
    context={'notes':notes,'searchFilter':searchFilter}
    return render(request, 'bulletin/notes.html', context)

def Import_csv(request):
                 
    if request.method=='POST':
        Eleve_Resource= EleveResource()
        dataset=Dataset()
        new_eleve=request.FILES['myfile']
        classes=Classe.objects.all()
        if not new_eleve.name.endswith('xlsx'):
            messages.info(request,'Format incorrect')
            return render(request, 'bulletin/importexcel.html',{})
        imported_data=dataset.load(new_eleve.read(),format='xlsx')   
       
        
        for data in imported_data:
            for item in classes:
                if item.nomClasse==data[2]:
                    value=Eleve(
                        data[0],
                        data[1],
                        item.id,
                
                        )        
            value.save()
            
    return render(request, 'bulletin/importexcel.html',{})

# Creeer eleve
# def createEleve(request):
#     form = EleveForm()
#     if request.method== 'POST':
#         form= EleveForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('createEleve')


#     context={'form':form }
#     # html_form=render_to_string('bulletin/eleve_form.html',context, request=request)
#     # return JsonResponse({'html_form':html_form})
#     return render(request, 'bulletin/eleve_form.html', context)

def updateEleve(request, pk):
    eleve =Eleve.objects.get(id=pk)
    form = EleveForm(instance=eleve)
    if request.method== 'POST':
        form= EleveForm(request.POST,instance=eleve)
        if form.is_valid():
            form.save()
            return redirect('createEleve')

    context={'form':form }
    return render(request, 'bulletin/eleve_form.html', context)

def deleteEleve(request, pk):
    eleve =Eleve.objects.get(id=pk)
    
    if request.method== 'POST':
        eleve.delete()
        return redirect('createClasse')


    context={'eleve':eleve }

    return render(request, 'bulletin/delete_eleve.html', context)


def createClasse(request):
    classes=Classe.objects.all()
    form = ClasseForm()
    if request.method== 'POST':
        form= ClasseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('createClasse')
    context={'form':form ,'classes':classes}
    return render(request, 'bulletin/classe_form.html', context)


def updateClasse(request, pk):
    classe =Classe.objects.get(id=pk)
    form = ClasseForm(instance=classe)
    if request.method== 'POST':
        form= ClasseForm(request.POST,instance=classe)
        if form.is_valid():
            form.save()
            return redirect('createClasse')

    context={'form':form }
    return render(request, 'bulletin/classe_form.html', context)

def deleteClasse(request, pk):
    classe =Classe.objects.get(id=pk)
    if request.method== 'POST':
        classe.delete()
        return redirect('createClasse')


    context={'classe':classe }
    return render(request, 'bulletin/delete_form.html', context)



def createMatiere(request):
    matieres=Matiere.objects.all()
    form = MatiereForm()
    if request.method== 'POST':
        form= MatiereForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('createMatiere')


    context={'form':form , 'matieres' : matieres}
    return render(request, 'bulletin/matiere_form.html', context)

def updateMatiere(request, pk):
    matiere =Matiere.objects.get(id=pk)
    form = MatiereForm(instance=matiere)
    if request.method== 'POST':
        form= MatiereForm(request.POST,instance=matiere)
        if form.is_valid():
            form.save()
            return redirect('createMatiere')

    context={'form':form }
    return render(request, 'bulletin/matiere_form.html', context)
#Delete Matiere
def deleteMatiere(request, pk):
    matiere =Matiere.objects.get(id=pk)
    if request.method== 'POST':
        matiere.delete()
        return redirect('createMatiere')


    context={'matiere':matiere }
    return render(request, 'bulletin/delete_matiere.html', context)

def deleteNote(request, pk):
    notes =Note.objects.get(id=pk)
    if request.method== 'POST':
        notes.delete()
        return redirect('AllNotes')


    context={'notes':notes }
    return render(request, 'bulletin/delete_note.html', context)

def updateNote(request, pk):
    notes =Note.objects.get(id=pk)
    form = NoteForm(instance=notes)
    if request.method== 'POST':
        form= NoteForm(request.POST,instance=notes)
        if form.is_valid():
            form.save()
            return redirect('AllNotes')

    context={'form':form }
    return render(request, 'bulletin/note_update.html', context)

def notes(request,pk):
    
  
    #-------------------------
    classes = Classe.objects.get(id=pk)
    eleves = classes.eleve_set.all()
    matieres= Matiere.objects.all()
    Televes=classes.eleve_set.count()
    counter = 0
    # verif=True
    notes = Note.objects.all()
    if request.method == "POST":
        
        matiere=Matiere.objects.get(id=request.POST.get('matiere',None))
        smestre=request.POST.get('sems',None)
        T_notes=Note.objects.count()
        i=1
        x=0
        while x<Televes:
            note=request.POST['txt'+str(i)]
            if T_notes==0:
                Lesnote= Note.objects.create(
                    lanote=note,
                    semestre=smestre,
                    eleves=eleves[x],
                    matieres=matiere,
                    classes=classes
                    )
            elif T_notes>0:   
                for item in notes:
                    if item.matieres==matiere and item.semestre==smestre and item.eleves==eleves[x]:
                        verif=True
                        obj = Note.objects.get(id=item.id)
                        obj.lanote = note
                        obj.save()
                        break
                    else:
                        verif=False       
            i=i+1
            x=x+1
        x=0
        i=1
        while x<Televes:
            note=request.POST['txt'+str(i)]
            if verif==False:
                Lesnote= Note.objects.create(
                    lanote=note,
                    semestre=smestre,
                    eleves=eleves[x],
                    matieres=matiere,
                    classes=classes
                    )
            x=x+1
            i=i+1    
    context={ 'eleves':eleves, 'matieres':matieres,'classes':classes,'Televes':Televes,'counter':counter,'notes':notes}             
    return render(request, 'bulletin/note_form.html', context)

class PDF(FPDF):
    def header(self):
        # Logo
        self.image('static/images/logo.png', 10, 8, 33)
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Move to the right
        self.cell(80)
               # Title
        self.cell(75, 20, "L'EDUCATION PREND DE LA HAUTEUR", 0, 0, 'C')
        self.ln(40)
        # Title
        self.cell(0, 15, 'ARRET BILAN N°1 OCTOBRE-DECEMBRE 2021', 1, 1, 'C')
        # Line break
        self.ln(5)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-20)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        
        self.cell(30, 15, 'Signature des parents', 0, 0, 'L')
        self.multi_cell(0, 5, 'La Cellule de Coordination '+ "\n" + 'et de Suivi Pédagogique', 0, 'R')
        # self.cell(0, 15, 'La Cellule de Coordination /n et de Suivi Pédagogique ', 0, 1, 'L')

def printFinal(request):
    
    classes=Classe.objects.all()
    
    
    form = ClasseForm()
    if request.method == "POST":
        
        classe=request.POST.get('classe',None)
        semestre=request.POST.get('sems',None)
        notes = Note.objects.all()
        
        classes1 = Classe.objects.get(nomClasse=classe)
        eleves = classes1.eleve_set.all()
        T_eleves=classes1.eleve_set.count()
        
    # classe=request.POST.get('classes',None)
        if semestre=='semestre1':
            sem='1'
        else:
            sem='2'    
        pdf = PDF()
        i=0
        
        
        while i<T_eleves:
            
            pdf.alias_nb_pages()
            pdf.add_page()
            pdf.set_font('Times', 'B', 12)
            
            pdf.cell(0, 10, ("Nom & Prénom: " + str(eleves[i])) , 0, 1,'L',link='updateEleve/'+ str(eleves[i].id))
            pdf.cell(0, 10, ("Classe: " + str(classe)) , 0, 1,'L')
            pdf.cell(0, 10, ("Semestre: " + str(sem)) , 0, 1,'L')
            pdf.ln(5)
            pdf.set_text_color(255  ,255,255)
            pdf.set_fill_color(0, 74, 152)
            # pdf.cell(5)
            pdf.cell(150, 10, ("Matière") , 1, 0,'C',True)
            pdf.cell(40, 10, ("Note Elève") , 1, 0,'C',True)  
            
            pdf.ln(10)
            for note in notes:
 
            # if  note.semestre==semestre:
                    if  str(note.classes)==str(classe) and note.semestre==semestre:
                        if eleves[i]==note.eleves:
                            # pdf.cell(5)
                            # pdf.cell(100, 10, str(note.matieres) , 1, 0,'C')
                            pdf.set_text_color(0,0,0)
                            pdf.cell(150,10, txt = str(note.matieres), border = 1, ln = 0, align = 'L', fill = False, link = 'createMatiere')
                            pdf.cell(40, 10, str(note.lanote) , 1, 0,'C')
                            pdf.ln(10)
            # pdf.add_page()
            i=i+1
            pdf.ln(10)
            pdf.cell(0, 20, 'Observation générale:' , 1, 1,'L')

                
        pdf.output(str(classe+".pdf"), 'F')

        file=open(str(classe+".pdf"),'rb')
        response = FileResponse(file,as_attachment=True)

        return response
   
    context={'classes':classes}
    return render(request, 'bulletin/print.html', context)


def page_not_found_view(request, exception):
    return render(request, 'bulletin/404.html')