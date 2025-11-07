#!/usr/bin/env python3
"""
countries_manager.py
Trabajo Práctico Integrador - Programación 1
Autor: Rodrigo Leonel Contreras
Fecha: October 30, 2025

Aplicación por consola para gestionar datos de países:
- Leer/escribir CSV
- Agregar, actualizar, buscar, filtrar, ordenar
- Mostrar estadísticas
"""

import csv
import sys
import os
from typing import List, Dict, Optional

CSV_DEFAULT = "countries_sample.csv"

def leer_csv(path: str) -> List[Dict]:
    paises = []
    while not os.path.exists(path):
        print(f"[WARN] Archivo {path} no encontrado.")
        crear = input("¿Desea crear un archivo de ejemplo? (s/n): ").strip().lower()
        if crear == 's':
            crear_csv_ejemplo(path)
        else:
            print("[INFO] Operación cancelada.")
            return []
    
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=1):
            nombre = row.get('nombre', '').strip()
            continente = row.get('continente', '').strip()
            
            # Validar campos obligatorios
            if not nombre or not continente:
                print(f"[WARN] Fila {i}: campos nombre/continente vacíos. Se ignora.")
                continue
            
            # Validar y convertir población
            pob_valida = False
            while not pob_valida:
                pob_str = row.get('poblacion', '0')
                if pob_str.isdigit():
                    poblacion = int(pob_str)
                    pob_valida = True
                else:
                    print(f"[WARN] Fila {i}: población '{pob_str}' no válida. Se usará 0.")
                    poblacion = 0
                    pob_valida = True
            
            # Validar y convertir superficie
            sup_valida = False
            while not sup_valida:
                sup_str = row.get('superficie', '0')
                if sup_str.isdigit():
                    superficie = int(sup_str)
                    sup_valida = True
                else:
                    print(f"[WARN] Fila {i}: superficie '{sup_str}' no válida. Se usará 0.")
                    superficie = 0
                    sup_valida = True
            
            paises.append({
                'nombre': nombre,
                'poblacion': poblacion,
                'superficie': superficie,
                'continente': continente
            })
    return paises

def guardar_csv(path: str, paises: List[Dict]):
    fieldnames = ['nombre', 'poblacion', 'superficie', 'continente']
    guardado = False
    while not guardado:
        # Verificar permisos de escritura
        dir_path = os.path.dirname(path) or '.'
        if not os.access(dir_path, os.W_OK):
            print(f"[ERROR] No hay permisos de escritura en {dir_path}")
            nuevo_path = input("Ingrese una ruta alternativa (o 'cancelar'): ").strip()
            if nuevo_path.lower() == 'cancelar':
                print("[INFO] Guardado cancelado.")
                return
            path = nuevo_path
            continue
        
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for p in paises:
                writer.writerow({
                    'nombre': p['nombre'],
                    'poblacion': p['poblacion'],
                    'superficie': p['superficie'],
                    'continente': p['continente']
                })
        print(f"[OK] Datos guardados en {path}.")
        guardado = True

def input_no_vacio(prompt: str) -> str:
    while True:
        v = input(prompt).strip()
        if v == '':
            print("No se permiten campos vacíos. Intente de nuevo.")
        else:
            return v

def input_entero(prompt: str) -> int:
    while True:
        valor = input(prompt).strip()
        if valor.lstrip('-').isdigit():
            return int(valor)
        else:
            print("Debe ingresar un número entero válido. Intente de nuevo.")

def agregar_pais(paises: List[Dict]):
    print("\n--- Agregar País ---")
    nombre = input_no_vacio("Nombre: ")
    while any(p['nombre'].lower() == nombre.lower() for p in paises):
        print("Ya existe un país con ese nombre (coincidencia exacta). Si quiere actualizarlo, use 'Actualizar'.")
        nombre = input_no_vacio("Nombre: ")
    poblacion = input_entero("Población (entero): ")
    superficie = input_entero("Superficie km² (entero): ")
    continente = input_no_vacio("Continente: ")
    paises.append({
        'nombre': nombre,
        'poblacion': poblacion,
        'superficie': superficie,
        'continente': continente
    })
    print(f"[OK] País '{nombre}' agregado.")

