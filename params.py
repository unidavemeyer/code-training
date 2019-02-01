# Definitions for parameters (problems to solve)

class Challenge:
	"""A challenge represents all of the stuff that is required to
	define, generate, and check answers for a single problem."""

	def __init__(self):
		pass

	def Title(self):
		"""Returns the text of the title of the problem"""

		return "The Undefined"

	def Text(self):
		"""Returns the text of the problem in proper HTML format"""

		return "<p>This problem has not been defined.</p>\n"

	def Submit(self):
		"""Returns the text that should appear by the submit field"""

		return "Sorry, we don't know what to ask for."

	def LHint(self):
		"""Returns the list of hints; each hint is a valid HTML fragment
		that could be included in a page"""

		return [ "<p>No first hint</p>", "<p>No second hint</p>" ]

	def Generate(self):
		"""Produces a single pair of (text, text) where the first text is
		the "input" data to provide to the user, and the second text is what
		the expected answer is for the given input. Subsequent calls may produce
		different pairs; the system will remember which user got what."""

		return ( "No data at all", "triangle" )

