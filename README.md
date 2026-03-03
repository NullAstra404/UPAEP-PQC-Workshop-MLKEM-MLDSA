
<img width="300" height="169" alt="logo_upaep" src="https://github.com/user-attachments/assets/27f31a27-aa4d-463f-8e32-66e95c2f831f" />





# Taller Práctico de Criptografía Post-Cuántica  
## ML-KEM y ML-DSA  
### UPAEP – 2026


## 📘 Descripción

Este repositorio contiene el material del taller práctico sobre algoritmos estandarizados de criptografía post-cuántica definidos por el NIST:

- **ML-KEM (FIPS 203)** – Para generación de secreto compartido y posterior uso en procesos de cifrado y descifrado.
- **ML-DSA (FIPS 204)** – Para generación y verificación de firmas digitales post-cuánticas.

El propósito del taller es que los estudiantes ejecuten y comprendan de manera práctica:

- Cómo se genera un secreto compartido.
- Cómo se puede cifrar y descifrar información.
- Cómo funciona una firma digital post-cuántica.
- Qué ocurre cuando un mensaje firmado es modificado.

---

## 🎯 Objetivos del Taller

Al finalizar la sesión, el estudiante será capaz de:

1. Ejecutar ML-KEM para generar un secreto compartido.
2. Utilizar dicho secreto para cifrar y descifrar un mensaje.
3. Firmar digitalmente un archivo utilizando ML-DSA.
4. Verificar la validez de una firma digital.
5. Comprender la diferencia entre confidencialidad e integridad.

---

## 🖥 Requisitos (Windows)

- Windows 10/11
- Python 3.10 o superior
- Git
- Entorno virtual (recomendado)

---

## ⚙️ Instalación

### 1️⃣ Crear entorno virtual

```powershell
py -m venv PQC
.\PQC\Scripts\Activate.ps1
python -m pip install --upgrade pip
```
---

2️⃣ Instalar dependencias
```powershell
pip install -r requirements.txt
```
---
📂 Estructura del Proyecto
```powershell
UPAEP-PQC-Workshop-MLKEM-MLDSA/
│
├── message.txt
├── 1_mlkem_cifrado.py
├── 2_mldsa_firma.py
├── requirements.txt
└── practicas_posteriores/
```
---
## 🔐 Parte 1 – ML-KEM (Cifrado y Descifrado)

En esta práctica se realizará:

- Generación de claves ML-KEM.

- Encapsulación para obtener un secreto compartido.

- Derivación de una clave simétrica.

- Cifrado del archivo message.txt.

- Descifrado del mensaje y verificación de integridad.

Resultado esperado:
```powershell
Secreto compartido generado correctamente.
Mensaje cifrado.
Mensaje descifrado correctamente.
¿Coinciden? True
```
---
## ✍️ Parte 2 – ML-DSA (Firma Digital)

En esta práctica se realizará:

- Generación de claves ML-DSA.

- Firma digital del archivo message.txt.

- Verificación de la firma.

- Modificación del archivo y nueva verificación.

Resultado esperado:
```powershell
Firma generada.
Verificación: VÁLIDA

Mensaje modificado...
Verificación: INVÁLIDA
```

---
🧠 Discusión Académica

- Diferencia entre cifrado y firma digital.

- Impacto del tamaño de claves y firmas post-cuánticas.

- Aplicaciones en certificados digitales, blockchain y sistemas distribuidos.

- Desafíos de la transición hacia criptografía post-cuántica.

---
📂 Prácticas Posteriores (Nivel Avanzado)

En la carpeta practicas_posteriores/ se incluyen ejercicios opcionales:

- Comparación entre ML-KEM-512, 768 y 1024.

- Medición de tiempos de ejecución.

- Análisis del tamaño de claves y firmas.

- Implementación de esquemas híbridos.

  ---
  📚 Referencias

NIST FIPS 203 – ML-KEM

NIST FIPS 204 – ML-DSA

Open Quantum Safe Project
---
👨‍🏫 Estudiante-Instructor

Israel Jaudy Pérez Bermúdez
Ingeniero Mecatrónico
Maestría en Ciencias y Tecnologías de Seguridad – INAOE
Principales lineas de trabajo en Identidad Digital y Criptografía Post-Cuántica
