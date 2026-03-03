

<p align="center"><img width="422" height="119" alt="logo_upaep" src="https://github.com/user-attachments/assets/85e05ec0-1d92-4462-b9b2-40467e113e7b" />              <img height="119" alt="Logos" src="https://github.com/user-attachments/assets/1c5ad650-a0cc-42ae-a3df-779b8cdaad04" /></p>






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

### 2️⃣ Instalar dependencias
```powershell
pip install -r requirements.txt
```
---

### 🔎 Verificación de instalación

Para comprobar que la biblioteca se instaló correctamente, ejecutar:

```powershell
python -c "import oqs; print('OQS instalado correctamente')"
```
---
### 🔬 Verificación de algoritmos disponibles

Para verificar que ML-KEM y ML-DSA están habilitados:

```powershell
python -c "import oqs; print('KEM disponibles:', oqs.get_enabled_KEM_mechanisms()); print('Firmas disponibles:', oqs.get_enabled_sig_mechanisms())"
```
Debe aparecer una lista que incluya variantes como:

- ML-KEM-512 / 768 / 1024

- ML-DSA-44 / 65 / 87

---
## ▶️ Ejecución del Taller

Una vez instalada la biblioteca y verificado el entorno, ejecutar los siguientes scripts en el siguiente orden:

### 🔐 1️⃣ ML-KEM — Cifrado y Descifrado

```powershell
python 1_mlkem_cifrado.py
```
Este script:

-Genera un secreto compartido mediante ML-KEM.

-Deriva una clave simétrica.

-Cifra el archivo message.txt.

-Descifra el mensaje y verifica que coincida.

-Muestra tamaños de claves y tiempos de ejecución.

---

### ✍️ 2️⃣ ML-DSA — Firma Digital
```powershell
python 2_mldsa_firma.py
```
Este script:

-Genera claves ML-DSA.

-Firma digitalmente el archivo message.txt.

-Verifica la validez de la firma.

-Permite modificar el archivo para observar cómo la verificación falla.

---
## 🧪 Actividad Guiada

1. Ejecutar el script de firma.

2. Modificar una línea en message.txt.

3. Ejecutar nuevamente el script.

4. Observar que la verificación ahora es INVÁLIDA.
   
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
## 📚 Referencias

1. National Institute of Standards and Technology (NIST).  
   **FIPS 203 – Module-Lattice-Based Key-Encapsulation Mechanism Standard (ML-KEM).**  
   https://csrc.nist.gov/pubs/fips/203/final

2. National Institute of Standards and Technology (NIST).  
   **FIPS 204 – Module-Lattice-Based Digital Signature Standard (ML-DSA).**  
   https://csrc.nist.gov/pubs/fips/204/final

3. Open Quantum Safe (OQS) Project.  
   **liboqs – Open-source quantum-resistant cryptographic library.**  
   https://openquantumsafe.org/

4. Open Quantum Safe GitHub Repository.  
   https://github.com/open-quantum-safe/liboqs

5. NIST Post-Quantum Cryptography Project.  
   https://csrc.nist.gov/projects/post-quantum-cryptography
---
👨‍🏫 Estudiante-Instructor

**Israel Jaudy Pérez Bermúdez**  
Ingeniero Mecatrónico  
Maestría en Ciencias y Tecnologías de Seguridad – INAOE  
Líneas de trabajo: Identidad Digital y Criptografía Post-Cuántica  
israelj.perezb@inaoep.mx
- ---

🎓 Instructor-Coordinación Académica

**Dr. Miguel Morales Sandoval**  
Investigador en Ciencias Computacionales  
Instituto Nacional de Astrofísica, Óptica y Electrónica (INAOE)  
mmorales@inaoep.mx

---
