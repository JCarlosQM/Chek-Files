from datetime import datetime
import os
import sys
import platform
from core.fileScanner import scan_directory, check_integrity
from core.hashManager import save_hashes_to_file, load_hashes_from_file
from utils.colors import Colors


def limpiar_consola():
    os.system("cls" if platform.system() == "Windows" else "clear")


def get_base_path():
    """Obtiene la ruta base del ejecutable o script actual"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))


def generar_reporte_html(changes, output_path="reporte_integridad.html"):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Reporte de Integridad de Archivos</title>
    <style>
        body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; color: #333; padding: 20px; }}
        h1 {{ color: #005f8d; }}
        .cambio {{ margin-bottom: 20px; }}
        ul {{ background: #fff; padding: 10px; border: 1px solid #ccc; border-radius: 5px; }}
        li {{ margin: 5px 0; }}
        .new {{ color: green; }}
        .modified {{ color: orange; }}
        .deleted {{ color: red; }}
    </style>
</head>
<body>
    <h1>Reporte de Integridad de Archivos</h1>
    <p>Fecha del escaneo: <strong>{fecha}</strong></p>
"""

    if changes["new"]:
        html += "<div class='cambio'><h2 class='new'>Archivos Nuevos</h2><ul>"
        for f in changes["new"]:
            html += f"<li class='new'>{f}</li>"
        html += "</ul></div>"

    if changes["changed"]:
        html += "<div class='cambio'><h2 class='modified'>Archivos Modificados</h2><ul>"
        for f in changes["changed"]:
            html += f"<li class='modified'>{f}</li>"
        html += "</ul></div>"

    if changes["deleted"]:
        html += "<div class='cambio'><h2 class='deleted'>Archivos Eliminados</h2><ul>"
        for f in changes["deleted"]:
            html += f"<li class='deleted'>{f}</li>"
        html += "</ul></div>"

    if not (changes["new"] or changes["changed"] or changes["deleted"]):
        html += "<p><strong>Todos los archivos están intactos. No se detectaron cambios.</strong></p>"

    html += "</body></html>"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n[✓] Reporte generado: {output_path}")

def mostrar_menu_principal():
    print(f"\n{Colors.BOLD}{Colors.BLUE}=== File Integrity Checker ==={Colors.RESET}")
    print(f"{Colors.CYAN}1. Guardar hashes iniciales{Colors.RESET}")
    print(f"{Colors.CYAN}2. Escanear cambios{Colors.RESET}")
    print(f"{Colors.CYAN}3. Salir{Colors.RESET}")


def mostrar_menu_acciones():
    print(f"\n{Colors.BOLD}{Colors.BLUE}=== Acciones con archivos detectados ==={Colors.RESET}")
    print(f"{Colors.CYAN}1. Guardar{Colors.RESET}")
    print(f"{Colors.CYAN}2. Volver al menú principal{Colors.RESET}")


def seleccionar_carpeta():
    folder = input(f"{Colors.YELLOW}Ingresa la ruta de la carpeta a monitorear: {Colors.RESET}").strip()
    if not os.path.isdir(folder):
        print(f"{Colors.RED}[!] Carpeta no válida.{Colors.RESET}")
        return None
    return folder


def guardar_hashes_iniciales(folder):
    print(f"{Colors.BLUE}[*] Escaneando archivos...{Colors.RESET}")
    hashes = scan_directory(folder)
    if hashes:
        save_hashes_to_file(hashes)
        print(f"{Colors.GREEN}[✓] Hashes guardados correctamente.{Colors.RESET}")
    else:
        print(f"{Colors.RED}[!] No se encontraron archivos.{Colors.RESET}")


def manejar_archivos_detectados(files):
    while True:
        mostrar_menu_acciones()
        choice = input(f"{Colors.YELLOW}Selecciona una opción: {Colors.RESET}").strip()

        if choice == "1":
            guardar_hashes_iniciales(files)
            break
        elif choice == "2":
            break
        else:
            print(f"{Colors.RED}[!] Opción no válida. Intenta de nuevo.{Colors.RESET}")


def detectar_cambios():
    saved_hashes = load_hashes_from_file()
    if not saved_hashes:
        print(f"{Colors.RED}[!] No hay hashes guardados. Primero debes guardar hashes iniciales.{Colors.RESET}")
        return

    print(f"{Colors.BLUE}[*] Comparando hashes...{Colors.RESET}")
    results = check_integrity(saved_hashes)

    nuevos = results.get("new", [])
    modificados = results.get("changed", [])
    eliminados = results.get("deleted", [])

    if eliminados:
        for f in eliminados:
            print(f"{Colors.RED}[!] Archivo eliminado: {f}{Colors.RESET}")

    if nuevos:
        print(f"{Colors.GREEN}[+] Nuevos archivos detectados:{Colors.RESET}")
        for f in nuevos:
            print(f"{Colors.GREEN} - {f}{Colors.RESET}")
        manejar_archivos_detectados(os.path.dirname(nuevos[0]))

    if modificados:
        print(f"{Colors.RED}[!] Archivos modificados:{Colors.RESET}")
        for f in modificados:
            print(f"{Colors.RED} - {f}{Colors.RESET}")
        manejar_archivos_detectados(os.path.dirname(modificados[0]))

    if not nuevos and not modificados and not eliminados:
        print(f"\n{Colors.GREEN}[✓] Todos los archivos están intactos.{Colors.RESET}")
    
    output_dir = os.path.join(get_base_path(), "reports")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "reporte_integridad.html")
    generar_reporte_html(results, output_file)



def main():
    folder_path = None
    while True:
        limpiar_consola()
        mostrar_menu_principal()
        choice = input(f"{Colors.YELLOW}Selecciona una opción: {Colors.RESET}").strip()

        if choice == "1":
            folder_path = seleccionar_carpeta()
            if folder_path:
                guardar_hashes_iniciales(folder_path)
        elif choice == "2":
            detectar_cambios()
        elif choice == "3":
            print(f"{Colors.MAGENTA}Saliendo...{Colors.RESET}")
            break
        else:
            print(f"{Colors.RED}[!] Opción no válida.{Colors.RESET}")

        input(f"\n{Colors.CYAN}Presiona Enter para continuar...{Colors.RESET}")


if __name__ == "__main__":
    main()
