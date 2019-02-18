# python3 code training server

import http.server as Hs
import xml.etree.ElementTree as ET

# various pages

s_strLogin = """
<html>
<head>
	<title>Login Required</title>
</head>
<body>
	<p>Welcome to the challenge server. You need to log in to continue.</p>
	<p>TODO: here is a username field</p>
	<p>TODO: here is a password field</p>
	<p>TODO: here is a submit button</p>
</body>
</html>
"""

s_strLoginFailed = """
<html>
<head>
	<title>Bad Login</title>
</head>
<body>
	<p>The username or password you provided were not correct.</p>
	<p>You may:</p>
	<ul>
		<li>Try to <a href="/login">login</a> again.</li>
		<li>Return to the <a href="/">main page</a>.</li>
	</ul>
</body>
</html>
"""

s_strUserPage = """
"""

def UserPage(session):
	"""Return the page content formatted with the session for the user's page"""

	# TODO: format with session
	# TODO: show information with current links (solved, next)

	return s_strUserPage.format()



class Handler(Hs.BaseHTTPRequestHandler):
	"""Handler class for http server. The plumbing for handling http requests and such
	are all in here, mostly in the do_GET and do_POST methods"""

	def do_GET(self):
		print("Requested path '{p}' from '{c}'".format(p=self.path, c=self.client_address))

		mpPathFn = {
				'' : self.OnHome,
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

		fn = mpPathFn.get(target, None)
		assert fn is not None
		if fn(args):
			return

		# indicate that things worked (should only do this for URLs that make sense, though)

		# TODO: switch to showing that there was a problem here, once we have real handlers running

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
		self.wfile.write(bytes('<p>Well, except that you asked for <pre>{p}</pre> from <pre>{c}</pre></p>\n'.format(
								p=self.path, c=self.client_address), 'ascii'))
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

	def TreeBasic(self):
		html = ET.Element('html')
		html.append(ET.Element('head'))
		html[-1].append(ET.Element('title'))
		html.append(ET.Element('body'))

		return ET.ElementTree(html)

	def OnHome(self, lPart):
		print("Got home request with {a}".format(a=lPart))

		# this method isn't really any better than just raw writing stuff. :/

		tree = self.TreeBasic()
		tree.find('head/title').text = 'Code Challenge Home'

		body = tree.find('body')
		body.append(ET.Element('h1'))
		body[-1].text = 'Welcome'

		body.append(ET.Element('p'))
		body[-1].text = 'Coding challenges await you. Are you up for the challenge?'

		body.append(ET.Element('ol'))
		ol = body[-1]

		ol.append(ET.Element('li'))
		ol[-1].text = 'Option the first'

		ol.append(ET.Element('li'))
		ol[-1].text = 'Option numero dos'

		# send back the response

		self.send_response(200)
		self.end_headers()
		tree.write(self.wfile, method='html')

		return True

	def OnLogin(self, lPart):
		print("Got login request with {a}".format(a=lPart))

		if len(lPart) == 0:
			# initial request for logon page

			self.send_response(200)
			self.end_headers()
			self.wfile.write(s_strLogin)
			return True

		elif len(lPart) == 2:
			# username and password sent

			# TODO: validate username and password against our database
			fValid = True

			if fValid:
				# TODO: if ok, generate session, and send to user page

				session = SessionCreate(lPart)

				self.send_response(200)
				self.end_headers()
				self.wfile.write(UserPage(session))

			else:
				# TODO: if not ok, return login failed page

				self.send_response(200)
				self.end_headers()
				self.wfile.write(s_strLoginFailed)

			return True

		# TODO: do we need to do something clever here? Maybe make OnError that takes a reason?

		return False

	def OnMenu(self, lPart):
		print("Got menu request with {a}".format(a=lPart))

		# TODO

		return False

	def OnTask(self, lPart):
		print("Got task request with {a}".format(a=lPart))

		# TODO

		return False

	def OnHint(self, lPart):
		print("Got hint request with {a}".format(a=lPart))

		# TODO

		return False



if __name__ == '__main__':

	# Generate a server using our handler on port 8000 which then serves forever

	# NOTE: I'm using a threading version here, although it's not overly clear that
	#  I actually need to do so for the low level of traffic I'm actually expecting

	server = Hs.ThreadingHTTPServer(('', 8000), Handler)
	server.serve_forever()
