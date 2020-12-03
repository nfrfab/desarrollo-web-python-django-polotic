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
@user_passes_test(is_ventas)
def ventasIndex(request):
    personal = Personal.objects.get(usuario=request.user)
    request.session["personalId"] = personal.id
    return render(request, "clinica/ventas/listapedidos.html", {"personal" : personal, "pedidos" : Pedido.objects.all()})

@login_required(login_url='/accounts/login/')
@user_passes_test(is_ventas)
def ventasListaPedidos(request, venta_id):
    personal = Personal.objects.get(id=venta_id)
    return render(request, "clinica/ventas/listapedidos.html", {"personal" : personal})

@login_required(login_url='/accounts/login/')
@user_passes_test(is_ventas)
def ventasNuevoPedido(request, vendedor_id):
    vendedor = Personal.objects.get(id=vendedor_id)
    form = PedidoForm()
    if request.method == "POST":
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.vendedor = vendedor
            estado = EstadoPedido.objects.get(tipo="P")
            pedido.estado = estado
            pedido.save()
            return HttpResponseRedirect(reverse("clinica:ventasDetallePedido", args=(pedido.id,)))##ventasIndex
        else:
            return HttpResponseRedirect(reverse("logout"))
    else:
        return render(request, "clinica/ventas/nuevopedido.html", {"vendedor":vendedor, "form" : form})

@login_required(login_url='/accounts/login/')
@user_passes_test(is_ventas)
def ventasNuevoItemPedido(request, pedido_id):
    pedido = Pedido.objects.get(id=pedido_id)
    form = ItemPedidoForm()
    if request.method == "POST":
        form = ItemPedidoForm(request.POST)
        if form.is_valid():
            itemPedido = form.save(commit=False)
            itemPedido.pedido = pedido
            itemPedido.vendedor = pedido.vendedor##para simplificar los reportes
            itemPedido.paciente = pedido.paciente##para simplificar los reportes
            total = itemPedido.producto.precio * itemPedido.cantidad
            itemPedido.total = total
            itemPedido.save()
            return HttpResponseRedirect(reverse("clinica:ventasDetallePedido", args=(pedido_id,)))##ventasIndex
        else:
            return HttpResponseRedirect(reverse("logout"))
    else:
        clasificacion = Clasificacion.objects.get(tipo="G")
        form.fields["producto"].queryset = Producto.objects.filter(clasificacion=clasificacion)
        return render(request, "clinica/ventas/nuevoitempedido.html", {"form":form, "pedido" : pedido})

@login_required(login_url='/accounts/login/')
@user_passes_test(is_ventas)
def ventasNuevoItemPedidoLente(request, pedido_id):
    pedido = Pedido.objects.get(id=pedido_id)
    form = ItemPedidoLenteForm()
    if request.method == "POST":
        form = ItemPedidoLenteForm(request.POST)
        if form.is_valid():
            itemPedido = form.save(commit=False)
            itemPedido.pedido = pedido
            total = itemPedido.producto.precio * itemPedido.cantidad
            itemPedido.total = total
            itemPedido.save()
            return HttpResponseRedirect(reverse("clinica:ventasDetallePedido", args=(pedido_id,)))##ventasIndex
        else:
            return HttpResponseRedirect(reverse("logout"))
    else:
        clasificacion = Clasificacion.objects.get(tipo="L")
        form.fields["producto"].queryset = Producto.objects.filter(clasificacion=clasificacion)
        return render(request, "clinica/ventas/nuevoitempedido.html", {"form":form, "pedido" : pedido})

@login_required(login_url='/accounts/login/')
@user_passes_test(is_ventas)
def ventasBorrarItemPedido(request, itemPedido_id):
    if request.method == "POST":
        itemPedido = ItemPedido.objects.get(id=itemPedido_id)
        pedido_id = itemPedido.pedido.id
        itemPedido.delete()
        return HttpResponseRedirect(reverse("clinica:ventasDetallePedido", args=(pedido_id,)))
    else:
        return HttpResponseRedirect(reverse("logout"))

@login_required(login_url='/accounts/login/')
@user_passes_test(is_ventas)
def ventasBorrarPedido(request, pedido_id):
    if request.method == "POST":
        pedido = Pedido.objects.get(id=pedido_id)
        pedido.delete()
        return HttpResponseRedirect(reverse("clinica:ventasIndex"))
    else:
        return HttpResponseRedirect(reverse("logout"))

@login_required(login_url='/accounts/login/')
@user_passes_test(is_ventas)
def ventasEdicionItemPedido(request, ItemPedido_id):
    itemPedido = ItemPedido.objects.get(id=ItemPedido_id)
    clasificacion = Clasificacion.objects.get(tipo="L")
    clasificacion1 = Clasificacion.objects.get(tipo="G")
    if itemPedido.producto.clasificacion == clasificacion:
        form = ItemPedidoLenteForm(instance=itemPedido)
        form.fields["producto"].queryset = Producto.objects.filter(clasificacion=clasificacion)
    else:
        form = ItemPedidoForm(instance=itemPedido)
        form.fields["producto"].queryset = Producto.objects.filter(clasificacion=clasificacion1)
    if request.method == "POST":
        if itemPedido.producto.clasificacion == clasificacion:
            form = ItemPedidoLenteForm(request.POST, instance=itemPedido)
        else:
            form = ItemPedidoForm(request.POST, instance=itemPedido)
        if form.is_valid():
            itemPedido = form.save(commit=False)
            total = itemPedido.producto.precio * itemPedido.cantidad
            itemPedido.total = total
            itemPedido.save()
            pedido_id = itemPedido.pedido.id
            return HttpResponseRedirect(reverse("clinica:ventasDetallePedido", args=(pedido_id,)))
    else:
        return render(request, "clinica/ventas/edicionitempedido.html", {"form":form, "itemPedido" : itemPedido})

def ventasDetallePedido(request, pedido_id):
    pedido = Pedido.objects.get(id=pedido_id)
    personal = Personal.objects.get(id=pedido.vendedor.id)
    ##if request.method == "POST":
    ##    form = FormularioPacienteIdSecretaria(request.POST)
    ##    if form.is_valid():
    ##        idSecretaria = form.cleaned_data["idSecretaria"]
    ##        idPaciente = form.cleaned_data["idPaciente"]
    ##        personal = Personal.objects.get(id=idSecretaria)
    ##        paciente = Paciente.objects.get(id=idPaciente)

    itemsPedido = ItemPedido.objects.all().filter(pedido=pedido)
    estado = pedido.estado
    estadoPedido = estado.get_tipo_display()
    return render(request, "clinica/ventas/detallepedido.html", {"personal" : personal, "pedido" : pedido, "estadoPedido" : estadoPedido, "itemsPedido" : itemsPedido, "form":FormularioNuevoTurno(idSecretaria=personal.id, idPaciente=1)})

def ventasModificarEstadoPedido(request, pedido_id):
    if request.method == "POST":
        form = FormularioEstadoPedido(request.POST)
        if form.is_valid():
            estadoPedido = form.cleaned_data["estadoPedido"]
            pedido = Pedido.objects.get(id=pedido_id)
            estado = EstadoPedido.objects.get(tipo=estadoPedido)
            pedido.estado = estado
            print(pedido)
            pedido.save()
            
            return HttpResponseRedirect(reverse("clinica:ventasDetallePedido", args=(pedido_id,)))
        else:
            return HttpResponseRedirect(reverse("logout"))
