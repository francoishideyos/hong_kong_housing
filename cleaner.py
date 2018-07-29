import pandas as pd

df 		  		   = pd.read_csv('assets/data/urls_to_scrape_07-28-2018.csv',index_col = 'ID')
df_master_location = pd.read_csv('assets/master_location.csv',index_col = 'ID')
df_master_pricing  = pd.read_csv('assets/master_pricing.csv',index_col = 'ID')

# Replace unwanted characters
# https://stackoverflow.com/questions/28986489/python-pandas-how-to-replace-a-characters-in-a-column-of-a-dataframe
df['Price']		   					    = df['Price'].str.replace('[^0123456789.]','')
df['Price per feet(built-up)']  	    = df['Price per feet(built-up)'].str.replace('[^0123456789.]','')
df['Price per feet(salesable area)']    = df['Price per feet(salesable area)'].str.replace('[^0123456789.]','')
df['Gross area(sq feet)'] 				= df['Gross area(sq feet)'].str.replace('[^0123456789.]','')
df['Net floor area(sq feet)']           = df['Net floor area(sq feet)'].str.replace('[^0123456789.]','')


df_location = df[['Region','Region Link', 'Estate', 'Estate Link','Block and unit number', 'Floor', 'Room', 'Gross area(sq feet)','Net floor area(sq feet)','Property age(year)','Address',]]
df_master_location = pd.concat([df_master_location,df_location]).reset_index().drop_duplicates(subset='ID', keep='last').set_index('ID')
df_master_location.to_csv('assets/master_location.csv')


df_pricing = df[['Status', 'Price','Price per feet(built-up)', 'Price per feet(salesable area)','Views #', 'Bookmarked #', 'Ads or renew date','Modified date', 'User last login', 'Expire date','Scrape Date']]
df_master_pricing = pd.concat([df_master_pricing, df_pricing]).reset_index().drop_duplicates(subset=['ID','Status', 'Price','Price per feet(built-up)', 'Price per feet(salesable area)','Views #', 'Bookmarked #', 'Ads or renew date','Modified date', 'User last login', 'Expire date','Scrape Date'], keep='last').set_index('ID')
df_master_pricing.to_csv('assets/master_pricing.csv')

