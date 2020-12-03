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
@user_passes_test(is_gerencia)
def gerenciasIndex(request):
    personal = Personal.objects.get(usuario=request.user)
    request.session["personalId"] = personal.id
    return render(request, "clinica/gerencias/panelprincipal.html", {"personal" : personal, "FormularioMesAnio":FormularioMesAnio(), "FormularioMesAnioAsistenciaChoice":FormularioMesAnioAsistenciaChoice()})
        
@login_required(login_url='/accounts/login/')
@user_passes_test(is_gerencia)
def gerenciasCantidadProductosPedidosPorPacientesEnMesResultado(request, gerencia_id):
    personal = Personal.objects.get(id=gerencia_id)
    totalRegistros = ItemPedido.objects.all().filter(fecha__year=request.session["anio"], fecha__month=request.session["mes"]).values('paciente').annotate(cantidad=Sum('cantidad')).order_by('-cantidad')
    for registro in totalRegistros:
        registro['paciente2'] = Paciente.objects.get(id=registro['paciente'])
    return render(request, "clinica/gerencias/reportes/pedidosmensualdepacientes.html", {"personal" : personal, "totalRegistros" : totalRegistros})##totalRegistros
        
@login_required(login_url='/accounts/login/')
@user_passes_test(is_gerencia)
def gerenciasCantidadProductosPedidosPorPacientesEnMesFiltrar(request, gerencia_id):
    if request.method == "POST":
        form = FormularioMesAnio(request.POST)
        if form.is_valid():
            anio = form.cleaned_data["anio"]
            request.session["anio"] = anio
            mes = form.cleaned_data["mes"]
            request.session["mes"] = mes
            return HttpResponseRedirect(reverse("clinica:gerenciasCantidadProductosPedidosPorPacientesEnMesResultado", args=(gerencia_id,)))
        else:
            return HttpResponseRedirect(reverse("logout"))
    else:
        return HttpResponseRedirect(reverse("logout"))
        
@login_required(login_url='/accounts/login/')
@user_passes_test(is_gerencia)
def gerenciasAsistenciaDePacientesResultado(request, gerencia_id):
    personal = Personal.objects.get(id=gerencia_id)
        
    if request.session["asistencia"] == "1":
        varAsistencia = "SI asistieron"
        totalRegistros = Turno.objects.all().filter(fecha__year=request.session["anio"], fecha__month=request.session["mes"], pacientepresente=True).values('paciente').annotate(cantidad=Count('paciente')).order_by('cantidad')
        for registro in totalRegistros:
            registro['paciente2'] = Paciente.objects.get(id=registro['paciente'])
        return render(request, "clinica/gerencias/reportes/asistenciasdepacientes.html", {"personal" : personal, "totalRegistros" : totalRegistros, "varAsistencia" : varAsistencia})##totalRegistros
    else:
        varAsistencia = "NO asistieron"
        totalRegistros = Turno.objects.all().filter(fecha__year=request.session["anio"], fecha__month=request.session["mes"], pacientepresente=False).values('paciente').annotate(cantidad=Count('paciente')).order_by('cantidad')
        for registro in totalRegistros:
            registro['paciente2'] = Paciente.objects.get(id=registro['paciente'])
        return render(request, "clinica/gerencias/reportes/asistenciasdepacientes.html", {"personal" : personal, "totalRegistros" : totalRegistros, "varAsistencia" : varAsistencia})##totalRegistros
        
@login_required(login_url='/accounts/login/')
@user_passes_test(is_gerencia)
def gerenciasAsistenciasDePacientesFiltrar(request, gerencia_id):
    if request.method == "POST":
        form = FormularioMesAnioAsistenciaChoice(request.POST)
        if form.is_valid():
            anio = form.cleaned_data["anio"]
            request.session["anio"] = anio
            mes = form.cleaned_data["mes"]
            request.session["mes"] = mes
            asistencia = form.cleaned_data["asistencia"]
            print("valor asistencia: " + asistencia)
            request.session["asistencia"] = asistencia
            return HttpResponseRedirect(reverse("clinica:gerenciasAsistenciaDePacientesResultado", args=(gerencia_id,)))
        else:
            return HttpResponseRedirect(reverse("logout"))
    else:
        return HttpResponseRedirect(reverse("logout"))
        
@login_required(login_url='/accounts/login/')
@user_passes_test(is_gerencia)
def gerenciasProductosMasVendidosResultado(request, gerencia_id):
    personal = Personal.objects.get(id=gerencia_id)
    totalRegistros = ItemPedido.objects.all().filter(fecha__year=request.session["anio"], fecha__month=request.session["mes"]).values('producto').annotate(cantidad=Sum('cantidad')).order_by('-cantidad')
    for registro in totalRegistros:
        registro['producto2'] = Producto.objects.get(id=registro['producto'])
    return render(request, "clinica/gerencias/reportes/productosmasvendidosenmes.html", {"personal" : personal, "totalRegistros" : totalRegistros})##totalRegistros
        
@login_required(login_url='/accounts/login/')
@user_passes_test(is_gerencia)
def gerenciasProductosMasVendidosFiltrar(request, gerencia_id):
    if request.method == "POST":
        form = FormularioMesAnio(request.POST)
        if form.is_valid():
            anio = form.cleaned_data["anio"]
            request.session["anio"] = anio
            mes = form.cleaned_data["mes"]
            request.session["mes"] = mes
            return HttpResponseRedirect(reverse("clinica:gerenciasProductosMasVendidosResultado", args=(gerencia_id,)))
        else:
            return HttpResponseRedirect(reverse("logout"))
    else:
        return HttpResponseRedirect(reverse("logout"))
        
@login_required(login_url='/accounts/login/')
@user_passes_test(is_gerencia)
def gerenciasVentasPormesPorVendedoresResultado(request, gerencia_id):
    personal = Personal.objects.get(id=gerencia_id)
    totalRegistros = ItemPedido.objects.all().filter(fecha__year=request.session["anio"], fecha__month=request.session["mes"]).values('vendedor').annotate(total=Sum('total')).order_by('total')
    for registro in totalRegistros:
        registro['vendedor2'] = Personal.objects.get(id=registro['vendedor'])
    return render(request, "clinica/gerencias/reportes/totalventasmesdevendedores.html", {"personal" : personal, "totalRegistros" : totalRegistros})##totalRegistros

@login_required(login_url='/accounts/login/')
@user_passes_test(is_gerencia)
def gerenciasVentasPormesPorVendedoresFiltrar(request, gerencia_id):
    if request.method == "POST":
        form = FormularioMesAnio(request.POST)
        if form.is_valid():
            anio = form.cleaned_data["anio"]
            request.session["anio"] = anio
            mes = form.cleaned_data["mes"]
            request.session["mes"] = mes
            return HttpResponseRedirect(reverse("clinica:gerenciasVentasPormesPorVendedoresResultado", args=(gerencia_id,)))
        else:
            return HttpResponseRedirect(reverse("logout"))
    else:
        return HttpResponseRedirect(reverse("logout"))
        
@login_required(login_url='/accounts/login/')
@user_passes_test(is_gerencia)
def gerenciasPanelPrincial(request, gerencia_id):
    personal = Personal.objects.get(id=gerencia_id)
    return render(request, "clinica/gerencias/panelprincipal.html", {"personal" : personal})
