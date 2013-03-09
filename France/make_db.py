import dlstats
import pandas
import matplotlib.pyplot as plt
from matplotlib.dates import *
import datetime

gdp = dlstats.INSEE('001615899','GDP')
gdp_mark = dlstats.INSEE('001615898','GDP market')

agriculture_gva = dlstats.INSEE('001615514','Agriculture GVA')
industry_gva = dlstats.INSEE('001616095','Industrial GVA')
industry_gva_mark = dlstats.INSEE('001616094','Industrial GVA market')
industry_man_gva = dlstats.INSEE('001616093','Manufacturing industry GVA')
industry_man_gva_mark = dlstats.INSEE('001616092','Manufacturing industry GVA market')
services_gva = dlstats.INSEE('001616101','Services_GVA')
construction_gva = dlstats.INSEE('001615758','Construction GVA')

#Contributions to nominal GDP
agriculture_gva_mark = dlstats.INSEE('001615513','Agriculture GVA market')
services_gva_mark = dlstats.INSEE('001616100','Services GVA market')
construction_gva_mark = dlstats.INSEE('001615757','Construction GVA market')

agrifood_gva_mark = dlstats.INSEE('001615745','Agrifood industry GVA market')
refining_gva_mark = dlstats.INSEE('001615747','Refining industry GVA market')
capgoods_gva_mark = dlstats.INSEE('001615749','Capital goods industry GVA market')
transport_ind_gva_mark = dlstats.INSEE('001615751','Transport industry GVA market')
other_branch_ind_gva_mark = dlstats.INSEE('001615753','Misc industry GVA market')
energy_gva_mark = dlstats.INSEE('001615755','Energy industry market')

trade_gva_mark = dlstats.INSEE('001615759','Trade GVA market')
transport_ser_gva_mark = dlstats.INSEE('001615761','Transport services GVA market')
hotel_restaurant_gva_mark = dlstats.INSEE('001615851','Hotels, restaurants GVA market')
infocom_gva_mark = dlstats.INSEE('001615853','Communication GVA market')
finance_gva_mark = dlstats.INSEE('001615855','Finance GVA market')
realestate_gva_mark = dlstats.INSEE('001615857','Real estate GVA')
corpservices_gva_mark = dlstats.INSEE('001615859','Corporate services GVA market')
nonmar_ser_gva_mark = dlstats.INSEE('001616088','Non merchant services GVA market')
hh_ser_gva_mark = dlstats.INSEE('001616090','Services to households GVA market')

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
gfcf_mark = dlstats.INSEE('001615378','Gross fixed capital formation market')
household_consumption = dlstats.INSEE('001615584','Household consumption')
household_consumption_mark = dlstats.INSEE('001615583','Household consumption market')
non_profit_consumption = dlstats.INSEE('001615916','Non profit organizations consumption')
non_profit_consumption_mark = dlstats.INSEE('001615915','Non profit organization consumption market')
gov_exp_ind = dlstats.INSEE('001616484','Individual government expenditures')
gov_exp_ind_mark = dlstats.INSEE('001616483','Individual government expenditures market')
gov_exp_col = dlstats.INSEE('001616556','Collective government expenditures')
gov_exp_col_mark = dlstats.INSEE('001616555','Collective government expenditures market')
imports = dlstats.INSEE('001615777','Imports')
imports_mark = dlstats.INSEE('001615776','Imports market')
exports = dlstats.INSEE('001615785','Exports')
exports_mark = dlstats.INSEE('001615784','Exports market')
imports_m = dlstats.INSEE('001569472','Imports')
imports_mark_m = dlstats.INSEE('001569471','Imports market')
exports_m = dlstats.INSEE('001568985','Exports')
exports_mark_m = dlstats.INSEE('001568985','Exports market')

def exports_stuff(list_of_stuff):
	for stuff in list_of_stuff:
		print(stuff.name)
		stuff.to_csv('db/'+stuff.name)


my_stuff = [gdp,gdp_mark,agriculture_gva,industry_gva,industry_gva_mark,industry_man_gva,industry_man_gva_mark,services_gva,construction_gva,agriculture_gva_mark,services_gva_mark,construction_gva_mark,agrifood_gva_mark,refining_gva_mark,capgoods_gva_mark,transport_ind_gva_mark,other_branch_ind_gva_mark,energy_gva_mark,trade_gva_mark,transport_ser_gva_mark,hotel_restaurant_gva_mark,infocom_gva_mark,finance_gva_mark,realestate_gva_mark,corpservices_gva_mark,nonmar_ser_gva_mark,hh_ser_gva_mark,turnover_index,business_climate,business_climate_industry,business_climate_construction,business_climate_services,ip_construction,ip,gfcf,gfcf_mark,household_consumption,household_consumption_mark,non_profit_consumption,non_profit_consumption_mark,gov_exp_ind,gov_exp_ind_mark,gov_exp_col,gov_exp_col_mark,imports,imports_mark,exports,exports_mark,imports_m,imports_mark_m,exports_m,exports_mark_m]

exports_stuff(my_stuff)


