import argparse
import json
from collections import Counter

from arsenal.aparare.parse_auth import citeste_esecuri

def suspecti(counts, prag=10):
    if prag < 1:
        print("\nB2:")
        raise ValueError(f"prag invalid: {prag} (cel putin 1)")

    rezultat = [(ip, n) for ip, n in counts.items() if n >= prag]
    rezultat.sort(key=lambda x: x[1], reverse=True)
    return rezultat



def main():
    p = argparse.ArgumentParser()
    p.add_argument("log")
    p.add_argument("--prag", type=int, default=10)
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    esecuri = citeste_esecuri(a.log)
    counts = Counter(e["ip"] for e in esecuri)
    sus = suspecti(counts, a.prag)

    print("\nB3:")

    if a.json:
        raport = {
            "esecuri": esecuri,
            "pe_ip": dict(counts),
            "suspecti": sus,
        }
        print(json.dumps(raport, indent=2))
    else:

        print(f"\nEsecuri de autentificare: {len(esecuri)}")
        for ip, n in counts.most_common():
            print(f"{ip}: {n}")

        print(f"\nSuspecti (prag {a.prag}):")
        for ip, n in sus:
            print(f"{ip} ({n} incercari) BRUTE FORCE")


if __name__ == "__main__":
    c = Counter({"203.0.113.9": 13, "198.51.100.7": 2})
    print("\nB1:")
    print(suspecti(c))
    print(suspecti(c, prag=2))

    main()