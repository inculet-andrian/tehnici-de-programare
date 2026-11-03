import argparse, json, os

def citeste_linii(cale):
    with open(cale, encoding="utf-8") as f:
        linii = f.read().split("\n")
        return [linie.strip() for linie in linii if linie and not linie[0].startswith("#")]

cai = citeste_linii("./arsenal/privesc/start/suid.txt")


def nume(cale):
    return cale.rsplit("/")[-1]


nume_unice = {nume(c) for c in cai}  # set comprehension


GTFO = {"find", "vim.basic", "vim", "nmap", "cp", "bash",
        "less", "awk", "python3", "perl"}


def suid_constatari(cale):
    cai = citeste_linii(cale)

    cai_unice_sortate = sorted(set(cai))

    rezultat = []

    for cale in cai_unice_sortate:
        nume_bin = cale.rsplit("/")[-1]

        risc = "mare" if nume_bin in GTFO else "normal"
        rezultat.append({
            "cale": cale,
            "nume": nume_bin,
            "risc": risc,
        })

    return rezultat


suid = suid_constatari("./arsenal/privesc/start/suid.txt")
mari = [c for c in suid if c["risc"] == "mare"]

def sudo_constatari(cale):
    out = []
    for ln in citeste_linii(cale):
        user, drept = ln.split(" : ", 1)  # despachetare in tuplu

        risc = "mare" if "NOPASSWD" in drept else "normal"

        out.append({
            "user": user.strip(),
            "drept": drept.strip(),
            "risc": risc
        })
    return out


def cron_constatari(cale):
    out = []

    for linie in citeste_linii(cale):
        campuri = linie.split()

        if len(campuri) < 7:
            continue

        user = campuri[5]
        comanda = " ".join(campuri[6:])


        out.append({
            "user": user,
            "comanda": comanda,
        })

    return out


def enumereaza(d):
    return {
        "suid": suid_constatari(os.path.join(d, "suid.txt")),
        "sudo": sudo_constatari(os.path.join(d, "sudo.txt")),
        "cron": cron_constatari(os.path.join(d, "crontab.txt")),
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("capturi")
    p.add_argument("--json", action="store_true")
    p.add_argument("--risc-mare", action="store_true")
    a = p.parse_args()

    raport = enumereaza(a.capturi)

    if a.risc_mare:
        raport = {
            categorie: [c for c in lista if c.get("risc") == "mare"] for categorie, lista in raport.items()
        }

    if a.json:
        print(json.dumps(raport, indent=2, ensure_ascii=False));
        return

    for categorie, lista in raport.items():
        mari = [c for c in lista if c.get("risc") == "mare"]
        print(f"{categorie}: {len(lista)} gasite, {len(mari)} cu risc mare")

    utilizatori_sudo = {c["user"] for c in raport["sudo"]}
    utilizatori_cron = {c["user"] for c in raport["cron"]}
    useri_implicati = utilizatori_cron.union(utilizatori_sudo)

    print("Utilizatori implicati:", ", ".join(sorted(useri_implicati)))

    # TODO: utilizatorii implicati = multimea userilor din sudo REUNITA cu cei din cron
    with open("./arsenal/privesc/enum.json", "w", encoding="utf-8") as f:
        json.dump(raport, f, indent=2, ensure_ascii=False)
    print("Raport salvat in enum.json")


    grupuri = grupeaza_dupa_risc(raport)
    print("\n\nGrupare dupa risc:")

    for risc, nume_binare in grupuri.items():
        print(f"{risc} : {nume_binare}")

def grupeaza_dupa_risc(raport):
    grupuri = {}

    for categorie, lista, in raport.items():
        for constatare in lista:
            risc = constatare.get("risc", "normal")

            nume_bin = constatare.get("nume")

            if nume_bin is None:
                continue

            grupuri.setdefault(risc, []).append(nume_bin)
    return grupuri


if __name__ == "__main__":

    print("A1.")
    cai = citeste_linii("./arsenal/privesc/start/suid.txt")
    print("linii SUID:", len(cai))

    print("\n\nA2.")
    nume_unice = {nume(c) for c in cai}
    print("SUID distincte:", len(nume_unice))

    print("\n\nA3.")
    suid = suid_constatari("./arsenal/privesc/start/suid.txt")
    mari = [c for c in suid if c["risc"] == "mare"]
    print(len(suid), "SUID,", len(mari), "cu risc mare")
    print(sorted(c["nume"] for c in mari))

    print("\n\nA4. (Functii definite)")

    print("\n\nA5.")

    main()




