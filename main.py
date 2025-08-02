import streamlit as st
import pandas as pd
from datetime import date

with st.sidebar:
    st.subheader('Contact: leckimcards@gmail.com')

st.title('Leckim Cards')
st.header('A strategic and fun card game')

users_df= pd.read_csv('csv_files/users.csv', dtype={'tokens': int})
holdings_df = pd.read_csv('csv_files/user_holdings.csv')
cards_df = pd.read_csv('csv_files/cards.csv')
cards_df = cards_df[cards_df['cardtype'] == 'attack']
users_df['tokens'] = users_df['tokens'].astype('Int64')

st.subheader('Top players')
top_players = users_df[['username', 'tokens']].sort_values(by='tokens', ascending=False).head(3)
top_players = top_players.rename(columns={'username': ''})
st.write(top_players.to_html(index=False), unsafe_allow_html=True)

st.subheader('Latest news')
latest_news = """
19 Jul 2025: first version completed
15 Jul 2025: add leckim contact email in sidebar and user email in sign up
14 Jul 2025: sign up page completed
14 Jul 2025: market page completed.
12 Jul 2025: Log in page completed. 
Early Jul 2025: The implementation started.
"""

st.text_area('', value=latest_news, height=150)

st.subheader('Log in')
user = st.text_input('Username')
passwd = st.text_input('Password', type='password')


if st.button('Login'):
    if users_df[users_df['username'] == user].shape[0] == 0:
        st.error('Username deosn\'t exist! Please sign up first.')
    else:
        passwd_csv = users_df['password'][users_df['username'] == user].iloc[0]
        if passwd == passwd_csv:
            st.session_state.authenticated = True
            st.session_state.current_user = user
            st.switch_page('pages/user_holdings.py')
            
        else:
            st.error('Incorrect password.')

st.write(' ')
st.write(' ')

st.subheader('Sign up')
st.write('Sign up here if you still dont\'s have an account.')
with st.popover('Sign up'):
    new_user = st.text_input('New username')
    if users_df[users_df['username'] == new_user].shape[0] > 0:
        st.error('Username already exists! If you forget your password, please contact us.')
    passwd1 = st.text_input('Password 1st time input', type='password')
    passwd2 = st.text_input('Password 2nd time input', type='password')
    user_email = st.text_input('Email address used to recover password')
    if st.button('Sign up'):
        if users_df[users_df['username'] == new_user].shape[0] == 0 and\
            passwd1 == passwd2 and\
            new_user != '' and passwd1 != '' and\
                user_email != '' and '@' in user_email:
            st.success('Welcome ' + new_user + '!')
            st.success('Please login using your new account and password.')
            free_cards_list = cards_df['cardname'][cards_df['pack'] == 'free'].to_list()
            free_cards_count = len(free_cards_list)

            st.success('You also got ' + str(free_cards_count) + ' free cards which can be found in user holdings.')
            users_df= pd.concat([users_df,
                                pd.DataFrame(data={'username': [new_user],
                                                    'password': [passwd1],
                                                    'tokens': [10],
                                                    'last_login': [date.today().isoformat()],
                                                    'first_login': [date.today().isoformat()],
                                                    'login_day_count': [1],
                                                    'email': user_email})])
            users_df.to_csv('csv_files/users.csv', index=False)
            holdings_df = pd.concat([holdings_df, pd.DataFrame(data={'username': [new_user] * free_cards_count, 
                                        'cardname': free_cards_list})])
            holdings_df.to_csv('csv_files/user_holdings.csv', index=False)
        elif passwd1 != passwd2:
            st.error('The two passwords dont match.')
        elif new_user == '':
            st.error('User name cannot be empty.')
        elif passwd1 == '':
            st.error('Password cannot be empty.')
        elif user_email == '':
            st.error('Email cannot be empty, which is needed to retrieve password.')
        elif '@' not in user_email:
            st.error('Please provide valid email, which is needed to retrieve password.')

# git --version
# git init
# git 