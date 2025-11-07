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
from typing import List, Dict, Optional

CSV_DEFAULT = "countries_sample.csv"

def leer_csv(path: str) -> List[Dict]:
    paises = []
    try:
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader, start=1):
                try:
                    nombre = row.get('nombre', '').strip()
                    poblacion = int(row.get('poblacion', '0'))
                    superficie = int(row.get('superficie', '0'))
                    continente = row.get('continente', '').strip()
                    if not nombre or not continente:
                        print(f"[WARN] Fila {i}: campos nombre/continente vacíos. Se ignora.")
                        continue
                    paises.append({
                        'nombre': nombre,
                        'poblacion': poblacion,
                        'superficie': superficie,
                        'continente': continente
                    })
                except ValueError:
                    print(f"[WARN] Fila {i}: error al convertir numeros. Se ignora.")
    except FileNotFoundError:
        print(f"[INFO] Archivo {path} no encontrado. Se creará uno de ejemplo al guardar.")
    except Exception as e:
        print(f"[ERROR] No se pudo leer {path}: {e}")
    return paises

def guardar_csv(path: str, paises: List[Dict]):
    fieldnames = ['nombre', 'poblacion', 'superficie', 'continente']
    try:
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
    except Exception as e:
        print(f"[ERROR] No se pudo guardar en {path}: {e}")

def input_no_vacio(prompt: str) -> str:
    while True:
        v = input(prompt).strip()
        if v == '':
            print("No se permiten campos vacíos. Intente de nuevo.")
        else:
            return v

def agregar_pais(paises: List[Dict]):
    print("\n--- Agregar País ---")
    nombre = input_no_vacio("Nombre: ")
    while any(p['nombre'].lower() == nombre.lower() for p in paises):
        print("Ya existe un país con ese nombre (coincidencia exacta). Si quiere actualizarlo, use 'Actualizar'.")
        nombre = input_no_vacio("Nombre: ")
    try:
        poblacion = int(input_no_vacio("Población (entero): "))
        superficie = int(input_no_vacio("Superficie km² (entero): "))
    except ValueError:
        print("Población y superficie deben ser números enteros. Operación cancelada.")
        return
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
    try:
        idx = int(input("Seleccione número: "))
        if 1 <= idx <= len(resultados):
            return resultados[idx-1]
    except ValueError:
        pass
    print("Selección inválida.")
    return None

def actualizar_pais(paises: List[Dict]):
    print("\n--- Actualizar País ---")
    termino = input_no_vacio("Ingrese nombre (o parte) del país a actualizar: ")
    p = seleccionar_pais_por_nombre(paises, termino)
    if not p:
        print("No se encontró el país.")
        return
    print(f"Actualizando {p['nombre']}. Dejar campo vacío para mantener valor actual.")
    try:
        s_pob = input("Nueva población (actual: {}): ".format(p['poblacion'])).strip()
        if s_pob != '':
            p['poblacion'] = int(s_pob)
        s_sup = input("Nueva superficie (actual: {}): ".format(p['superficie'])).strip()
        if s_sup != '':
            p['superficie'] = int(s_sup)
        print(f"[OK] País '{p['nombre']}' actualizado.")
    except ValueError:
        print("Valores inválidos. No se realizaron cambios.")

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
        try:
            sel = int(input("Seleccione una opción (número): "))
        except ValueError:
            print("Opción inválida.")
            continue
        if sel == 1:
            listar_paises(paises)
        elif sel == 2:
            agregar_pais(paises)
        elif sel == 3:
            actualizar_pais(paises)
        elif sel == 4:
            termino = input_no_vacio("Ingrese término de búsqueda: ")
            res = buscar_paises(paises, termino)
            if res:
                for p in res:
                    print(f"{p['nombre']} - Población: {p['poblacion']}, Superficie: {p['superficie']}, Continente: {p['continente']}")
            else:
                print("No se encontraron coincidencias.")
        elif sel == 5:
            cont = input_no_vacio("Ingrese continente: ")
            res = filtrar_por_continente(paises, cont)
            if res:
                for p in res:
                    print(f"{p['nombre']} - {p['continente']}")
            else:
                print("No se encontraron países para ese continente.")
        elif sel == 6:
            try:
                mn = int(input_no_vacio("Población mínima: "))
                mx = int(input_no_vacio("Población máxima: "))
                res = filtrar_por_rango(paises, 'poblacion', mn, mx)
                if res:
                    for p in res:
                        print(f"{p['nombre']} - Población: {p['poblacion']}")
                else:
                    print("No se encontraron países en ese rango.")
            except ValueError:
                print("Rango inválido.")
        elif sel == 7:
            try:
                mn = int(input_no_vacio("Superficie mínima: "))
                mx = int(input_no_vacio("Superficie máxima: "))
                res = filtrar_por_rango(paises, 'superficie', mn, mx)
                if res:
                    for p in res:
                        print(f"{p['nombre']} - Superficie: {p['superficie']}")
                else:
                    print("No se encontraron países en ese rango.")
            except ValueError:
                print("Rango inválido.")
        elif sel == 8:
            print("Ordenar por:\n1.Nombre\n2.Población\n3.Superficie")
            try:
                opt = int(input("Seleccione: "))
                desc = input("Descendente? (s/n): ").strip().lower() == 's'
                key = 'nombre' if opt == 1 else 'poblacion' if opt == 2 else 'superficie'
                paises[:] = ordenar_paises(paises, key, descending=desc)
                print("[OK] Lista ordenada.")
            except ValueError:
                print("Opción inválida.")
        elif sel == 9:
            mostrar_estadisticas(paises)
        elif sel == 10:
            guardar_csv(CSV_DEFAULT, paises)
        elif sel == 11:
            confirm = input("Desea guardar antes de salir? (s/n): ").strip().lower()
            if confirm == 's':
                guardar_csv(CSV_DEFAULT, paises)
            print("Saliendo...")
            break
        else:
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
        print("[INFO] No hay datos cargados. Se generará un CSV de ejemplo.")
        crear_csv_ejemplo(CSV_DEFAULT)
        paises = leer_csv(CSV_DEFAULT)
    try:
        menu_principal(paises)
    except KeyboardInterrupt:
        print("\n[INFO] Interrupción por teclado. Guardando y saliendo.")
        guardar_csv(CSV_DEFAULT, paises)
    except Exception as e:
        print(f"[ERROR] Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    main()
