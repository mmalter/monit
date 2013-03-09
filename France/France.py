import dlstats
import numpy
import pandas
import matplotlib.pyplot as plt
from matplotlib.dates import *
import datetime

#numbers of quarters to forecast
forecast_horizon = 4

gdp = dlstats.INSEE('001615899','GDP')
gdp_mark = dlstats.INSEE('001615898','GDP')

agriculture_gva = dlstats.INSEE('001615514','Agriculture GVA')
industry_gva = dlstats.INSEE('001616095','Industrial GVA')
industry_gva_mark = dlstats.INSEE('001616094','Industrial GVA')
industry_man_gva = dlstats.INSEE('001616093','Manufacturing industry GVA')
industry_man_gva_mark = dlstats.INSEE('001616092','Manufacturing industry GVA')
services_gva = dlstats.INSEE('001616101','Services GVA')
construction_gva = dlstats.INSEE('001615758','Construction GVA')

#Contributions to nominal GDP
agriculture_gva_mark = dlstats.INSEE('001615513','Agriculture GVA')
services_gva_mark = dlstats.INSEE('001616100','Services GVA')
construction_gva_mark = dlstats.INSEE('001615757','Construction GVA')

agrifood_gva_mark = dlstats.INSEE('001615745','Agrifood industry GVA')
refining_gva_mark = dlstats.INSEE('001615747','Refining industry GVA')
capgoods_gva_mark = dlstats.INSEE('001615749','Capital goods industry GVA')
transport_ind_gva_mark = dlstats.INSEE('001615751','Transport industry GVA')
other_branch_ind_gva_mark = dlstats.INSEE('001615753','Misc industry GVA')
energy_gva_mark = dlstats.INSEE('001615755','Energy industry')
industry_gva_mark_sum = agrifood_gva_mark + refining_gva_mark + capgoods_gva_mark + transport_ind_gva_mark + other_branch_ind_gva_mark +  energy_gva_mark

trade_gva_mark = dlstats.INSEE('001615759','Trade GVA')
transport_ser_gva_mark = dlstats.INSEE('001615761','Transport services GVA')
hotel_restaurant_gva_mark = dlstats.INSEE('001615851','Hotels, restaurants GVA')
infocom_gva_mark = dlstats.INSEE('001615853','Communication GVA')
finance_gva_mark = dlstats.INSEE('001615855','Finance GVA')
realestate_gva_mark = dlstats.INSEE('001615857','Real estate GVA')
corpservices_gva_mark = dlstats.INSEE('001615859','Corporate services GVA')
nonmar_ser_gva_mark = dlstats.INSEE('001616088','Non merchant services GVA')
hh_ser_gva_mark = dlstats.INSEE('001616090','Services to households GVA')
ser_gva_mark_sum = trade_gva_mark + transport_ser_gva_mark + hotel_restaurant_gva_mark + infocom_gva_mark + finance_gva_mark + realestate_gva_mark + corpservices_gva_mark + nonmar_ser_gva_mark + hh_ser_gva_mark

#Supply side predictors
turnover_index = dlstats.INSEE('001562084','Turnover index')
business_climate = dlstats.INSEE('001565530','Business climate - synthetic')
business_climate_industry = dlstats.INSEE('001585934','Business climate - industry')
business_climate_construction = dlstats.INSEE('001586890','Business climate - construction')
business_climate_services = dlstats.INSEE('001587025','Business climate - services')
ip_construction = dlstats.INSEE('001562796','Industrial production index - construction')
ip = dlstats.INSEE('001562715','Industrial production index')

#Demand side contributions to the real GDP
gfcf = dlstats.INSEE('001615379','Gross fixed capital formation')
gfcf_mark = dlstats.INSEE('001615378','Gross fixed capital formation')
household_consumption = dlstats.INSEE('001615584','Household consumption')
household_consumption_mark = dlstats.INSEE('001615583','Household consumption')
non_profit_consumption = dlstats.INSEE('001615916','Non profit organizations consumption')
non_profit_consumption_mark = dlstats.INSEE('001615915','Non profit organization consumption')
gov_exp_ind = dlstats.INSEE('001616484','Individual government expenditures')
gov_exp_ind_mark = dlstats.INSEE('001616483','Individual government expenditures')
gov_exp_col = dlstats.INSEE('001616556','Collective government expenditures')
gov_exp_col_mark = dlstats.INSEE('001616555','Collective government expenditures')
gov_exp = gov_exp_ind + gov_exp_col
gov_exp_mark = gov_exp_ind_mark + gov_exp_col_mark
private_consumption = pandas.concat([household_consumption, non_profit_consumption],axis=1)
private_consumption = private_consumption['Household consumption'] + private_consumption['Non profit organizations consumption']
private_consumption = pandas.DataFrame(list(private_consumption.values),index=private_consumption.index)
private_consumption.columns = ['Consumption']
private_consumption_mark = household_consumption_mark + non_profit_consumption_mark
imports = dlstats.INSEE('001615777','Imports')
imports_mark = dlstats.INSEE('001615776','Imports')
exports = dlstats.INSEE('001615785','Exports')
exports_mark = dlstats.INSEE('001615784','Exports')
imports_m = dlstats.INSEE('001569472','Imports index')
imports_mark_m = dlstats.INSEE('001569471','Imports index')
exports_m = dlstats.INSEE('001568985','Exports index')
exports_mark_m = dlstats.INSEE('001568985','Exports index')
#INVENTORIES_CONTRIB_Q = insee_indicator('001627594','Q');

