import streamlit as st
import pandas as pd
import random
from datetime import date

# Load users and cards
users_df = pd.read_csv('csv_files/users.csv', dtype={'tokens': int})
cards_df = pd.read_csv('csv_files/cards.csv')
cards_df['power'] = (cards_df['strength'] + cards_df['charisma'] + cards_df['intelligence']) / 3 
holdings_df = pd.read_csv('csv_files/user_holdings.csv')

# Check login
if not st.session_state.get('authenticated'):
    st.warning('Please log in first.')
    st.stop()

username = st.session_state.current_user
user_row = users_df[users_df['username'] == username].iloc[0]
tokens = int(user_row['tokens'])
last_login = user_row['last_login']

st.title(f'Welcome, {username}')

with st.sidebar:
    st.subheader('Contact: leckimcards@gmail.com')
    
# Daily reward
today = date.today().isoformat()
if last_login != today:
    idx = users_df.index[users_df['username'] == username].tolist()[0]
    users_df.at[idx, 'tokens'] += 10
    users_df.at[idx, 'login_day_count'] += 1
    users_df.at[idx, 'last_login'] = today
    users_df.to_csv('csv_files/users.csv', index=False)
    st.success('Daily reward: +10 tokens!')
    tokens += 10

st.header(f'{tokens} tokens')


user_holdings_df = pd.merge(holdings_df[holdings_df['username'] == username],
                            cards_df,
                            on='cardname',
                            how='left')

card_count = user_holdings_df.shape[0]
pack_count = user_holdings_df['pack'].nunique()

card_in_a_row = 5
for pack in user_holdings_df['pack'].unique():
    st.subheader(pack)
    user_pack_df = user_holdings_df[user_holdings_df['pack'] == pack]
    user_pack_df = user_pack_df.sort_values(by=['power', 'cardname'], ascending=False).reset_index(drop=True)
    user_pack_summary = user_pack_df.groupby('cardname')['pack'].count().reset_index(drop=False)
    user_pack_summary = user_pack_summary.rename(columns={'pack': 'card_count'})
    user_pack_summary['image'] = 'card_images/' + user_pack_summary['cardname'] + '.jpg'
    images = user_pack_summary['image'].to_list()
    counts = user_pack_summary['card_count'].to_list()
    for i in range(0, len(images), card_in_a_row):
        cols = st.columns(card_in_a_row)
        for j in range(card_in_a_row):
            if i + j < len(images):
                with cols[j]:
                    st.image(images[i + j], 
                             caption='X ' + str(counts[i+j]),
                             use_container_width=True)

