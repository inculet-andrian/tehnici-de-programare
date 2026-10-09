# Laborator:  functii, metode si importuri pe web
# Student: Inculet Andrian
import json
import re
import socket
import ssl
import time
import urllib.parse
import requests

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

DEFAULT_HEADERS = {"User-Agent": "WebLab-Inculet Andrian"}

def fetch(url: str, timeout: int = TIMEOUT) -> requests.Response:
    time.sleep(1)
    return requests.get(url, timeout=timeout, headers=DEFAULT_HEADERS)

def get_status(url: str) -> int:
    return fetch(url).status_code

def get_title(html: str) -> str:
    start = html.find("<title>")
    if start == -1:
        return ""
    start += len("<title>")
    end = html.find("</title>", start)
    if end == -1:
        return ""
    return html[start:end].strip()


def security_headers(url: str) -> dict[str, bool]:
    """Verifica prezenta celor 5 antete de securitate esentiale."""
    headers = fetch(url).headers
    return {
        "Strict-Transport-Security": "Strict-Transport-Security" in headers,
        "Content-Security-Policy": "Content-Security-Policy" in headers,
        "X-Frame-Options": "X-Frame-Options" in headers,
        "X-Content-Type-Options": "X-Content-Type-Options" in headers,
        "Referrer-Policy": "Referrer-Policy" in headers
    }

def check_paths(base: str, paths: list[str]) -> dict[str, int]:
    """Verifica statusul unei liste de cai relative."""
    return {path: get_status(urllib.parse.urljoin(base, path)) for path in paths}

def extract_links(html: str) -> set[str]:
    """Extrage toate valorile din atributul href."""
    return set(re.findall(r'href="([^"]+)"', html))

def resolve(hostname: str) -> str:
    """Afla adresa IP pentru domeniul dat."""
    clean_host = urllib.parse.urlparse(hostname).netloc or hostname
    return socket.gethostbyname(clean_host)

def split_links(links: set[str], base_url: str) -> tuple[list[str], list[str]]:
    """Imparte legaturile in interne si externe."""
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

def cert_days_left(hostname: str) -> int:
    """Calculeaza zilele ramase pana la expirarea certificatului SSL."""
    clean_host = urllib.parse.urlparse(hostname).netloc or hostname
    context = ssl.create_default_context()

    with socket.create_connection((clean_host, 443), timeout=TIMEOUT) as sock:
        with context.wrap_socket(sock, server_hostname=clean_host) as ssock:
            cert = ssock.getpeercert()

    expiration = cert.get("notAfter")
    exp_seconds = ssl.cert_time_to_seconds(expiration)
    return int((exp_seconds - time.time()) / (24 * 60 * 60))

def score_headers(results: dict[str, bool]) -> str:
    """Returneaza scorul antetelor (ex: 3/5)."""
    score = sum(1 for v in results.values() if v)
    return f"{score}/{len(results)}"

def page_exists(url: str) -> bool:
    """Verifica daca o pagina este accesibila (200 OK)."""
    try:
        return get_status(url) == 200
    except requests.RequestException:
        return False

def fetch_robots(base: str) -> str | None:
    """Aduce continutul robots.txt."""
    robots_url = urllib.parse.urljoin(base, "/robots.txt")
    if page_exists(robots_url):
        return fetch(robots_url).text
    return None

def disallowed_paths(robots_text: str | None) -> list[str]:
    """Extrage caile marcate cu Disallow."""
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

def site_report(url: str) -> dict[str, object]:
    """Genereaza raportul complet al site-ului si il salveaza in report.json."""
    rsp = fetch(url)
    status = rsp.status_code
    titlu = get_title(rsp.text)
    ip = resolve(url)

    redirects = []
    http_url = url.replace("https://", "http://")
    try:
        rsp_redir = fetch(http_url)
        for r in rsp_redir.history:
            redirects.append(f"{r.status_code} -> {r.url}")
    except Exception:
        pass

    scor_sec = score_headers(security_headers(url))
    zile_cert = cert_days_left(url)

    links = extract_links(rsp.text)
    legaturi_int, legaturi_ext = split_links(links, url)

    robots = fetch_robots(url)
    cai_interzise = disallowed_paths(robots)

    rezultat = {
        "Cod de stare:    ": status,
        "Titlu:           ": titlu,
        "IP:              ": ip,
        "Redirectionari:  ": redirects,
        "Scor securitate: ": scor_sec,
        "Certificat:      ": f"{zile_cert} zile",
        "Legaturi:        ": f"{len(legaturi_int)} interne, {len(legaturi_ext)} externe",
        "Cai interzise    ": cai_interzise,
    }

    print(f"=== Raport site: {url} ===")
    for k, v in rezultat.items():
        print(f"{k}: {v}")

    with open("report.json", "w", encoding="utf-8") as file:
        json.dump(rezultat, file, indent=2, ensure_ascii=False)

    print("Salvat in report.json")
    return rezultat

## ex 46
if __name__ == "__main__":
    print("Autotest:", get_status("https://cybercor.org"))