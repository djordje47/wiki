from django.shortcuts import render
from . import util
from markdown2 import Markdown


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
    print(entry)
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
    all_entries = util.list_entries()


def randomPage(request):
    """
    Renders a random entry page
    """
