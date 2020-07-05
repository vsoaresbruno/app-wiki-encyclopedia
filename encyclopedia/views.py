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
