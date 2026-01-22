import random
from django.shortcuts import render
from django.forms import Form, CharField, Textarea, TextInput
from django.http import HttpResponseRedirect
from django.urls import reverse

from markdown2 import Markdown
from . import util


class NewEntryForm(Form):
    title = CharField(required=True, max_length=10, widget=TextInput(attrs={'class':'form-control'}))
    content = CharField(
        required=True,
        max_length=500,
        widget=Textarea(attrs={'rows': 4, 'cols': 40, 'class':'form-control'})
    )


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def page(request, title):
    """
        Renders an entry page if the entry exists,
        If the entry doesn't exist it renders the 404 page
    """
    entry = util.get_entry(title)
    if not entry:
        return render(request, 'encyclopedia/404.html', {
            'title': title,
            'message': 'This entry does not exist.'
        })
    markdown = Markdown()
    html_entry = markdown.convert(entry)
    return render(request, "encyclopedia/entry-page.html", {
        "title": title,
        'entry': html_entry,
    })


def search(request):
    """
    Renders an entry page if there is an exact match,
    Else renders the search page with the results that match the search term
    """
    search_term = request.GET.get('q')
    entry = util.get_entry(search_term)
    if not entry:
        all_entries = util.list_entries()
        results = [
            entry for entry in all_entries if search_term.lower() in entry.lower()]
        return render(request, "encyclopedia/search.html", {
            "results": results,
            "term": search_term
        })
    
    return HttpResponseRedirect(reverse('wiki:page', args=[search_term]))


def randomPage(request):
    """
    Renders a random entry page
    """
    random_title = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse('wiki:page', args=[random_title]))

def createEntry(request):
    """
    Creates the new entry if it doesn't exists 
    If it does it returns an error
    When the entry is created, it returns the index page.

    :param request: POST or GET request depending on the action
    """
    if request.method == 'GET':
        return render(request, 'encyclopedia/create-entry.html', {
            'form': NewEntryForm()
        })
    form = NewEntryForm(request.POST)
    if form.is_valid():
        cleaned_data = form.cleaned_data
        if not util.get_entry(cleaned_data['title']):
            util.save_entry(cleaned_data['title'], cleaned_data['content'])
            return HttpResponseRedirect(reverse('wiki:page', args=[cleaned_data['title']]))
        return render(request, 'encyclopedia/create-entry.html', {
            'error': 'The entry already exists!',
            'form': form
        })
    else:
        return render(request, 'encyclopedia/create-entry.html', {
            'form': form
        })

def editEntry(request, title):
    """
    Docstring for updateEntry

    :param request: Description
    """
    entryContent = util.get_entry(title)
    if not entryContent:
        return render(request, 'encyclopedia/404.html', {
                'title': title,
                'message': 'This entry doesn\'t exist!' 
            })
    
    if request.method == 'GET':
        form = NewEntryForm({'title': title, 'content': entryContent})
        # Makes the title read-only:
        form.fields['title'].widget.attrs['readonly'] = 'readonly'
        
        return render(request, 'encyclopedia/edit-entry.html', {
            'title': title,
            'form': form
        })

    form = NewEntryForm(request.POST)
    if form.is_valid():
        clean_data = form.cleaned_data
        util.save_entry(clean_data['title'], clean_data['content'])
        return HttpResponseRedirect(reverse('wiki:page', args=[title]))
    
    return render(request, 'encyclopedia/edit-entry.html', {
            'title': title,
            'form': form,
            'error': 'Something went wrong'
        })
