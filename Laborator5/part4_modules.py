# Laborator:  functii, metode si importuri pe web
# Student: Inculet Andrian
import hashlib
import json
import re
import socket
import ssl
import time
from html.parser import HTMLParser
import urllib.parse
import requests

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

def fetch(url: str) -> requests.Response:
    time.sleep(1)
    return requests.get(url, timeout=TIMEOUT, headers={"User-Agent": "laborator"})

## ex 35
print("\n\nExercitiul 35")
rezultat = urllib.parse.urlparse("https://cybercor.org/path?x=1#top")

print("scheme: ", rezultat.scheme)
print("netloc: ", rezultat.netloc)
print("path: ", rezultat.path)
print("query: ", rezultat.query)
print("fragment: ", rezultat.fragment)


## ex 36
print("\n\nExercitiul 36")
print(urllib.parse.urljoin(BASE_URL, "/about"))
print(urllib.parse.urljoin(BASE_URL, "contact.html"))
print(urllib.parse.urljoin(BASE_URL, "../index.html"))


## ex 37
print("\n\nExercitiul 37")
def extract_links(html: str) -> set[str]:
    """Extrage toate legaturile href dintr-un HTML fara duplicate."""
    return set(re.findall(r'href="([^"]+)"', html))

html_content = fetch(BASE_URL).text
print("Numar legaturi gasite:", len(extract_links(html_content)))


## ex 38
print("\n\nExercitiul 38")
def split_links(links: set[str], base_url: str) -> tuple[list[str], list[str]]:
    """Separa linkurile interne si externe folosind urljoin si urlparse."""
    same_domain = []
    diff_domains = []
    base_netloc = urllib.parse.urlparse(base_url).netloc

    for link in links:
        full_url = urllib.parse.urljoin(base_url, link)
        link_netloc = urllib.parse.urlparse(full_url).netloc
        if link_netloc == base_netloc:
            same_domain.append(full_url)
        else:
            diff_domains.append(full_url)

    return same_domain, diff_domains

interne, externe = split_links(extract_links(html_content), BASE_URL)
print(f"Legaturi interne: {len(interne)}, Legaturi externe: {len(externe)}")


## ex 39
print("\n\nExercitiul 39")
class ImageFinder(HTMLParser):
    """Parser HTML pentru colectarea atributelor src ale tag-urilor img."""
    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "img":
            src = dict(attrs).get("src")
            if src is not None:
                self.images.append(src)

test_html = """
<html><body>
  <img src="/logo.png" alt="Logo">
  <IMG SRC="poza.jpg">
  <img alt="imagine fara src">
  <img src="https://cdn.example.com/banner.webp" />
  <a href="/despre">Aceasta nu este o imagine</a>
</body></html>
"""

finder = ImageFinder()
finder.feed(test_html)
assert finder.images == [
    "/logo.png",
    "poza.jpg",
    "https://cdn.example.com/banner.webp",
], "Parserul nu a gasit exact imaginile asteptate"
print("Testul unitar pentru ImageFinder a trecut cu succes!")


finder_real = ImageFinder()
finder_real.feed(html_content)
print(f"{len(finder_real.images)} imagini gasite pe pagina reala.")


## ex 40
print("\n\nExercitiul 40")
def page_fingerprint(url: str) -> str:
    """Calculeaza amprenta SHA256 a continutului paginii."""
    return hashlib.sha256(fetch(url).content).hexdigest()

fp1 = page_fingerprint(BASE_URL)
fp2 = page_fingerprint(BASE_URL)

print("FP1:", fp1)
print("FP2:", fp2)
print("Sunt ambele fingerprinturi egale? ", fp1 == fp2)
# amprentele ar fi diferite daca continutul se modifica intre cererile efectuate (eg. banere, timestampuri, etc etc)


## ex 41
print("\n\nExercitiul 41")
response = fetch(BASE_URL)
with open("headers.json", "w", encoding="utf-8") as file:
    json.dump(dict(response.headers), file, indent=2)

with open("headers.json", "r", encoding="utf-8") as file:
    headers_loaded = json.load(file)

print("Content-Type extras din json:", headers_loaded.get("Content-Type"))


## ex 42
print("\n\nExercitiul 42")
def resolve(hostname: str) -> str:
    """Returneaza adresa IP a unui nume de gazda."""
    clean_host = urllib.parse.urlparse(hostname).netloc or hostname
    return socket.gethostbyname(clean_host)

print(f"IP pentru {BASE_URL}:", resolve(BASE_URL))


## ex 43
print("\n\nExercitiul 43")
def cert_days_left(hostname: str) -> int:
    """Calculeaza numarul de zile ramase pana la expirarea certificatului SSL."""
    clean_host = urllib.parse.urlparse(hostname).netloc or hostname
    context = ssl.create_default_context()

    with socket.create_connection((clean_host, 443), timeout=TIMEOUT) as sock:
        with context.wrap_socket(sock, server_hostname=clean_host) as ssock:
            cert = ssock.getpeercert()

    expiration = cert.get("notAfter")
    exp_seconds = ssl.cert_time_to_seconds(expiration)
    return int((exp_seconds - time.time()) / (24 * 60 * 60))

print(f"Zile ramase certificat SSL:", cert_days_left(BASE_URL))

