# Guía de Instalación – Windows  
## Taller ML-KEM y ML-DSA (UPAEP)

Esta guía describe el proceso completo para preparar un entorno en Windows 10/11 para ejecutar los scripts del taller de Criptografía Post-Cuántica.

---

## 1️⃣ Requisitos Previos

Instalar lo siguiente:

- Windows 10/11
- Python 3.10 o superior (recomendado 3.12.x)
- Git for Windows
- PowerShell

Opcional (solo si hubiera errores de compilación):
- Visual Studio Build Tools (C++ Desktop Development)
- CMake
- Ninja

---

## 2️⃣ Instalación de Python

Descargar desde:
```powershell
https://www.python.org/downloads/windows/
```
⚠️ IMPORTANTE:
Durante la instalación marcar la opción:

☑ Add Python to PATH

Verificar instalación:

```powershell
python --version
```
## 3️⃣ Instalación de Git

Descargar desde:
```powershell
https://git-scm.com/download/win
```
Instalar con opciones por defecto.

Verificar:
```powershell
git --version
```
## 4️⃣ Descargar el Repositorio
Opción A – Clonar con Git (Recomendado)
```powershell
git clone https://github.com/NullAstra404/UPAEP-PQC-Workshop-MLKEM-MLDSA.git
cd UPAEP-PQC-Workshop-MLKEM-MLDSA
```

Opción B – Descargar ZIP

- Ir al repositorio en GitHub.

- Hacer clic en el botón verde Code.

- Seleccionar Download ZIP.

- Extraer el contenido.

- Abrir PowerShell dentro de la carpeta del proyecto.

## 5️⃣ Crear Entorno Virtual

Dentro de la carpeta del proyecto:
```powershell
py -m venv PQC
.\PQC\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

## 6️⃣ Instalar Dependencias
```powershell
pip install -r requirements.txt
```

## 7️⃣ Verificación de Instalación

Verificación básica:
```powershell
python -c "import oqs; print('OQS OK')"
```

Verificación avanzada (listar algoritmos disponibles):
```powershell
python -c "import oqs; print('KEM:', oqs.get_enabled_KEM_mechanisms()); print('SIG:', oqs.get_enabled_sig_mechanisms())"
```
Debe aparecer una lista que incluya variantes como:

- ML-KEM-512 / 768 / 1024

- ML-DSA-44 / 65 / 87

## 8️⃣ Ejecutar el Taller

Primero ejecutar:
```powershell
python 1_mlkem_cifrado.py
```
Luego ejecutar:
```powershell
python 2_mldsa_firma.py
```
## 9️⃣ Posibles Problemas

Si aparece error relacionado con compilación:

Instalar:

- Visual Studio Build Tools
  Descargar desde:

https://visualstudio.microsoft.com/visual-cpp-build-tools/

Durante la instalación seleccionar:

☑ Desktop development with C++

- CMake
  Descargar desde:

https://cmake.org/download/

- Ninja
  Instalar mediante winget:
```powershell
winget install Ninja-build.Ninja
```
Verificar:
```powershell
ninja --version
```
Y repetir:
```powershell
pip install liboqs-python
```
