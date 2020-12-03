from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import *
from .forms import *
from django.db.models import Sum, Count
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from .decorators import *
import sys

@login_required(login_url='/accounts/login/')
def index(request):
    usuario = request.user
    if (usuario.groups.filter(name='Secretarias').exists()):
        return HttpResponseRedirect(reverse("clinica:secretariasIndex"))
    elif (usuario.groups.filter(name='Gerencias').exists()):
        return HttpResponseRedirect(reverse("clinica:gerenciasIndex"))
    elif (usuario.groups.filter(name='Taller').exists()):
        return HttpResponseRedirect(reverse("clinica:talleresIndex"))
    elif (usuario.groups.filter(name='Ventas').exists()):
        return HttpResponseRedirect(reverse("clinica:ventasIndex"))
    elif (usuario.groups.filter(name='Medicos').exists()):
        return HttpResponseRedirect(reverse("clinica:medicosIndex"))
    personal = Personal.objects.get(usuario=request.user)
    return render(request, "clinica/index.html", {"personal": personal})

