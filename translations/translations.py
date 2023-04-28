import json

def cargar_traducciones_inicio(idioma):
    with open('translations/translations-inicio.json', encoding='utf-8') as f:
        traducciones = json.load(f)
    return traducciones

def cargar_traducciones_login(idioma):
    with open('translations/translations-login.json', encoding='utf-8') as f:
        traducciones = json.load(f)
    return traducciones

def cargar_traducciones_registro(idioma):
    with open('translations/translations-registro.json', encoding='utf-8') as f:
        traducciones = json.load(f)
    return traducciones

def cargar_traducciones_menu_juegos(idioma):
    with open('translations/translations-menu-juegos.json', encoding='utf-8') as f:
        traducciones = json.load(f)
    return traducciones

def cargar_traducciones_añadir_juego(idioma):
    with open('translations/translations-añadir-juego.json', encoding='utf-8') as f:
        traducciones = json.load(f)
    return traducciones

def cargar_traducciones_visualizar_juego(idioma):
    with open('translations/translations-visualizar-juego.json', encoding='utf-8') as f:
        traducciones = json.load(f)
    return traducciones

def cargar_traducciones_errores(idioma):
    with open('translations/translations-errores.json', encoding='utf-8') as f:
        traducciones = json.load(f)
    return traducciones