from django.shortcuts import render
from django.http import HttpResponse
from . import util

from markdown2 import Markdown 

markdowner = Markdown()

def siteexists(entry):
    if util.get_entry(entry) == None:
        return False
    return True

def convertToHTML(entry):
    markdowner.convert(entry)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# When this is called, we want to render the template page.html and pass in the title of our page to the get_entry function
# We want to use the markdown function to convert the page into HTML before displaying it to the user using markdowner.convert(content)
def page(request, entry):
    if siteexists(entry) == False:
        return render(request, "encyclopedia/pagenotfound.html")
    else:
        return render(request, "encyclopedia/page.html", {
            "entry": markdowner.convert(util.get_entry(entry))
        })


