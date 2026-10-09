# Laborator:  functii, metode si importuri pe web
# Student: Inculet Andrian

import time
import requests

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

## ex 21
print("\n\nExercitiul 21")
def fetch(url: str, timeout: int = TIMEOUT) -> requests.Response:
    """Efectueaza o cerere GET cu pauza de 1 secunda si User-Agent setat."""
    time.sleep(1)
    return requests.get(url, timeout=timeout, headers={'User-Agent': 'laborator'})

print("Status cod: ", fetch(BASE_URL).status_code)


## ex 22
print("\n\nExercitiul 22")
def get_status(url: str) -> int:
    """Returneaza codul de stare HTTP pentru adresa url."""
    return fetch(url).status_code

print("Status pentru '/': ", get_status(BASE_URL))
print("Status pentru 'robots.txt': ", get_status(BASE_URL + "/robots.txt"))
print("Status pentru 'sitemap.xml': ", get_status(BASE_URL + "/sitemap.xml"))


## ex 23
print("\n\nExercitiul 23")
print("Fetch cu timeout implicit:", fetch(BASE_URL).status_code)
print("Fetch cu timeout explicit (3s):", fetch(BASE_URL, timeout=3).status_code)


## ex 24
print("\n\nExercitiul 24")
def get_title(html: str) -> str:
    """Returneaza titlul din HTML, din <title></title>"""
    start = html.find("<title>")
    if start == -1:
        return ""
    start += len("<title>")
    end = html.find("</title>", start)
    if end == -1:
        return ""
    return html[start:end].strip()

print("Titlu: ", get_title(fetch(BASE_URL).text))


## ex 25
print("\n\nExercitiul 25")
help(get_title)


## ex 26
print("\n\nExercitiul 26")
# adnotarile de tip sunt cu scop de informare
# eg get_status(123) va esua din cauza tipului de date incorect


## ex 27
print("\n\nExercitiul 27")
def page_exists(url: str) -> bool:
    """Verifica daca o pagina exista si trateaza exceptiile."""
    try:
        return get_status(url) == 200
    except requests.RequestException:
        return False

print("Domeniul neexistent exista? ", page_exists("https://this-domain-does-not-exist.invalid"))
print(f"Domeniul '{BASE_URL}' exista? ", page_exists(BASE_URL))


## ex 28
print("\n\nExercitiul 28")
def check_paths(base: str, paths: list[str]) -> dict[str, int]:
    """Verifica o lista de cai relative si returneaza un dictionar {path: status_code}."""
    results = {}
    for path in paths:
        results[path] = get_status(base + path)
    return results

print("Status cai: ", check_paths(BASE_URL, ["/", "/robots.txt", "/sitemap.xml"]))


## ex 29
print("\n\nExercitiul 29")
def get_header(url: str, name: str, default: str = "lipseste") -> str:
    """Returneaza valoarea unui antet specific de la un URL."""
    return fetch(url).headers.get(name, default)

print("Header 'Server': ", get_header(BASE_URL, name="Server"))


## ex 30
print("\n\nExercitiul 30")
def security_headers(url: str) -> dict[str, bool]:
    """Verifica prezenta principalelor 5 antete de securitate."""
    headers = fetch(url).headers
    return {
        "Strict-Transport-Security": "Strict-Transport-Security" in headers,
        "Content-Security-Policy": "Content-Security-Policy" in headers,
        "X-Frame-Options": "X-Frame-Options" in headers,
        "X-Content-Type-Options": "X-Content-Type-Options" in headers,
        "Referrer-Policy": "Referrer-Policy" in headers
    }

print("Security headers: ", security_headers(BASE_URL))


## ex 31
print("\n\nExercitiul 31")
def score_headers(results: dict[str, bool]) -> str:
    """Calculeaza scorul antetelor de securitate prezente."""
    score = sum(1 for present in results.values() if present)
    return f"{score}/{len(results)}"

print("Scor securitate:", score_headers(security_headers(BASE_URL)))


## ex 32
print("\n\nExercitiul 32")
def fetch_robots(base: str) -> str | None:
    """Returneaza textul fisierului /robots.txt sau None daca nu exista."""
    robots_url = base.rstrip("/") + "/robots.txt"
    if page_exists(robots_url):
        return fetch(robots_url).text
    return None

def disallowed_paths(robots_text: str | None) -> list[str]:
    """Extrage caile blocate (Disallow:) din continutul robots.txt."""
    if not robots_text:
        return []
    paths = []
    for line in robots_text.splitlines():
        line = line.strip()
        if line.lower().startswith("disallow:"):
            parts = line.split(":", 1)
            if len(parts) > 1:
                path = parts[1].strip()
                if path:
                    paths.append(path)
    return paths

print("Disallowed paths: ", disallowed_paths(fetch_robots(BASE_URL)))


## ex 33
print("\n\nExercitiul 33")
def response_times(*urls: str) -> dict[str, float]:
    """Masoara timpul de raspuns pentru un numar variabil de URL-uri."""
    times = {}
    for url in urls:
        start = time.time()
        fetch(url, timeout=TIMEOUT)
        end = time.time()
        times[url] = round(end - start, 3)
    return times

print("Response times: ", response_times(BASE_URL, ECHO_URL))


## ex 34
print("\n\nExercitiul 34")
def log(message: str, **details) -> None:
    """Afiseaza un mesaj urmat de detalii cheie-valoare."""
    details_str = " | ".join(f"{k}={v}" for k, v in details.items())
    print(f"{message} | {details_str}")

log("verificat", url=BASE_URL, status=200)

# cand se afiseaza o valoare intr-o metoda, se face print() si se returneaza None (depinde de caz_
# cand se returneaza inapoi ea poate fi salvata intr-o variabila sau prelucrata

