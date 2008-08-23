from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from django.core import urlresolvers,serializers
from lieswetellourselves.lies.models import Lie,Vote
from lieswetellourselves.lies.json_encode import json_encode

def add(request):
    lie = Lie(lie=request.POST['lie'])
    lie.save()
    return HttpResponseRedirect(lie.get_absolute_url())
    
def add_vote(request):
    lie = None
    try:
        lie = Lie.objects.filter(id=request.POST['lie_id'])[0]
        if(request.POST['vote'] == 'up'):
            Vote(lie=lie, value=1).save()
        elif(request.POST['vote'] == 'down'):
            Vote(lie=lie, value=-1).save()
        lie.vote_total_value = lie.vote_total()
    except(IndexError):
        pass

    if(request.is_ajax()):
        return HttpResponse(json_encode(lie))
    else:
        return HttpResponseRedirect(urlresolvers.reverse('index'))
