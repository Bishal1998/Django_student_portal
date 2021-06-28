from django.shortcuts import redirect, render
from .models import Homework, Notes, Todo
from .forms import ConversionForm, ConversionLenghthForm, ConversionMassForm, CreateHomework, CreateNote, CreateToDo, SearchForm, UserRegistrationForm
from django.views.generic.detail import DetailView
from youtubesearchpython import VideosSearch
import requests
import wikipedia
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


def home(request):
    return render(request, 'dashboard/home.html')

@login_required
def notes(request):
    form = CreateNote()
    if request.method == "POST":
        form = CreateNote(request.POST)
        if form.is_valid():
            ins = Notes(
                user=request.user, title=request.POST['title'], description=request.POST['description'],)
            ins.save()
            return redirect('/notes')
    notes = Notes.objects.filter(user=request.user)
    context = {
        'notes': notes,
        'form': form
    }
    return render(request, 'dashboard/notes.html', context)

@login_required
def notedelete(request, id):
    note = Notes.objects.filter(id=id)
    note.delete()
    return redirect('/notes')

@login_required
def noteupdate(request, id):
    _update = Notes.objects.get(id=id)
    if request.method == "POST":
        _update.title = request.POST['title']
        _update.description = request.POST['description']
        _update.save()
        return redirect('/notes')
    form = CreateNote(instance=_update)
    context = {
        "form": form
    }
    return render(request, 'dashboard/notes.html', context)


class NoteDetailView(LoginRequiredMixin, DetailView):
    model = Notes
    template_name = "dashboard/notes_detail.html"

