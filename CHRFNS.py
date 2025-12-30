#!/usr/bin/env python3
import json, requests
import urllib.parse as urlp
from http.server import BaseHTTPRequestHandler, HTTPServer
from html.parser import HTMLParser
from html.entities import name2codepoint

class LeParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parsed = []

    def handle_starttag(self, tag, attrs):
        self.parsed.append({"type": "starttag", "value": tag,
                            "attr": attrs})

    def handle_endtag(self, tag):
        self.parsed.append({"type": "endtag", "value": tag})

    def handle_data(self, data):
        self.parsed.append({"type": "data", "value": data})

    def handle_comment(self, data):
        self.parsed.append({"type": "comment", "value": data})

    def handle_entityref(self, name):
        c = chr(name2codepoint[name])
        self.parsed.append({"type": "namedentity", "value": c})

    def handle_charref(self, name):
        if name.startswith('x'):
            c = chr(int(name[1:], 16))
        else:
            c = chr(int(name))
        self.parsed.append({"type": "numentity", "value": c})

    def handle_decl(self, data):
        self.parsed.append({"type": "decl", "value": data})

def nsac_get(path: str) -> str:
    path = path.removeprefix("nsac://").removesuffix("/")

    if len(path.split("/")) <= 2: path += "/"
    if path.endswith("/"): path += "index.html"
    
    r = requests.get(
        "https://raw.githubusercontent.com/pid-j/NSAC/refs/heads/main/web/%s" % path
    ).text
    if r is not None: return str(r)
    return ""

def parse_html(path: str) -> str:
    text = path.removeprefix("chrfns://parse/").removesuffix("/")

    parser = LeParser()
    parser.feed(text)
    parser.close()

    if type(parser.parsed) is list:
        parsed = json.dumps(parser.parsed)
        return parsed
    return ""

EXCEPTIONS = {
    # Informational Exceptions
    "chrfns://ping/": "Pong. 0x1194 says hello from Syria!",
    "chrfns://ver/": "CHRFNS Server v1.0-beta",
    "chrfns://credits/": "Created by @0x1194 on scratch.mit.edu",
    "chrfns://help/": "Hey there! If you're seeing this, that means "\
        "the setup succeeded. So.. welcome to this page, I guess! "\
        "This is still work in progress, so... I guess... "\
        "Try typing chrfns://ver/ to see the version of this server. "\
        "Well, it's been fun talking to you. Adios! -0x1194",
    # HTML Parser
    "chrfns://parse/": parse_html,
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
