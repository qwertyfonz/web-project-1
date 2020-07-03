from django import forms
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import random
from . import util

from markdown2 import Markdown 

markdowner = Markdown()

class NewPageForm(forms.Form):
    newPageTitle = forms.CharField(label=("Page Title"))
    newPageContent = forms.CharField(widget=forms.Textarea, label="Page Content")

# Renders a main page of all existing entries
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Determines if a site exists or not
def siteexists(entry):
    if util.get_entry(entry) == None:
        return False
    return True

# Converts a page from Markdown to HTML
def convertToHTML(entry):
    return markdowner.convert(entry)

# Renders a page if it exists; returns a "Page Not Found" if no page exists
def page(request, entry):
    if siteexists(entry) == False:
        return render(request, "encyclopedia/pagenotfound.html")
    else:
        return render(request, "encyclopedia/page.html", {
            "entry": convertToHTML(util.get_entry(entry)),
            "title": entry.capitalize()
        })

# Determines if there is a match for a given search query, and returns a list of all matched entries
def searchmatch(request):
    searchlist = []
    for entry in util.list_entries():
        searchresult = entry.find(request.GET.get("q"))
        if searchresult >= 0:
            searchlist.append(entry)
    return searchlist

# Determines if there are any matched search results (no matches has list length 0)
def emptylist(request):
    if len(searchmatch(request)) == 0:
        return 0
    else:
        return 1
        
# Redirects a user to a given page if search query matches an entry title; else return a search result page of all given searches
def search(request):
    query = request.GET.get("q")
    if util.get_entry(query) != None:
        return page(request, query)
    else:
        return render(request, "encyclopedia/search.html", {
            "list": searchmatch(request),
            "emptylist": emptylist(request) == 0
        })

# Allows user to create a new entry
def newpage(request):

    # Checks to see if method is POST
    if request.method == "POST":

        # Create new form object using user-submitted data
        form = NewPageForm(request.POST)

        # If server-side form data is valid:
        if form.is_valid():

            # Use "cleaned" data
            newTitle = form.cleaned_data["newPageTitle"]
            newContent = form.cleaned_data["newPageContent"]

            # If title already exists, render an error page
            if newTitle in util.list_entries():
                return render(request, "encyclopedia/pagealreadyexists.html")

            # Else, save the entry and redirect user to their newly created entry    
            else:
                util.save_entry(newTitle, newContent)
                return HttpResponseRedirect(f"http://127.0.0.1:8000/wiki/{newTitle}")
        
        # If the form is invalid, render the page again with existing info
        else:
            return render(request, "encyclopedia/newpage.html", {
                "form": form
            })
    
    # Used to render newpage.html
    return render(request, "encyclopedia/newpage.html", {
        "form": NewPageForm()
    })

# Returns random page
def randompage(request):
    randomName = random.choice(util.list_entries())
    return HttpResponseRedirect(f"http://127.0.0.1:8000/wiki/{randomName}")