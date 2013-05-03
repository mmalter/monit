import pandas
import random
import numpy
import re
import logging
import datetime
import matplotlib
import matplotlib.pyplot as plt
from mako.template import Template

lgr = logging.getLogger('monitoring')
lgr.setLevel(logging.DEBUG)

fh = logging.FileHandler('monitoring.log')
fh.setLevel(logging.DEBUG)

frmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(frmt)

lgr.addHandler(fh)

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
			nan_count = 1 + len(self.lvl.values) - len(self.lvl.dropna().values)
			for i in range(nan_count):
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
			nan_count = 1 + len(dataframe.values) - len(dataframe.dropna().values) + 9
			for i in range(nan_count):
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
			nan_count = 1 + len(dataframe.values) - len(dataframe.dropna().values)
			self.lvl = (dataframe / 100 + 1) * self.lvl.shift(1, freq='Y-DEC')
		if self.lvl.index.freqstr in ('Q', 'Q-DEC'):
			nan_count = 1 + len(dataframe.values) - len(dataframe.dropna().values)
			self.lvl = ((dataframe / 100) + 1) * self.lvl.shift(4, freq='Q-DEC')
		elif self.lvl.index.freqstr == 'M':
			nan_count = 1 + len(dataframe.values) - len(dataframe.dropna().values)
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
			nan_count = 1 + len(dataframe.values) - len(dataframe.dropna().values)
			for i in range(nan_count):
				self.lvl = (dataframe / 100 + 1) * self.lvl.shift(1, freq='Y-DEC')
		if self.lvl.index.freqstr in ('Q', 'Q-DEC'):
			nan_count = 1 + len(dataframe.values) - len(dataframe.dropna().values)
			for i in range(nan_count):
				self.lvl = ((((dataframe*100)+1)**(1/4) / 100 + 1)
						* self.lvl.shift(1, freq='Q-DEC'))
		elif self.lvl.index.freqstr == 'M':
			nan_count = 1 + len(dataframe.values) - len(dataframe.dropna().values)
			for i in range(nan_count):
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

class _coefficients(object):
	def __init__(self):
		self.beta = None

