import json, requests
import urllib.parse as urlp
from http.server import BaseHTTPRequestHandler, HTTPServer

def nsac_get(path: str) -> str:
    path = path.removeprefix("nsac://").removesuffix("/")

    if len(path.split("/")) <= 2: path += "/"
    if path.endswith("/"): path += "index.html"
    
    r = requests.get(
        "https://raw.githubusercontent.com/pid-j/NSAC/refs/heads/main/web/%s" % path
    ).text
    if r is not None: return str(r)
    return ""

EXCEPTIONS = {
    # Informational Exceptions
    "chrfns://ping/": "Pong. 0x1194 says hello from Syria!",
    "chrfns://ver/": "CHRFNS Server v1.0-alpha",
    "chrfns://credits/": "Created by @0x1194 on scratch.mit.edu",
    "chrfns://help/": "Hey there! If you're seeing this, that means "\
        "the setup succeeded. So.. welcome to this page, I guess! "\
        "This is still work in progress, so... I guess... "\
        "Try typing chrfns://ver/ to see the version of this server. "\
        "Well, it's been fun talking to you. Adios! -0x1194",
    # NSAC Integration (https://github.com/pid-j/NSAC)
    "nsac://": nsac_get
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
                    if (path + "/").startswith(e):
                        f = EXCEPTIONS[e]
                        if callable(f): f = f(path)
                        r = f.replace(
                            "\n", "\\n").replace(
                            "\r", "\\r").replace(
                            "\t", "\\t").replace(
                            "\x1b", "\\e").strip()
                        self.wfile.write(bytes(json.dumps({"result": r}), "utf-8"))
                        return
                r = requests.get(path).text.replace(
                    "\n", "\\n").replace(
                    "\r", "\\r").replace(
                    "\t", "\\t").replace(
                    "\x1b", "\\e").strip()
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
