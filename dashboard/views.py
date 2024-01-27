from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import generic
from wikipedia import wikipedia
from django.contrib.auth.decorators import login_required
from .forms import *
from youtubesearchpython import VideosSearch
import requests
from .models import *


# Create your views here.
# """
# This function takes a request parameter and returns the rendered 'dashboard/home.html' template.
# """
def home(request):
    return render(request, 'dashboard/home.html')


# VIEWS FOR NOTES SECTION

# This function handles the notes request. It requires the request object as a parameter
# and returns a rendered notes template. It also creates a new note if the request method is POST.
@login_required
def notes(request):
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user=request.user, title=request.POST['title'], description=request.POST['description'])
            notes.save()
            return redirect('notes')
        messages.success(request, 'Note created successfully')
    else:
        form = NotesForm()
        notes = Notes.objects.filter(user=request.user)
        context = {
            'notes': notes,
            'form': form
        }
        return render(request, 'dashboard/notes.html', context)

    # """
    # Deletes a note with the given primary key.
    #
    # Args:
    #     request: The request object.
    #     pk: The primary key of the note to be deleted.
    #
    # Returns:
    #     A redirect to the 'notes' page.
    # """


@login_required
def delete_note(request, pk):
    Notes.objects.get(id=pk).delete()
    return redirect('notes')


class NotesDetailView(generic.DetailView):
    model = Notes


