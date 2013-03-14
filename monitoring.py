import pandas
import numpy

class EconVariable(object):
#I'm not subclassing pandas.DataFrame because it heavily uses __new__ to check if self is a DataFrame. pandas classes are difficult to subclass.
	def __init__(self, dataframe):
		self.lvl = dataframe
	def get_mom(self):
		if self.lvl.index.freqstr == 'M':
			return self.lvl.pct_change(1)*100
		else:
			raise TypeError("Month on Month growth rates are only for data with monthly frequencies")
	def set_mom(self, dataframe):
		if self.lvl.index.freqstr == 'M':
			self.lvl = (dataframe / 100 + 1) * self.lvl.shift(1)
		else:
			raise TypeError("Month on Month growth rates are only for data with monthly frequencies")
	mom = property(get_mom,set_mom)
	def get_qoq(self):
		if self.lvl.index.freqstr in ('Q', 'Q-DEC'):
			return self.lvl.pct_change(1)*100
		else:
			raise TypeError("Quarter on quarter growth rates are only for data with quarterly frequencies")
	def set_qoq(self, dataframe):
		if self.lvl.index.freqstr in ('Q', 'Q-DEC'):
			self.lvl = (dataframe / 100 + 1) * self.lvl.shift(1)
		else:
			raise TypeError("Quarter on quarter growth rates are only for data with quarterly frequencies")
	qoq = property(get_qoq,set_qoq)
	def get_yoy(self):
		if self.lvl.index.freqstr in ('Y', 'Y-DEC'):
			return self.lvl.pct_change(1)*100
		elif self.lvl.index.freqstr in ('Q', 'Q-DEC'):
			return self.lvl.pct_change(4)*100
		elif self.lvl.index.freqstr == 'M':
			return self.lvl.pct_change(12)*100
		else:
			raise NotImplemented("Only monthly, quarterly and yearly data have been implemented")
	def set_yoy(self, dataframe):
		if self.lvl.index.freqstr in ('Y', 'Y-DEC'):
			self.lvl = (dataframe / 100 + 1) * self.lvl.shift(1)
		if self.lvl.index.freqstr in ('Q', 'Q-DEC'):
			self.lvl = (dataframe / 100 + 1) * self.lvl.shift(4)
		elif self.lvl.index.freqstr == 'M':
			self.lvl = (dataframe / 100 + 1) * self.lvl.shift(12)
		else:
			raise NotImplemented("Only monthly, quarterly and yearly data have been implemented")
	yoy = property(get_yoy,set_yoy)
	def get_an(self):
		if self.lvl.index.freqstr == 'Y':
			return self.lvl.pct_change(1)*100
		elif self.lvl.index.freqstr == 'Q' or 'Q-DEC':
			return (((self.lvl.pct_change(1) + 1)**4)-1)*100
		elif self.lvl.index.freqstr == 'M':
			return (((self.lvl.pct_change(1) + 1)**12)-1)*100
		else:
			raise NotImplemented("Only monthly, quarterly and yearly data have been implemented")
	def set_an(self, dataframe):
		if self.lvl.index.freqstr == 'Y':
			self.lvl = (dataframe / 100 + 1) * self.lvl.shift(1)
		if self.lvl.index.freqstr == 'Q' or 'Q-DEC':
			self.lvl = (((dataframe*100)+1)**(1/4) / 100 + 1) * self.lvl.shift(1)
		elif self.lvl.index.freqstr == 'M':
			self.lvl = (((dataframe*100)+1)**(1/12) / 100 + 1) * self.lvl.shift(1)
		else:
			raise NotImplemented("Only monthly, quarterly and yearly data have been implemented")
	an = property(get_an,set_an)


