from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

def is_secretaria(user):
    return user.groups.filter(name='Secretarias').exists()

def is_medico(user):
    return user.groups.filter(name='Medicos').exists()

def is_ventas(user):
    return user.groups.filter(name='Ventas').exists()

def is_taller(user):
    return user.groups.filter(name='Taller').exists()

def is_gerencia(user):
    return user.groups.filter(name='Gerencias').exists()