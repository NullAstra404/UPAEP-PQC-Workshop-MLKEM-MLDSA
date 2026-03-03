import os
import time
from dataclasses import dataclass

import oqs

# =========================
# Configuración del taller
# =========================
SIG_ALG = "ML-DSA-65"   # Cambiar a: ML-DSA-44 / ML-DSA-65 / ML-DSA-87
INPUT_FILE = "message.txt"

# Archivos de salida (evidencias)
PUBLIC_KEY_FILE = "mldsa_pk.bin"
SECRET_KEY_FILE = "mldsa_sk.bin"     # (solo para demo local; NO recomendado en producción)
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

# =========================
# Flujo principal
# =========================
def main() -> None:
    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(
            f"No se encontró '{INPUT_FILE}'. Crea el archivo en el repo antes de ejecutar."
        )

    print_header("Parte 2 — ML-DSA: firma digital + verificación")

    # 1) Leer mensaje
    with open(INPUT_FILE, "rb") as f:
        message = f.read()

    print(f"Archivo de entrada: {INPUT_FILE}")
    print(f"Tamaño del mensaje (bytes): {len(message)}")
    print(f"Algoritmo de firma seleccionado: {SIG_ALG}")

    # 2) Keygen + firma + verificación
    with oqs.Signature(SIG_ALG) as signer:
        # Keygen
        t0 = time.perf_counter_ns()
        public_key = signer.generate_keypair()
        secret_key = signer.export_secret_key()
        t1 = time.perf_counter_ns()

        # Firma
        t2 = time.perf_counter_ns()
        signature = signer.sign(message)
        t3 = time.perf_counter_ns()

    # Verificación (con una instancia nueva usando public_key)
    with oqs.Signature(SIG_ALG) as verifier:
        t4 = time.perf_counter_ns()
        valid = verifier.verify(message, signature, public_key)
        t5 = time.perf_counter_ns()

    # 3) Guardar evidencias (demo)
    with open(PUBLIC_KEY_FILE, "wb") as f:
        f.write(public_key)

    with open(SECRET_KEY_FILE, "wb") as f:
        f.write(secret_key)

    with open(SIGNATURE_FILE, "wb") as f:
        f.write(signature)

    # 4) Tamaños
    sizes = Sizes(
        public_key=len(public_key),
        secret_key=len(secret_key),
        signature=len(signature),
        message=len(message),
    )

    # 5) Resultados
    print_header("Resultados")
    print("Firma generada.")
    print("Verificación:", "VÁLIDA ✅" if valid else "INVÁLIDA ❌")

    print("\nTamaños (bytes)")
    print(f" - Public Key:  {sizes.public_key}")
    print(f" - Secret Key:  {sizes.secret_key}")
    print(f" - Firma:       {sizes.signature}")
    print(f" - Mensaje:     {sizes.message}")

    print("\nTiempos (ms)")
    print(f" - KeyGen:      {ns_to_ms(t1 - t0):.3f}")
    print(f" - Firma:       {ns_to_ms(t3 - t2):.3f}")
    print(f" - Verificación:{ns_to_ms(t5 - t4):.3f}")

    print("\nArchivos generados")
    print(f" - {PUBLIC_KEY_FILE}   (llave pública)")
    print(f" - {SECRET_KEY_FILE}   (llave privada - solo demo local)")
    print(f" - {SIGNATURE_FILE}    (firma del mensaje)")

    # 6) Actividad guiada: modificar mensaje y verificar de nuevo
    print_header("Actividad (modificación del mensaje)")
    print("1) Abre 'message.txt' y cambia UNA línea (por ejemplo, el nombre del autor).")
    print("2) Guarda el archivo.")
    print("3) Vuelve a ejecutar este script.")
    print("   La verificación debe salir como INVÁLIDA, porque el mensaje cambió.")

if __name__ == "__main__":
    main()
