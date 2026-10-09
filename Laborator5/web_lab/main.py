# Laborator:  functii, metode si importuri pe web
# Student: Inculet Andrian
import argparse
import csv
import datetime

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

## ex 44
print("\n\nExercitiul 44")
import webtools
print("Titlu din webtools:", webtools.get_title(webtools.fetch(BASE_URL).text))


## ex 45
print("\n\nExercitiul 45")
from webtools import get_title, security_headers, fetch, check_paths, site_report, DEFAULT_HEADERS

print("Titlu (import direct):", get_title(fetch(BASE_URL).text))
print("Antete securitate:", security_headers(BASE_URL))

# Explicatie: Daca main.py ar defini propria functie numita `get_title`, aceasta ar suprascrie (shadowing)
# functia `get_title` importata anterior din webtools.


## ex 46
print("\n\nExercitiul 46")
# Blocul `if __name__ == "__main__":` din webtools.py previne executarea autotestului la importare.
# Cand rulam `python main.py`, `__name__` in webtools este `"webtools"`, nu `"__main__"`.


## ex 47
print("\n\nExercitiul 47")
print("DEFAULT_HEADERS:", DEFAULT_HEADERS)


## ex 48
print("\n\nExercitiul 48")
parser = argparse.ArgumentParser(description="Script de analiza web")
parser.add_argument("url", nargs="?", default=BASE_URL, help="URL-ul de analizat")

args = parser.parse_args()
target_url = args.url

response = fetch(target_url)
print("Status pentru URL primit:", response.status_code)


## ex 49
print("\n\nExercitiul 49")
paths_to_check = ["/", "/robots.txt", "/sitemap.xml"]
results_dict = check_paths(target_url, paths_to_check)

with open("report.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["path", "status", "checked_at"]
    )
    writer.writeheader()
    for path, status in results_dict.items():
        writer.writerow({
            "path": path,
            "status": status,
            "checked_at": datetime.datetime.now().isoformat()
        })

print("Raportul a fost salvat in report.csv")


## ex 50
print("\n\nExercitiul 50")
site_report(target_url)