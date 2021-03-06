from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.views.decorators.csrf import csrf_protect
from urban.forms import *
from urban.models import *
from django.template.defaultfilters import slugify

#users
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
                              'action':reverse('urban.views.forms.add_user'),
                              'form': form,
                              'form_id' : slugify(reverse('urban.views.forms.add_user'))
                              }, context_instance=RequestContext(request))


def login_user(request):
    from django.contrib.auth import authenticate, login
    from django.core.urlresolvers import reverse
    if request.method == 'POST': # If the form has been submitted...
        form = LogInForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            un = form.cleaned_data['username']
            print 'un: ' + un
            pw = form.cleaned_data['password']
            print 'pw: ' + pw
            user = authenticate(username=un, password=pw)
            if user is None:
                return HttpResponseForbidden()
            login(request, user)
            return HttpResponse('OK')
        return HttpResponseForbidden()
    else:
        form = LogInForm() # An unbound form

        return render_to_response('form.xml', {
                                  'action':reverse('urban.views.forms.login_user'),
                                  'form': form,
                                  'form_id' : slugify(reverse('urban.views.forms.login_user'))
                                  }, context_instance=RequestContext(request))
@login_required
def del_user(request, username):
    if request.method == 'POST':
        r = request.REQUEST.get('user', "")
        if r == username:
            User.object.get(username=username).delete()

#venues
@login_required
def add_venue(request):
    from django.core.urlresolvers import reverse
    if request.method == 'POST': 
        form = VenueForm(request.POST) 
        if form.is_valid():
            form.save()
            return HttpResponse('OK')
    else:
        form = VenueForm()

    return render_to_response('form.xml', {
                              'action':reverse('urban.views.forms.add_venue'),
                              'form': form,
                              'form_id' : slugify(reverse('urban.views.forms.add_venue'))
                              }, context_instance=RequestContext(request))

@login_required
def edit_venue(request, id):
    from django.core.urlresolvers import reverse
    if request.method == 'POST': 
        form = VenueForm(request.POST) 
        if form.is_valid(): 
            form.save()
            return HttpResponse('OK')
    else:
        v = Venue.objects.get(id=id)
        form = VenueForm(instance=v) 

    return render_to_response('form.xml', {
                              'action':reverse('urban.views.forms.edit_venue'),
                              'form': form,
                              'form_id' : slugify(reverse('urban.views.forms.edit_venue'))
                              }, context_instance=RequestContext(request))
@login_required
def add_group(request):
    from django.core.urlresolvers import reverse
    if request.method == 'POST': # If the form has been submitted...
        form = SignUpForm(request.POST) # A form bound to the POST data
        print('asd')
        print(dir(form))
        if form.is_valid(): # All validation rules pass
            u = User()
            u.username = form.cleaned_data['username']
            u.password = form.cleaned_data['password1']
            u.email = form.cleaned_data['email']
            u.save()
            return HttpResponse('OK')
    else:
        form = SignUpForm()

    return render_to_response('form.xml', {
                              'action':reverse('urban.views.forms.add_group'),
                              'form': form,
                              'form_id' : slugify(reverse('urban.views.forms.add_group'))
                              }, context_instance=RequestContext(request))
@login_required
def edit_group(request):
    from django.core.urlresolvers import reverse
    if request.method == 'POST': 
        form = SignUpForm(request.POST)
        print('asd')
        print(dir(form))
        if form.is_valid(): 
            u = User()
            u.username = form.cleaned_data['username']
            u.password = form.cleaned_data['password1']
            u.email = form.cleaned_data['email']
            u.save()
            return HttpResponse('OK')
    else:
        form = SignUpForm() 

    return render_to_response('form.xml', {
                              'action':reverse('urban.views.forms.edit_group'),
                              'form': form,
                              'form_id' : slugify(reverse('urban.views.forms.edit_group'))
                              }, context_instance=RequestContext(request))