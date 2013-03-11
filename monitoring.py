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


class Equation(predicted,predictors,title,unit,figname=None):
	def __init__(self):
		self.predicted = predicted
		self.predictors = predictors
		self.title = title
		self.figname = figname
		predicted = eval()
		predictors = []
		for key, value in predictors:
			predictors.append(eval(key+'.'+value))
		predictors_df = pandas.concat([predicted,predictors[0]],axis=1)
		if len(predictors) > 1:
			for predictor in predictors[1:]:
				predictors_df = pandas.concat([predictors_df,predictor],axis=1)

		self.reg = pandas.ols(y=predictors_df[predictors_df.columns[0]],x=predictors_df[predictors_df.columns[1:]])
		self.reg.y_name = predictors_df.columns[0]

		if figname != None:
			fig = plt.figure()
			actual_vs_fitted = pandas.concat([self.reg.y,self.reg.y_fitted],axis=1)
			actual_vs_fitted.columns = ['actual','fitted']
			graph = pandas.DataFrame.plot(actual_vs_fitted)
			plt.title(title+' - Actual vs fitted')
			plt.ylabel(unit)
			plt.savefig(figname)
		self.reg.true_x = predictors_df[predictors_df.columns[1:]]

	def init_assumption(self):
		for variable in self.reg.x.columns[:-1]:
			try:
				with open('assumptions/'+variable.replace('/','')+'.csv') as f: pass
			except IOError as e:
				print('Initializing '+variable)
				if self.reg.y.index.freq == 'Q-DEC':
					period = self.reg.true_x[variable].index.to_period()+forecast_horizon
					timestamp = period.to_timestamp(how='end')
					timestamp =  timestamp[-4:]
				if self.reg.y.index.freq == 'M':
					period = self.reg.true_x[variable].index.to_period()+forecast_horizon*3
					timestamp = period.to_timestamp(how='end')
					timestamp =  timestamp[-12:]
				assumption = pandas.DataFrame(index=timestamp,columns = [variable])
				assumption.index.name = 'Date'
				assumption.to_csv('assumptions/'+variable.replace('/','')+'.csv')

	#Turn it into a getter
	def forecast(self):
		assumptions = []
		for variable in self.reg.x.columns[:-1]:
			assumption = pandas.read_table('assumptions/'+variable.replace('/','')+'.csv',sep=',',parse_dates=['Date'],index_col=0)
			assumption = assumption.resample(self.reg.x[variable].index.freq,fill_method='ffill')
			assumption = pandas.DataFrame({variable : numpy.append(self.reg.true_x[variable].values,assumption.values)}, index = numpy.append(self.reg.true_x[variable].index,assumption.index))
			assumption.index.name = 'Date'
			assumptions.append(assumption)
		if len(assumptions) == 1:
			assumptions_ = assumptions[0]
		if len(assumptions) > 1:
			assumptions_ = pandas.concat([assumptions[0],assumptions[1]],axis=1)
		if len(assumptions) > 2:
			for assumption in assumptions:
				assumptions_ = pandas.concat([assumptions_,assumption],axis=1)
		#Now that we have the assumptions, let's predict!!!
		return self.reg.predict(self.reg.beta,assumptions_)

class Node(object):
	def __init__(self, name):
		self.name = name
		self.edges = []
	def addEgde(self, node)	
		self.edges.append(node)

def dep_resolv(node,resolved,unresolved):		
	unresolved.append(node)
	if node.edges == []:
		hypothesis.append(node)
	for edge in node.edges:
		if edge not in resolved:
			if edge in unresolved:
				raise Exception('Circular dependence found')
			dep_resol(edge,resolved,unresolvedr)
	resolved.append(node)		
	unresolved.remove(node)

class Model(object):	
	def __init__(self,equations):
		for equation in equations
			#get the key in equation.predicted
		for predictor_name, predictor_transformation in equation.predictors:
			equation.predictors_names.append(predictors_names)
			#Test wether the predictor is in the list of predictor. If so, add an Edge to this node. Make sure forecast() takes advantage of the predicted values. Put the predicted values in a dictionnary. A function get_predictions_or_assumptions() pass the additional inputs to forecast(). forecast() shouldn't take care of the assumptions.