def listar_paises(paises: List[Dict]):
    if not paises:
        print("[INFO] Sin países cargados.")
        return
    print("\nListado de países:")
    for i, p in enumerate(paises, start=1):
        print(f"{i}. {p['nombre']} - Población: {p['poblacion']}, Superficie: {p['superficie']} km², Continente: {p['continente']}")

def buscar_paises(paises: List[Dict], termino: str) -> List[Dict]:
    termino = termino.lower()
    resultados = [p for p in paises if termino in p['nombre'].lower()]
    return resultados

def seleccionar_pais_por_nombre(paises: List[Dict], termino: str) -> Optional[Dict]:
    resultados = buscar_paises(paises, termino)
    if not resultados:
        return None
    if len(resultados) == 1:
        return resultados[0]
    
    print("Se encontraron múltiples coincidencias:")
    for i, p in enumerate(resultados, start=1):
        print(f"{i}. {p['nombre']}")
    
    while True:
        valor = input("Seleccione número: ").strip()
        if valor.isdigit():
            idx = int(valor)
            if 1 <= idx <= len(resultados):
                return resultados[idx-1]
        print("Selección inválida. Intente de nuevo.")

def actualizar_pais(paises: List[Dict]):
    print("\n--- Actualizar País ---")
    termino = input_no_vacio("Ingrese nombre (o parte) del país a actualizar: ")
    p = seleccionar_pais_por_nombre(paises, termino)
    if not p:
        print("No se encontró el país.")
        return
    
    print(f"Actualizando {p['nombre']}. Dejar campo vacío para mantener valor actual.")
    
    s_pob = input("Nueva población (actual: {}): ".format(p['poblacion'])).strip()
    while s_pob != '':
        if s_pob.lstrip('-').isdigit():
            p['poblacion'] = int(s_pob)
            break
        else:
            print("Debe ingresar un número entero válido.")
            s_pob = input("Nueva población (actual: {}): ".format(p['poblacion'])).strip()
    
    s_sup = input("Nueva superficie (actual: {}): ".format(p['superficie'])).strip()
    while s_sup != '':
        if s_sup.lstrip('-').isdigit():
            p['superficie'] = int(s_sup)
            break
        else:
            print("Debe ingresar un número entero válido.")
            s_sup = input("Nueva superficie (actual: {}): ".format(p['superficie'])).strip()
    
    print(f"[OK] País '{p['nombre']}' actualizado.")

def filtrar_por_continente(paises: List[Dict], continente: str) -> List[Dict]:
    return [p for p in paises if p['continente'].lower() == continente.lower()]

def filtrar_por_rango(paises: List[Dict], campo: str, minimo: int, maximo: int) -> List[Dict]:
    if campo not in ('poblacion', 'superficie'):
        return []
    return [p for p in paises if minimo <= p[campo] <= maximo]

def ordenar_paises(paises: List[Dict], clave: str, descending: bool=False) -> List[Dict]:
    if clave not in ('nombre', 'poblacion', 'superficie'):
        return paises
    return sorted(paises, key=lambda p: p[clave] if clave != 'nombre' else p['nombre'].lower(), reverse=descending)

def mostrar_estadisticas(paises: List[Dict]):
    if not paises:
        print("[INFO] No hay países para calcular estadísticas.")
        return
    mayor = max(paises, key=lambda p: p['poblacion'])
    menor = min(paises, key=lambda p: p['poblacion'])
    promedio_pob = sum(p['poblacion'] for p in paises) / len(paises)
    promedio_sup = sum(p['superficie'] for p in paises) / len(paises)
    conteo_continente = {}
    for p in paises:
        conteo_continente[p['continente']] = conteo_continente.get(p['continente'], 0) + 1
    print("\n--- Estadísticas ---")
    print(f"País con mayor población: {mayor['nombre']} ({mayor['poblacion']})")
    print(f"País con menor población: {menor['nombre']} ({menor['poblacion']})")
    print(f"Promedio de población: {promedio_pob:.2f}")
    print(f"Promedio de superficie: {promedio_sup:.2f} km²")
    print("Cantidad de países por continente:")
    for cont, cnt in conteo_continente.items():
        print(f" - {cont}: {cnt}")

