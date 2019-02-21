# python3 code training server

import hashlib
import http.server as Hs
import random
import xml.etree.ElementTree as ET

# various pages

s_strHome = """
<html>
<head>
	<title>Code Challenge Home</title>
</head>
<body>
	<h1>Welcome</h1>
	<p>Coding challenges await you. Are you up for the challenge?</p>
	<ol>
		<li><a href="/login">Login</a></li>
		<li><a href="/user">User</a> (won't work)</li>
		<li><a href="/task">Task</a> (won't work)</li>
		<li><a href="/hint">Hint</a> (won't work)</li>
	</ol>
</body>
</html>
"""

s_strLogin = """
<html>
<head>
	<title>Login Required</title>
</head>
<body>
	<p>Welcome to the challenge server. You need to log in to continue.</p>
	<form action="/login" method="POST">
		Username: <input type="text" name="username"/></br>
		Password: <input type="password" name="password"/></br>
		<input type="submit" value="Login"/>
	</form>
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
<html>
<head>
	<title>{username} Status</title>
</head>
<body>
	<p>Available challenges:</p>
	<ul>
	{challenges}
	</ul>
	<p>Completed challenges:</p>
	<ul>
	{completed}
	</ul>
</body>
</html>
"""

def UserPage(session):
	"""Return the page content formatted with the session for the user's page"""

	# TODO: username as nice text of user name
	# TODO: challenges as <li> items block (has surrounding <ul> already)
	# TODO: completed as <li> items block (has surrounding <ul> already>

	username = 'SampleUser'
	challenges = '<li>Nothing yet</li>\n'
	completed = '<li>Nothing yet</li>\n'

	return s_strUserPage.format(
							username=username,
							challenges=challenges,
							completed=completed)

# BB (davidm) tune? do something smarter?
#	- want "slow" algo to convert pw + salt -> hash, such as argon2, etc.

s_cIterHashPass = 50003

def HashPassword(password, salt):
	"""Generate the hash given the password and the salt"""

	abHash = hashlib.pbkdf2_hmac('sha512', password, salt, s_cIterHashPass)
	return abHash

def SaltGen():
	"""Generate salt value suitable for use with our password system"""

	s_strCh = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
	cCh = len(s_strCh) - 1
	strOut = ''.join([s_strCh[random.randint(0, cCh)] for i in range(64)])
	return strOut

class User:
	"""Information about a particular user"""

	def __init__(self):
		self.username = None
		self.salt = None
		self.abHash = None

def UserEnsure(username):
	"""Find the user with the given username, or generate one if it isn't there."""

	# TODO: where do we pull this stuff from? Look it up somewhere, I guess
	# TODO: to get timing the same, do we run HashPassword anyway?

	# Not a user we have, so generate one

	user = User()
	user.username = username
	user.salt = SaltGen()
	user.abHash = HashPassword(b'\x00', bytes(user.salt, 'ascii'))

	return user

def SessionCreate(username, password):
	"""Generate a session for the given login information, if valid, and return the associated session
	object. Failure means we return None instead."""

	print("session asked about '{u}' with '{p}'".format(u=username, p=password))

	user = UserEnsure(username)
	abHash = HashPassword(password, user.salt)

	# TODO: expire any existing sessions for that login
	# TODO: generate and record a new session object
	# TODO: return the associated session object

	return None

def SessionFind(sid):
	"""Look up the session with the given sid. If the session cannot be found or has timed out, will
	return None instead."""

	# TODO: look up the given session by the given sid
	# TODO: validate the expiration details for the session
	# TODO: return the associated session object

	return None



class Handler(Hs.BaseHTTPRequestHandler):
	"""Handler class for http server. The plumbing for handling http requests and such
	are all in here, mostly in the do_GET and do_POST methods"""

	def do_GET(self):
		print("Requested path '{p}' from '{c}'".format(p=self.path, c=self.client_address))

		mpPathFn = {
				'' : self.OnHome,
				'login' : self.OnLogin,
				'user' : self.OnUser,
				'task' : self.OnTask,
				'hint' : self.OnHint,
			}

		# Tasks (which I think map to URLs in some way):
		# - Request login (maybe?)
		# - Post answer to specific problem (only if not already solved?)

		# Dispatch the request to the appropriate function

		lPart = self.path.split('/')
		assert lPart[0] == ''
		target = lPart[1]
		args = lPart[2:]

		fn = mpPathFn.get(target, None)
		if fn is not None and fn(args):
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

		mpPathFn = {
				'login' : self.OnLoginPost,
			}

		# unpack post data

		# TODO: fix to pay attention to Content-Type header (currently assumes application/x-www-form-urlencoded)

		cBRead = int(self.headers.get('Content-Length', 0))
		strIn = self.rfile.read(cBRead).decode('ascii')

		parts = strIn.split('&')
		post = { part.split('=')[0] : part.split('=')[1] for part in parts }

		# determine handler function and dispatch to it

		lPart = self.path.split('/')
		assert lPart[0] == ''
		target = lPart[1]

		fn = mpPathFn.get(target, None)
		if fn is not None and fn(post):
			return

		self.send_error(404, 'We do not handle this yet')

	def TreeBasic(self):
		html = ET.Element('html')
		html.append(ET.Element('head'))
		html[-1].append(ET.Element('title'))
		html.append(ET.Element('body'))

		return ET.ElementTree(html)

	def OnHome(self, lPart):
		print("Got home request with {a}".format(a=lPart))

		# send back the response

		self.send_response(200)
		self.end_headers()
		self.wfile.write(bytes(s_strHome, 'ascii'))

		return True

	def OnLogin(self, lPart):
		print("Got login request with {a}".format(a=lPart))

		if len(lPart) == 0:
			# initial request for login page

			self.send_response(200)
			self.end_headers()
			self.wfile.write(bytes(s_strLogin, 'ascii'))
			return True

		# TODO: do we need to do something clever here? Maybe make OnError that takes a reason?

		return False

	def OnLoginPost(self, post):

		session = SessionCreate(post.get('username', None), post.get('password', None))

		if session is not None:
			# username and password sent

			self.send_response(200)
			self.end_headers()
			self.wfile.write(UserPage(session))

		else:

			# failed to login (and establish a session)

			self.send_response(200)
			self.end_headers()
			self.wfile.write(bytes(s_strLoginFailed, 'ascii'))

		return True

	def OnUser(self, lPart):

		if len(lPart) != 1:
			# TODO: report that there was an error

			return False

		session = SessionFind(lPart[0])
		if not session:
			# TODO: report that there was an error

			return False

		# send back the user's page

		self.send_response(200)
		self.end_headers()
		self.wfile.write(UserPage(session))

		return True

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

	try:
		server = Hs.ThreadingHTTPServer(('', 8000), Handler)
	except:
		server = Hs.HTTPServer(('', 8000), Handler)

	server.serve_forever()
