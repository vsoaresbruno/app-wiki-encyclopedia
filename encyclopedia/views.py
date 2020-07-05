import markdown2, random
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound

from . import util


def index(request):
    list_entries = util.list_entries()

    if request.method == 'POST':

        search = request.POST.get('q')
        entry = util.get_entry(search)

        if entry is None:

            results = [entry_item for entry_item in list_entries 
                        if search.lower() in entry_item.lower()]

            return render(request, "encyclopedia/results.html", {
                "entries": results
            })

        return redirect('entry_page', title=search)

    return render(request, "encyclopedia/index.html", {
        "entries": list_entries
    })

def entry_page(request, title):
    entry = util.get_entry(title)
    html = markdown2.markdown(entry)

    if entry is None:
        return HttpResponseNotFound('<h1>Page not found</h1>')

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": html
    })

def new_page(request):
    message = ""

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        entries = [x.lower() for x in util.list_entries()]
        matching = [s for s in entries if title.lower() in s]

        if len(matching) > 0:
            message = "content already exists"
        else:
            util.save_entry(title, content)

    return render(request, "encyclopedia/new-page.html", {"message": message })
