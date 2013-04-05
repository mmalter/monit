import dlstats
import pandas
import matplotlib.pyplot as plt
import matplotlib
import monitoring


gdp = dlstats.INSEE('001615899','GDP')
gdp_mark = dlstats.INSEE('001615898','GDP')

agriculture_gva = dlstats.INSEE('001615514','Agriculture GVA')
industry_gva = dlstats.INSEE('001616095','Industrial GVA')
industry_gva_mark = dlstats.INSEE('001616094','Industrial GVA')
industry_man_gva = dlstats.INSEE('001616093','Manufacturing industry GVA')
industry_man_gva_mark = dlstats.INSEE('001616092','Manufacturing industry GVA')
services_gva = dlstats.INSEE('001616101','Services_GVA')
construction_gva = dlstats.INSEE('001615758','Construction GVA')

#Contributions to nominal GDP
agriculture_gva_mark = dlstats.INSEE('001615513','Agriculture GVA')
services_gva_mark = dlstats.INSEE('001616100','Services GVA')
construction_gva_mark = dlstats.INSEE('001615757','Construction GVA')


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
business_climate = dlstats.INSEE('001565530','Business climate - synthetic')
business_climate_industry = dlstats.INSEE('001585934','Business climate - industry')
business_climate_construction = dlstats.INSEE('001586890','Business climate - construction')
business_climate_services = dlstats.INSEE('001587025','Business climate - services')
#ip_construction = dlstats.INSEE('001562796','Industrial production index - construction')
ip_construction = dlstats.INSEE('001654287','Industrial production index - construction')
#ip = dlstats.INSEE('001562715','Industrial production index')
ip = dlstats.INSEE('001654236','Industrial production index')

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
gov_exp = pandas.DataFrame(gov_exp_ind.values + gov_exp_col.values,index=gov_exp_ind.index)
gov_exp.columns = ['Goverment expenditures']
gov_exp_mark = gov_exp_ind_mark + gov_exp_col_mark
consumption = pandas.DataFrame(household_consumption.values + non_profit_consumption.values, index=household_consumption.index)
consumption.columns = ['Consumption']
consumption_mark = household_consumption_mark + non_profit_consumption_mark
imports = dlstats.INSEE('001615777','Imports')
exports = dlstats.INSEE('001615785','Exports')
imports_m = dlstats.INSEE('001569472','Imports monthly index')
exports_m = dlstats.INSEE('001568985','Exports monthly index')
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

tax_minus_subsidies = pandas.DataFrame(gdp.values - agriculture_gva.values - industry_man_gva.values - construction_gva.values - services_gva.values, index = gdp.index)
tax_minus_subsidies.columns = ['Tax minus subsidies']

agriculture_share = pandas.DataFrame(agriculture_gva.values/gdp.values, index=gdp.index)
industry_share = pandas.DataFrame(industry_gva.values/gdp.values, index=gdp.index)
industry_man_share = pandas.DataFrame(industry_man_gva.values/gdp.values, index=gdp.index)
construction_share = pandas.DataFrame(construction_gva.values/gdp.values, index=gdp.index)
services_share = pandas.DataFrame(services_gva.values/gdp.values, index=gdp.index)
tax_minus_subsidies_share = pandas.DataFrame(tax_minus_subsidies.values/gdp.values, index=gdp.index)

contribution_agriculture_gva = pandas.DataFrame(agriculture_gva.pct_change().values*100*agriculture_share.values,index = agriculture_share.index)
contribution_industry_man_gva = pandas.DataFrame(industry_man_gva.pct_change().values*100*industry_man_share.values, index=industry_man_share.index)
contribution_construction_gva = pandas.DataFrame(construction_gva.pct_change().values*100*construction_share.values, index=construction_share.index)
contribution_services_gva = pandas.DataFrame(services_gva.pct_change().values*100*services_share.values, index=services_share.index)
contribution_tax_minus_subsidies = pandas.DataFrame(tax_minus_subsidies.pct_change().values*100*tax_minus_subsidies_share.values, index=tax_minus_subsidies_share.index)

