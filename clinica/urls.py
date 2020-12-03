from django.urls import path, include
from . import views, secretariasviews, gerenciasviews, talleresviews, ventasviews, medicosviews

app_name = "clinica"
urlpatterns = [
    path("", views.index, name="index"),
    
    path("secretarias/", secretariasviews.secretariasIndex, name="secretariasIndex"),
    path("secretarias/nuevopaciente/<int:secretaria_id>", secretariasviews.nuevoPaciente, name="nuevoPaciente"),
    path("secretarias/nuevoturno/<int:secretaria_id>", secretariasviews.nuevoTurno, name="nuevoTurno"),
    path("secretarias/turno/edicion/<int:turno_id>", secretariasviews.edicionTurno, name="edicionTurno"),
    path("secretarias/turno/borrado/<int:turno_id>", secretariasviews.borrarTurno, name="borrarTurno"),
    path("secretarias/turno/modificarestado/<int:turno_id>", secretariasviews.secretariasModificarEstadoTurno, name="secretariasModificarEstadoTurno"),
    path("secretarias/detallepaciente/", secretariasviews.secretariasDetallePaciente, name="secretariasDetallePaciente"),
    
    path("gerencias/", gerenciasviews.gerenciasIndex, name="gerenciasIndex"),
    path("gerencias/<int:gerencia_id>", gerenciasviews.gerenciasPanelPrincial, name="gerenciasPanelPrincial"),
    path("gerencias/operaciones/pacientesasistencias/<int:gerencia_id>", gerenciasviews.gerenciasAsistenciasDePacientesFiltrar, name="gerenciasAsistenciasDePacientesFiltrar"),
    path("gerencias/reportes/pacientesasistencias/<int:gerencia_id>", gerenciasviews.gerenciasAsistenciaDePacientesResultado, name="gerenciasAsistenciaDePacientesResultado"),
    path("gerencias/operaciones/totalventasmesdevendedores/<int:gerencia_id>", gerenciasviews.gerenciasVentasPormesPorVendedoresFiltrar, name="gerenciasVentasPormesPorVendedoresFiltrar"),
    path("gerencias/reportes/totalventasmesdevendedores/<int:gerencia_id>", gerenciasviews.gerenciasVentasPormesPorVendedoresResultado, name="gerenciasVentasPormesPorVendedoresResultado"),
    path("gerencias/operaciones/productosmasvendidosenmes/<int:gerencia_id>", gerenciasviews.gerenciasProductosMasVendidosFiltrar, name="gerenciasProductosMasVendidosFiltrar"),
    path("gerencias/reportes/productosmasvendidosenmes/<int:gerencia_id>", gerenciasviews.gerenciasProductosMasVendidosResultado, name="gerenciasProductosMasVendidosResultado"),
    path("gerencias/operaciones/pacientesconpedidosenmes/<int:gerencia_id>", gerenciasviews.gerenciasCantidadProductosPedidosPorPacientesEnMesFiltrar, name="gerenciasCantidadProductosPedidosPorPacientesEnMesFiltrar"),
    path("gerencias/reportes/pacientesconpedidosenmes/<int:gerencia_id>", gerenciasviews.gerenciasCantidadProductosPedidosPorPacientesEnMesResultado, name="gerenciasCantidadProductosPedidosPorPacientesEnMesResultado"),

    path("talleres/", talleresviews.talleresIndex, name="talleresIndex"),
    path("talleres/<int:taller_id>", talleresviews.talleresListaPedidos, name="talleresListaPedidos"),
    path("talleres/pedido/modificarEstadoPedido/<int:pedido_id>", talleresviews.tallerModificarEstadoPedido, name="tallerModificarEstadoPedido"),
    path("talleres/pedido/<int:pedido_id>", talleresviews.tallerDetallePedido, name="tallerDetallePedido"),

    path("ventas/", ventasviews.ventasIndex, name="ventasIndex"),
    path("ventas/pedido/<int:pedido_id>", ventasviews.ventasDetallePedido, name="ventasDetallePedido"),
    path("ventas/nuevopedido/<int:vendedor_id>", ventasviews.ventasNuevoPedido, name="ventasNuevoPedido"),
    path("ventas/pedido/nuevoproducto/<int:pedido_id>", ventasviews.ventasNuevoItemPedido, name="ventasNuevoItemPedido"),
    path("ventas/pedido/nuevoproductolente/<int:pedido_id>", ventasviews.ventasNuevoItemPedidoLente, name="ventasNuevoItemPedidoLente"),
    path("ventas/pedido/itempedido/edicion/<int:ItemPedido_id>", ventasviews.ventasEdicionItemPedido, name="ventasEdicionItemPedido"),
    path("ventas/pedido/itempedido/borrado/<int:itemPedido_id>", ventasviews.ventasBorrarItemPedido, name="ventasBorrarItemPedido"),
    path("ventas/pedido/modificarEstadoPedido/<int:pedido_id>", ventasviews.ventasModificarEstadoPedido, name="ventasModificarEstadoPedido"),
    path("ventas/pedido/borrado/<int:pedido_id>", ventasviews.ventasBorrarPedido, name="ventasBorrarPedido"),
    path("ventas/<int:venta_id>", ventasviews.ventasListaPedidos, name="ventasListaPedidos"),

    path("medicos/", medicosviews.medicosIndex, name="medicosIndex"),
    path("medicos/<int:medico_id>", medicosviews.medicosListaPacientes, name="medicosListaPacientes"),
    path("medicos/detallepaciente/<int:turno_id>", medicosviews.medicosDetallePaciente, name="medicosDetallePaciente"),
    path("medicos/detallepaciente/nuevahistoriaclinica/<int:turno_id>", medicosviews.medicosNuevaHistoriaClinica, name="medicosNuevaHistoriaClinica"),
]