class SocialNetwork:
	def __init__(self, config):
		self.config = config
	def share(self, message, files=[]):
		raise NotImplementedError("The class SocialNetwork must be inherited")