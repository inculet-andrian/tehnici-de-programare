# Laborator:  functii, metode si importuri pe web
# Student: Inculet Andrian
import time

import requests
import requests as rq
from requests import get
import urllib.request

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

## ex 1
print("\n\nExercitiul 1")
print("Versiune requests:", requests.__version__)
# requests are un nevoie de pip install fiindca e o blbioteca 3rd party
# urllib e un modul built-in in python


## ex 2
print("\n\nExercitiul 2")
status_code = requests.get(BASE_URL, timeout=TIMEOUT).status_code
print("Status cu requests.get():", status_code)

time.sleep(1)
status_code = get(BASE_URL, timeout=TIMEOUT).status_code
print("Status cu get():", status_code)
# avantaj la import requests: codul e clar, si evita conflictele cu alte functii
# avantaj la from requests import get: codul e mai scurt si mai usor de scris


## ex 3
print("\n\nExercitiul 3")
time.sleep(1)
pagina = rq.get(BASE_URL, timeout=TIMEOUT)
print("Status cu alias rq:", pagina.status_code)
# aliasul face codul mai usor de citit cand numele modulului e foarte lung sau frecvent utlizat
# aliasul face codul mai greu de citit cand se utlizeaza aliasuri scurte sau prea multe aliasuri in acelasi fisier


## ex 4
print("\n\nExercitiul 4")
headers = {"User-Agent": "laborator"}
request = urllib.request.Request(BASE_URL, headers=headers)

time.sleep(1)
with urllib.request.urlopen(request, timeout=TIMEOUT) as raspuns:
    print("Status urllib:", raspuns.status)
    print("Primele 200 caractere:", raspuns.read().decode("utf-8")[:200])


## ex 5
print("\n\nExercitiul 5")
print(dir(requests))
# get - functie - trimite o cerere http get
# Response - clasa - obiect returnat de cereri
# exceptions - modul - pachet pentru tratarea erorilor http sau retea


## ex 6
print("\n\nExercitiul 6")
help(requests.get)
# parametrul care seteaza timpul maxim de asteptare este `timeout`.

time.sleep(1)
raspuns = requests.get(BASE_URL, timeout=TIMEOUT)
print("Status code cu timeout:", raspuns.status_code)


## ex 7
print("\n\nExercitiul 7")
time.sleep(1)
start = time.perf_counter()
raspuns = requests.get(BASE_URL, timeout=TIMEOUT)
end = time.perf_counter()
dt = end - start

print("Status code:", raspuns.status_code)
print("response.elapsed:", raspuns.elapsed)
print("time dt:", dt)


## ex 8
print("\n\nExercitiul 8")
try:
    import bs4
    print("Modulul bs4 este deja instalat!")
except ImportError:
    print("Instalati modulul cu: pip install beautifulsoup4")


# un modul e un fisier py
# un packet e un director cu fisiere py
# o biblioteca ii o colectie de pachete si module p/u o functionalitate extinsa
