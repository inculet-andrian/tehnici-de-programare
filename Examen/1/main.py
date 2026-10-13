from checker import build_url, is_https, show_response, check_site, scan_sites, check_headers, retry_check
# Partea 1: apeluri pentru build_url și is_https
print("\n\nPartea 1: ")
print("is_https: ", is_https("http://example.com"))
print("is_https: ", is_https("https://example.com"))

print("build_url: ", build_url("httpbin.org", "html"))

# Partea 2: apeluri pentru show_response
print("\n\nPartea 2: ")
show_response("https://example.com")
show_response("https://httpbin.org/status/404")

# Partea 3: apeluri pentru check_site
print("\n\nPartea 3: ")
print(check_site("https://example.com"))
print(check_site("http://this-site-does-not-exist.invalid"))


# Partea 4: apelul scan_sites()
print("\n\nPartea 4: ")
scan_sites()


# Partea 5: apeluri pentru check_headers
print("Headers: ", check_headers("https://example.com"))
print("Headers: ", check_headers("http://this-site-does-not-exist.invalid"))
# Partea 6: apeluri pentru retry_check

print("\n\nPartea 6:")
print("Retry attempts: ", retry_check("https://example.com"))
print("Retry attempts: ", retry_check("http://this-site-does-not-exist.invalid")) # nu merge :((