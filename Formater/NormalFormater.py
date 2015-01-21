from Formater import Formater


def getFormater():
	return NormalFormater()


class NormalFormater(Formater):

	def formart(self, element):
		return {element}

