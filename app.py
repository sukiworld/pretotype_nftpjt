#%%
import streamlit as st
from utils.utils import read_json, download_df, plot_candle
from utils.utils_fdr import get_comp_info, get_stock_data
import pandas as pd
import json 
import requests
import numpy as np
#%%

menu_items = {
    'Get help' : 'https://github.com/sukiworld/pretotype_nftpjt',
    'Report a bug' : 'https://github.com/sukiworld/pretotype_nftpjt/issues',
    'About' : '''
    ## opensea nft project
    Download stock price data in US, South Korean stock market
    '''
}

st.title('NFT Projects Stats')

@st.cache
def load_data(nrows):
    aa = pd.read_csv('test.csv')
    collection_list = aa["Collection"].values
    collection_list = collection_list[:nrows] #item holder sort, sales volumne >= 500

    final_df = pd.DataFrame()
    for i in collection_list:
        url = "https://api.opensea.io/api/v1/collection/"+i+"/stats"
        r = requests.get(url) 
        j = json.loads(r.text)
        df =  pd.json_normalize(j)
        print(df)
        final_df = final_df.append(df)

    final_df["collection"] = collection_list
    return final_df

data_load_state = st.text('Loading data...')
data = load_data(10)
data_load_state.text("Done! (using st.cache)")

st.dataframe(data)

# if st.checkbox('Show raw data'):
#     st.subheader('Raw data')
#     st.write(data)

# st.subheader('Number of pickups by hour')
# hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
# st.bar_chart(hist_values)

# hour_to_filter = st.slider('hour', 0, 23, 17)
# filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

# st.subheader('Map of all pickups at %s:00' % hour_to_filter)
# st.map(filtered_data)

#%%
# @st.cache(suppress_st_warning=True, show_spinner=False)
# def load_comp_list():
#     stock_const = read_json('resource/stock_list.json')
#     return stock_const


# def get_target_comp_info(comp_info_all: dict):
#     # split view into 2 columns
#     col1, col2 = st.columns([3, 3])

#     # first col for selecting target country
#     country = col1.radio("Select country", comp_info_all.keys())

#     # second col for selecting target stock market
#     market = col2.radio("Select market", comp_info_all[country].keys())

#     # select company name from dropdown select box
#     company = st.selectbox('Select company', comp_info_all[country][market].keys())
#     comp_info = comp_info_all[country][market][company]

#     return comp_info



# def main():
#     st.title("NFT Collections Stats")
#     # stock_list = load_comp_list()

#     # comp_info = get_target_comp_info(stock_list)
#     # num_month = st.slider('Select months', 1, 36, step=3)
    
#     try:
#         # data = get_stock_data(comp_info, days = num_month*30)
#         data = final_df.copy()

#     except ValueError:
#         # st.warning("Company '{}' information currently not avaliable".format(comp_info['Symbol']))        
    
#     else:
        
#         # st.markdown("**Stock data ({} months) : {} ({})**".format(num_month, comp_info['Name'], comp_info['Symbol']))
#         # plot_candle(data)
#         # filename = 'stockprice_{}_{}_{}m'.format(comp_info['Symbol'], comp_info['Name'], num_month)
#         # st.dataframe(data)
#         # download_df(data, filename)


# if __name__ == "__main__":
#     st.set_page_config(menu_items=menu_items)
#     main()