from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from lieswetellourselves.lies.models import Lie,Vote

def add(request):
    lie = Lie(lie=request.POST['lie'])
    lie.save()
    return HttpResponseRedirect('/lies/%s/' % lie.id)
    
def add_vote(request):
    lie = Lie.objects.filter(id=request.POST['lie_id'])[0]
    if(request.POST['vote'] == 'up'):
        Vote(lie=lie, value=1).save()
    elif(request.POST['vote'] == 'down'):
        Vote(lie=lie, value=-1).save()
    return HttpResponseRedirect('/')
