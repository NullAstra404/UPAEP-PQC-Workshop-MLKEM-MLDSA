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
CIPHERTEXT_FILE = "message.cipher.bin"     # texto cifrado
ENCAPSULATION_FILE = "kem.ciphertext.bin"  # "ciphertext" del KEM (encapsulación)
DECRYPTED_FILE = "message.dec.txt"         # texto descifrado

# =========================
# Utilidades
# =========================
def sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()

def xor_stream(data: bytes, key: bytes) -> bytes:
    """
    Cifrado/descifrado por XOR con un keystream derivado del secreto.
    NO es un cifrado recomendado para producción; se usa por simplicidad didáctica.
    """
    out = bytearray(len(data))
    # Expandimos la clave a un keystream del tamaño del mensaje
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

    # 2) Keygen + encapsulación/decapsulación
    with oqs.KeyEncapsulation(KEM_ALG) as kem:
        # Keygen
        t0 = time.perf_counter_ns()
        public_key = kem.generate_keypair()
        secret_key = kem.export_secret_key()
        t1 = time.perf_counter_ns()

        # Encapsulación: genera (kem_ciphertext, shared_secret_sender)
        t2 = time.perf_counter_ns()
        kem_ciphertext, shared_secret_sender = kem.encap_secret(public_key)
        t3 = time.perf_counter_ns()

        # Decapsulación: recupera shared_secret_receiver usando secret_key
        # Nota: para decapsular necesitamos una instancia con la secret_key cargada.
    with oqs.KeyEncapsulation(KEM_ALG, secret_key) as kem_receiver:
        t4 = time.perf_counter_ns()
        shared_secret_receiver = kem_receiver.decap_secret(kem_ciphertext)
        t5 = time.perf_counter_ns()

    # 3) Validación del secreto compartido
    secrets_match = (shared_secret_sender == shared_secret_receiver)

    # 4) Derivar clave simétrica y cifrar/descifrar
    # (clave = SHA-256(shared_secret))
    key = sha256(shared_secret_sender)

    t6 = time.perf_counter_ns()
    ciphertext = xor_stream(plaintext, key)
    t7 = time.perf_counter_ns()

    t8 = time.perf_counter_ns()
    recovered = xor_stream(ciphertext, key)
    t9 = time.perf_counter_ns()

    recovered_ok = (recovered == plaintext)

    # 5) Guardar evidencias
    with open(CIPHERTEXT_FILE, "wb") as f:
        f.write(ciphertext)

    with open(ENcapsulation_FILE := ENCAPSULATION_FILE, "wb") as f:
        f.write(kem_ciphertext)

    with open(DECRYPTED_FILE, "wb") as f:
        f.write(recovered)

    # 6) Métricas de tamaño
    sizes = Sizes(
        public_key=len(public_key),
        secret_key=len(secret_key),
        kem_ciphertext=len(kem_ciphertext),
        shared_secret=len(shared_secret_sender),
    )

    # 7) Resultados
    print_header("Resultados")
    print("Secreto compartido generado correctamente:", secrets_match)
    print("Mensaje cifrado y descifrado correctamente:", recovered_ok)

    print("\nTamaños (bytes)")
    print(f" - Public Key:      {sizes.public_key}")
    print(f" - Secret Key:      {sizes.secret_key}")
    print(f" - KEM Ciphertext:  {sizes.kem_ciphertext}")
    print(f" - Shared Secret:   {sizes.shared_secret}")
    print(f" - Ciphertext msg:  {len(ciphertext)}")

    print("\nTiempos (ms)")
    print(f" - KeyGen:          {ns_to_ms(t1 - t0):.3f}")
    print(f" - Encapsulación:   {ns_to_ms(t3 - t2):.3f}")
    print(f" - Decapsulación:   {ns_to_ms(t5 - t4):.3f}")
    print(f" - Cifrado (XOR):   {ns_to_ms(t7 - t6):.3f}")
    print(f" - Descifrado (XOR):{ns_to_ms(t9 - t8):.3f}")

    print("\nArchivos generados")
    print(f" - {CIPHERTEXT_FILE}        (mensaje cifrado)")
    print(f" - {ENcapsulation_FILE}     (ciphertext de ML-KEM / encapsulación)")
    print(f" - {DECRYPTED_FILE}         (mensaje descifrado)")

    print_header("Siguiente")
    print("Ahora ejecuta:  python 2_mldsa_firma.py")
    print("y luego modifica message.txt para ver que la verificación falla.")

if __name__ == "__main__":
    main()
