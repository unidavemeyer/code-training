import params

# Define challenges for this series

class Chal01(params.Challenge):

	def Title(self):
		return "Owls and O Trolls, Part 1"

	def Text(self):
		return """<p>
		The Owls of the forest have sent us an important message. Unfortunately, though, the O Trolls got to the
		message before we could see it, and have added a whole bunch of "o" characters to the message so we can't
		figure out what the original message was. Can you count how many "o" characters are in the message for us?
		</p>"""

	def Submit(self):
		return "How many o characters are in the message?"

	def LHint(self):
		return [
				"""<p>In python, you can do this:</p>
				<pre>for ch in "hello":
					print(ch)
				</pre>""",

				"""<p>In python, you can do this:</p>
				<pre>if ch == "a":
					print("Saw an a")
				</pre>""",

				"""<p>In python, you can do this:</p>
				<pre>c = 1
				c += 1
				print("c is now {}".format(c))
				</pre>""",
			]

		return [ "<p>No first hint</p>", "<p>No second hint</p>" ]

	def Generate(self):
		"""Produces a single pair of (text, text) where the first text is
		the "input" data to provide to the user, and the second text is what
		the expected answer is for the given input. Subsequent calls may produce
		different pairs; the system will remember which user got what."""

		lSrc = [
				"Doom for the trolls have taken all of our jellybeans",
				"Soon we will not have troll problems of any kind",
				"This balloon is only one of the ones the trolls dislike",
				"At noon there will be only one troll that we are scared of",
				"Our troll book will come in the mail tomorrow",
				"The door to our tree cannot be found by any of the trolls",
			]

		# TODO: generate the extra o characters at the appropriate spots (see later days for constraints)
		# TODO: write a tester that calculates the answer as well, so that the whole result is found

		return ( "No data at all", "triangle" )

