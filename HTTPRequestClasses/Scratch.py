from fuzzywuzzy import fuzz, process

x = {'name' : 'Robby B!', 'DOB' : '1/1/2018'}
y = {'name' : 'Bobby B!', 'DOB' : '1/02/2018'}

def WRatioComparison(dict1, dict2):
    for key in dict1:
        print(key, fuzz.token_set_ratio(dict1[key], dict2[key])*1.2)

WRatioComparison(x,y)