# VIEWS FOR HOMEWORK SECTION
#     """
#     A view function for handling homework creation and rendering the homework template.
#     Takes a request object and returns an HTTP response.
#     """
@login_required
def homework(request):
    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homework = Homework(
                user=request.user,
                subject=request.POST['subject'],
                title=request.POST['title'],
                description=request.POST['description'],
                due=request.POST['due'],
                is_finished=finished
            )
            homework.save()
            messages.success(request, 'Homework created successfully')
            return redirect('homework')
    else:
        form = HomeworkForm()
    homework = Homework.objects.filter(user=request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False
    context = {
        'homeworks': homework,
        'homeworks_done': homework_done,
        'form': form
    }
    return render(request, 'dashboard/homework.html', context)

    # """
    # Updates the status of a homework task and redirects to the 'homework' page.
    #
    # Args:
    #     request: The HTTP request object.
    #     pk: The primary key of the homework task to be updated.
    #
    # Returns:
    #     HttpResponseRedirect: Redirects to the 'homework' page.
    # """


@login_required
def update_homework(request, pk):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect('homework')

    # """
    # Delete a homework item.
    #
    # Args:
    #     request: The HTTP request object.
    #     pk: The primary key of the homework item to be deleted.
    #
    # Returns:
    #     A redirect to the 'homework' page.
    # """


@login_required
def delete_homework(request, pk):
    Homework.objects.get(id=pk).delete()
    return redirect('homework')

    # """
    # Process a POST request to search for videos and display the results using the YouTube API.
    #
    # Args:
    #     request: HttpRequest object containing the request data.
    #
    # Returns:
    #     HttpResponse object rendering the 'dashboard/YouTube.html' template with the search results.
    # """


# YOUTUBE SECTION
def youtube(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text, limit=10)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input': text,
                'title': i['title'],
                'duration': i['duration'],
                'thumbnail': i['thumbnails'][0]['url'],
                'channel': i['channel']['name'],
                'link': i['link'],
                'views': i['viewCount']['short'],
                'published': i['publishedTime']
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
            context = {'form': form, 'results': result_list}
        return render(request, 'dashboard/youtube.html', context)
    else:
        form = DashboardForm()
    context = {'form': form}
    return render(request, 'dashboard/youtube.html', context)


# TO_DO SECTION
#     """
#     A view for creating and listing_todo items for the logged-in user.
#     """
@login_required
def todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todo = Todo(
                user=request.user,
                title=request.POST['title'],
                is_finished=finished
            )
            todo.save()
            messages.success(request, 'Todo created successfully')
            return redirect('todo')
    else:
        form = TodoForm()
    todo = Todo.objects.filter(user=request.user)
    if len(todo) == 0:
        todo_done = True
    else:
        todo_done = False
    context = {
        'todos': todo,
        'form': form,
        'todos_done': todo_done
    }
    return render(request, 'dashboard/todo.html', context)

    # """
    # Update the status of a_todo item.
    #
    # Args:
    #     request: The request object.
    #     pk: The primary key of the_todo item to be updated.
    #
    # Returns:
    #     A redirect to the_todo page.
    # """


@login_required
def update_todo(request, pk):
    Any = Todo.objects.get(id=pk)
    if Any.is_finished:
        Any.is_finished = False
    else:
        Any.is_finished = True
    Any.save()
    return redirect('todo')

    # """
    # Delete a to-do item.
    #
    # Args:
    #     request: The HTTP request object.
    #     pk: The primary key of the to-do item to be deleted.
    #
    # Returns:
    #     A redirection to the_todo page.
    # """


@login_required
def delete_todo(request, pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect('todo')


# BOOKS SECTION
#     """
#     Takes a request object and returns a rendered books dashboard with search results.
#     """
def books(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q=" + text
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
                'preview': answer['items'][i]['volumeInfo'].get('previewLink'),

            }
            result_list.append(result_dict)
            context = {'form': form, 'results': result_list}
        return render(request, 'dashboard/books.html', context)
    else:
        form = DashboardForm()
    context = {'form': form}
    return render(request, 'dashboard/books.html', context)

    # """
    # Retrieves dictionary data from an API based on the given text input and renders
    # it in the dashboard dictionary page.
    #
    # Args:
    #     request: The HTTP request object.
    #
    # Returns:
    #     The rendered dictionary page with the retrieved dictionary data.
    # """


# DICTIONARY SECTION
def dictionary(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/" + text
        r = requests.get(url)
        answer = r.json()
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
            context = {
                'form': form,
                'input': text,
                'phonetics': phonetics,
                'audio': audio,
                'definition': definition,
                'example': example,
                'synonyms': synonyms
            }
        except:
            context = {
                'form': form,
                'input': ''
            }
        return render(request, 'dashboard/dictionary.html', context)
    else:
        form = DashboardForm()
        context = {'form': form}
    return render(request, 'dashboard/dictionary.html', context)

    # """
    # Takes a request object and renders a wiki page based on the request method.
    # If the method is POST, it retrieves the text from the request, creates a DashboardForm,
    # searches Wikipedia for the text, and renders the wiki page with the search results.
    # If the method is not POST, it creates a DashboardForm and renders the wiki page with the form.
    # """


# WIKIPEDIA SECTION
def wiki(request):
    if request.method == 'POST':
        text = request.POST['text']
        form = DashboardForm(request.POST)
        search = wikipedia.page(text)
        context = {
            'form': form,
            'title': search.title,
            'link': search.url,
            'details': search.summary
        }
        return render(request, 'dashboard/wiki.html', context)
    else:
        form = DashboardForm()
        context = {'form': form}
    return render(request, 'dashboard/wiki.html', context)

    # """
    # Register a user based on the request and return the rendered registration page.
    #
    # Args:
    #     request: The HTTP request object containing the user's data.
    #
    # Returns:
    #     A rendered registration page.
    # """


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'dashboard/register.html', context)

    # """ This function is the profile view for the user. It requires a request object as a parameter and returns a
    # rendered profile page with the user's homeworks, todos, and their completion status. """


@login_required
def profile(request):
    homeworks = Homework.objects.filter(is_finished=False, user=request.user)
    todos = Todo.objects.filter(is_finished=False, user=request.user)
    if len(homeworks) == 0:
        homework_done = True
    else:
        homework_done = False
    if len(todos) == 0:
        todos_done = True
    else:
        todos_done = False
    context = {
        'homeworks': homeworks,
        'todos': todos,
        'homework_done': homework_done,
        'todo_done': todos_done
    }

    return render(request, 'dashboard/profile.html', context)