contribution_tax_minus_subsidies.columns = ['Tax minus subsidies']
contribution_services_gva.columns = ['Services']
contribution_construction_gva.columns = ['Construction']
contribution_industry_man_gva.columns = ['Industry']
contribution_agriculture_gva.columns = ['Agriculture']

industry_share = pandas.DataFrame(industry_gva.values/gdp.values, index=gdp.index)
industry_man_share = pandas.DataFrame(industry_man_gva.values/gdp.values, index=gdp.index)
construction_share = pandas.DataFrame(construction_gva.values/gdp.values, index=gdp.index)
services_share = pandas.DataFrame(services_gva.values/gdp.values, index=gdp.index)
tax_minus_subsidies_share = pandas.DataFrame(tax_minus_subsidies.values/gdp.values, index=gdp.index)

gdp_components = pandas.concat([contribution_agriculture_gva,contribution_industry_man_gva,contribution_construction_gva,contribution_services_gva,contribution_tax_minus_subsidies,gdp.pct_change()],axis=1)
#gdp_components.columns = ['Agriculture','Industry','Construction','Services','Tax minus subsidies','GDP']

xticks = pandas.date_range(start=gdp_components.index[-64], end=gdp_components.index[-1], freq='Q-DEC')
fig = plt.figure(1)
ax2 = fig.add_subplot(212)
ax1 = fig.add_subplot(211)
gdp_components[['Agriculture','Industry','Construction','Services','Tax minus subsidies']].truncate(before='01/01/2003').plot(kind='bar', stacked=True, ax=ax1)
plt.ylabel('Contributions to GDP')
plt.xlabel('')
plt.legend()
gdpplot = (gdp.truncate(before='01/01/2003').pct_change()*100).plot(ax=ax2)
plt.ylabel('GDP growth')
plt.legend()
plt.setp(ax1.get_xticklabels(), visible=False)
plt.tight_layout()
plt.savefig('gdp_contrib.eps')

gdp_ = monitoring.EconVariable(gdp)
ip_ = monitoring.EconVariable(ip)
industry_man_gva_ = monitoring.EconVariable(industry_man_gva)
agriculture_gva_ = monitoring.EconVariable(agriculture_gva)
construction_gva_ = monitoring.EconVariable(construction_gva)
services_gva_ = monitoring.EconVariable(services_gva)
business_climate_industry_ = monitoring.EconVariable(business_climate_industry)
business_climate_services_ = monitoring.EconVariable(business_climate_services)
business_climate_construction_ = monitoring.EconVariable(business_climate_construction)
business_climate_ = monitoring.EconVariable(business_climate)
gfcf_ = monitoring.EconVariable(gfcf)
tax_minus_subsidies_ = monitoring.EconVariable(tax_minus_subsidies)
imports_ = monitoring.EconVariable(imports)
imports_m_ = monitoring.EconVariable(imports_m)
exports_ = monitoring.EconVariable(exports)
exports_m_ = monitoring.EconVariable(exports_m)
consumption_ = monitoring.EconVariable(consumption)
gov_exp_ = monitoring.EconVariable(gov_exp)
household_confidence_m_ = monitoring.EconVariable(household_confidence_m)
consumption_goods_m_ = monitoring.EconVariable(consumption_goods_m)
ip_construction_ = monitoring.EconVariable(ip_construction)

consumption_share = pandas.DataFrame(consumption.values/gdp.values, index=gdp.index)
gfcf_share = pandas.DataFrame(gfcf.values/gdp.values, index=gdp.index)
imports_share = pandas.DataFrame(imports.values/gdp.values, index=gdp.index)
exports_share = pandas.DataFrame(exports.values/gdp.values, index=gdp.index)
gov_exp_share = pandas.DataFrame(gov_exp.values/gdp.values, index=gdp.index)