#Demand side predictors

consumption_goods_m = dlstats.INSEE('001613501','Housholds consumption of goods')
pi_imports = dlstats.INSEE('001558171','Import prices')
pi_exports = dlstats.INSEE('001558991','Export prices')
household_confidence_m = dlstats.INSEE('001587668','Household confidence')
business_climate_retail_m = dlstats.INSEE('001580428','Business climate - Retail trade')
bottlenecks = dlstats.INSEE('001586682','Bottlenecks')

vat_mark = dlstats.INSEE('001616141','VAT')
import_taxes_mark = dlstats.INSEE('001616411','Taxes on imports')
subsidies_mark = dlstats.INSEE('001615715','Subsidies')
other_taxes_mark = dlstats.INSEE('001615155','Misc taxes')
exp_subsidies_mark = dlstats.INSEE('001615371','Subsidies on exports')
tax_prod_mark = dlstats.INSEE('001615108','Taxes on products')

na_d = pandas.concat([gdp,agriculture_gva,industry_man_gva,construction_gva,services_gva],axis=1)
tax_minus_subsidies = na_d['GDP'] - na_d['Agriculture GVA'] - na_d['Manufacturing industry GVA'] - na_d['Construction GVA'] - na_d['Services GVA']
tax_minus_subsidies = pandas.DataFrame(list(tax_minus_subsidies.values),index=tax_minus_subsidies.index)
tax_minus_subsidies.columns = ['Tax minus subsidies']
na_d = pandas.concat([na_d,tax_minus_subsidies],axis=1)

agriculture_share = agriculture_gva/gdp
industry_share = industry_gva/gdp
industry_man_share = industry_man_gva/gdp
construction_share = construction_gva/gdp
services_share = services_gva/gdp
tax_minus_subsidies_share = tax_minus_subsidies/gdp

contribution_agriculture_gva = agriculture_gva.pct_change()*100*agriculture_share
contribution_industry_man_gva = industry_man_gva.pct_change()*100*industry_man_share
contribution_construction_gva = construction_gva.pct_change()*100*construction_share
contribution_services_gva = services_gva.pct_change()*100*services_share
contribution_tax_minus_subsidies = tax_minus_subsidies.pct_change()*100*tax_minus_subsidies_share

ip_q = ip.resample('Q',how='mean')
ip_q_gr = ip_q.pct_change()*100
ip_q_gr.columns = ['Industrial production index - Q/Q-1 growth rate']
ip_gr = ip.pct_change(12)*100
ip_gr.columns = ['Industrial production index - M/M-12 growth rate']
industry_man_gva_gr = industry_man_gva.pct_change(4)*100
industry_man_gva_gr = industry_man_gva_gr.resample('Q',fill_method='ffill')
industry_man_gva_gr.columns = ['Manufacturing industry GVA - Q/Q-1 growth rate']

#gdp_components = pandas.concat([contribution_agriculture_gva,contribution_industry_man_gva,contribution_construction_gva,contribution_services_gva,contribution_tax_minus_subsidies,gdp.pct_change()*100],axis=1)
#gdp_components.columns = ['Agriculture','Industry','Construction','Services','Tax minus subsidies','GDP']

#xticks = pandas.date_range(start=gdp_components.index[-64], end=gdp_components.index[-1], freq='Q-DEC')
#fig = plt.figure(1)
#ax = fig.add_subplot(211)
#gdpplot = (gdp.truncate(before='01/01/2006').pct_change()*100).plot(label='GDP', ax=ax)
#plt.legend()
#plt.xlabel('GDP growth')
#ax2 = fig.add_subplot(212)
#gdp_components[['Agriculture','Industry','Construction','Services','Tax minus subsidies']].truncate(before=gdp_components.index[-64]).plot(kind='bar', stacked=True, label=gdp_components.columns, ax=ax2, xticks=xticks.to_period())

#plt.legend()
#plt.xlabel('Contributions to GDP')
#ax.xaxis.set_major_locator(AutoDateLocator())
#ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
#ax.xaxis.set_major_formatter(AutoDateFormatter())
#plt.tight_layout()
#plt.show()

def monitoring_model(predicted,predictors,title,unit,figname=None):
	predictors_df = pandas.concat([predicted,predictors[0]],axis=1)
	if len(predictors) > 1:
		for predictor in predictors[1:]:
			predictors_df = pandas.concat([predictors_df,predictor],axis=1)

	model = pandas.ols(y=predictors_df[predictors_df.columns[0]],x=predictors_df[predictors_df.columns[1:]])
	model.y_name = predictors_df.columns[0]

	if figname != None:
		fig = plt.figure()
		actual_vs_fitted = pandas.concat([model.y,model.y_fitted],axis=1)
		actual_vs_fitted.columns = ['actual','fitted']
		graph = pandas.DataFrame.plot(actual_vs_fitted)
		plt.title(title+' - Actual vs fitted')
		plt.ylabel(unit)
		plt.savefig(figname)

	model.true_x = predictors_df[predictors_df.columns[1:]]
	return model