@login_required
def homework(request):
    form = CreateHomework()
    if request.method == "POST":
        form = CreateHomework(request.POST)
        if form.is_valid():
            try:
                complete = request.POST['is_complete']
                if complete == "on":
                    complete = True
                else:
                    complete = False
            except:
                complete = False
            ins = Homework(user=request.user, subject=request.POST['subject'],
                           title=request.POST['title'], description=request.POST['description'],
                           due=request.POST['due'], is_complete=complete)
            ins.save()
            return redirect("/homework")
    homework = Homework.objects.filter(user=request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False
    context = {
        "homeworks": homework,
        "homeworks_done": homework_done,
        "form": form
    }
    return render(request, 'dashboard/homework.html', context)

@login_required
def deletehomework(request, id):
    _delete = Homework.objects.get(id=id)
    _delete.delete()
    return redirect('/homework')

@login_required
def updatehomework(request, id):
    _updates = Homework.objects.get(id=id)
    if request.method == "POST":
        _updates.subject = request.POST['subject']
        _updates.title = request.POST['title']
        _updates.description = request.POST['description']
        _updates.due = request.POST['due']
        _updates.save()
        return redirect("/homework")
    form = CreateHomework(instance=_updates)
    context = {
        "form": form
    }
    return render(request, 'dashboard/homework.html', context)

@login_required
def markhomework(request, id):
    _mark = Homework.objects.get(id=id)
    if _mark.is_complete == True:
        _mark.is_complete = False
    else:
        _mark.is_complete = True
    _mark.save()
    return redirect('/homework')


def youtube(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        search = request.POST['search']
        video = VideosSearch(search, limit=15)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input': search,
                'title': i['title'],
                'duration': i['duration'],
                'thumbnail': i['thumbnails'][0]['url'],
                'channel': i['channel']['name'],
                'link': i['link'],
                'views': i['viewCount']['short'],
                'published': i['publishedTime'],
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
            context = {
                'form': form,
                'results': result_list
            }
        return render(request, 'dashboard/youtube.html', context)

    else:
        form = SearchForm()
    context = {
        "form": form
    }
    return render(request, 'dashboard/youtube.html', context)

@login_required
def todo(request):
    if request.method == "POST":
        form = CreateToDo(request.POST)
        if form.is_valid():
            try:
                complete = request.POST['is_complete']
                if complete == "on":
                    complete = True
                else:
                    complete = False
            except:
                complete = False
            ins = Todo(user=request.user,
                       title=request.POST['title'],
                       is_complete=complete)
            ins.save()
            return redirect('/todo')
    else:
        form = CreateToDo()
    _todo = Todo.objects.all()
    if len(_todo) == 0:
        todo_done = True
    else:
        todo_done = False
    context = {
        "todos": _todo,
        "form": form,
        "todo_done": todo_done
    }
    return render(request, 'dashboard/todo.html', context)

@login_required
def deletetodo(request, id):
    _delete = Todo.objects.filter(id=id)
    _delete.delete()
    return redirect('todo')

@login_required
def updatetodo(request, id):
    _update = Todo.objects.get(id=id)
    if request.method == "POST":
        _update.title = request.POST['title']
        _update.save()
        return redirect('/todo')
    form = CreateToDo(instance=_update)
    context = {
        "form": form
    }
    return render(request, 'dashboard/todo.html', context)

@login_required
def marktodo(request, id):
    _mark = Todo.objects.get(id=id)
    if _mark.is_complete == True:
        _mark.is_complete = False
    else:
        _mark.is_complete = True
    _mark.save()
    return redirect('/todo')


def books(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        search = request.POST['search']
        url = "https://www.googleapis.com/books/v1/volumes?q="+search
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dict = {
                'title': answer['items'][i]['volumeInfo']['title'],
                'subtitle': answer['items'][i]['volumeInfo'].get('subtitle'),
                'description': answer['items'][i]['volumeInfo'].get('description'),
                'count': answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories': answer['items'][i]['volumeInfo'].get('categories'),
                'rating': answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail': answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview': answer['items'][i]['volumeInfo'].get('previewLink')
            }
            result_list.append(result_dict)
            context = {
                'form': form,
                'results': result_list
            }
        return render(request, 'dashboard/books.html', context)

    else:
        form = SearchForm()
    context = {
        "form": form
    }
    return render(request, 'dashboard/books.html', context)


def dictionary(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        search = request.POST['search']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/"+search
        r = requests.get(url)
        answer = r.json()
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            exmaple = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
            context = {
                "form": form,
                'input': search,
                'phonetics': phonetics,
                'audio': audio,
                'definition': definition,
                'example': exmaple,
                'synonyms': synonyms
            }
        except:
            context = {
                'form': form,
                'input': ""
            }
        return render(request, 'dashboard/dictionary.html', context)
    else:
        form = SearchForm()
    context = {
        "form": form
    }

    return render(request, 'dashboard/dictionary.html', context)


def wiki(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        text = request.POST['search']
        search = wikipedia.page(text)
        context = {
            "form": form,
            'title': search.title,
            "link": search.url,
            "details": search.summary
        }
        return render(request, 'dashboard/wiki.html', context)
    else:
        form = SearchForm()

        context = {
            'form': form
        }
    return render(request, 'dashboard/wiki.html', context)


def conversion(request):
    if request.method == "POST":
        form = ConversionForm(request.POST)
        if request.POST['measurement'] == 'length':
            measurement_form = ConversionLenghthForm()
            context = {
                'form': form,
                'm_form': measurement_form,
                'input': True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ""
                if input and int(input) >= 0:
                    if first == "yard" and second == "foot":
                        answer = f'{input} yard = {int(input)*3} foot'
                    if first == "foot" and second == "yard":
                        answer = f'{input} foot = {int(input)/3} yard'
                context = {
                    'form': form,
                    'm_form': measurement_form,
                    'input': True,
                    'answer': answer
                }
        if request.POST['measurement'] == 'mass':
            measurement_form = ConversionMassForm()
            context = {
                "form": form,
                "m_form": measurement_form,
                "input": True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ""
                if input and int(input) >= 0:
                    if first == "pound" and second == "kilogram":
                        answer = f'{input} pound = {int(input)*0.453592} kilogram'
                    if first == "kilogram" and second == "pound":
                        answer = f'{input} kilogram = {int(input)*2.20462} pound'
                context = {
                    'form': form,
                    'm_form': measurement_form,
                    'input': True,
                    'answer': answer
                }

    else:
        form = ConversionForm()
        context = {
            'form': form,
            'input': False
        }
    return render(request, 'dashboard/conversion.html', context)


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data['username']
            return redirect('login')
    else:

        form = UserRegistrationForm()
    context = {
        'form': form
    }
    return render(request, 'dashboard/register.html', context)

@login_required
def profile(request):
    homeworks = Homework.objects.filter(is_complete = False, user = request.user)
    todos = Todo.objects.filter(is_complete = False, user = request.user)
    if len(homeworks) == 0:
        homework_done = True
    else:
        homework_done = False
    if len(todos) == 0:
        todo_done = True
    else:
        todo_done = False
    context = {
        'homeworks': homeworks,
        'todos': todos,
        'homework_done':homework_done,
        'todo_done': todo_done
    }
    return render(request, 'dashboard/profile.html', context)