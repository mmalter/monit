import dlstats
import pandas
import matplotlib.pyplot as plt
from matplotlib.dates import *
import datetime

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
private_consumption = household_consumption + non_profit_consumption
private_consumption_mark = household_consumption_mark + non_profit_consumption_mark
imports = dlstats.INSEE('001615777','Imports')
imports_mark = dlstats.INSEE('001615776','Imports')
exports = dlstats.INSEE('001615785','Exports')
exports_mark = dlstats.INSEE('001615784','Exports')
imports_m = dlstats.INSEE('001569472','Imports')
imports_mark_m = dlstats.INSEE('001569471','Imports')
exports_m = dlstats.INSEE('001568985','Exports')
exports_mark_m = dlstats.INSEE('001568985','Exports')
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

tax_minus_subsidies_mark = gdp_mark - agriculture_gva_mark  - industry_man_gva_mark - construction_gva_mark - services_gva_mark
tax_minus_subsidies = gdp - agriculture_gva- industry_man_gva- construction_gva- services_gva

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


gdp_components = pandas.concat([contribution_agriculture_gva,contribution_industry_man_gva,contribution_construction_gva,contribution_services_gva,contribution_tax_minus_subsidies,(gdp.pct_change()*100)],axis=1)
gdp_components.columns = ['Agriculture','Industry','Construction','Services','Tax minus subsidies','GDP']

xticks = pandas.date_range(start=gdp_components.index[-64], end=gdp_components.index[-1], freq='Q-DEC')
fig = plt.figure(1)
ax = fig.add_subplot(211)
gdpplot = (gdp.truncate(before='01/01/2006').pct_change()*100).plot(label='GDP', ax=ax)
plt.legend()
plt.xlabel('GDP growth')
ax2 = fig.add_subplot(212)
gdp_components[['Agriculture','Industry','Construction','Services','Tax minus subsidies']].truncate(before=gdp_components.index[-64]).plot(kind='bar', stacked=True, label=gdp_components.columns, ax=ax2, xticks=xticks.to_period())

plt.legend()
plt.xlabel('Contributions to GDP')
#ax.xaxis.set_major_locator(AutoDateLocator())
#ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
#ax.xaxis.set_major_formatter(AutoDateFormatter())
#plt.tight_layout()
plt.show()
