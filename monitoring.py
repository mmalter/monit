import pandas
import numpy
import re

class EconVariable(object):
# I'm not subclassing pandas.DataFrame because  pandas often relies
# on __new__ to check if self is a DataFrame. pandas classes are 
# difficult to subclass.
	def __init__(self, dataframe):
		self.lvl = dataframe
	def get_mom(self):
		if self.lvl.index.freqstr == 'M':
			return self.lvl.pct_change(1)*100
		else:
			raise TypeError(
					"Month on Month growth rates are only for data with "
					"monthly frequencies")
	def set_mom(self, dataframe):
		if self.lvl.index.freqstr == 'M':
			self.lvl = (dataframe / 100 + 1) * self.lvl.shift(1, freq='M')
		else:
			raise TypeError(
					"Month on Month growth rates are only "
					"for data with monthly frequencies")
	mom = property(get_mom,set_mom)
	def get_qoq(self):
		if self.lvl.index.freqstr in ('Q', 'Q-DEC'):
			return self.lvl.pct_change(1)*100
		else:
			raise TypeError(
					"Quarter on quarter growth rates are only "
					"for data with quarterly frequencies")
	def set_qoq(self, dataframe):
		if self.lvl.index.freqstr in ('Q', 'Q-DEC'):
			self.lvl = (dataframe / 100 + 1) * self.lvl.shift(1, freq='Q-DEC')
		else:
			raise TypeError(
					"Quarter on quarter growth rates are only "
					"for data with quarterly frequencies")
	qoq = property(get_qoq,set_qoq)
	def get_yoy(self):
		if self.lvl.index.freqstr in ('Y', 'Y-DEC'):
			return self.lvl.pct_change(1)*100
		elif self.lvl.index.freqstr in ('Q', 'Q-DEC'):
			return self.lvl.pct_change(4)*100
		elif self.lvl.index.freqstr == 'M':
			return self.lvl.pct_change(12)*100
		else:
			raise NotImplemented(
					"Only monthly, quarterly and yearly data "
					"have been implemented")
	def set_yoy(self, dataframe):
		if self.lvl.index.freqstr in ('Y', 'Y-DEC'):
			self.lvl = (dataframe / 100 + 1) * self.lvl.shift(1, freq='Y-DEC')
		if self.lvl.index.freqstr in ('Q', 'Q-DEC'):
			self.lvl = (dataframe / 100 + 1) * self.lvl.shift(4, freq='Q-DEC')
		elif self.lvl.index.freqstr == 'M':
			self.lvl = (dataframe / 100 + 1) * self.lvl.shift(12, freq='M')
		else:
			raise NotImplemented(
					"Only monthly, quarterly and yearly data "
					"have been implemented")
	yoy = property(get_yoy,set_yoy)
	def get_an(self):
		if self.lvl.index.freqstr == 'Y':
			return self.lvl.pct_change(1)*100
		elif self.lvl.index.freqstr in ('Q', 'Q-DEC'):
			return (((self.lvl.pct_change(1) + 1)**4)-1)*100
		elif self.lvl.index.freqstr == 'M':
			return (((self.lvl.pct_change(1) + 1)**12)-1)*100
		else:
			raise NotImplemented(
					"Only monthly, quarterly and yearly data "
					"have been implemented")
	def set_an(self, dataframe):
		if self.lvl.index.freqstr in ('Y', 'Y-DEC'):
			self.lvl = (dataframe / 100 + 1) * self.lvl.shift(1, freq='Y-DEC')
		if self.lvl.index.freqstr in ('Q', 'Q-DEC'):
			self.lvl = ((((dataframe*100)+1)**(1/4) / 100 + 1)
					* self.lvl.shift(1, freq='Q-DEC'))
		elif self.lvl.index.freqstr == 'M':
			self.lvl = ((((dataframe*100)+1)**(1/12) / 100 + 1) 
					* self.lvl.shift(1, freq='Q-DEC'))
		else:
			raise NotImplemented(
					"Only monthly, quarterly and yearly data "
					"have been implemented")
	an = property(get_an,set_an)
	def get_q(self):
		if self.lvl.index.freqstr in ('Q', 'Q-DEC'):
			return self
		elif self.lvl.index.freqstr == 'M':
			return EconVariable(self.lvl.resample('Q',how='mean'))
		else:
			raise NotImplemented(
					"Only monthly and quarterly data have been implemented")
	def set_q(self):
		raise NotImplemented(
				"Do not input resampled data. It makes my mom cry.")
	q = property(get_q,set_q)


