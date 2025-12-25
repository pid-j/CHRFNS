import json, requests
import urllib.parse as urlp
from http.server import BaseHTTPRequestHandler, HTTPServer

EXCEPTIONS = {
    "chrfns://ping": "Pong. Hello from Syria!",
    "chrfns://ver": "CHRFNS Server v1.1",
    "chrfns://credits": "Created by @0x1194 on scratch.mit.edu",
}

class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
                path = urlp.urlparse(self.path).path
                path = urlp.unquote(path.lstrip("/"))

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()

                for e in EXCEPTIONS.keys():
                    if path.startswith(e):
                        f = EXCEPTIONS[e]
                        if callable(f): f = f(path)
                        r = f.replace(
                            "\n", "\\n").replace(
                            "\r", "\\r").replace(
                            "\t", "\\t").strip()
                        self.wfile.write(bytes(json.dumps({"result": r}), "utf-8"))
                        return
                r = requests.get(path).text.replace(
                    "\n", "\\n").replace(
                    "\r", "\\r").replace(
                    "\t", "\\t").strip()
                self.wfile.write(bytes(json.dumps({"result": r}), "utf-8"))

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
