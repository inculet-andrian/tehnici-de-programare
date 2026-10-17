from httptools import *

def main():
    print(search({"q": "python", "page": "2"}))
    print(search({"q": "hello world & co"}))
    print(search_url({"q": "python", "page":"2"}))
    print(fetch_with_agent("MyBot/1.0"))
    print(default_agent())
    print(post_json({"name": "Ana", "age": 19,"tags": ["a", "b"]}))
    print(post_form({"user": "ana", "city":"Bălți"}))
    print(describe_status(200))
    print(describe_status(404))
    print(describe_status(503))
    print(is_ok(204))
    print(is_ok(500))
    print(count_redirects(3))
    print(final_url(2))
    print(first_hop(3))
    print(cookie_demo("theme", "dark"))
    print(no_session_demo("theme", "dark"))
    print(report("/get"))
    print(report("/redirect/2"))
    print(report("/delay/1"))
    print(report("/delay/5"))
    print(check_login("admin", "secret"))
    print(check_login("admin", "gresit"))

    rezultate = []
    succes = 0
    esec = 0

    for path in PATHS:
        res = report(path)
        res["path"] = path
        rezultate.append(res)

        if res.get("status") == 200:
            succes += 1
        else:
            esec += 1

    pagini_succ = [rez for rez in rezultate if rez.get("status") == 200]
    pagini_succ = sorted(pagini_succ, key=lambda x: x["seconds"], reverse=True)

    for pagina in pagini_succ:
        print(f"{pagina['path']} -> {pagina['status']}, {pagina['seconds']:.2f} secunde")

    print(f"Reusite {succes} | Esuate {esec}")




if __name__ == "__main__":
    main()