class Equation(object):
	def __init__(self,predicted_,predictors_,title,unit,figname=None):
		self.predicted = predicted_
		'''A list (EconVariable,transformation)'''
		self.predictors = predictors_
		'''A list of lists (EconVariable,transformation,lag)'''
		self.title = title
		self.figname = figname
		self.dependencies = []
		self.predictions = []
		predicted = eval('self.predicted[0].'+self.predicted[1])
		predictors = []
		for predictor in predictors_:
			predictors.append(
					eval('predictor[0].'+predictor[1]
						'.shift('+str(predictor[2])+')'))
		self.predictors_df = pandas.concat([predicted,predictors[0]],axis=1)
		if len(predictors) > 1:
			for predictor in predictors[1:]:
				self.predictors_df = pandas.concat(
						[self.predictors_df,predictor],
						axis=1)
		self.reg = pandas.ols(
				y=self.predictors_df.iloc[:,0],
				x=self.predictors_df.iloc[:,1:])
		self.reg.true_x = self.predictors_df[self.predictors_df.columns[1:]]
		self.lags = [0] 
		p = re.compile('\d+')
		for predictor in predictors_:
			match = (p.findall(predictor[1]))
			if match != []:
				self.lags.append(int(match[0]))
		self.lags = max(self.lags)

	def addDependency(self, equation):
		self.dependencies.append(equation)


	def init_assumption(self,variable,end):
		# Taking the date of the end of the forecast is a better
		# option than asking for than asking for the forecast
		# horizon. We would end up with too large date ranges for
		# indicator that are released earlier.
		try:
			with open(
					'assumptions/'
					variable.lvl.columns[0].replace('/','')
					'.csv') as f: pass
		except IOError as e:
			print('Initializing '+variable.lvl.columns[0])
			period = pandas.period_range(
					variable.lvl.index.to_period()[-1],
					end.to_period(),
					freq=variable.lvl.index.freqstr)
			timestamp = period.to_timestamp(how='end')
			assumption = pandas.DataFrame(
					index=timestamp,columns = [variable.lvl.columns])
			assumption.index.name = 'Date'
			assumption.to_csv(
					'assumptions/'
					variable.lvl.columns[0].replace('/','')
					'.csv')
	
	#Turn it into a getter
	def forecast(self, forecast_horizon, predictions=[]):
		forecast_horizon_ = forecast_horizon
		if self.predicted[0].lvl.index.freqstr == 'Q':
			forecast_horizon_ = forecast_horizon/3
		period = self.predicted[0].lvl.index.to_period()+forecast_horizon_
		timestamp = period.to_timestamp(how='end')
		start = timestamp[-forecast_horizon_]
		end = timestamp[-1]
		'''predictions must be a list of EconVariables'''
		self.predictions_ = predictions
		for i in range(-1,forecast_horizon_-1):
			assumptions = []
			for variable, transformation, lags in self.predictors:
				assumption = None
				for prediction in self.predictions_:
					if prediction.columns[0] == variable.lvl.columns[0]:
						variable_ = eval(
								'variable.'
								transformation
								'.shift('+str(lags)
								', freq="'
								variable.lvl.index.freqstr
								'")')
						assumption = prediction.shift(
								lags, freq=prediction.index.freqstr)
						assumption = pandas.DataFrame(
								{variable_.columns[0] : 
									numpy.append(variable_.values,
										assumption.values)},
									index = numpy.append(variable_.index,
										assumption.index))
						assumption.index.name = 'Date'
						assumption = assumption.resample(
								variable.lvl.index.freq, fill_method=None)
						assumption = assumption.truncate(after=end)
				if type(assumption) != pandas.core.frame.DataFrame:
					if (variable.lvl.columns[0] 
							!= self.predicted[0].lvl.columns[0]):
						self.init_assumption(variable,end)
						assumption = pandas.read_table(
								'assumptions/'
								variable.lvl.columns[0].replace('/','')
								'.csv',
								sep=',',parse_dates=['Date'],index_col=0)
						assumption = pandas.DataFrame(
								{variable.lvl.columns[0] : numpy.append(
									variable.lvl.values,assumption.values)},
								index = numpy.append(
									variable.lvl.index,assumption.index))
						assumption.index.name = 'Date'
						assumption = assumption.resample(
								variable.lvl.index.freq,fill_method=None)
						assumption = assumption.truncate(after=end)
						assumption = EconVariable(assumption)
						assumption = eval(
								'assumption.'
								transformation
								'.shift('+str(lags)+')')
					else:
						assumption = variable.lvl
						assumption = assumption.truncate(after=end)
						assumption = EconVariable(assumption)
						assumption = eval(
								'assumption.'
								transformation
								'.shift('+str(lags)
								', freq="'+assumption.lvl.index.freqstr
								'")')
				assumptions.append(assumption)
			if len(assumptions) == 1:
				assumptions_ = assumptions[0]
			if len(assumptions) > 1:
				assumptions_ = pandas.concat(
						[assumptions[0],assumptions[1]],axis=1)
			if len(assumptions) > 2:
				for assumption in assumptions:
					assumptions_ = pandas.concat(
							[assumptions_,assumption],axis=1)
			prediction = self.reg.predict(self.reg.beta,assumptions_)
			prediction = pandas.DataFrame(
					prediction,index=prediction.index,
					columns=self.predicted[0].lvl.columns)
			prediction = prediction.truncate(
					before=timestamp[-forecast_horizon_],
					after=timestamp[-1])
			prediction = pandas.DataFrame(
					{prediction.columns[0] : numpy.append(
						eval('self.predicted[0].'+self.predicted[1]+'.values'),
						prediction.values)},
					index=numpy.append(
						eval('self.predicted[0].'+self.predicted[1]+'.index'),
						prediction.index))
			prediction = prediction.resample(
					self.predicted[0].lvl.index.freqstr, fill_method=None)
			prediction_ = EconVariable(self.predicted[0].lvl)
			exec('prediction_.'+self.predicted[1]+' = prediction')
			self.predictions_.append(prediction)
		return prediction

class Node(object):
	def __init__(self, name):
		self.name = name

class Model(object):	
	def __init__(self,equations):
		self.unresolved = []
		self.resolved = []
		self.equations = []
		self.hypothesis = []
		self.predictions = []
		for equation in equations:
			equation.dependencies = []
			for predictor in equation.predictors:
				for equation_ in equations:
					if equation != equation_:
						if (predictor[0].lvl.columns[0] == 
								equation_.predicted[0].lvl.columns[0]):
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
		self.unresolved = []
		self.resolved = []
		self.equations = []
		self.hypothesis = []
		self.predictions = []
		self.dep_resolv(equation)
		for equation_ in self.resolved:
			self.predictions.append(
					[equation_,equation_.forecast(12),self.predictions])
			#for foo in self.predictions:
				#print(foo[1].tail(12))
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