class Equation(object):
	def __init__(self,predicted_,predictors_,title,unit,figname=None):
		self.predicted = predicted_
		'''A list of lists (EconVariable,transformation)'''
		self.predictors = predictors_
		'''A list of lists (EconVariable,transformation)'''
		self.title = title
		self.figname = figname
		self.dependencies = []
		predicted = eval('self.predicted[0].'+self.predicted[1])
		predictors = []
		for predictor in predictors_:
			predictors.append(eval('predictor[0].'+predictor[1]))
		self.predictors_df = pandas.concat([predicted,predictors[0]],axis=1,keys=[1,2])
		if len(predictors) > 1:
			i = 0
			for predictor in predictors[1:]:
				self.predictors_df = pandas.concat([self.predictors_df,predictor],axis=1,keys=[i,i+1])
		self.predictors_df.columns = [predicted.columns[0]]+[predictor[0].lvl.columns[0] for predictor in predictors_]
		self.reg = pandas.ols(y=self.predictors_df.iloc[:,0],x=self.predictors_df.iloc[:,1:])
		self.reg.true_x = self.predictors_df[self.predictors_df.columns[1:]]

	def addDependency(self, equation):
		self.dependencies.append(equation)


	def init_assumption(self,variable,forecast_horizon):
		try:
			with open('assumptions/'+variable.lvl.columns[0].replace('/','')+'.csv') as f: pass
		except IOError as e:
			print('Initializing '+variable.lvl.columns[0])
			if variable.lvl.index.freq == 'Q-DEC':
				period = variable.lvl.index.to_period()+forecast_horizon
				timestamp = period.to_timestamp(how='end')
				timestamp =  timestamp[-4:]
			if variable.lvl.index.freq == 'M':
				period = variable.lvl.index.to_period()+forecast_horizon*3
				timestamp = period.to_timestamp(how='end')
				timestamp =  timestamp[-12:]
			assumption = pandas.DataFrame(index=timestamp,columns = [variable.lvl.columns])
			assumption.index.name = 'Date'
			assumption.to_csv('assumptions/'+variable.lvl.columns[0].replace('/','')+'.csv')
	
	#Turn it into a getter
	def forecast(self, forecast_horizon, predictions=[]):
		'''predictions must be a list of EconVariables'''
		assumptions = []
		for variable, transformation in self.predictors:
			assumption = None
			for prediction in predictions:
				if prediction.columns[0] == variable.lvl.columns[0]:
					assumption = prediction[-forecast_horizon:]
			if assumption == None:
				self.init_assumption(variable,forecast_horizon)
				assumption = pandas.read_table('assumptions/'+variable.lvl.columns[0].replace('/','')+'.csv',sep=',',parse_dates=['Date'],index_col=0)
				#assumption = assumption.resample(variable.lvl.index.freq,fill_method='ffill')
				assumption = pandas.DataFrame({variable.lvl.columns[0] : numpy.append(variable.lvl.values,assumption.values)}, index = numpy.append(variable.lvl.index,assumption.index))
				assumption.index.name = 'Date'
				assumption = assumption.resample(variable.lvl.index.freq,fill_method='ffill')
				assumption = EconVariable(assumption)
			assumption = eval('assumption.'+transformation)
			assumptions.append(assumption)
		if len(assumptions) == 1:
			assumptions_ = assumptions[0]
		if len(assumptions) > 1:
			assumptions_ = pandas.concat([assumptions[0],assumptions[1]],axis=1)
		if len(assumptions) > 2:
			for assumption in assumptions:
				assumptions_ = pandas.concat([assumptions_,assumption],axis=1)
		return self.reg.predict(self.reg.beta,assumptions_)

class Node(object):
	def __init__(self, name):
		self.name = name

class Model(object):	
	def __init__(self,equations):
		self.unresolved = []
		self.resolved = []
		self.equations = []
		self.hypothesis = []
		for equation in equations:
			equation.dependencies = []
			for predictor in equation.predictors:
				for equation_ in equations:
					if equation != equation_:
						if predictor[0].lvl.columns[0] == equation_.predicted[0].lvl.columns[0]:
							equation.addDependency(equation_)
			self.equations.append(equation)

	def dep_resolv(self,equation):		
		self.unresolved.append(equation)
		if equation.dependencies == []:
			self.hypothesis.append(equation)
		for dependency in equation.dependencies:
			if dependency not in self.resolved:
				if dependency in self.unresolved:
					raise Exception('Circular dependence found')
				self.dep_resolv(dependency)
		self.resolved.append(equation)		
		self.unresolved.remove(equation)

	def solve(self,equation):
		self.dep_resolv(equation)
		self.predictions = []
		for equation_ in self.resolved:
			self.prediction.append([equation_,equation_.forecast(4),self.predictions])
		return self.predictions

	def report():
		print('TODO')






		#if figname != None:
			#fig = plt.figure()
			#actual_vs_fitted = pandas.concat([self.reg.y,self.reg.y_fitted],axis=1)
			#actual_vs_fitted.columns = ['actual','fitted']
			#graph = pandas.DataFrame.plot(actual_vs_fitted)
			#plt.title(title+' - Actual vs fitted')
			#plt.ylabel(unit)
			#plt.savefig(figname)
