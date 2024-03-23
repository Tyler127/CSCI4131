from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote_plus

all_responses = ""

def get_body_params(body):
    if not body:
        return {}
    parameters = body.split("&")

    # split each parameter into a (key, value) pair, and escape both
    def split_parameter(parameter):
        k, v = parameter.split("=", 1)
        k_escaped = unquote_plus(k)
        v_escaped = unquote_plus(v)
        return k_escaped, v_escaped

    body_dict = dict(map(split_parameter, parameters))
    print(f"Parsed parameters as: {body_dict}")
    # return a dictionary of the parameters
    return body_dict


def submission_to_table(item):
    """TODO: Takes a dictionary of form parameters and returns an HTML table row
    An example input dictionary might look like: 
    {
     'event': 'Sleep',
     'day': 'Sun',
     'start': '01:00',
     'end': '11:00', 
     'phone': '1234567890', 
     'location': 'Home',
     'extra': 'Have a nice dream', 
     'url': 'https://example.com'
    }
    """
    global all_responses

    # If there is nothing in the dict, return all previous responses
    if len(item) == 0:
        return all_responses

    # Add the new response to all responses
    all_responses += "<tr>"
    all_responses += "<td>" + item.get("event") + "</td>"
    all_responses += "<td>" + item.get("day") + "</td>"
    all_responses += "<td>" + item.get("start_time") + "</td>"
    all_responses += "<td>" + item.get("end_time") + "</td>"
    all_responses += "<td>" + item.get("phone") + "</td>"
    all_responses += "<td>" + item.get("location") + "</td>"
    all_responses += "<td>" + item.get("extra_info") + "</td>"
    all_responses += "<td><a href=\"" + item.get("url") + '\">' + item.get("url") + "</a></td>"
    all_responses += "</tr>"

    return all_responses


