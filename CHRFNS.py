import json, requests, urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

page_cache = {}

class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
                global page_cache
                path = urllib.parse.urlparse(self.path).path
                path = path.replace("%2F", "/").replace("%3A", ":")

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                if path in page_cache.keys():
                    self.wfile.write(bytes(page_cache[path], "utf-8"))
                else:
                    r = requests.get(path).text.replace(
                        "\n", "\\n").replace(
                        "\r", "\\r").replace(
                        "\t", "\\t").strip()
                    self.wfile.write(bytes(json.dumps({"result": r}), "utf-8"))
                    page_cache[path] = json.dumps({"result": r})

def main() -> None:
    print("CHRFNS - ChickenSuite HTML Requests From Native Scratch")
    print("Hosting Scratch-Python request server at localhost:6942")
    print("Requestly rule is ready. Press Ctrl+C to stop hosting")
    
    httpserver = HTTPServer(("localhost", 6942), Handler)

    try:
        httpserver.serve_forever()
    except KeyboardInterrupt:
        httpserver.server_close()

    del httpserver

if __name__ == "__main__":
    main()
