# python3 code training server

import http.server as Hs



class Handler(Hs.BaseHTTPRequestHandler):
    """Handler class for http server. The plumbing for handling http requests and such
    are all in here, mostly in the do_GET and do_POST methods"""

    def do_GET(self):
        print("Requested path '{p}' from '{c}'".format(p=self.path, c=self.client_address))

        mpPathFn = {
                'login' : self.OnLogin,
                'menu' : self.OnMenu,
                'task' : self.OnTask,
                'hint' : self.OnHint,
            }

        # Tasks (which I think map to URLs in some way):
        # - Request login (maybe?)
        # - Login
        # - View problem list (include progress?)
        # - View specific problem
        # - Post answer to specific problem (only if not already solved?)
        # - View hint chain on a specific problem

        # Dispatch the request to the appropriate function

        lPart = self.path.split('/')
        assert lPart[0] == ''
        target = lPart[1]
        args = lPart[2:]

        fn = mpPathFn.get(target, self.OnError)
        assert fn is not None
        fn(args)

        # indicate that things worked (should only do this for URLs that make sense, though)

        self.send_response(200)
        self.end_headers()

        # NOTE: wfile wants to be written with bytes, which makes sense, so we have to either directly use bytes
        #  objects (as I do in some cases), or conver strings to bytes using an appropriate encoding. I'm not
        #  yet clear on whether I should be using ascii or utf-8 for my encodings; more research will be needed
        #  to really understand the distinction between these cases.

        self.wfile.write(b'<html>\n')
        self.wfile.write(b'<head>\n')
        self.wfile.write(b'<title>Basic Title</title>\n')
        self.wfile.write(b'</head>\n')
        self.wfile.write(b'<body>\n')
        self.wfile.write(b'<p>There is nothing to see here yet</p>\n')
        self.wfile.write(bytes('<p>Well, except that you asked for <pre>{p}</pre> from <pre>{c}</pre></p>\n'.format(p=self.path, c=self.client_address), 'ascii'))
        self.wfile.write(b'<p>Here are some things you can try to do:</p>\n')
        self.wfile.write(b'<ul>\n')
        for link in mpPathFn.keys():
            self.wfile.write(bytes('<li><a href="/{l}/{l}">{l}</a></li>\n'.format(l=link), 'utf-8'))
        self.wfile.write(b'</ul>\n')
        self.wfile.write(b'</body>\n')
        self.wfile.write(b'</html>\n')

    def do_HEAD(self):
        print("Requested head '{p}' from '{c}'".format(p=self.path, c=self.client_address))

        self.send_error(404, 'We do not handle this yet')

    def do_POST(self):
        print("Requested post '{p}' from '{c}'".format(p=self.path, c=self.client_address))

        self.send_error(404, 'We do not handle this yet')

    def OnLogin(self, lPart):
        print("Got login request with {a}".format(a=lPart))

        # TODO

    def OnMenu(self, lPart):
        print("Got menu request with {a}".format(a=lPart))

        # TODO

    def OnTask(self, lPart):
        print("Got task request with {a}".format(a=lPart))

        # TODO

    def OnHint(self, lPart):
        print("Got hint request with {a}".format(a=lPart))

        # TODO

    def OnError(self, lPart):
        print("Got error request with {a}".format(a=lPart))

        # TODO

if __name__ == '__main__':

    # Generate a server using our handler on port 8000 which then serves forever

    # NOTE: I'm using a threading version here, although it's not overly clear that
    #  I actually need to do so for the low level of traffic I'm actually expecting

    server = Hs.ThreadingHTTPServer(('', 8000), Handler)
    server.serve_forever()
