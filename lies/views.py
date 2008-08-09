from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core import urlresolvers
from lieswetellourselves.lies.models import Lie,Vote

def add(request):
    lie = Lie(lie=request.POST['lie'])
    lie.save()
    return HttpResponseRedirect(lie.get_absolute_url())
    
def add_vote(request):
    try:
        lie = Lie.objects.filter(id=request.POST['lie_id'])[0]
        if(request.POST['vote'] == 'up'):
            Vote(lie=lie, value=1).save()
        elif(request.POST['vote'] == 'down'):
            Vote(lie=lie, value=-1).save()
    except(IndexError):
        pass

    if(request.is_ajax()):
        return render_to_response('ajax_vote.html')
    else:
        return HttpResponseRedirect(urlresolvers.reverse('index'))
