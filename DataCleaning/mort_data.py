import pandas as pd

data = pd.read_csv('mort_filtered.csv', encoding='unicode_escape')

# clean up padding in LC50/LD50
data.loc[data['Endpoint Description'].str.contains('LC50'), 'Endpoint Description'] = 'LC50'
data.loc[data['Endpoint Description'].str.contains('LD50'), 'Endpoint Description'] = 'LD50'


# handle unusual values in the data
#61-64 Zenaida macroura are ranges, use the average of the range instead
data.iloc[61, 4] = '16 mg/kg'
data.iloc[62, 4] = '45 mg/kg'
data.iloc[63, 4] = '225 mg/kg'
data.iloc[64, 4] = '475 mg/kg'

#12 Thamnophis gigas is missing a space between the value + unit, also unit uses period instead of slash
data.iloc[12, 4] = '1867 mg/kg'

# so, for each row:
# get the string for endpoint value
# remove any padding, set it to lowercase
# split it into two tokens: numerical value + unit
# then analyze the unit
    # ppm : ppm
    # <>/<>: handle the unit properly
# return the value as mg/kg
def convert_unit(value, target='mg/kg'):

    UNITS = {}
    UNITS['ug'] = 1e-6
    UNITS['µg'] = 1e-6
    UNITS['mg'] = 1e-3
    UNITS['g'] = 1
    UNITS['kg'] = 1e3

    UNITS['l'] = 1e3
    

    assert type(value) == str

    # strip leading/trailing whitespace, lowercase string
    value = value.strip().lower()

    # split string into two tokens
    value, unit = value.split()
    #print(value, unit)

    value = float(value)
        
    if unit == 'ppm':
        # ppm -> 1 mg/kg
        value = value * UNITS['mg'] / UNITS['kg']

    else:
        top, bot = unit.split(sep='/')
        #print(top, bot)

        top = UNITS[top]
        bot = UNITS[bot]
        
        value = value * top / bot

    #target_top, target_bot = target.split(sep='/')
    #target_top = UNITS[top]
    #target_bot = UNITS[bot]

    # default units
    value /= UNITS['mg']
    value *= UNITS['kg']

    return f"{value} mg/kg"

data['Endpoint Value'] = data['Endpoint Value'].apply(convert_unit)
