from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from lieswetellourselves.lies.models import Lie

def add(request):
    lie = Lie(lie=request.POST['lie'])
    lie.save()
    return HttpResponseRedirect('/lies/%s/' % lie.id)
    
