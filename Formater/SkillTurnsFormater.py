from Formater import Formater

def getFormater():
	return SkillTurnsFormater()

class SkillTurnsFormater(Formater):

	def formart(self, elements):
		return {str(element[1]) for element in eval(elements)}
