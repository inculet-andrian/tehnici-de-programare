# Laborator:  functii, metode si importuri pe web
# Student: Inculet Andrian

import time
import requests
import requests as rq

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

## ex 9
print("\n\nExercitiul 9")
raspuns = rq.get(BASE_URL, timeout=TIMEOUT, headers={"User-Agent": "laborator"})

print("status code: ", raspuns.status_code)  # atribut
print("status ok: ", raspuns.ok)             # metoda
print("url: ", raspuns.url)                 # atribut
print("encoding: ", raspuns.encoding)       # atribut


## ex 10
print("\n\nExercitiul 10")
try:
    time.sleep(1)
    raspuns_good = rq.get(BASE_URL, timeout=TIMEOUT, headers={"User-Agent": "laborator"})
    raspuns_good.raise_for_status()
    print(f"Cererea catre {BASE_URL} a fost cu succes!")

    time.sleep(1)
    raspuns_bad = rq.get(BASE_URL + "/this-page-does-not-exist", timeout=TIMEOUT, headers={"User-Agent": "laborator"})
    raspuns_bad.raise_for_status()
except requests.HTTPError as err:
    print(f"Pagina nu exista sau a returnat eroare: {err}")


## ex 11
print("\n\nExercitiul 11")
time.sleep(1)
raspuns = rq.get(BASE_URL, timeout=TIMEOUT, headers={"User-Agent": "laborator"})

for key, value in raspuns.headers.items():
    print(f"{key}: {value}")


## ex 12
print("\n\nExercitiul 12")
print("Server: ", raspuns.headers.get("Server", "lipseste"))
print("Content-Type: ", raspuns.headers.get("Content-Type", "lipseste"))
print("content-type: ", raspuns.headers.get("content-type", "lipseste"))
# response.headers e case insensitive, deci ambele returneaza aceiasi valoare


## ex 13
print("\n\nExercitiul 13")
print("cyber count: ", raspuns.text.lower().count("cyber"))
# metodele se pot inlantui fiindca .lower() returneaza un nou str care poate fi apelat de .count()



## ex 14
print("\n\nExercitiul 14")
start = raspuns.text.find("<title>") + len("<title>")
end = raspuns.text.find("</title>")

titlu = raspuns.text[start:end].strip()
print("Titlul extras:", titlu)


## ex 15
print("\n\nExercitiul 15")
lines = raspuns.text.splitlines()

total_lines = len(lines)
longest_line = max(lines, key=len) if lines else ""
max_len = len(longest_line)

print("Total lines: ", total_lines)
print("Lungimea celei mai lungi linii: ", max_len)


## ex 16
print("\n\nExercitiul 16")
if raspuns.url.startswith("https://"):
    print("Conexiune securizata")
else:
    print("Conexiune nesecurizata")


## ex 17
print("\n\nExercitiul 17")
time.sleep(1)
raspuns_redir = rq.get("http://cybercor.org", timeout=TIMEOUT, headers={"User-Agent": "laborator"})
for rsp in raspuns_redir.history:
    print(f"{rsp.status_code} -> {rsp.url}")

print(f"Url final: {raspuns_redir.status_code} -> {raspuns_redir.url}")


## ex 18
print("\n\nExercitiul 18")
time.sleep(1)
rsp_get = rq.get(BASE_URL, timeout=TIMEOUT, headers={"User-Agent": "laborator"})
time.sleep(1)
rsp_head = rq.head(BASE_URL, timeout=TIMEOUT, headers={"User-Agent": "laborator"})

print(f"rsp_head len content: {len(rsp_head.content)}")
print(f"rsp_get len content: {len(rsp_get.content)}")
# cererea head solicit doar headerele de raspuns, fara content
# cererea get descarca headerele si contentul paginii (html)


## ex 19
print("\n\nExercitiul 19")
time.sleep(1)
raspuns_cookie = rq.get(BASE_URL, timeout=TIMEOUT, headers={"User-Agent": "laborator"})
if raspuns_cookie.cookies:
    for cookie in raspuns_cookie.cookies:
        print(f"cookie name: {cookie.name}; cookie secure: {cookie.secure}")
else:
    print("Nici un cookie setat.")


## ex 20
print("\n\nExercitiul 20")
session = requests.Session()
session.headers.update({"User-Agent": "laborator"})

time.sleep(1)
raspuns_session = session.get(ECHO_URL + "/headers", timeout=TIMEOUT)
print("Raspuns de la httpbin headers:")
print(raspuns_session.text)
# response.text e un atribut care contine textul decodat al raspunsului
# response.json() e o metoda care face json parsing si returneaza un dict/lista python