class Equation(object):
	def __init__(self,predicted_,predictors_,
		title,unit,comment=None,reg_comment=None,
		figname=str(random.randint(0,999999999999))+'.png',coefficients=None):
		self.comment = comment
		self.predicted = predicted_
		'''A list (EconVariable,transformation)'''
		self.predictors = predictors_
		'''A list of lists (EconVariable,transformation,lag)'''
		self.title = title
		self.unit = unit
		self.figname = figname
		self.dependencies = []
		self.predictions = []
		self.reg_comment = reg_comment
		self.reg = _coefficients()
		self.ols = False
		predicted = eval('self.predicted[0].'+self.predicted[1])
		predictors = []
		if coefficients != None:
			self.reg.beta = pandas.Series()
			i = 0
			lgr.debug('coef %s', coefficients)
			for predictor in self.predictors:
				data_beta = {}
				data_beta[predictor[0].lvl.columns[0]] = coefficients[i]
				data_beta = pandas.Series(data_beta)
				self.reg.beta = self.reg.beta.append(data_beta)
				i += 1
			data_beta = {}
			data_beta['intercept'] = 0
			data_beta = pandas.Series(data_beta)
			self.reg.beta = self.reg.beta.append(data_beta)
			lgr.debug('beta %s', self.reg.beta)
		else:
			for predictor in self.predictors:
				predictors.append(
						eval('predictor[0].'+predictor[1]+
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
			self.ols = True
			fig = plt.figure()
			ax1 = fig.add_subplot(111)
			graph = self.reg.y.plot(colors='b',label='Actual')
			graph = self.reg.y_fitted.plot(colors='r',label='Fitted')
			plt.legend(loc='best')
			plt.title(self.title+' - Actual vs fitted')
			plt.ylabel(self.unit)
			plt.savefig(self.figname+'_actualvsfitted.eps')

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
		# option than asking for the forecast horizon. We would 
        # end up with too large date ranges for indicator that 
        # are released earlier.
		try:
			with open(
					'assumptions/'+
					variable.lvl.columns[0].replace('/','')+
					'.csv') as f: pass
		except IOError as e:
			lgr.info('Initializing %s', variable.lvl.columns[0])
			period = pandas.period_range(
					variable.lvl.index.to_period()[-1],
					end.to_period(),
					freq=variable.lvl.index.freqstr)
			timestamp = period.to_timestamp(how='end')
			assumption = pandas.DataFrame(
				index=timestamp[1:],columns = [variable.lvl.columns])
			assumption.index.name = 'Date'
			assumption.to_csv(
					'assumptions/'+
					variable.lvl.columns[0].replace('/','')+
					'.csv')
	
	#Turn it into a getter
	def forecast(self, forecast_horizon, predictions=[]):
		lgr.info('Forecasting %s', self.predicted[0].lvl.columns[0])
		forecast_horizon_ = forecast_horizon
		if self.predicted[0].lvl.index.freqstr in ('Q', 'Q-DEC'):
			forecast_horizon_ = int(forecast_horizon/3)
		period = self.predicted[0].lvl.index.to_period()+forecast_horizon_
		timestamp = period.to_timestamp(how='end')
		start = timestamp[-forecast_horizon_]
		end = timestamp[-1]
		lgr.info('Number of periods to forecast : %s', forecast_horizon_)
		lgr.info('End of the forecast : %s', end)
		'''predictions must be a list of EconVariables'''
		self.predictions_ = predictions
		lgr.info('Predictions provided : %s', [x.lvl.tail(24) for x in self.predictions_])
		for i in range(-1,forecast_horizon_):
			assumptions_csv = []
			assumptions = []
			for variable, transformation, lags in self.predictors:
				lgr.info('Assumptions for : %s', variable.lvl.columns[0])
				assumption = None
				for prediction in self.predictions_:
					lgr.info('Inspecting available predictions')
					if prediction.lvl.columns[0] == variable.lvl.columns[0]:
						lgr.info('Prediction found')
						variable_ = eval(
								'variable.'+
								transformation+
								'.shift('+str(lags)+
								', freq="'+
								eval('variable.'+transformation+'.index.freqstr')+
								'")')
						assumption = eval(
								'prediction.'+
								transformation+
								'.shift('+str(lags)+
								', freq="'+
								eval('prediction.'+transformation+'.index.freqstr')+
								'")')
						assumption = pandas.DataFrame(
								{variable_.columns[0] : 
									numpy.append(variable_.values,
										assumption.values)},
									index = variable_.index.append(assumption.index))
						assumption.index.name = 'Date'
						assumption = assumption.resample(
								eval('variable.'+transformation+'.index.freq'),
								fill_method=None)
						assumption = assumption.truncate(after=end)
				if type(assumption) != pandas.core.frame.DataFrame:
					lgr.info('Prediction not found')
					if (variable.lvl.columns[0] 
							!= self.predicted[0].lvl.columns[0]):
						lgr.debug('The predicted variable is different from the predictor.')
						self.init_assumption(variable,end)
						assumption = pandas.read_table(
								'assumptions/'+
								variable.lvl.columns[0].replace('/','')+
								'.csv',
								sep=',',parse_dates=['Date'],index_col=0)
						assumption = assumption.resample(
								eval('variable.'+transformation+'.index.freqstr'),
								fill_method=None)
						assumption = EconVariable(assumption)
						start_ass = assumption.lvl.index[0]
						lgr.info('PH : %s', assumption.lvl.tail(24))
						assumption = pandas.DataFrame(
								{variable.lvl.columns[0] : numpy.append(
									eval('variable.lvl.values'),eval('assumption.lvl.values'))},
								#index = numpy.append(
									#eval('variable.lvl.index'),eval('assumption.lvl.index')))
								index =	variable.lvl.index.append(assumption.lvl.index))
						assumption.index.name = 'Date'
						assumption = assumption.resample(
								eval('variable.'+transformation+'.index.freqstr'),
								fill_method=None)
						assumption = EconVariable(assumption)
						lgr.info('PH2 : %s', assumption.lvl.tail(24))
						assumptions_csv.append([assumption,start_ass])
						assumption = eval(
								'assumption.'+
								transformation+
								'.shift('+str(lags)+')')
						assumption = assumption.truncate(after=end)
					else:
						lgr.debug('The predictor is a transformed version of the predicted variable.')
						assumption = variable.lvl
						assumption = assumption.truncate(after=end)
						assumption = EconVariable(assumption)
						assumption = eval(
								'assumption.'+
								transformation+
								'.shift('+str(lags)+
								', freq="'+assumption.lvl.index.freqstr+
								'")')
				assumptions.append(assumption)
				assumption = None
			if len(assumptions) == 1:
				assumptions_ = assumptions[0]
			if len(assumptions) > 1:
				assumptions_ = pandas.concat(
						[assumptions[0],assumptions[1]],axis=1)
			if len(assumptions) > 2:
				for assumption in assumptions[2:]:
					assumptions_ = pandas.concat(
							[assumptions_,assumption],axis=1)
			lgr.debug('Assumptions : %s', assumptions_.tail(24))
			prediction = pandas.DataFrame([self.reg.beta.values[-1] for i in range(len(assumptions_.index))],index=assumptions_.index)
			prediction.columns = self.predicted[0].lvl.columns
			lgr.debug('Coefficients : %s',  self.reg.beta.values)
			for i in range(0,len(self.reg.beta)-1):
				prediction = prediction + self.reg.beta.values[i] * assumptions_.iloc[:,i]
				lgr.debug('Predictor %s', i+1)
				lgr.debug('Prediction %s', prediction.tail(24))
			#prediction = self.reg.predict(self.reg.beta,assumptions_)
			prediction = pandas.DataFrame(
					prediction,index=prediction.index,
					columns=self.predicted[0].lvl.columns)
			prediction = prediction.truncate(
					before=timestamp[-forecast_horizon_],
					after=timestamp[-1])
			lgr.debug('ICH BIN AUFGEREGT! %s', prediction.tail(24))
			prediction = pandas.DataFrame(
					{prediction.columns[0] : numpy.append(
						eval('self.predicted[0].'+self.predicted[1]+'.values'),
						prediction.values)},
					#index=numpy.append(
						#eval('self.predicted[0].'+self.predicted[1]+'.index'),
						#prediction.index))
					index=eval('self.predicted[0].'+self.predicted[1]+'.index.append(prediction.index)'))
			lgr.debug('ICH BIN ENTAUSCHT! %s', prediction.tail(24))
			prediction = prediction.resample(
					self.predicted[0].lvl.index.freqstr, fill_method=None)
			prediction_ = EconVariable(self.predicted[0].lvl)
			exec('prediction_.'+self.predicted[1]+' = prediction')
			for i in range(len(self.predictions_)):
				if self.predictions_[i].lvl.columns[0] == prediction_.lvl.columns[0]:
					del self.predictions_[i]
			self.predictions_.append(prediction_)
			lgr.debug('Intermediate prediction %s', prediction.tail(24))
			lgr.debug('Intermediate predictions lvl %s', [pred.lvl.tail(24) for pred in self.predictions_])
			#À ce stade je ne l'ai plus
		lgr.debug('Final prediction %s', prediction_.lvl.tail(24))
		if self.figname != None:
			fig = plt.figure()
			ax1 = fig.add_subplot(111)
			graph = eval('prediction_.'+self.predicted[1]+'.truncate(before=eval("self.predicted[0]."+self.predicted[1]+".index[-12]")).dropna().plot(ax=ax1)')
			ax1.axvline(x=start)
			plt.title(self.title+' - Forecast')
			plt.ylabel(self.unit)
			plt.savefig(self.figname+'_forecast.eps')

			i = 0
			for assum in assumptions_csv:
				fig = plt.figure()
				ax1 = fig.add_subplot(111)
				graph = eval('assum[0].'+self.predicted[1]+'.truncate(before=eval("self.predicted[0]."+self.predicted[1]+".index[-12]")).dropna().plot(ax=ax1)')
				ax1.axvline(x=assum[1])
				plt.title(self.title+' - Assumption')
				plt.ylabel(self.unit)
				plt.savefig(self.figname+'_assumption'+str(i)+'.eps')
				i += 1
		return (prediction_,self.figname,assumptions_csv,self.comment)

class Node(object):
	def __init__(self, name):
		self.name = name

class Model(object):	
	def __init__(self,equations,title):
		self.title = title
		self.unresolved = []
		self.resolved = []
		self.equations = []
		self.hypothesis = []
		self.predictions = []
		now = datetime.datetime.now()
		self.now = now.strftime("%Y-%m-%d_%HM%M")
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
					raise Exception('Circular dependency found')
				self.dep_resolv(dependency)
		self.resolved.append(equation)		
		self.unresolved.remove(equation)

	def solve(self,equation):
		self.unresolved = []
		self.resolved = []
		self.hypothesis = []
		self.predictions = []
		self.predictions__ = []
		self.dep_resolv(equation)
		for equation_ in self.resolved:
			fct,fig,ass,com = equation_.forecast(12,self.predictions)
			self.predictions.append(fct)
			self.predictions__.append([fct,fig,ass,com])
		pred_ = []
		i = 1
		return self.predictions__

	def report(self,filename,template,my_solve_object):
		mytemplate = Template(filename=template,input_encoding="utf-8")
		tex_report = mytemplate.render(title=self.title,solve_object=my_solve_object)
		f = open(filename+self.now+'.tex', 'wb')
		f.write(tex_report.encode('utf-8'))

	def document(self,filename,template):
		mytemplate = Template(filename=template,input_encoding="utf-8")
		tex_report = mytemplate.render(title=self.title,model=self)
		f = open(filename+self.now+'.tex', 'wb')
		f.write(tex_report.encode('utf-8'))