def init_assumption(model):
	for variable in model.x.columns[:-1]:
		try:
			with open('assumptions/'+variable.replace('/','')+'.csv') as f: pass
		except IOError as e:
			print('Initializing '+variable)
			if model.y.index.freq == 'Q-DEC':
				period = model.true_x[variable].index.to_period()+forecast_horizon
				timestamp = period.to_timestamp(how='end')
				timestamp =  timestamp[-4:]
			if model.y.index.freq == 'M':
				period = model.true_x[variable].index.to_period()+forecast_horizon*3
				timestamp = period.to_timestamp(how='end')
				timestamp =  timestamp[-12:]
			assumption = pandas.DataFrame(index=timestamp,columns = [variable])
			assumption.index.name = 'Date'
			assumption.to_csv('assumptions/'+variable.replace('/','')+'.csv')

def forecast(model):
	assumptions = []
	for variable in model.x.columns[:-1]:
		assumption = pandas.read_table('assumptions/'+variable.replace('/','')+'.csv',sep=',',parse_dates=['Date'],index_col=0)
		assumption = assumption.resample(model.x[variable].index.freq,fill_method='ffill')
		assumption = pandas.DataFrame({variable : numpy.append(model.true_x[variable].values,assumption.values)}, index = numpy.append(model.true_x[variable].index,assumption.index))
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
	return model.predict(model.beta,assumptions_)

mod = {}
#mod['ind_q'] = monitoring_model(industry_man_gva_gr,[ip_q_gr],'Manufacturing industry - quarterly equation','% Q/Q-4')
mod['ind_q'] = monitoring_model(industry_man_gva_gr,[ip_q_gr],'Manufacturing industry - quarterly equation','% Q/Q-4')

#shiftedip = ip.shift(1).pct_change(12)*100
#shiftedip.columns = ['Industrial production index - M/M-12 growth rate - one lag']
#mod.ip = monitoring_model(ip_gr,[business_climate_industry,shiftedip],'IP - monthly equation','% M/M-12')
mod['ind_m'] = monitoring_model(ip_gr,[business_climate_industry],'IP - monthly equation','% M/M-12')

shiftedip_con_q = construction_gva.shift(1).pct_change(4)*100
shiftedip_con_q.columns = ['Construction GVA - Q/Q-4 growth rate - one lags']
mod['con_q'] = monitoring_model(construction_gva.pct_change(4)*100,[ip_construction.resample('Q').pct_change(4)*100],'Construction - quarterly equation','% Q/Q-4')

mod['ser_q'] = monitoring_model(services_gva.pct_change(4)*100,[business_climate_services.resample('Q',how='mean')],'Services - quarterly equation','% Q/Q-4')

mod['c_q'] = monitoring_model(private_consumption.pct_change()*100,[consumption_goods_m.resample('Q',how='mean').pct_change()*100,household_confidence_m.resample('Q',how='mean')],'Services - quarterly equation','% Q/Q-1')

mod['gfcf_q'] = monitoring_model(gfcf.pct_change(4)*100,[business_climate.resample('Q',how='mean')],'Services - quarterly equation','% Q/Q-4')

#mod['m_q'] = monitoring_model(imports.pct_change()*100,[imports_m.resample('Q',how='mean').pct_change()*100],'Imports - quarterly equation','% Q/Q-1')

mod['m_m'] = monitoring_model(imports_m.pct_change(12)*100,[ip_gr],'Imports - monthly equation','% M/M-12')

mod['x_q'] = monitoring_model(exports.pct_change()*100,[exports_m.resample('Q',how='mean').pct_change()*100],'Exports - quarterly equation','% Q/Q-1')

[init_assumption(mod[x]) for x in mod]
forecasts = {}
for x in mod:
	print(x)
	forecasts[x] = forecast(mod[x])
ipgr_fc = forecasts['ind_m']
newip = ((ipgr_fc/100)+1) * ip.shift(12,freq='M')
ipgrqqlag = newip.resample('Q',how='mean').shift(1).pct_change()*100
newip[-12:].to_csv('assumptions/'+'Industrial production index'.replace('/','')+'.csv')
newipgr = (newip-newip.shift(12,freq='M'))/newip.shift(12,freq='M')*100
newipgr[-24:-12].to_csv('assumptions/'+'Industrial production index - MM-12 growth rate'.replace('/','')+'.csv')
ipgrqqlag.index.name='Date'
ipgrqqlag[-4:].to_csv('assumptions/'+'Industrial production index - QQ-1 growth rate'.replace('/','')+'.csv')
mgr_fc = forecasts['m_m']
newm = ((mgr_fc/100)+1) * imports_m.shift(12,freq='M')
m_q = newm.resample('Q',how='mean').pct_change()*100
m_q[-5:].to_csv('assumptions/'+'Imports index'.replace('/','')+'.csv')
