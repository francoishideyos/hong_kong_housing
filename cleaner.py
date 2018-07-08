import pandas as pd

df 		  = pd.read_csv('assets/data/urls_to_scrape_07-08-2018.csv',index_col = 'ID')
# df_master = pd.read_csv('assets/data/master.csv',index_col = 'ID')

# Replace unwanted characters
# https://stackoverflow.com/questions/28986489/python-pandas-how-to-replace-a-characters-in-a-column-of-a-dataframe
df['Price']		   					    = df['Price'].str.replace('[^0123456789.]','')
df['Price per feet(built-up)']  	    = df['Price per feet(built-up)'].str.replace('[^0123456789.]','')
df['Price per feet(salesable area)']    = df['Price per feet(salesable area)'].str.replace('[^0123456789.]','')
df['Gross area(sq feet)'] 				= df['Gross area(sq feet)'].str.replace('[^0123456789.]','')
df['Net floor area(sq feet)']           = df['Net floor area(sq feet)'].str.replace('[^0123456789.]','')

# print(pd.merge(df_master, df, left_index = True,right_index=True, how='outer').head())

df.to_csv('assets/data/urls_to_scrape_07-08-2018.csv')
