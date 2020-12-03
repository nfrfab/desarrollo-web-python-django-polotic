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
@user_passes_test(is_taller)
def talleresIndex(request):
    personal = Personal.objects.get(usuario=request.user)
    request.session["personalId"] = personal.id
    estado = EstadoPedido.objects.get(tipo="T")
    pedidos = Pedido.objects.all().filter(estado=estado)
    return render(request, "clinica/talleres/listapedidos.html", {"personal" : personal, "pedidos" : pedidos})

@login_required(login_url='/accounts/login/')
@user_passes_test(is_taller)
def talleresListaPedidos(request, taller_id):
    personal = Personal.objects.get(id=taller_id)
    return render(request, "clinica/talleres/listapedidos.html", {"personal" : personal})

@login_required(login_url='/accounts/login/')
@user_passes_test(is_taller)
def tallerDetallePedido(request, pedido_id):
    pedido = Pedido.objects.get(id=pedido_id)
    personal = Personal.objects.get(id=pedido.vendedor.id)
    if request.method == "POST":
        form = FormularioPacienteIdSecretaria(request.POST)
        if form.is_valid():
            idSecretaria = form.cleaned_data["idSecretaria"]
            idPaciente = form.cleaned_data["idPaciente"]
            personal = Personal.objects.get(id=idSecretaria)
            paciente = Paciente.objects.get(id=idPaciente)
    itemsPedido = ItemPedido.objects.all().filter(pedido=pedido)
    estado = pedido.estado
    estadoPedido = estado.get_tipo_display()
    return render(request, "clinica/talleres/detallepedido.html", {"personal" : personal, "pedido" : pedido, "estadoPedido" : estadoPedido, "itemsPedido" : itemsPedido})


def modificarEstadoPedidoEnBD(request, pedido_id):
    form = FormularioEstadoPedido(request.POST)
    if form.is_valid():
        estadoPedido = form.cleaned_data["estadoPedido"]
        pedido = Pedido.objects.get(id=pedido_id)
        estado = EstadoPedido.objects.get(tipo=estadoPedido)
        pedido.estado = estado
        print(pedido)
        pedido.save()

@login_required(login_url='/accounts/login/')
@user_passes_test(is_taller)
def tallerModificarEstadoPedido(request, pedido_id):
    if request.method == "POST":
        modificarEstadoPedidoEnBD(request, pedido_id)
        return HttpResponseRedirect(reverse("clinica:talleresIndex"))
    else:
        return HttpResponseRedirect(reverse("logout"))