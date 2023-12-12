from url import URL



url = URL("https://exmaple.com")

url.print_state()

body = url.request()
print("status_code:",url.status_code)
print("http_version:",url.http_version)
print("body:")
print(body)

