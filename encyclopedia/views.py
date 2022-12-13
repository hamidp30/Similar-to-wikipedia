from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown
from . import util
from django import forms
from django.contrib import messages
import os
import random
class NewForme(forms.Form):
    subject = forms.CharField(widget=forms.TextInput(attrs={'class': 'inp'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'inp'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, title):
    if util.get_entry(title) == None:
         contant = "Your requested page could not be found!"
         return render(request,"encyclopedia/wiki.html",{
         "message": contant
          })
    else:
         contants = util.get_entry(title)
         contant = markdown.markdown(contants)    
         return render(request,"encyclopedia/wiki.html",{
         "title": title,
         "contant": contant
       })

def add(request):
    if request.method == "POST":
        form = NewForme(request.POST)
        if form.is_valid():
            title = form.cleaned_data['subject'].capitalize()
            content = form.cleaned_data['message']
            if util.get_entry(title) == None:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse('wiki:wiki', args={title}))
            else:
                return render(request,"encyclopedia/add_page.html",{
                    "message": "sorry! The title is repetitive."
            })
        else:
            return render(request, "encyclopedia/add_page.html",{
            "form": form,
        })

    return render(request, "encyclopedia/add_page.html",{
        "form": NewForme()
    })

def edit_function(request,title):    
    contant = open(f"entries/{title}.md").read()  
    if request.method == "POST":
            contentt = request.POST.get('message')
            util.save_entry(title, contentt)
            return HttpResponseRedirect(reverse('wiki:wiki', args={title}))
    return render(request, "encyclopedia/edit_page.html",{
        "title": title,
        "contant": contant,
        "form": NewForme()
    })

def delete_function(request,title):   
    os.remove(f"entries/{title}.md")
    return HttpResponseRedirect(reverse('wiki:index'))

def Search_function(request):
    list_search = []     
    if request.method == "GET":
            for entry in util.list_entries():
                result_equal = request.GET["q"].casefold() == entry.casefold() 
                Unequal = request.GET["q"].casefold() in entry.casefold()    
                if result_equal:
                    return HttpResponseRedirect(reverse("wiki:wiki",kwargs={"title": entry}))
                elif Unequal: 
                    list_search.append(entry)
    return render(request,"encyclopedia/search.html",{
         "list_search": list_search
    })

def random_function(request):
    list_search = []     
    for entry in util.list_entries(): 
        Unequal = entry.casefold()    
        if Unequal: 
            list_search.append(entry)
    rnd = random.sample(list_search, 1)
    return HttpResponseRedirect(reverse("wiki:wiki",kwargs={"title": rnd[0]}))    