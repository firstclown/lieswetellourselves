from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from django.core import urlresolvers,serializers
from lieswetellourselves.lies.models import Lie,Vote
from lieswetellourselves.lies.forms import LieForm
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

def list_lies(request):
    object_list = Lie.objects.all().order_by('-modified')
    for lie in object_list:
        lie.vote_total_value = lie.vote_total()
    if(request.is_ajax()):
        return HttpResponse(json_encode(object_list))
    else:
        return render_to_response('lies/lie_list.html', {'object_list':object_list, 'form': LieForm()})
