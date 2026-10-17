import argparse
import base64
import hashlib
import json
import os
import re
from urllib.parse import unquote

print("A1:")
s = "Salut"
b = s.encode()          # bytes
print(b, b[0])          # b"Salut" 83

h = b.hex()
print(bytes.fromhex(h))

print("\nA2:")
def ghici_strat(s: str) -> str:
    if re.fullmatch("%[a-zA-Z0-9%]+", s):
        return "url"
    elif re.fullmatch("[0-9a-fA-F]+",s) and len(s) % 2 == 0:
        return "hex"
    elif re.fullmatch("[A-Za-z0-9+/]+={0,2}",s):
        return "base64"
    else:
        return "necunoscut"

print("%2Fetc: ", ghici_strat("%2Fetc"))   # url
print("48656c6c6f: ",ghici_strat("48656c6c6f"))  # hex

print("\nA3:")
def desfa(s: str) -> tuple[str, bytes | None]:
    strat = ghici_strat(s)

    match strat:
        case "url":
            return strat, unquote(s).encode()
        case "hex":
            return strat, bytes.fromhex(s)
        case "base64":
            return strat, base64.b64decode(s)
    return strat, None

print(desfa("48656c6c6f"))


def citibil(b: bytes) -> bool:
    # TODO: True daca toti octetii sunt 32..126
    return all(32 <= c < 127 for c in b)


if __name__ == "__main__":
    print("\nA4:")

    val = "NTM1OTU3NTk="
    for _ in range(8):
        strat, b = desfa(val)
        if b is None:
            break
        nou = b.decode("latin-1")
        if "necunoscut" == ghici_strat(nou):
            print(nou)
            break
        else:
            val = nou

    print("\nA5:")

    date = open("../../probe/xor.bin", "rb").read()
    for k in range(256):
        clar = bytes(b ^ k for b in date)
        if citibil(clar):
            print("cheie: ", k , ", ", clar.decode())
            break

    print("\nA6:")
    tinta = open("../../probe/hashuri.txt").readline().strip()
    print(len(tinta))   # 32 md5 / 40 sha1 / 64 sha256
    for cuv in open("../../probe/wordlist.txt", encoding="latin1"):
        cuv = cuv.strip()

        if hashlib.md5(cuv.encode()).hexdigest() == tinta:
            print("Gasit: ", cuv)
            break

    print("\nA7:")

    p = argparse.ArgumentParser()
    p.add_argument("intrare")
    p.add_argument("--fisier", action="store_true")
    a = p.parse_args()

    if a.fisier:
        with open(a.intrare, "rb") as f:
            val = f.read()
    else:
        val = a.intrare

    val = val.decode()

    fisa_strat = "necunoscut"
    for _ in range(8):
        strat, b = desfa(val)
        if b is None:
            break
        val = b.decode("latin-1")
        fisa_strat = strat
        if citibil(b) and ghici_strat(val) == "necunoscut":
            break




    if not citibil(val.encode("latin-1")):
        print("Rezultatul final nu este complet citibil ca text simplu.")
    else:
        print("Rezultat final decodat:", val)

        fisa = {
            "strat": fisa_strat,
            "rezultat": val
        }

        os.makedirs("../../arsenal/forensics", exist_ok=True)
        with open("../../arsenal/forensics/fisa.json", "w", encoding="utf-8") as f:
            json.dump(fisa, f, indent=4)

        print("Rezultat salvat cu succes în fisa.json")


    print("\nextra punct:")
    with open("../../probe/challenge.bin", "rb") as f:
        secret = f.read().decode()
        b64_bytes = base64.b64decode(secret)
        decoded = ""
        for byte in b64_bytes:
            decoded += chr(byte - 128)

        print(decoded)