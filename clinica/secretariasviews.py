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
@user_passes_test(is_secretaria)
def secretariasIndex(request):
    personal = Personal.objects.get(usuario=request.user)
    request.session["personalId"] = personal.id
    return render(request, "clinica/secretarias/listaturnos.html", {"secretaria" : personal, "turnos" : Turno.objects.all()})

@login_required(login_url='/accounts/login/')
@user_passes_test(is_secretaria)
def secretariasModificarEstadoTurno(request, turno_id):
    if request.method == "POST":
        form = FormularioEstadoTurno(request.POST)
        if form.is_valid():
            pacientepresente = form.cleaned_data["pacientepresente"]
            turno = Turno.objects.get(id=turno_id)
            ##estado = EstadoPedido.objects.get(tipo=estadoPedido)
            if (pacientepresente == 1):
                turno.pacientepresente = True
            else:
                turno.pacientepresente = False
            print(pacientepresente)
            turno.save()
            
            return HttpResponseRedirect(reverse("clinica:secretariasIndex"))
        else:
            return HttpResponseRedirect(reverse("logout"))

@login_required(login_url='/accounts/login/')
@user_passes_test(is_secretaria)
def secretariasDetallePaciente(request):
    if request.method == "POST":
        form = FormularioPacienteIdSecretaria(request.POST)
        if form.is_valid():
            idSecretaria = form.cleaned_data["idSecretaria"]
            idPaciente = form.cleaned_data["idPaciente"]
            personal = Personal.objects.get(id=idSecretaria)
            paciente = Paciente.objects.get(id=idPaciente)
    else:
        personal = Personal.objects.get(id=request.session["personalId"])
        paciente = Paciente.objects.get(id=request.session["pacienteId"])
    turnosPaciente = Turno.objects.all().filter(paciente=paciente)
    return render(request, "clinica/secretarias/detallepaciente.html", {"personal" : personal, "paciente" : paciente, "turnos" : turnosPaciente, "form":FormularioNuevoTurno(idSecretaria=personal.id, idPaciente=paciente.id)})

@login_required(login_url='/accounts/login/')
@user_passes_test(is_secretaria)
def borrarTurno(request, turno_id):
    if request.method == "POST":
        turno = Turno.objects.get(id=turno_id)
        turno.delete()
    return HttpResponseRedirect(reverse("clinica:secretariasIndex"))

@login_required(login_url='/accounts/login/')
@user_passes_test(is_secretaria)
def edicionTurno(request, turno_id):
    turno = Turno.objects.get(id=turno_id)
    form = TurnoForm(instance=turno)
    if request.method == "POST":
        form = TurnoForm(request.POST, instance=turno)
        if form.is_valid():
            turno = form.save(commit=False)
            turno.save()
            return HttpResponseRedirect(reverse("clinica:secretariasIndex"))
    else:
        return render(request, "clinica/secretarias/edicionturno.html", {"form":form, "turno_id" : turno_id})

@login_required(login_url='/accounts/login/')
@user_passes_test(is_secretaria)
def nuevoTurno(request, secretaria_id):
    if request.method == "POST":
        form = FormularioNuevoTurno(request.POST, idSecretaria=0, idPaciente=0)
        if form.is_valid():
            idSecretaria = form.cleaned_data["idSecretaria"]
            idPaciente = form.cleaned_data["idPaciente"]
            idMedico = form.cleaned_data["idMedico"]
            fecha = form.cleaned_data["fecha"]
            hora = form.cleaned_data["hora"]
            try:
                secretaria = Personal.objects.get(id=idSecretaria)
                paciente = Paciente.objects.get(id=idPaciente)
                medico = Personal.objects.get(id=idMedico)
                turno = Turno(medico=medico, paciente=paciente, secretaria=secretaria, fecha=fecha, hora=hora)
                turno.save()
                return HttpResponseRedirect(reverse("clinica:secretariasIndex"))
            except:
                return render(request, "clinica/secretarias/detallepaciente.html", {"form":form})
        else:
            return render(request, "clinica/secretarias/detallepaciente.html", {"form":form})
    else:
        return render(request, "clinica/secretarias/nuevoturno.html", { "secretaria_id":secretaria_id, "form":FormularioNuevoTurnoCompleto(idSecretaria=secretaria_id)})

@login_required(login_url='/accounts/login/')
@user_passes_test(is_secretaria)
def nuevoPaciente(request, secretaria_id):
    if request.method == "POST":
        form = FormularioNuevoPaciente(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data["nombre"]
            apellido = form.cleaned_data["apellido"]
            telefono = form.cleaned_data["telefono"]
            try:
                paciente = Paciente(nombre=nombre, apellido=apellido, telefono=telefono)
                paciente.save()
                request.session["pacienteId"] = paciente.id
                return HttpResponseRedirect(reverse("clinica:secretariasDetallePaciente"))
            except:
                return render(request, "clinica/secretarias/nuevopaciente.html", {"secretaria_id":secretaria_id, "form":form})
        else:
            return render(request, "clinica/secretarias/nuevopaciente.html", {"secretaria_id":secretaria_id, "form":form})
    else:
        return render(request, "clinica/secretarias/nuevopaciente.html", {"secretaria_id":secretaria_id, "form":FormularioNuevoPaciente()})
