import hashlib
import json
import os
import sys

def get_base_path():
    """Obtiene la ruta base, compatible con PyInstaller"""
    if getattr(sys, 'frozen', False):
        # Cuando está empaquetado como .exe
        return os.path.dirname(sys.executable)
    else:
        # Cuando se ejecuta como script .py
        return os.path.dirname(os.path.abspath(__file__))

def get_file_hash(file_path):
    """Calcula el hash SHA-256 de un archivo"""
    sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        print(f"[ERROR] No se pudo leer {file_path}: {e}")
        return None


def save_hashes_to_file(hashes_dict, output_file=None):
    """Guarda los hashes en un archivo JSON"""
    base_path = get_base_path()
    if not output_file:
        output_file = os.path.join(base_path, "data", "file_hashes.json")
    else:
        output_file = os.path.join(base_path, output_file)

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(hashes_dict, f, indent=4)
    print(f"[✓] Hashes guardados en {output_file}")


def load_hashes_from_file(hash_file=None):
    """Carga los hashes desde un archivo JSON"""
    base_path = get_base_path()
    if not hash_file:
        hash_file = os.path.join(base_path, "data", "file_hashes.json")
    else:
        hash_file = os.path.join(base_path, hash_file)

    if not os.path.exists(hash_file):
        return {}
    with open(hash_file, "r", encoding="utf-8") as f:
        return json.load(f)
