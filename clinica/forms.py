from django import forms
from django.forms import ModelForm
from .models import *


class TurnoForm(ModelForm):
    class Meta:
        model = Turno
        fields = ['fecha', 'hora'] 

class ItemPedidoForm(ModelForm):
    class Meta:
        model = ItemPedido
        fields = ['producto', 'cantidad'] 

class HistoriaClinicaForm(ModelForm):
    class Meta:
        model = HistoriaClinica
        fields = ['observacion'] 

class ItemPedidoLenteForm(ModelForm):
    class Meta:
        model = ItemPedido
        fields = ['producto', 'armazon', 'lejos', 'izquierda', 'cantidad'] 

class PedidoForm(ModelForm):
    class Meta:
        model = Pedido
        fields = ['paciente', 'tipoPago'] 

#####

class FormularioNuevoPaciente(forms.Form):
    nombre = forms.CharField(label="Nombre")
    apellido = forms.CharField(label="Apellido")
    telefono = forms.CharField(label="Telefono")

class FormularioNuevoTurno(forms.Form):
    def __init__(self,*args,**kwargs):
        idSecretaria = kwargs.pop('idSecretaria')
        idPaciente = kwargs.pop('idPaciente')
        super(FormularioNuevoTurno,self).__init__(*args,**kwargs)
        self.fields['idSecretaria'] = forms.CharField(widget=forms.HiddenInput(), initial=idSecretaria)
        self.fields['idPaciente'] = forms.CharField(widget=forms.HiddenInput(), initial=idPaciente)
    idMedico = forms.IntegerField(label="Medico", widget=forms.Select(choices=Personal.objects.all().filter(rol=2).values_list('id', 'nombre')))
    fecha = forms.DateTimeField(label='Fecha',input_formats=['%d/%m/%Y'], widget=forms.TextInput(attrs={'placeholder': 'dd/mm/yyyy'}))
    hora = forms.DateTimeField(label='Hora',input_formats=['%H:%M'], widget=forms.TextInput(attrs={'placeholder': 'HH:MM'}))

class FormularioNuevoTurnoCompleto(forms.Form):
    def __init__(self,*args,**kwargs):
        idSecretaria = kwargs.pop('idSecretaria')
        super(FormularioNuevoTurnoCompleto,self).__init__(*args,**kwargs)
        self.fields['idSecretaria'] = forms.CharField(widget=forms.HiddenInput(), initial=idSecretaria)
 

    rolMedido = Rol2.objects.get(tipo="M")
    
    idMedico = forms.IntegerField(label="Medico", widget=forms.Select(choices=Personal.objects.all().filter(rol=rolMedido).values_list('id', 'nombre')))

    idPaciente = forms.IntegerField(label="Paciente", widget=forms.Select(choices=Paciente.objects.all().values_list('id', 'nombre')))
    fecha = forms.DateTimeField(label='Fecha',input_formats=['%d/%m/%Y'], widget=forms.TextInput(attrs={'placeholder': 'dd/mm/yyyy'}))
    hora = forms.DateTimeField(label='Hora',input_formats=['%H:%M'], widget=forms.TextInput(attrs={'placeholder': 'HH:MM'}))

class FormularioPacienteIdSecretaria(forms.Form):
    idPaciente = forms.IntegerField()
    idSecretaria = forms.IntegerField()

class FormularioEstadoPedido(forms.Form):
    estadoPedido = forms.CharField(label="estadoPedido")

class FormularioIdTurno(forms.Form):
    idTurno = forms.IntegerField()

class FormularioDiaMesAnio(forms.Form):
    dia = forms.IntegerField()
    mes = forms.IntegerField()
    anio = forms.IntegerField()

class FormularioMesAnio(forms.Form):
    mes = forms.IntegerField()
    anio = forms.IntegerField()

class FormularioMesAnioAsistenciaChoice(forms.Form):
    OPCIONES =( 
        ("1", "SI Asistieron a los turnos"), 
        ("2", "NO Asistieron a los turnos"), 
    )
    mes = forms.IntegerField()
    anio = forms.IntegerField()
    asistencia = forms.ChoiceField(choices = OPCIONES)

class FormularioEstadoTurno(forms.Form):
    pacientepresente = forms.IntegerField()