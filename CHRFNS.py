import json, requests, urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
                path = urllib.parse.urlparse(self.path).path
                path = path.lstrip("/").replace("%2F", "/").replace("%3A", ":")

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
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
