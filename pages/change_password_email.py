import streamlit as st
import pandas as pd

# Check login
if not st.session_state.get('authenticated'):
    st.warning('Please log in first.')
    st.stop()

with st.sidebar:
    st.subheader('Contact: leckimcards@gmail.com')

username = st.session_state.current_user
users_df = pd.read_csv('csv_files/users.csv')

st.title('Change user password or email')

passwd1 = st.text_input('Password 1st time input', type='password')
passwd2 = st.text_input('Password 2nd time input', type='password')
if st.button('Change password'):
    if passwd1 == passwd2:
        st.success('Password for ' + username + ' has been changed.')
        idx = users_df.index[users_df['username'] == username].tolist()[0]
        users_df.at[idx, 'password'] = passwd1
        users_df.to_csv('csv_files/users.csv', index=False)
    else:
        st.error('The two passwords dont match')

st.write(' ')
st.write(' ')
st.write(' ')
st.write(' ')

user_email = st.text_input('Email address used to recover password')
if st.button('Change email'):
    if user_email != '' and '@' in user_email:
        st.success('Email for ' + username + ' has been changed.')
        idx = users_df.index[users_df['email'] == username].tolist()[0]
        users_df.at[idx, 'email'] = user_email
        users_df.to_csv('csv_files/users.csv', index=False)
    else:
        st.error('Please provide valid email, which is needed to retrieve password.')