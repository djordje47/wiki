from django.shortcuts import render
from markdown2 import Markdown
from . import util


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
    markdown = Markdown()
    html_entry = markdown.convert(entry)
    return render(request, "encyclopedia/entry-page.html", {
        "title": search_term,
        'entry': html_entry,
    })


def randomPage(request):
    """
    Renders a random entry page
    """

def createEntry(request):
    """
    Docstring for createEntry

    :param request: Description
    """

def updateEntry(request):
    """
    Docstring for updateEntry

    :param request: Description
    """