ind_m = monitoring.Equation([ip_,'yoy'],[[business_climate_industry_,'lvl',0],[ip_,'yoy',1]],'Industry - Monthly equation','% YoY',figname='ind_m',reg_comment='This the YoY growth rate of IP and the business climate survey in level (industrial component, from the INSEE).')
ind_q = monitoring.Equation([industry_man_gva_,'qoq'],[[ip_,'q.qoq',0]],'Industry - Quarterly equation','% qoq',figname='ind_q',reg_comment='The variables are QoQ.')
con_q = monitoring.Equation([construction_gva_,'qoq'],[[ip_construction_,'q.qoq',0],[construction_gva_,'qoq',1]],'Construction - Quarterly equation','% QoQ',figname='con_q',comment='con_q.tex',reg_comment='Everything is QoQ. To get a value for IP, we take the average of the three months in the quarter.')
con_m = monitoring.Equation([ip_construction_,'yoy'],[[business_climate_construction_,'lvl',0]],'Construction - Monthly equation','% YoY',figname='con_m',reg_comment='IP in the construction sector is YoY, the business climate survey is in level.')
ser_q = monitoring.Equation([services_gva_,'qoq'],[[business_climate_services_,'q.lvl',0]],'Services - Quarterly equation','% QoQ',figname='ser_q',reg_comment='The lhs is QoQ and the survey is in level.')
gdp_s_q = monitoring.Equation([gdp_,'qoq'],[[industry_man_gva_,'qoq',0],[construction_gva_,'qoq',0],[services_gva_,'qoq',0],[agriculture_gva_,'qoq',0],[tax_minus_subsidies_,'qoq',0]],'GDP - Quarterly equation','%',coefficients=[industry_man_share.values[-1][-1],construction_share.values[-1][-1],services_share.values[-1][-1],agriculture_share.values[-1][-1],tax_minus_subsidies_share.values[-1][-1]],figname='gdp_s_q')
supply_side = monitoring.Model([ind_q,ind_m,con_q,con_m,ser_q,gdp_s_q],'France Forecast - Supply side')



c_q = monitoring.Equation([consumption_,'qoq'],[[household_confidence_m_,'q.lvl',0],[consumption_goods_m_,'q.qoq',0]],'Consumption - Quarterly equation','% QoQ',figname='c_q',comment='c_q.tex',reg_comment='Everything is QoQ except the household confidence survey that is in level.')
gfcf_q = monitoring.Equation([gfcf_,'qoq'],[[business_climate_,'q.lvl',1]],'Investment - Quarterly equation','% QoQ',figname='gfcf',comment='gfcf.tex',reg_comment='The lhs is QoQ, the survey is in level.')
m_m = monitoring.Equation([imports_m_,'yoy'],[[ip_,'yoy',1]],'Imports - Monthly equation','% YoY',figname='m_m',reg_comment='Everything is YoY.')
m_q = monitoring.Equation([imports_,'qoq'],[[imports_m_,'q.qoq',0]],'Imports - Quarterly equation','% QoQ',figname='m_q',reg_comment='Everything is QoQ')
x_q = monitoring.Equation([exports_,'qoq'],[[exports_m_,'q.qoq',0]],'Exports - Quarterly equation','% QoQ',figname='x_q',comment='x_q.tex',reg_comment='Everything is QoQ.')
gdp_d_q = monitoring.Equation([gdp_,'qoq'],[[consumption_,'qoq',0],[gfcf_,'qoq',0],[imports_,'qoq',0],[exports_,'qoq',0],[gov_exp_,'qoq',0]],'GDP - Quarterly equation','%',coefficients=[consumption_share.values[-1][-1],gfcf_share.values[-1][-1],-imports_share.values[-1][-1],exports_share.values[-1][-1],gov_exp_share.values[-1][-1]],figname='gdp_d_q')

demand_side = monitoring.Model([c_q,gfcf_q,ind_m,m_m,m_q,x_q,gdp_d_q],'France Forecast - Demand side')

solve_s = supply_side.solve(gdp_s_q)
solve_d = demand_side.solve(gdp_d_q)

supply_side.report('supply_side','templateFrance.tex',solve_s)
demand_side.report('demand_side','templateFrance.tex',solve_d)

demand_side.document('demand_side_doc','templateDoc.tex')
supply_side.document('supply_side_doc','templateDoc.tex')

