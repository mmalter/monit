import pandas

class EconVariable(object):
#I'm not subclassing pandas.DataFrame because it heavily uses __new__ to check if self is a DataFrame. pandas classes are difficult to subclass.
	def __init__(self, dataframe):
		self.lvl = lvl
	mom = property(get_mom,set_mom)
	def get_mom(self):
		if self.lvl.freqstr == 'M':
			return self.level.pct_change(1)*100
		else:
			raise TypeError("Month on Month growth rates are only for data with monthly frequencies")
	def set_mom(self, dataframe):
		if self.lvl.freqstr == 'M':
			self.lvl = (dataframe / 100 + 1) * self.lvl.shift(1)
		else:
			raise TypeError("Month on Month growth rates are only for data with monthly frequencies")
	qoq = property(get_qoq,set_qoq)
	def get_qoq(self):
		if self.lvl.freqstr == 'Q' or 'Q-DEC':
			return self.level.pct_change(1)*100
		else:
			raise TypeError("Quarter on quarter growth rates are only for data with quarterly frequencies")
	def set_qoq(self, dataframe):
		if self.lvl.freqstr == 'Q' or 'Q-DEC':
			self.lvl = (dataframe / 100 + 1) * self.lvl.shift(1)
		else:
			raise TypeError("Quarter on quarter growth rates are only for data with quarterly frequencies")
	yoy = property(get_yoy,set_yoy)
	def get_yoy(self):
		if self.lvl.freqstr == 'Y' or 'Y-DEC':
			return self.level.pct_change(1)*100
		if self.lvl.freqstr == 'Q' or 'Q-DEC':
			return self.level.pct_change(4)*100
		elif self.lvl.freqstr == 'M':
			return self.level.pct_change(12)*100
		else:
			raise NotImplemented("Only monthly, quarterly and yearly data have been implemented")
	def set_yoy(self, dataframe):
		if self.lvl.freqstr == 'Y':
			self.lvl = (dataframe / 100 + 1) * self.lvl.shift(1)
		if self.lvl.freqstr == 'Q' or 'Q-DEC':
			self.lvl = (dataframe / 100 + 1) * self.lvl.shift(4)
		elif self.lvl.freqstr == 'M':
			self.lvl = (dataframe / 100 + 1) * self.lvl.shift(12)
		else:
			raise NotImplemented("Only monthly, quarterly and yearly data have been implemented")
	an = property(get_an,set_an)
	def get_an(self):
		if self.lvl.freqstr == 'Y':
			return self.level.pct_change(1)*100
		elif self.lvl.freqstr == 'Q' or 'Q-DEC':
			return (((self.level.pct_change(1) + 1)**4)-1)*100
		elif self.lvl.freqstr == 'M':
			return (((self.level.pct_change(1) + 1)**12)-1)*100
		else:
			raise NotImplemented("Only monthly, quarterly and yearly data have been implemented")
	def set_an(self, dataframe):
		if self.lvl.freqstr == 'Y':
			self.lvl = (dataframe / 100 + 1) * self.lvl.shift(1)
		if self.lvl.freqstr == 'Q' or 'Q-DEC':
			self.lvl = (((dataframe*100)+1)**(1/4) / 100 + 1) * self.lvl.shift(1)
		elif self.lvl.freqstr == 'M':
			self.lvl = (((dataframe*100)+1)**(1/12) / 100 + 1) * self.lvl.shift(1)
		else:
			raise NotImplemented("Only monthly, quarterly and yearly data have been implemented")


class model:


class Node:
	def __init__(self, name):
		self.name = name
		self.edges = []
	def addEgde(self, node)	
		self.edges.append(node)

def dep_resolv(node,resolved,unresolved):		
	unresolved.append(node)
	for edge in node.edges:
		if edge not in resolved:
			if edge in unresolved:
				raise Exception('Circular dependence found')
			dep_resol(edge,resolved,unresolvedr)
	resolved.append(node)		
	unresolved.remove(node)

