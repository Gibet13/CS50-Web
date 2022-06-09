from django.shortcuts import render

from . import util
from django.shortcuts import redirect
import random
import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entrypage(request, name):
    html_entry = markdown2.markdown(util.get_entry(name))
    return render(request, "encyclopedia/entry.html", {
        "entry": html_entry,
        "title": name
    })

def newpage(request):
    if request.method == "POST" :
        new_entry_content = request.POST.get("content")
        new_entry_title = request.POST.get("title")
        util.save_entry(new_entry_title, new_entry_content)
    
    return render(request, "encyclopedia/new_page.html")

def editpage(request, name):
    if request.method == "POST" :
        entry_update = request.POST.get("content")
        util.save_entry(name, entry_update)
        
    return render(request, "encyclopedia/edit_page.html", {
        "entry": util.get_entry(name),
        "title": name
    })

def randpage(request):
    entrylist = util.list_entries()
    rand_entry = random.choice(entrylist)
    return redirect('entrypage', name=rand_entry)

def search(request):
    search = request.GET.get("q")

    if search in util.list_entries() :
        return redirect('entrypage', name=search)
    else:
        return redirect('index')