def menu_principal(paises: List[Dict]):
    opciones = [
        "Listar países",
        "Agregar país",
        "Actualizar país",
        "Buscar país",
        "Filtrar por continente",
        "Filtrar por rango de población",
        "Filtrar por rango de superficie",
        "Ordenar países",
        "Mostrar estadísticas",
        "Guardar cambios",
        "Salir"
    ]
    while True:
        print("\n--- Menú Principal ---")
        for i, opt in enumerate(opciones, start=1):
            print(f"{i}. {opt}")
        
        sel = input_entero("Seleccione una opción (número): ")
        
        match sel:
            case 1:
                listar_paises(paises)
            case 2:
                agregar_pais(paises)
            case 3:
                actualizar_pais(paises)
            case 4:
                termino = input_no_vacio("Ingrese término de búsqueda: ")
                res = buscar_paises(paises, termino)
                if res:
                    for p in res:
                        print(f"{p['nombre']} - Población: {p['poblacion']}, Superficie: {p['superficie']}, Continente: {p['continente']}")
                else:
                    print("No se encontraron coincidencias.")
            case 5:
                cont = input_no_vacio("Ingrese continente: ")
                res = filtrar_por_continente(paises, cont)
                if res:
                    for p in res:
                        print(f"{p['nombre']} - {p['continente']}")
                else:
                    print("No se encontraron países para ese continente.")
            case 6:
                mn = input_entero("Población mínima: ")
                mx = input_entero("Población máxima: ")
                res = filtrar_por_rango(paises, 'poblacion', mn, mx)
                if res:
                    for p in res:
                        print(f"{p['nombre']} - Población: {p['poblacion']}")
                else:
                    print("No se encontraron países en ese rango.")
            case 7:
                mn = input_entero("Superficie mínima: ")
                mx = input_entero("Superficie máxima: ")
                res = filtrar_por_rango(paises, 'superficie', mn, mx)
                if res:
                    for p in res:
                        print(f"{p['nombre']} - Superficie: {p['superficie']}")
                else:
                    print("No se encontraron países en ese rango.")
            case 8:
                print("Ordenar por:\n1.Nombre\n2.Población\n3.Superficie")
                opt = input_entero("Seleccione: ")
                desc = input("Descendente? (s/n): ").strip().lower() == 's'
                key = 'nombre' if opt == 1 else 'poblacion' if opt == 2 else 'superficie'
                paises[:] = ordenar_paises(paises, key, descending=desc)
                print("[OK] Lista ordenada.")
            case 9:
                mostrar_estadisticas(paises)
            case 10:
                guardar_csv(CSV_DEFAULT, paises)
            case 11:
                confirm = input("Desea guardar antes de salir? (s/n): ").strip().lower()
                if confirm == 's':
                    guardar_csv(CSV_DEFAULT, paises)
                print("Saliendo...")
                break
            case _:
                print("Opción fuera de rango. Intente de nuevo.")

def crear_csv_ejemplo(path: str):
    ejemplo = [
        {'nombre': 'Argentina', 'poblacion': 45376763, 'superficie': 2780400, 'continente': 'América'},
        {'nombre': 'Japón', 'poblacion': 125800000, 'superficie': 377975, 'continente': 'Asia'},
        {'nombre': 'Brasil', 'poblacion': 213993437, 'superficie': 8515767, 'continente': 'América'},
        {'nombre': 'Alemania', 'poblacion': 83149300, 'superficie': 357022, 'continente': 'Europa'},
    ]
    guardar_csv(path, ejemplo)

def main():
    paises = leer_csv(CSV_DEFAULT)
    if not paises:
        print("[INFO] No hay datos cargados.")
        return
    
    salir = False
    while not salir:
        try:
            menu_principal(paises)
            salir = True
        except KeyboardInterrupt:
            print("\n[INFO] Interrupción detectada.")
            guardar = input("¿Desea guardar antes de salir? (s/n): ").strip().lower()
            if guardar == 's':
                guardar_csv(CSV_DEFAULT, paises)
            print("Saliendo...")
            salir = True

if __name__ == "__main__":
    main()