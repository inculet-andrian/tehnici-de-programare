from dataclasses import dataclass, asdict
import json

SUSPECTE_ID = {4625, 1102, 7045}
CAI_SUSPECTE = ("\\Temp\\", "\\Roaming\\")


@dataclass
class Proces:
    pid: int
    nume: str
    user: str
    cale: str

    def e_suspect(self):
        for cale in CAI_SUSPECTE:
            if cale in self.cale:
                return True
        return False


@dataclass
class Eveniment:
    id: int
    nivel: str
    sursa: str
    cont: str
    mesaj: str

    def e_suspect(self):
        return self.id in SUSPECTE_ID or self.nivel == "critical"


def procese_din_json(cale):
    with open(cale, encoding="utf-8") as f:
        return [Proces(**d) for d in json.load(f)]

def evenimente_din_json(cale):
    with open(cale, encoding="utf-8") as f:
        return [Eveniment(**d) for d in json.load(f)]


@dataclass
class Inventar:
    procese: list

    @classmethod
    def din_json(cls, cale):
        with open(cale, encoding="utf-8") as f:
            return cls([Proces(**d) for d in json.load(f)])

    def __len__(self):
        return len(self.procese)

    def suspecte(self):
        sus_proces = []
        for p in self.procese:
            if p.e_suspect():
                sus_proces.append(p)
        return sus_proces

    def pe_user(self):
        rez = {}
        for p in self.procese:
            rez.setdefault(p.user, []).append(p.nume)
        return rez

def main():
    # p = Proces(3120, "update.exe", "ana", r"C:\Users\ana\AppData\Local\Temp\update.exe")
    # print(p.pid, p.nume)
    # print(p)
    #
    # print(p.e_suspect())
    #
    # procese = procese_din_json("./arsenal/windows/start/procese.json")
    # print("procese:", len(procese))
    # print("suspecte:", sum(1 for p in procese if p.e_suspect()))
    #
    # inv = Inventar.din_json("./arsenal/windows/start/procese.json")
    # print("procese:", len(inv))
    #
    # for p in inv.suspecte():
    #     print(f"  [{p.pid}] {p.nume}  {p.cale}")
    # print(inv.pe_user())

    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("capturi")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    inv = Inventar.din_json(a.capturi + "/procese.json")
    ev = evenimente_din_json(a.capturi + "/evenimente.json")
    alarma = [e for e in ev if e.e_suspect()]

    if a.json:
        raport = {
            "procese_sus": [asdict(p) for p in inv.suspecte()],
            "eveniment_alarma": [asdict(e) for e in alarma]
        }

        print(json.dumps(raport, indent=4))

    else:
        print(f"Procese: {len(inv)} | suspecte: {len(inv.suspecte())}")
        for p in inv.suspecte():
            print(f"  [{p.pid}] {p.nume}  ({p.user})  {p.cale}")

        print(f"Evenimente: {len(ev)} | alarma: {len(alarma)}")
        for e in alarma:
            print(f"  {e.id} [{e.nivel}] {e.cont}: {e.mesaj}")

if __name__ == "__main__":
    main()