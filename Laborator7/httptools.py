import requests


BASE = "https://httpbin.org"
PATHS = ["/get", "/redirect/2", "/delay/1", "/status/404", "/delay/5"]
# Partea 1: parametri în URL
def search(params):
    """GET pe /get cu parametri în URL; returnează parametrii primiți de server."""
    r = requests.get(f"{BASE}/get", params=params, timeout=5)
    return r.json()["args"]

def search_url(params):
    """Returnează adresa completă construită de requests, cu tot cu parametri."""
    r = requests.get(f"{BASE}/get", params=params, timeout=5)
    return r.url

# Partea 2: anteturi
def fetch_with_agent(agent):
    """GET pe /headers cu User-Agent=agent; returnează User-Agent-ul văzut de server."""
    r = requests.get(f"{BASE}/headers", headers={"User-Agent": agent}, timeout=5)
    return r.json()["headers"]["User-Agent"]

def default_agent():
    """Returnează User-Agent-ul trimis de requests când nu setezi nimic."""
    r = requests.get(f"{BASE}/headers", timeout=5)
    return r.json()["headers"]["User-Agent"]

# Partea 3: trimiterea datelor
def post_json(data):
    """POST cu datele ca JSON pe /post; returnează JSON-ul primit de server."""
    r = requests.post(f"{BASE}/post", json=data, timeout=5)
    return r.json()["json"]

def post_form(data):
    """POST cu datele ca formular pe /post; returnează formularul primit de server."""
    r = requests.post(f"{BASE}/post", data=data, timeout=5)
    return r.json()["form"]

# Partea 4: coduri de stare
def describe_status(code):
    """GET pe /status/<code>; returnează 'succes', 'eroare client' sau 'eroare server'."""
    r = requests.get(f"{BASE}/status/{code}", timeout=5)

    if 200<= r.status_code <= 299:
        return "succes"
    if 400 <= r.status_code <= 499:
        return "eroare client"
    if 500 <= r.status_code <= 599:
        return "eroare server"
    return "altceva"

def is_ok(code):
    """GET pe /status/<code>; returnează True dacă cererea a reușit, altfel False."""
    r = requests.get(f"{BASE}/status/{code}", timeout=5)

    try:
        r.raise_for_status()
        return True

    except requests.HTTPError:
        return False


# Partea 5: redirecționări
def count_redirects(n):
    """GET pe /redirect/<n>; returnează câte redirecționări au fost urmate."""
    r = requests.get(f"{BASE}/redirect/{n}", timeout=5)

    return len(r.history)

def final_url(n):
    """GET pe /redirect/<n>; returnează adresa la care ai ajuns."""
    r = requests.get(f"{BASE}/redirect/{n}", timeout=5)
    return r.url

def first_hop(n):
    """GET pe /redirect/<n> FĂRĂ a urma redirecționarea; returnează antetul Location."""
    r = requests.get(f"{BASE}/redirect/{n}", allow_redirects=False, timeout=5)
    return r.headers.get("Location")

# Partea 6: sesiuni și cookie-uri
def cookie_demo(name, value):
    """Setează un cookie, apoi citește cookie-urile înapoi folosind O SINGURĂ sesiune."""
    s = requests.Session()
    s.get(f"{BASE}/cookies/set?{name}={value}", timeout=5)
    r = s.get(f"{BASE}/cookies")
    return r.json()["cookies"]

def no_session_demo(name, value):
    """Fă același lucru cu apeluri simple requests.get; returnează cookie- urile văzute de server."""
    requests.get(f"{BASE}/cookies/set?{name}={value}", timeout=5)
    r = requests.get(f"{BASE}/cookies", timeout=5)
    return r.json()["cookies"]


# Partea 7: raportul final
def report(path):
    """Returnează un dicționar care descrie pagina de la BASE + path."""

    try:
        r = requests.get(BASE + path, timeout=3)
        raspuns = {
            "status": r.status_code,
            "final_url": r.url,
            "redirects": len(r.history),
            "seconds": r.elapsed.total_seconds(),
            "content_type": r.headers.get("Content-Type"),
        }

    except requests.exceptions.RequestException as e:
        raspuns = {
            "status": None,
            "error": str(e)
        }

    return raspuns


# Bonus: autentificare
def check_login(user, password):
    """Returnează True dacă serverul acceptă datele de autentificare, altfel False."""
    r = requests.get(f"{BASE}/basic-auth/admin/secret", auth=(user, password))
    return r.status_code == 200