from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.request
import json
import urllib.parse

class ProxyHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/api/proxy'):
            # Parse query parameters
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)

            if 'url' in params:
                target_url = params['url'][0]

                # Prevent SSRF: only allow requests to our specific API provider
                parsed_url = urllib.parse.urlparse(target_url)
                if parsed_url.netloc != 'cj.lziapi.com':
                    self.send_response(403)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(b'{"error": "Forbidden: Invalid domain"}')
                    return

                # Reconstruct any additional query parameters passed to the proxy
                additional_params = {k: v[0] for k, v in params.items() if k != 'url'}
                if additional_params:
                    # Parse the original target URL
                    url_parts = list(urllib.parse.urlparse(target_url))
                    # Parse its existing query string
                    target_query = dict(urllib.parse.parse_qsl(url_parts[4]))
                    # Update with additional parameters
                    target_query.update(additional_params)
                    # Rebuild the query string and the target URL
                    url_parts[4] = urllib.parse.urlencode(target_query)
                    target_url = urllib.parse.urlunparse(url_parts)

                try:
                    req = urllib.request.Request(target_url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req) as response:
                        self.send_response(200)
                        self.send_header('Content-Type', 'application/json')
                        self.send_header('Access-Control-Allow-Origin', '*')
                        self.end_headers()
                        self.wfile.write(response.read())
                except Exception as e:
                    self.send_response(500)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    error_msg = json.dumps({'error': str(e)})
                    self.wfile.write(error_msg.encode('utf-8'))
            else:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(b'{"error": "Missing url parameter"}')
        else:
            super().do_GET()

if __name__ == '__main__':
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, ProxyHTTPRequestHandler)
    print("Serving at port 8080")
    httpd.serve_forever()
