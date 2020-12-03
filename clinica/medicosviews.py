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
@user_passes_test(is_medico)
def medicosIndex(request):
    personal = Personal.objects.get(usuario=request.user)
    request.session["personalId"] = personal.id
    if "filtrarListaPacientesDeMedico" in request.session:
        if request.session["filtrarListaPacientesDeMedico"]:
            if request.session["filtroAnio"]:
                if request.session["filtroMes"]:
                    if request.session["filtroDia"]:
                        turnos = Turno.objects.all().filter(medico=personal, fecha__year=request.session["anio"], fecha__month=request.session["mes"], fecha__day=request.session["dia"])
                    else:
                        turnos = Turno.objects.all().filter(medico=personal, fecha__year=request.session["anio"], fecha__month=request.session["mes"])
                else:
                    if request.session["filtroDia"]:
                        turnos = Turno.objects.all().filter(medico=personal, fecha__year=request.session["anio"], fecha__day=request.session["dia"])
                    else:
                        turnos = Turno.objects.all().filter(medico=personal, fecha__year=request.session["anio"])
            else:
                if request.session["filtroMes"]:
                    if request.session["filtroDia"]:
                        turnos = Turno.objects.all().filter(medico=personal, fecha__month=request.session["mes"], fecha__day=request.session["dia"])
                    else:
                        turnos = Turno.objects.all().filter(medico=personal, fecha__month=request.session["mes"])
                else:
                    if request.session["filtroDia"]:
                        turnos = Turno.objects.all().filter(medico=personal, fecha__day=request.session["dia"])
                    else:
                        turnos = Turno.objects.all().filter(medico=personal)
        else:
            turnos = Turno.objects.all().filter(medico=personal)
    else:
        turnos = Turno.objects.all().filter(medico=personal)
    return render(request, "clinica/medicos/listapacientes.html", {"personal" : personal, "turnos" : turnos, "form":FormularioDiaMesAnio()})

@login_required(login_url='/accounts/login/')
@user_passes_test(is_medico)
def medicosListaPacientes(request, medico_id):
    if request.method == "POST":
        medico = Personal.objects.get(id=medico_id)
        form = FormularioDiaMesAnio(request.POST)
        form.is_valid()
        filtrar = False
        try:
            anio = form.cleaned_data["anio"]
            request.session["anio"] = anio
            request.session["filtroAnio"] = True
            filtrar = True
        except:
            request.session["filtroAnio"] = False
        try:
            mes = form.cleaned_data["mes"]
            request.session["mes"] = mes
            request.session["filtroMes"] = True
            filtrar = True
        except:
            request.session["filtroMes"] = False
        try:
            dia = form.cleaned_data["dia"]
            request.session["dia"] = dia
            request.session["filtroDia"] = True
            filtrar = True
        except:
            request.session["filtroDia"] = False
        request.session["filtrarListaPacientesDeMedico"] = filtrar
        return HttpResponseRedirect(reverse("clinica:medicosIndex"))
        
    medico = Personal.objects.get(id=medico_id)
    return render(request, "clinica/login.html", {"form":FormularioLogIn()})

@login_required(login_url='/accounts/login/')
@user_passes_test(is_medico)
def medicosDetallePaciente(request, turno_id):
    turno = Turno.objects.get(id=turno_id)
    historiasClinica = HistoriaClinica.objects.all().filter(paciente=turno.paciente)
    form = HistoriaClinicaForm()
    return render(request, "clinica/medicos/detallepaciente.html", {"turno" : turno, "historiasClinica" : historiasClinica, "form": form})

@login_required(login_url='/accounts/login/')
@user_passes_test(is_medico)
def medicosNuevaHistoriaClinica(request, turno_id):
    if request.method == "POST":
        turno = Turno.objects.get(id=turno_id)
        form = HistoriaClinicaForm(request.POST)
        if form.is_valid():
            historiaClinica = form.save(commit=False)
            historiaClinica.medico = turno.medico
            historiaClinica.paciente = turno.paciente
            historiaClinica.save()
            return HttpResponseRedirect(reverse("clinica:medicosDetallePaciente", args=(turno_id,)))##ventasIndex
        else:
            return HttpResponseRedirect(reverse("logout"))
    else:
        return HttpResponseRedirect(reverse("logout"))
