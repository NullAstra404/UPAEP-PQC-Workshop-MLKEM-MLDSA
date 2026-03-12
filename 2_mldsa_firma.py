import os
import sys
import time
from dataclasses import dataclass

import oqs

# =========================
# Configuración del taller
# =========================
SIG_ALG = "ML-DSA-65"   # Cambiar a: ML-DSA-44 / ML-DSA-65 / ML-DSA-87
INPUT_FILE = "message.txt"

# Archivos de salida / persistencia
PUBLIC_KEY_FILE = "mldsa_pk.bin"
SECRET_KEY_FILE = "mldsa_sk.bin"     # solo para demo local; NO recomendado en producción
SIGNATURE_FILE = "message.sig.bin"

# =========================
# Utilidades
# =========================
@dataclass
class Sizes:
    public_key: int
    secret_key: int
    signature: int
    message: int

def print_header(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)

def ns_to_ms(ns: int) -> float:
    return ns / 1_000_000.0

def read_bytes(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()

def write_bytes(path: str, data: bytes) -> None:
    with open(path, "wb") as f:
        f.write(data)

def ensure_exists(path: str, description: str) -> None:
    if not os.path.exists(path):
        raise FileNotFoundError(f"No se encontró {description}: '{path}'")

def usage() -> None:
    print("Uso:")
    print("  python 2_mldsa_firma.py sign")
    print("  python 2_mldsa_firma.py verify")

# =========================
# Modo: sign
# =========================
def sign_mode() -> None:
    ensure_exists(INPUT_FILE, "el archivo de entrada")

    print_header("ML-DSA — Modo sign (generación de llaves y firma)")

    message = read_bytes(INPUT_FILE)

    print(f"Archivo de entrada: {INPUT_FILE}")
    print(f"Tamaño del mensaje (bytes): {len(message)}")
    print(f"Algoritmo de firma seleccionado: {SIG_ALG}")

    with oqs.Signature(SIG_ALG) as signer:
        # KeyGen
        t0 = time.perf_counter_ns()
        public_key = signer.generate_keypair()
        secret_key = signer.export_secret_key()
        t1 = time.perf_counter_ns()

        # Firma
        t2 = time.perf_counter_ns()
        signature = signer.sign(message)
        t3 = time.perf_counter_ns()

    # Guardar materiales
    write_bytes(PUBLIC_KEY_FILE, public_key)
    write_bytes(SECRET_KEY_FILE, secret_key)
    write_bytes(SIGNATURE_FILE, signature)

    sizes = Sizes(
        public_key=len(public_key),
        secret_key=len(secret_key),
        signature=len(signature),
        message=len(message),
    )

    print_header("Resultados")
    print("Firma generada correctamente y guardada en disco.")

    print("\nTamaños (bytes)")
    print(f" - Public Key:  {sizes.public_key}")
    print(f" - Secret Key:  {sizes.secret_key}")
    print(f" - Firma:       {sizes.signature}")
    print(f" - Mensaje:     {sizes.message}")

    print("\nTiempos (ms)")
    print(f" - KeyGen:      {ns_to_ms(t1 - t0):.3f}")
    print(f" - Firma:       {ns_to_ms(t3 - t2):.3f}")

    print("\nArchivos generados")
    print(f" - {PUBLIC_KEY_FILE}   (llave pública)")
    print(f" - {SECRET_KEY_FILE}   (llave privada - solo demo local)")
    print(f" - {SIGNATURE_FILE}    (firma del mensaje)")

    print_header("Siguiente")
    print("Ahora ejecuta:")
    print("  python 2_mldsa_firma.py verify")
    print("Luego modifica message.txt y vuelve a ejecutar verify.")
    print("Finalmente restaura message.txt y vuelve a ejecutar verify.")

# =========================
# Modo: verify
# =========================
def verify_mode() -> None:
    ensure_exists(INPUT_FILE, "el archivo de entrada")
    ensure_exists(PUBLIC_KEY_FILE, "la llave pública")
    ensure_exists(SIGNATURE_FILE, "la firma guardada")

    print_header("ML-DSA — Modo verify (verificación de firma existente)")

    message = read_bytes(INPUT_FILE)
    public_key = read_bytes(PUBLIC_KEY_FILE)
    signature = read_bytes(SIGNATURE_FILE)

    print(f"Archivo de entrada: {INPUT_FILE}")
    print(f"Tamaño del mensaje (bytes): {len(message)}")
    print(f"Algoritmo de firma seleccionado: {SIG_ALG}")

    with oqs.Signature(SIG_ALG) as verifier:
        t0 = time.perf_counter_ns()
        valid = verifier.verify(message, signature, public_key)
        t1 = time.perf_counter_ns()

    print_header("Resultado de verificación")
    print("Verificación:", "VÁLIDA ✅" if valid else "INVÁLIDA ❌")

    print("\nTamaños (bytes)")
    print(f" - Public Key:  {len(public_key)}")
    print(f" - Firma:       {len(signature)}")
    print(f" - Mensaje:     {len(message)}")

    print("\nTiempo (ms)")
    print(f" - Verificación: {ns_to_ms(t1 - t0):.3f}")

    print("\nInterpretación")
    if valid:
        print("La firma corresponde exactamente al contenido actual de message.txt.")
    else:
        print("La firma NO corresponde al contenido actual de message.txt.")
        print("Esto indica que el mensaje fue modificado o que la firma/llave pública no corresponden.")

# =========================
# Flujo principal
# =========================
def main() -> None:
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)

    mode = sys.argv[1].strip().lower()

    if mode == "sign":
        sign_mode()
    elif mode == "verify":
        verify_mode()
    else:
        usage()
        sys.exit(1)

if __name__ == "__main__":
    main()
