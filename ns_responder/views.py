# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.urls import reverse
from .forms import InputForm
from .forms import UnbindPolicyForm
from .forms import BindPolicyForm
from django.shortcuts import render
from .utils import get_primary_mgmt_ip
from .utils import isBound
from .utils import unbindPolicy
from .utils import bindPolicy
from .utils import getBindingPriority
from .utils import saveConfig
from django.shortcuts import redirect



def home_view (request):


    input_form = InputForm()
    if request.method == 'POST':
        input_form = InputForm(request.POST)

        if input_form.is_valid():

            username = input_form.cleaned_data['username']
            password = input_form.cleaned_data['password']

            primary_mgmt_ip = str(get_primary_mgmt_ip(username,password))

            request.session['params_dict'] = {
                'username': username,
                'password': password,
                'primary_mgmt_ip':primary_mgmt_ip
            }
            return redirect('policy_binding_view')

    context = {
        'form': input_form
    }
    return render(request, 'initial_form.html', context)

def policy_binding_view(request):

    username = request.session['params_dict']['username']
    password = request.session['params_dict']['password']
    mgmt = request.session['params_dict']['primary_mgmt_ip']

    dict = isBound(username,password)
    if dict['bound'] == True:

        if request.method == 'POST':
            unbind_form = UnbindPolicyForm(request.POST)

            if unbind_form.is_valid():

                unbindPolicy(username,password)
                saveConfig(username,password)

                return redirect('policy_binding_view')

        return render(request, 'unbind_form.html', dict)
    else:
        if request.method == 'POST':
            bind_form = BindPolicyForm(request.POST)

            if bind_form.is_valid():

                if getBindingPriority(username, password) is None:
                    return HttpResponse ('<h2>There is responder policy with priority 1 bound to Virtual server already.</h2>')

                bindPolicy(username,password)
                saveConfig(username,password)

                return redirect('policy_binding_view')

        return render(request, 'bind_form.html', dict)

    return HttpResponse('Responder policy bindings will be listed here, mgmt IP: ' + mgmt)