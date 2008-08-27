from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from django.core import urlresolvers,serializers
from django.template import RequestContext
from django.core.paginator import Paginator
from lieswetellourselves.lies.models import Lie,Vote
from lieswetellourselves.lies.forms import LieForm
from lieswetellourselves.lies.json_encode import json_encode
from datetime import datetime

def add(request):
    lie = Lie(lie=request.POST['lie'])
    lie.save()
    return HttpResponseRedirect(lie.get_absolute_url())
    
def add_vote(request):
    lie = None
    try:
        lie = Lie.objects.filter(id=request.POST['lie_id'])[0]
        voted_items = request.session['voted_items'] if 'voted_items' in request.session else []
        if(lie.id not in voted_items):
            if(request.POST['vote'] == 'up'):
                Vote(lie=lie, value=1).save()
                voted_items.append(lie.id)
#            elif(request.POST['vote'] == 'down'):
#                Vote(lie=lie, value=-1).save()
#                voted_items.append(lie.id)
            request.session['voted_items'] = voted_items

            lie.modified = datetime.now()
            lie.save()
            lie.vote_total_value = lie.vote_total()
        else:
            return HttpResponse('dupe')
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
        return render_to_response('lies/lie_list.html', {'object_list':object_list, 'form': LieForm()}, context_instance=RequestContext(request))

def list_lies_page(request,page_num):
    object_list = Lie.objects.all().order_by('-modified')
    object_pages = Paginator(object_list, 10)
    object_page = object_pages.page(page_num)
    for lie in object_page.object_list:
        lie.vote_total_value = lie.vote_total()
    if(request.is_ajax()):
        return HttpResponse(json_encode(object_page.object_list))
    else:
        return render_to_response('lies/lie_list.html', {'pager':object_page, 'form': LieForm()}, context_instance=RequestContext(request))
