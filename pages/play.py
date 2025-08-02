import streamlit as st
import pandas as pd
import random

# Check login
if not st.session_state.get('authenticated'):
    st.warning('Please log in first.')
    st.stop()
username = st.session_state.current_user

st.title('Play')
users_df = pd.read_csv('csv_files/users.csv', dtype={'tokens': int})
with st.sidebar:
    st.subheader('Contact: leckimcards@gmail.com')

st.subheader('Play instruction')
st.write('If you still don\' know how to play, please go to below instruction page.')
with st.popover('Play instruction'):
    st.write('1. You need to select 5 attack cards from your holdings.')
    st.write('2. Bot will randomly select 5 attack cards with the same rank of your selected cards.')
    st.write('3. One game has multiple rounds. In each round, one card is randomly selected from your 5 cards for battling.')
    st.write('4. Each attack card has 3 attributes, namely strength, charisma and intelligence. You may choose one of them to battle with bot.')
    st.write('5. After you choose the attribute, you will be able to see bot\' card and the battle result.')
    st.write('6. If you lose the round, your health points will be deducted by the attribute value difference.')
    st.write('7. If you win the round, bot health points will be deducted by the attribute value difference.')
    st.write('8. The game will be finished once you or bot health points are less 0.')
    st.write('9. If you win the game, you will be awarded 10 tokens')

st.subheader('Select your cards to battle')
st.write('Else, you can proceed to select your cards for battle.')

holdings_df = pd.read_csv('csv_files/user_holdings.csv')
cards_df = pd.read_csv('csv_files/cards.csv')
cards_df = cards_df[cards_df['cardtype'] == 'attack']
cards_df['power'] = (cards_df['strength'] + cards_df['charisma'] + cards_df['intelligence']) / 3 
username = st.session_state.current_user

user_holdings_df = pd.merge(holdings_df[holdings_df['username'] == username],
                            cards_df,
                            on='cardname',
                            how='left')


user_holdings_df = user_holdings_df.sort_values(by=['power', 'cardname'], ascending=False).reset_index(drop=True)

attack_card_list = user_holdings_df['cardname'][user_holdings_df['cardtype'] == 'attack'].drop_duplicates().to_list()
selected_attack_cards = st.multiselect('Pick 5 attack cards', attack_card_list, max_selections=5)
user_cards_df = cards_df[cards_df['cardname'].isin(selected_attack_cards)].reset_index(drop=True)


def random_select_cards(num, df):
    cards = []

    random_number_0 = -1
    if num <= df.shape[0]:
        for i in range(num):
            random_number = random.randint(0, df.shape[0] - 1)
            while random_number == random_number_0:
                random_number = random.randint(0, df.shape[0] - 1)
            cards.append(df['cardname'].iloc[random_number])
            random_number_0 = random_number
    else: # allow duplication
        for i in range(num):
            random_number = random.randint(0, df.shape[0] - 1)
            cards.append(df['cardname'].iloc[random_number])

    return cards

bot_cards_df0 = pd.DataFrame()
if len(selected_attack_cards) == 5:
    st.write('Here are your selected attack cards.')
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image('card_images/' + selected_attack_cards[i] + '.jpg', 
                                    caption=selected_attack_cards[i],
                                    use_container_width=True)
    bot_cards_selected = []
    for rank in user_cards_df['rank'].unique():
        rank_cards_count = user_cards_df[user_cards_df['rank'] == rank].shape[0]
        rank_cards_selected = random_select_cards(rank_cards_count, cards_df[(cards_df['rank'] == rank) & (cards_df['cardtype'] == 'attack')])
        
        for j in range(len(rank_cards_selected)):
            bot_cards_selected.append(rank_cards_selected[j])
    

    for card_i in bot_cards_selected: # if the cards are too few, the bot cards selected could be duplicated
        bot_cards_df0 = pd.concat([bot_cards_df0, cards_df[cards_df['cardname'] == card_i]])

    bot_cards_df0 = bot_cards_df0.reset_index(drop=True)

    st.write('Bot also selected 5 attack cards with the same rank of yours.')

st.subheader('Start play')

if 'bot_cards_df' not in st.session_state or st.session_state.bot_cards_df.shape[0] == 0:
    st.session_state.bot_cards_df = bot_cards_df0
if 'random_list' not in st.session_state:
    st.session_state.random_list = [random.randint(0, 4) for _ in range(1000000)]
    # maximum round is 1000000

