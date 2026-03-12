import os
import time
import hashlib
from dataclasses import dataclass

import oqs

# =========================
# Configuración del taller
# =========================
KEM_ALG = "ML-KEM-768"   # Cambiar a: ML-KEM-512 / ML-KEM-768 / ML-KEM-1024
INPUT_FILE = "message.txt"

# Archivos de salida (para evidencias del taller)
CIPHERTEXT_FILE = "message.cipher.bin"          # mensaje cifrado
ENCAPSULATION_FILE = "kem.ciphertext.bin"       # ciphertext del KEM (encapsulación)
DECRYPTED_FILE = "message.dec.txt"              # mensaje descifrado con clave correcta
WRONG_DECRYPTED_FILE = "message.wrong.dec.txt"  # intento de descifrado con clave incorrecta

# =========================
# Utilidades
# =========================
def sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()

def xor_stream(data: bytes, key: bytes) -> bytes:
    """
    Cifrado/descifrado por XOR con un keystream derivado de la clave.
    NO es un cifrado recomendado para producción; se usa por simplicidad didáctica.
    """
    out = bytearray(len(data))
    counter = 0
    offset = 0

    while offset < len(data):
        block = sha256(key + counter.to_bytes(4, "big"))
        n = min(len(block), len(data) - offset)
        for i in range(n):
            out[offset + i] = data[offset + i] ^ block[i]
        offset += n
        counter += 1

    return bytes(out)

def safe_decode(data: bytes) -> str:
    """
    Intenta decodificar bytes como UTF-8. Si falla, reemplaza caracteres inválidos.
    """
    return data.decode("utf-8", errors="replace")

def short_hex(data: bytes, max_chars: int = 120) -> str:
    """
    Devuelve una representación hexadecimal truncada para visualización.
    """
    h = data.hex()
    return h[:max_chars] + ("..." if len(h) > max_chars else "")

@dataclass
class Sizes:
    public_key: int
    secret_key: int
    kem_ciphertext: int
    shared_secret: int

def print_header(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)

def ns_to_ms(ns: int) -> float:
    return ns / 1_000_000.0

# =========================
# Flujo principal
# =========================
def main() -> None:
    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(
            f"No se encontró '{INPUT_FILE}'. Crea el archivo en el repo antes de ejecutar."
        )

    print_header("Parte 1 — ML-KEM: secreto compartido + cifrar/descifrar (demo)")

    # 1) Lectura del mensaje
    with open(INPUT_FILE, "rb") as f:
        plaintext = f.read()

    print(f"Archivo de entrada: {INPUT_FILE}")
    print(f"Tamaño del mensaje (bytes): {len(plaintext)}")
    print(f"Algoritmo KEM seleccionado: {KEM_ALG}")

    # 2) KeyGen + encapsulación/decapsulación
    with oqs.KeyEncapsulation(KEM_ALG) as kem:
        # KeyGen
        t0 = time.perf_counter_ns()
        public_key = kem.generate_keypair()
        secret_key = kem.export_secret_key()
        t1 = time.perf_counter_ns()

        # Encapsulación: genera (kem_ciphertext, shared_secret_sender)
        t2 = time.perf_counter_ns()
        kem_ciphertext, shared_secret_sender = kem.encap_secret(public_key)
        t3 = time.perf_counter_ns()

    # Decapsulación: recupera shared_secret_receiver usando secret_key
    with oqs.KeyEncapsulation(KEM_ALG, secret_key) as kem_receiver:
        t4 = time.perf_counter_ns()
        shared_secret_receiver = kem_receiver.decap_secret(kem_ciphertext)
        t5 = time.perf_counter_ns()

    # 3) Validación del secreto compartido
    secrets_match = (shared_secret_sender == shared_secret_receiver)

    # 4) Derivar clave simétrica y cifrar/descifrar
    # La clave se deriva a partir del secreto compartido
    key = sha256(shared_secret_sender)

    t6 = time.perf_counter_ns()
    ciphertext = xor_stream(plaintext, key)
    t7 = time.perf_counter_ns()

    t8 = time.perf_counter_ns()
    recovered = xor_stream(ciphertext, key)
    t9 = time.perf_counter_ns()

    recovered_ok = (recovered == plaintext)

    # 4b) Intento de descifrado con clave incorrecta
    wrong_key = sha256(b"wrong-key-demo")
    t10 = time.perf_counter_ns()
    wrong_recovered = xor_stream(ciphertext, wrong_key)
    t11 = time.perf_counter_ns()

    wrong_recovered_ok = (wrong_recovered == plaintext)

    # 5) Guardar evidencias
    with open(CIPHERTEXT_FILE, "wb") as f:
        f.write(ciphertext)

    with open(ENCAPSULATION_FILE, "wb") as f:
        f.write(kem_ciphertext)

    with open(DECRYPTED_FILE, "wb") as f:
        f.write(recovered)

    with open(WRONG_DECRYPTED_FILE, "wb") as f:
        f.write(wrong_recovered)

    # 6) Métricas de tamaño
    sizes = Sizes(
        public_key=len(public_key),
        secret_key=len(secret_key),
        kem_ciphertext=len(kem_ciphertext),
        shared_secret=len(shared_secret_sender),
    )

    # 7) Resultados generales
    print_header("Resultados")
    print("Secreto compartido generado correctamente:", secrets_match)
    print("Mensaje cifrado y descifrado correctamente:", recovered_ok)
    print("¿Descifrado con clave incorrecta coincide con el original?:", wrong_recovered_ok)

    print("\nTamaños (bytes)")
    print(f" - Public Key:        {sizes.public_key}")
    print(f" - Secret Key:        {sizes.secret_key}")
    print(f" - KEM Ciphertext:    {sizes.kem_ciphertext}")
    print(f" - Shared Secret:     {sizes.shared_secret}")
    print(f" - Ciphertext msg:    {len(ciphertext)}")

    print("\nTiempos (ms)")
    print(f" - KeyGen:            {ns_to_ms(t1 - t0):.3f}")
    print(f" - Encapsulación:     {ns_to_ms(t3 - t2):.3f}")
    print(f" - Decapsulación:     {ns_to_ms(t5 - t4):.3f}")
    print(f" - Cifrado (XOR):     {ns_to_ms(t7 - t6):.3f}")
    print(f" - Descifrado correcto:{ns_to_ms(t9 - t8):.3f}")
    print(f" - Descifrado erróneo:{ns_to_ms(t11 - t10):.3f}")

    # 8) Visualización del experimento
    print_header("Visualización del experimento")

    print("Mensaje original:")
    print(safe_decode(plaintext))

    print("\nMensaje cifrado (hex, primeros 120 caracteres):")
    print(short_hex(ciphertext, 120))

    print("\nMensaje descifrado con clave correcta:")
    print(safe_decode(recovered))

    print("\nMensaje descifrado con clave incorrecta:")
    print(safe_decode(wrong_recovered))

    # 9) Archivos generados
    print_header("Archivos generados")
    print(f" - {CIPHERTEXT_FILE}         (mensaje cifrado)")
    print(f" - {ENCAPSULATION_FILE}      (ciphertext de ML-KEM / encapsulación)")
    print(f" - {DECRYPTED_FILE}          (mensaje descifrado con clave correcta)")
    print(f" - {WRONG_DECRYPTED_FILE}    (descifrado con clave incorrecta)")

    # 10) Siguiente paso
    print_header("Siguiente")
    print("Ahora ejecuta: python 2_mldsa_firma.py")
    print("y luego modifica message.txt para ver que la verificación de firma falla.")

if __name__ == "__main__":
    main()
