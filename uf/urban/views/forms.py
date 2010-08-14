from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils import simplejson
from urban.models import *
from django.core import serializers
from urban.forms import *
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext

@csrf_protect
def add_user(request):
    from django.core.urlresolvers import reverse
    if request.method == 'POST': # If the form has been submitted...
        form = SignUpForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            u = User()
            u.username = form.cleaned_data['username']
            u.password = form.cleaned_data['password1']
            u.email = form.cleaned_data['email']
            u.save()
            return HttpResponse('OK')
    else:
        form = SignUpForm() # An unbound form

    return render_to_response('form.xml', {
        'action':reverse('urban.views.form_add_user'),
        'form': form,
    }, context_instance=RequestContext(request))