with st.popover('Play'):
    if len(selected_attack_cards) != 5:
        st.error('The number of attack cards needs to be 5.')
    else:
        user_health_points = 20
        bot_health_points = 20
        round_count = 1
        while user_health_points > 0 and bot_health_points > 0:
            play_cols = st.columns(4)
            
            with play_cols[0]:
                st.subheader('Round ' + str(round_count))
                st.write('Your health point: ' + str(user_health_points))
                st.write('Bot health point: ' + str(bot_health_points))
            with play_cols[1]:
                user_card_row = user_cards_df.iloc[st.session_state.random_list[round_count * 2 - 1]]
                st.write('Your card')
                st.image('card_images/' + user_card_row['cardname'] + '.jpg', 
                                                    use_container_width=True)
                st.write(user_card_row['cardname'])    
                st.write('Strength: ' + str(user_card_row['strength']))
                st.write('Charisma: ' + str(user_card_row['charisma']))
                st.write('Intelligence: ' + str(user_card_row['intelligence']))
                st.write('Which attribute do you choose to battle?')
                attribute = st.radio('', ['Strength', 'Charisma', 'Intelligence'],
                                                    index=None,
                                                    key=str(round_count))
                
            if attribute is None:
                st.stop()
            else:
                with play_cols[2]:      
                    bot_card_row = st.session_state.bot_cards_df.iloc[st.session_state.random_list[round_count * 2]]
                    st.write('Bot card')
                    st.image('card_images/' + bot_card_row['cardname'] + '.jpg', 
                                                        use_container_width=True) 
                    st.write(bot_card_row['cardname'])    
                    st.write('Strength: ' + str(bot_card_row['strength']))
                    st.write('Charisma: ' + str(bot_card_row['charisma']))
                    st.write('Intelligence: ' + str(bot_card_row['intelligence']))
                with play_cols[3]:
                    if user_card_row[attribute.lower()] < bot_card_row[attribute.lower()]:
                        user_health_points = user_health_points - (bot_card_row[attribute.lower()] - user_card_row[attribute.lower()])
                        st.write('Your ' + attribute.lower() + ': ' + str(user_card_row[attribute.lower()]))
                        st.write('VS')
                        st.write('Bot '+ attribute.lower() + ': ' + str(bot_card_row[attribute.lower()]))
                        st.write(' ')
                        st.write(' ')
                        deducted_points = bot_card_row[attribute.lower()] - user_card_row[attribute.lower()]
                        st.write('You lose in round ' + str(round_count) + ' and your health points will deducted ' + str(deducted_points))
                    elif user_card_row[attribute.lower()] > bot_card_row[attribute.lower()]:
                        bot_health_points = bot_health_points - (user_card_row[attribute.lower()] - bot_card_row[attribute.lower()])
                        st.write('Your ' + attribute.lower() + ': ' + str(user_card_row[attribute.lower()]))
                        st.write('VS')
                        st.write('Bot '+ attribute.lower() + ': ' + str(bot_card_row[attribute.lower()]))
                        st.write(' ')
                        st.write(' ')
                        deducted_points = user_card_row[attribute.lower()] - bot_card_row[attribute.lower()]
                        st.write('You win in round ' + str(round_count) + ' and bot health points will deducted ' + str(deducted_points))
                    else:
                        st.write('Your ' + attribute.lower() + ': ' + str(user_card_row[attribute.lower()]))
                        st.write('VS')
                        st.write('Bot '+ attribute.lower() + ': ' + str(bot_card_row[attribute.lower()]))
                        st.write(' ')
                        st.write(' ')
                        st.write('You draw in round ' + str(round_count))
            round_count += 1

        if user_health_points <= 0:
            st.subheader('You lose in this game.')
            st.write('You can exit by clicking outside the popup window.')
            
            del st.session_state.bot_cards_df
            del st.session_state.random_list
        elif bot_health_points <= 0:
            st.subheader('You win this game.')
            st.subheader('You will get 10 tokens.')
            st.write('You can exit by clicking outside the popup window.')
            idx = users_df.index[users_df['username'] == username].tolist()[0]
            users_df.at[idx, 'tokens'] += 10
            users_df.to_csv('csv_files/users.csv', index=False)
            del st.session_state.bot_cards_df
            del st.session_state.random_list



with st.popover('Restart a game'):
    st.write('Restart a game by changing the selected 5 attack cards.')
