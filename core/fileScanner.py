import os
from core.hashManager import get_file_hash


def scan_directory(directory):
    """Escanea una carpeta y devuelve un diccionario {ruta: hash}"""
    hashes = {}
    for root, _, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)
            try:
                file_hash = get_file_hash(full_path)
                if file_hash:
                    hashes[full_path] = file_hash
            except Exception as e:
                print(f"[!] Error al obtener hash de {full_path}: {e}")
    return hashes


def check_integrity(saved_hashes):
    """Compara los hashes actuales contra los previamente guardados"""
    if not saved_hashes:
        print("[!] No hay hashes guardados para comparar.")
        return {"changed": [], "deleted": [], "new": []}

    # Carpeta base común (asumida) para escanear
    base_dir = os.path.dirname(next(iter(saved_hashes)))
    if not os.path.isdir(base_dir):
        print("[!] Carpeta no válida para escanear.")
        return {"changed": [], "deleted": [], "new": []}

    current_hashes = {}
    changed_files = []
    new_files = []
    deleted_files = []

    # Escanear archivos actuales
    for root, _, files in os.walk(base_dir):
        for file in files:
            full_path = os.path.join(root, file)
            try:
                file_hash = get_file_hash(full_path)
                if file_hash:
                    current_hashes[full_path] = file_hash
            except Exception as e:
                print(f"[!] Error escaneando {full_path}: {e}")

    # Comparar con los guardados
    for file_path, current_hash in current_hashes.items():
        if file_path in saved_hashes:
            if current_hash != saved_hashes[file_path]:
                changed_files.append(file_path)
        else:
            new_files.append(file_path)

    # Archivos eliminados
    for file_path in saved_hashes:
        if file_path not in current_hashes:
            deleted_files.append(file_path)

    return {
        "changed": changed_files,
        "deleted": deleted_files,
        "new": new_files
    }
