import pandas as pd
import datetime as dt
from matplotlib import pyplot as plt
import seaborn as sns

CVD = pd.read_csv('data/Data_ WHO_Coronavirus.csv')
print(CVD.head())

print(CVD.isnull().sum())
CVD=CVD.dropna()


CVD.drop(['OBJECTID', 'Date_epicrv', 'NewCase', 'TotalCase', 'NewDeath'], axis=1, inplace=True)

print(CVD.dtypes)


CVD['Date'] = [dt.datetime.strptime(x,'%d/%m/%y') for x in CVD['Date']] 
print(CVD.dtypes)




CVD.columns = ['Date_epicrv', 'COUNTRY_NAME', 'TotalDeath', 'TotalCase']


CVD = pd.DataFrame(CVD.groupby(['COUNTRY_NAME', 'Date_epicrv'])['Total Case', 'TotalDeath'].sum()).reset_index()

CVD = CVD.sort_values(by = ['COUNTRY_NAME','Date_epicrv'], ascending=False)
print(CVD)



def plot_bar(feature, value, title, df, size):
    f, ax = plt.subplots(1,1, figsize=(4*size,4))
    df = df.sort_values([value], ascending=False).reset_index(drop=True)
    g = sns.barplot(df[feature][0:10], df[value][0:10], palette='Set3')
    g.set_title("Number of {} - highest 10 values".format(title))

    plt.show()    

filtered_CVD = CVD.drop_duplicates(subset = ['COUNTRY_NAME'], keep='first')
plot_bar('COUNTRY_NAME', 'TotalCase', 'Total cases in the World', filtered_CVD, size=4)
plot_bar('COUNTRY_NAME', 'TotalDeath', 'Total deaths in the World', filtered_CVD, size=4)


def plot_world_aggregate(df, title='Aggregate plot', size=1):
    f, ax = plt.subplots(1,1, figsize=(4*size,2*size))
    g = sns.lineplot(x="Date_epicrv", y='TotalCase', data=df, color='blue', label='TotalCase')
    g = sns.lineplot(x="Date_epicrv", y='TotalDeath', data=df, color='red', label='TotalDeath')
    plt.xlabel('Date_epicrv')
    plt.ylabel(f'Total {title} cases')
    plt.xticks(rotation=90)
    plt.title(f'Total {title} cases')
    ax.grid(color='black', linestyle='dotted', linewidth=0.75)
    plt.show()  


CVD_aggregate = CVD.groupby(['Date_epicrv']).sum().reset_index()
print(CVD_aggregate)

plot_world_aggregate(CVD_aggregate, 'Whole World', size=4)


def plot_aggregate_states(df, states, case_type='TotalCase', size=3, is_log=False):
    f, ax = plt.subplots(1,1, figsize=(4*size, 3*size))
    for state in states:
        df_ = df[(df['COUNTRY_NAME']==state) & (df['Date_epicrv'] > '2020-03-01')] 
        g = sns.lineplot(x="Date_epicrv", y=case_type, data=df_,  label=state)  
        ax.text(max(df_['Date_epicrv']), max(df_[case_type]), str(state))
    plt.xlabel('Date_epicrv')
    plt.ylabel(f' {case_type} ')
    plt.title(f' {case_type} ')
    plt.xticks(rotation=90)
    if(is_log):
        ax.set(yscale="log")
    ax.grid(color='black', linestyle='dotted', linewidth=0.75)
    plt.show()  

CVD_state_aggregate = CVD.groupby(['COUNTRY_NAME', 'Date_epicrv']).sum().reset_index()


countries=["Afghanistan","Albania","Algeria","Andorra","Angola","Anguilla","Antigua and Barbuda,","Argentina","Armenia","Aruba","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh",
           "Barbados","Belarus","Belgium","Belize","Benin","Bermuda","Bhutan","Bolivia (Plurinational State of)", "Bosnia and Herzegovina", "Botswana", "Brazil", "British Virgin Islands", "Brunei Darussalam",
           "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Cayman Islands", "Central African Republic", "Chad", "Chile", "China","Colombia", "Congo", "Costa Rica",
           "CÃ´te dâ€™Ivoire", "Croatia", "Cuba", "CuraÃ§ao", "Cyprus", "Czechia", "Democratic Republic of the Congo", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt", 
           "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Falkland Islands (Malvinas)", "Faroe Islands", "Fiji", "Finland", "France", 
            "French Guiana", "French Polynesia", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Gibraltar", "Greece", "Greenland", "Grenada", "Guadeloupe", "Guam", "Guatemala", "Guernsey", "Guinea",
            "Guinea-Bissau", "Guyana", "Haiti", "Holy See", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "International conveyance (Diamond Princess)", "Iran (Islamic Republic of)", "Iraq",
            "Ireland", "Isle of Man", "Israel", "Italy", "Jamaica", "Japan", "Jersey", "Jordan", "Kazakhstan", "Kenya", "Kosovo[1]", "Kuwait", "Kyrgyzstan", "Lao People's Democratic Republic", "Latvia",
            "Lebanon", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Martinique", "Mauritania", "Mauritius", "Mayotte",
            "Mexico", "Monaco", "Mongolia", "Montenegro", "Montserrat", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nepal", "Netherlands", "New Caledonia", "New Zealand", "Nicaragua", "Niger", "Nigeria",
            "North Macedonia", "Northern Mariana Islands (Commonwealth of the)", "Norway", "occupied Palestinian territory", "Oman", "Pakistan", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines",
            "Poland", "Portugal", "Puerto Rico", "Qatar", "Republic of Korea", "Republic of Moldova", "RÃ©union", "Romania", "Russian Federation", "Rwanda", "Saint BarthÃ©lemy", "Saint Kitts and Nevis", "Saint Lucia",
            "Saint Martin", "Saint Pierre and Miquelon", "Saint Vincent and the Grenadines", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone",
            "Singapore", "Sint Maarten", "Slovakia", "Slovenia", "Somalia", "South Africa", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syrian Arab Republic", "Thailand", 
            "The United Kingdom", "Timor-Leste", "Togo", "Trinidad and Tobago", "Tunisia", "Turkey", "Turks and Caicos Islands", "Uganda", "Ukraine", "United Arab Emirates", "United Republic of Tanzania", "United States of America"
            "United States Virgin Islands", "Uruguay", "Uzbekistan", "Venezuela (Bolivarian Republic of)", "Viet Nam", "Yemen", "Zambia", "Zimbabwe"]

plot_aggregate_states(CVD_state_aggregate, countries, case_type = 'Total Cases', size=4)    

plot_aggregate_states(CVD_state_aggregate, countries, case_type = 'Total Deaths', size=4)



def plot_mortality(df, title='Deaths', size=1):
    f, ax = plt.subplots(1,1, figsize=(4*size,2*size))
    g = sns.lineplot(x="Date", y='Mortality (Deaths/Cases)', data=df, color='blue', label='Mortality (Deaths / Total Cases)')
    plt.xlabel('Date_epicrv')
    plt.ylabel(f'Mortality {title} [%]')
    plt.xticks(rotation=90)
    plt.title(f'Mortality percent {title}\nCalculated as Deaths/Confirmed cases')
    ax.grid(color='black', linestyle='dashed', linewidth=1)
    plt.show()  

CVD_aggregate['Mortality (Deaths/Cases)'] = CVD_aggregate['Total Deaths'] / CVD_aggregate['Total Cases'] * 100
plot_mortality(CVD_aggregate, title = ' - Whole World', size = 3)












