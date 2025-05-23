import os
from django.utils.text import slugify

def caminho_foto_perfil(instance, filename):
    entidade_nome = slugify(instance.u_entidade.e_nome)
    username = slugify(instance.username)
    tipo = slugify(instance.is_staff)
    if tipo == 'true':
        tipo = 'administrador'
    else:
        tipo = 'utilizador'
    if instance.is_superuser:
        tipo = 'superutilizador'
        return f'Entidades/{entidade_nome}/utilizadores/{tipo}/{username}/perfil/{filename}'
    return f'Entidades/{entidade_nome}/utilizadores/{tipo}/{username}/perfil/{filename}'

def caminho_foto_veiculo(instance, filename):
    entidade_nome = slugify(instance.v_entidade.e_nome)
    matricula = slugify(instance.v_matricula)
    return f'Entidades/{entidade_nome}/veiculos/{matricula}/fotos/{filename}'

def caminho_anexo_veiculo(instance, filename):
    entidade_nome = slugify(instance.an_veiculo.v_entidade.e_nome)
    matricula = slugify(instance.an_veiculo.v_matricula)
    tipo = slugify(instance.an_tipo)
    if tipo == '1':
        tipo = 'seguro'
    elif tipo == '2':
        tipo = 'inspecao'
    elif tipo == '3':
        tipo = 'iuc'
    else:
        tipo = 'outros'
    return f'Entidades/{entidade_nome}/veiculos/{matricula}/anexos/{tipo}/{filename}'
