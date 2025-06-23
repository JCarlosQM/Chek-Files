# 🔐 File Integrity Checker en Python

Un verificador de integridad de archivos sencillo y potente hecho en Python.  
Permite detectar cambios, eliminaciones o adiciones en los archivos de una carpeta seleccionada, generando un **reporte HTML** limpio y comprensible. Ideal para monitoreo de sistemas, backups, código o carpetas críticas.

---

## 🧠 ¿Qué hace?

- Calcula el hash SHA-256 de todos los archivos en una carpeta.
- Guarda un **snapshot** de hashes para usar como referencia.
- Detecta:
  - ✅ Archivos nuevos
  - ✅ Archivos modificados
  - ✅ Archivos eliminados
- Genera automáticamente un **reporte HTML actualizado** con los cambios detectados.
- Pensado para ejecutarse como script o empaquetarse como `.exe`.

---

## 🚀 Uso rápido

1. Clona o descarga el repositorio:
    ```bash
    git clone https://github.com/JCarlosQM/Chek-Files.git
    cd Chek-Files
    ```

2. Instala las dependencias (opcional, si se agregan nuevas funcionalidades):
    ```bash
    pip install -r requirements.txt
    ```

3. Ejecuta el script principal:
    ```bash
    python main.py
    ```

---

## 📋 Menú principal

```text
=== File Integrity Checker ===
1. Guardar hashes iniciales
2. Escanear cambios
3. Salir
