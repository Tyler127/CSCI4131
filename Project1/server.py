from http.server import BaseHTTPRequestHandler, HTTPServer
import os

def getFile(url):
    """
    The url parameter is a *PARTIAL* URL of type string that contains
    the path name and query string.
    If you enter the following URL in your browser's address bar:
    `http://localhost:4131/contact?name=joe`
    then the `url` parameter will have the value "/contact?name=joe"

    This function should return a string.
    """

    # current_dir = os.getcwd()
    # print("Current Working Directory:", current_dir)

    # script_dir = os.path.dirname(os.path.abspath(__file__))
    # print("This files's dir:", script_dir)

    # The following approach isn't a good approach. A better approach would be to find 
    # the index of ? and/or # and ignore everything after it, then just string-match.
    if url.startswith("/My"):
        return open("MySchedule.html").read()
    # Note, you will have to add an elif case for your AboutMe.html page - it should
    # be similar to the condition in the beginning of the if statement above.
    elif url.startswith("/Ab"):
        return open("AboutMe.html").read()
    # file not found, we provide this file!!!!
    else:
        return open("404.html").read()  
    

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Call the student-edited server code.
        message = getFile(self.path)

        # Convert the return value into a byte string for network transmission
        if type(message) == str:
            message = bytes(message, "utf8")

        # prepare the response object with minimal viable headers.
        self.protocol_version = "HTTP/1.1"
        # Send response code
        self.send_response(200)
        # Send headers
        # Note -- this would be binary length, not string length
        self.send_header("Content-Length", len(message))
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()

        # Send the file.
        self.wfile.write(message)
        return

def run():
    PORT = 4131
    print(f"Starting server http://localhost:{PORT}/")
    server = ('', PORT)
    httpd = HTTPServer(server, RequestHandler)
    httpd.serve_forever() 
run()
