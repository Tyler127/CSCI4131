from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from stat import S_IROTH
from urllib.parse import unquote_plus
import datetime

all_responses = ""

last_filename = ""
log_file = open("response.txt", "w")
def create_log_entry(message, response_code, headers):
    time = datetime.datetime.now()
    print("LOGGING")
    global last_filename
    log_file.write(f"{time}: STATUS: {response_code}, HEADERS: {headers}, {last_filename}\n")
    log_file.flush()


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
    #print(f"Full URL: {url}")

    filename = url.split("/")[-1]
    global last_filename 
    last_filename = filename
    print(f"File: {filename}")

    filetype = url.split(".")[-1]
    print(f"Filetype: {filetype}")

    is_br_type = {
        "html": False,
        "css": False,
        "js": False,
        "png": True,
        "jpg": True,
        "jpeg": True,
        "mp3": True,
        "txt": False
    }

    type_mime_strings = {
        "html": "text/html",
        "css": "text/css",
        "js": "text/javascript",
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "mp3": "audio/mpeg",
        "txt": "text/plain"
    }

    file_directory = {
        "html": "html",
        "css": "css",
        "js": "js",
        "png": "img",
        "jpg": "img",
        "jpeg": "img",
        "mp3": "audio",
        "txt": ""
    }

    # Parse any form parameters submitted via POST
    parameters = get_body_params(body)

    # Attempt to open the file and if there is an error return the 404 page
    try:
        file_path = "static/" + file_directory[filetype] + "/" + filename

        # If others do not have read permissions return the 403 page
        # Found this from Python documentation: https://docs.python.org/3/library/stat.html
        # Additional help from https://tutorialspoint.com/How-to-check-the-permissions-of-a-file-using-Python
        if not (file_directory[filetype] == "img"):
            if not bool(os.stat(file_path).st_mode & S_IROTH):
                return open("static/html/403.html").read(), "text/html; charset=utf-8"  

        if filename == "EventLog.html":
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
                        <h2 class="nav"><a class="nav" href="/stockQuotes.html">Stock Quotes</a></h2>
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
                "text/html; charset=utf-8",)
    
        elif is_br_type[filetype]:
            return open(file_path, "br").read(), type_mime_strings[filetype]

        elif not is_br_type[filetype]:
            return open(file_path).read(), type_mime_strings[filetype]

    except FileNotFoundError:
        return open("static/html/404.html").read(), "text/html; charset=utf-8"


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

        # Create a log entry
        create_log_entry(message, response_code, headers)


    def do_GET(self):
        global last_filename

        if self.path.startswith("/calculator"):
            # Find the params by first splitting on ? then on the second half
            # of the path which is the params which then need to be split on &
            # Then loop over the params in that list and split them into a dictionary
            # with the key on the left of the = and the value on the right
            params = {param.split('=')[0]: param.split('=')[1] for param in self.path.split("?")[1].split("&")}

            last_filename = "Calculator"

            value = 0
            if params["operator"] == "%2B":
                value = int(params["num1"]) + int(params["num2"])
            elif params["operator"] == "-":
                value = int(params["num1"]) - int(params["num2"])
            elif params["operator"] == "*":
                value = int(params["num1"]) * int(params["num2"])
            elif params["operator"] == "%2F":
                value = int(params["num1"]) / int(params["num2"])

            message = f"<!DOCTYPE><html><head><title>Response</title></head><body><h2>{value}</h2></body></html>"
            self.__c_send_response(
                    message,
                    200,
                    {
                        "Content-Type": "text/html",
                        "Content-Length": len(message),
                        "X-Content-Type-Options": "nosniff",
                    },
                )

        # Create a redirect response for YouTube or Google
        elif self.path.startswith("/redirect"):
            params = {param.split('=')[0]: param.split('=')[1] for param in self.path.split("?")[1].split("&")}
            print(params)

            last_filename = "Redirect"

            if params["search_source"] == "youtube":
                self.__c_send_response(
                    "",
                    307,
                    {
                        "Location": f"https://www.youtube.com/results?search_query={params['search_term']}",
                    },
                )

            elif params["search_source"] == "google":
                self.__c_send_response(
                    "",
                    307,
                    {
                        "Location": f"https://www.google.com/search?q={params['search_term']}",
                    },
                )

        # Else do a normal response by finding the file
        else:
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