# NOTE: Please read the updated function carefully, as it has changed from the
# version in the previous homework. It has important information in comments
# which will help you complete this assignment.
def handle_req(url, body=None):
    """
    The url parameter is a *PARTIAL* URL of type string that contains the path
    name and query string.

    If you enter the following URL in your browser's address bar:
    `http://localhost:4131/MyForm.html?name=joe` then the `url` parameter will have
    the value "/MyForm.html?name=joe"

    This function should return two strings in a list or tuple. The first is the
    content to return, and the second is the content-type.
    """
    # NOTE: These files may be different for your server, but we include them to
    # show you examples of how yours may look. You may need to change the paths
    # to match the files you want to serve. Before you do that, make sure you
    # understand what the code is doing, specifically with the MIME types and
    # opening some files in binary mode, i.e. `open(..., "br")`.

    # Get rid of any query string parameters
    url, *_ = url.split("?", 1)
    filename, filetype = url.split(".", 1)
    print(url)
    print(filename)
    print(filetype)

    # Parse any form parameters submitted via POST
    parameters = get_body_params(body)

    # Will not attempt to load a static page for URLs in this list
    dynamic_pages = ["/EventLog.html"]

    # Finds the static resource based on the file type
    if filetype == "html" and url not in dynamic_pages:
        return open("static/html" + url).read(), "text/html"
    
    elif filetype == "css":
        return open("static/" + url).read(), "text/css"
    
    elif filetype == "js":
        return open("static/" + url).read(), "text/javascript"
    
    elif filetype == "png":
        return open("static" + url, "br").read(), "image/png"
    
    elif filetype == "jpg":
        return open("static" + url, "br").read(), "image/jpeg"


    # if url == "/MySchedule.html":
    #     return open("static/html/MySchedule.html").read(), "text/html"
    # if url == "/MyForm.html":
    #     return open("static/html/MyForm.html").read(), "text/html"
    # elif url == "/AboutMe.html":
    #     return open("static/html/AboutMe.html").read(), "text/html"
    # elif url == "/css/styles.css":
    #     return open("static/css/styles.css").read(), "text/css"
    # elif url == "/css/MySchedule.css":
    #     return open("static/css/MySchedule.css").read(), "text/css"
    # elif url == "/css/AboutMe.css":
    #     return open("static/css/AboutMe.css").read(), "text/css"
    # elif url == "/css/MyForm.css":
    #     return open("static/css/MyForm.css").read(), "text/css"
    # elif url == "/js/MySchedule.js":
    #     return open("static/js/MySchedule.js").read(), "text/javascript"
    # elif url == "/js/AboutMe.js":
    #     return open("static/js/AboutMe.js").read(), "text/javascript"
    # elif url == "/img/anderson.jpg":
    #     return open("static/img/anderson.jpg", "br").read(), "image/png"
    # elif url == "/img/gophers-mascot.png":
    #     return open("static/img/gophers-mascot.png", "br").read(), "image/png"
    # elif url == "/img/rec.jpg":
    #     return open("static/img/rec.jpg", "br").read(), "image/png"
    # elif url == "/img/Tate.png":
    #     return open("static/img/Tate.png", "br").read(), "image/png"
    # elif url == "/img/walter.jpg":
    #     return open("static/img/walter.jpg", "br").read(), "image/jpeg"
    # elif url == "/img/zoom.jpg":
    #     return open("static/img/zoom.jpg", "br").read(), "image/jpeg"
  
    # TODO: Add update the HTML below to match your other pages and
    # implement the `submission_to_table`.
    elif url == "/EventLog.html":
        return (
            """
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <title>Form Submissions</title>
                <link rel="stylesheet"  type="text/css" href="/css/styles.css">
            </head>
            <body>
                <div class="nav">
                    <h2 class="nav"><a class="nav" href="/MySchedule.html">My Schedule</a></h2>
                    <h2 class="nav"><a class="nav" href="/AboutMe.html">About Me</a></h2>
                    <h2 class="nav"><a class="nav" href="/MyForm.html">Form</a></h2>
                    <h2 class="nav"><a class="nav active" href="/EventLog.html">Form Responses</a></h2>
                </div>

                <div class="header centered margin-spacing-top-bottom">
                    <h1>Form Responses</h1>
                </div>

                <div class="content">
                    <div class="table-container">
                        <table>
                            <thead>
                                <tr>
                                    <th>Event</th>
                                    <th>Day</th>
                                    <th>Start</th>
                                    <th>End</th>
                                    <th>Phone</th>
                                    <th>Location</th>
                                    <th>Extra Info</th>
                                    <th>URL</th>
                                </tr>
                            </thead>
                            <tbody>
                            """
                + submission_to_table(parameters)
                + """
                            </tbody>
                        </table>
                    </div>
                </div>
            </body>
            </html>""",
            "text/html; charset=utf-8",
        )
    else:
        return open("static/html/404.html").read(), "text/html; charset=utf-8"


# You shouldn't change content below this. It would be best if you just left it alone.


class RequestHandler(BaseHTTPRequestHandler):
    def __c_read_body(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        body = str(body, encoding="utf-8")
        return body

    def __c_send_response(self, message, response_code, headers):
        # Convert the return value into a byte string for network transmission
        if type(message) == str:
            message = bytes(message, "utf8")

        # Send the first line of response.
        self.protocol_version = "HTTP/1.1"
        self.send_response(response_code)

        # Send headers (plus a few we'll handle for you)
        for key, value in headers.items():
            self.send_header(key, value)
        self.send_header("Content-Length", len(message))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()

        # Send the file.
        self.wfile.write(message)

    def do_GET(self):
        # Call the student-edited server code.
        message, content_type = handle_req(self.path)

        # Convert the return value into a byte string for network transmission
        if type(message) == str:
            message = bytes(message, "utf8")

        self.__c_send_response(
            message,
            200,
            {
                "Content-Type": content_type,
                "Content-Length": len(message),
                "X-Content-Type-Options": "nosniff",
            },
        )

    def do_POST(self):
        body = self.__c_read_body()
        message, content_type = handle_req(self.path, body)

        # Convert the return value into a byte string for network transmission
        if type(message) == str:
            message = bytes(message, "utf8")

        self.__c_send_response(
            message,
            200,
            {
                "Content-Type": content_type,
                "Content-Length": len(message),
                "X-Content-Type-Options": "nosniff",
            },
        )


def run():
    PORT = 4131
    print(f"Starting server http://localhost:{PORT}/")
    server = ("", PORT)
    httpd = HTTPServer(server, RequestHandler)
    httpd.serve_forever()


run()
