import time

import requests

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]

def build_url(host, path):
    """Returnează o adresă completă, de exemplu https://example.com/login."""
    return f"https://{host}/{path}"

def is_https(url):
    """Returnează True dacă adresa începe cu https://, altfel False."""
    return url.startswith("https://")

def show_response(url):
    """Trimite un GET la url și afișează statusul și Content-Type."""
    r = requests.get(url)

    print(f"Status: {r.status_code}")
    print(f"Content_type: {r.headers['content-type']}")


def check_site(url):
    """Returnează un dicționar cu: status, content_type, length, server."""

    try:
        time.sleep(5)
        r = requests.get(url, timeout=5)

        r.raise_for_status()
    except Exception as e:
        rezultat = {
            "status": None,
            "error": "Site-ul nu poate fi accesat"
        }
        return rezultat

    rezultat = {
        "status": r.status_code,
        "content_type": r.headers["content-type"],
        "length": len(r.text),
        "server": r.headers.get("server", "unknown"),
    }

    return rezultat


def scan_sites():
    """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""

    rezultat = []

    for site in SITES:
        if check_site(site).get("status") == 200 :
            rezultat.append(site)

    rezultat.sort()


    for site in rezultat:
        if check_site(site) in rezultat:
            print(f"{site}\t -> {check_site(site).get('status')}, {check_site(site).get('length')}")

    print(f"Reusite: {len(rezultat)} | Esuate: {len(SITES)-len(rezultat)}")
    pass


def check_headers(url):
    """Returnează un dicționar cu: present, missing, score."""

    present = []
    missing = []

    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()

        site_headers = r.headers

        for header in SECURITY_HEADERS:
            if header in site_headers:
                present.append(header)
            else:
                missing.append(header)

        rezultat = {
            "present": present,
            "missing": missing,
            "score": int((len(present) / len(SECURITY_HEADERS)) * 100)
        }

        return rezultat

    except:
        return {"status": None, "error": "Nu s-a putut incarca site-ul"}


def retry_check(url, attempts=3):
    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""

    rezultat = {}
    curr_attempt = 0

    while (curr_attempt <= attempts):
        try:
            curr_attempt += 1
            r = requests.get(url, timeout=5)


            if r.status_code < 500:
                return {
                    "status": r.status_code,
                    "attempts": curr_attempt
                }
            r.raise_for_status()

        except requests.exceptions.HTTPError as e:
            rezultat = {
                    # "status": e.response.status_code,
                    "attempts": curr_attempt
            }


    return rezultat







