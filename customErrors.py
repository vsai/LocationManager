class UberError(Exception):
	def __init__(self, num, message):
		self.num = num
		self.message = message

	def __repr__(self):
		return "UberError: <num:%d\tmessage:%s>" % (self.num, self.message)

		