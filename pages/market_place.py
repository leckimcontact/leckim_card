import streamlit as st
import pandas as pd
import random

# Check login
if not st.session_state.get('authenticated'):
    st.warning('Please log in first.')
    st.stop()

username = st.session_state.current_user

# Load users and cards
users_df = pd.read_csv('csv_files/users.csv', dtype={'tokens': int})
cards_df = pd.read_csv('csv_files/cards.csv')
cards_df = cards_df[cards_df['cardtype'] == 'attack']
holdings_df = pd.read_csv('csv_files/user_holdings.csv')
packs_df = pd.read_csv('csv_files/packs.csv')

user_row = users_df[users_df['username'] == username].iloc[0]
tokens = int(user_row['tokens'])

st.title(f'Welcome {username} to Leckim market place!')
st.header(f'You have {tokens} tokens.')

for pack in packs_df['packname'].to_list():
    st.subheader(pack + ' pack')
    pack_row = packs_df[packs_df['packname'] == pack].iloc[0]
    cols = st.columns(2)
    with cols[0]:
        st.image('card_images/' + pack + '.jpg', 
                  use_container_width=True)
        st.write('Token needed: ' + str(pack_row['token']))
        st.write('Common card probability: ' + str(pack_row['common']) + '\%')
        st.write('Uncommon card probability: ' + str(pack_row['uncommon']) + '\%')
        st.write('Rare card probability: ' + str(pack_row['rare']) + '\%')
        st.write('Epic card probability: ' + str(pack_row['epic']) + '\%')
        st.write('Legendary card probability: ' + str(pack_row['legendary']) + '\%')
        st.write('Chrome card probability: ' + str(pack_row['chroma']) + '\%')
    with cols[1]:
        st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
        if st.button('Buy ' + pack + ' pack card'):
            if tokens < pack_row['token']:
                st.error('Your tokens are not enough to buy this pack!')
            else:
                random_number = random.randint(1, 1000)
                if random_number >= (pack_row['legendary'] + pack_row['epic'] +\
                                    pack_row['rare'] + pack_row['uncommon'] + pack_row['common']) * 10:
                    card_rank = 'chroma'
                elif  random_number >=  (pack_row['epic'] +\
                                    pack_row['rare'] + pack_row['uncommon'] + pack_row['common']) * 10:
                    card_rank = 'legendary'
                elif  random_number >= (pack_row['rare'] + pack_row['uncommon'] + pack_row['common']) * 10:
                    card_rank = 'epic'
                elif  random_number >= (pack_row['uncommon'] + pack_row['common']) * 10:
                    card_rank = 'rare'
                elif  random_number >= pack_row['common'] * 10:
                    card_rank = 'uncommon'
                else:
                    card_rank = 'common'
                cards_rank_df = cards_df[(cards_df['rank'] == card_rank) & (cards_df['pack'] == pack)]
                random_number = random.randint(0, cards_rank_df.shape[0] - 1)
                card_got = cards_rank_df['cardname'].iloc[random_number]

                holdings_df = pd.concat([holdings_df, pd.DataFrame(data={'username': [username], 'cardname':[card_got]})])
                holdings_df.to_csv('csv_files/user_holdings.csv', index=False)
                idx = users_df.index[users_df['username'] == username].tolist()[0]
                users_df.at[idx, 'tokens'] -= pack_row['token']
                users_df.to_csv('csv_files/users.csv', index=False)

                st.write('Congratulation!')
                st.write('You got ' + card_got)
                st.write('Your tokens have been deducted by ' + str(pack_row['token']))

                card_got_cols = st.columns(2)
                with card_got_cols[0]:
                    st.image('card_images/' + card_got + '.jpg', use_container_width=True)
                
        
with st.sidebar:
    st.subheader('Contact: leckimcards@gmail.com')
