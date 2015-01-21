from Formater import Formater


def getFormater():
	return SkillFormater()


class SkillFormater(Formater):

	def formart(self, element):
		print {str(eval(element)[1])}
		return {str(eval(element)[1])}

