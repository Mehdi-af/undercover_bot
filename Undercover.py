##############################################################################
## README                                                                   ##
##                                                                          ##
## This program requires:                                                   ##
## Selenium                                                                 ##
## NLTK                                                                     ##
## Telepot                                                                  ##
## Requests                                                                 ##
## lxml                                                                     ##
## BeautifulSoup                                                            ##
## Geckodriver                                                              ##
##                                                                          ##
##############################################################################

import telepot, random, sys, time
from pprint import pprint
from statistics import mode
sys.path.append('SYNONYM.PY file PATH') #Insert synonym.py path here so that it can be imported
import synonym
from telepot.namedtuple import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton

#Variables
count           = 0
step            = 0
players         = list()
players_name    = list()
voters          = list()
describer       = list()
words           = list()
vote            = list()
vote_text_list  = list()
undercover_name = list()
voting_text     = ''
voting_turn     = ''
desc_turn       = 0
desc_list       = list()
a_var           = 0
undercover_name_fix = list()



Help_Text = "Hello, this is a bot to play undercover game. A game which can be played by at least 4 people and at most 16 people.\n\n\
Your roles will be divided into civillians and undercovers. There are more civillians than undercovers in a game.\
The civillians will each get the same word while the undercovers will also get the same word with slight difference to the word for civillians.\n\n\
At the beginning of each round, you will descibe your word with a word or phrase in turn. Then, everyone will vote a person to be killed.\n\n\
The objective of the civillians is to kill all the undercovers while the objective of the undercovers is to survive until they outnumber the civillians.\n\nHave fun playing!\
\n\nImportant: To use this bot, you need to chat with bot privately at least once."


    
def on_chat_message(msg):
    pprint(msg)
    content_type, chat_type, chat_id = telepot.glance(msg)
    command = msg['text']
    player_id = msg['from']['id']
    name = msg['from']['first_name']
    global count, step, undercover_n, players, players_name, voters, describer_id, words, inline_polling, undercover_name, undercover_name_fix
    global chat_id, desc_turn, desc_list, cid, mid, diff, words, a, b, vote, vote_text_list, voting_text, voting_turn, a_var



    #Inline Keyboard
    inline_polling  = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text= namename, callback_data = namename + "_Voted")] for namename in players_name
                ])

    if player_id == chat_id:
        if command == "/help":
            bot.sendMessage(chat_id, Help_Text)
            bot.sendMessage(chat_id, "Add this bot to your group to start playing.")

    #For command /help
    if command == "/help@Undercover_bot":
        bot.sendMessage(chat_id, Help_Text)

    if step > 0 and command == "/join@Undercover_bot":
        bot.sendMessage(chat_id, name + ", you no longer can join. The game has already started.")


    #For command /quit    
    if command == "/quit@Undercover_bot":
        if player_id in players:
            players.remove(player_id)
            count = count-1
            players_name.remove(name)
            bot.sendMessage(chat_id, name + ", just left the game.")
        else:
            bot.sendMessage(chat_id, name + ", you're not in the game.")


    #Step 0 means nothing happened yet. In this section, players will join and start the game.
    if step == 0:
        if command == "/join@Undercover_bot":
            if player_id not in players and count < 16:
                players.append(player_id)
                players_name.append(name)
                count = count + 1
                if count < 4:
                    bot.sendMessage(chat_id, "Hi " + name + ", you have joined the game. Waiting for at least " + str(4-count) + " more players \n\nMake sure you had clicked start on the private chat")
                else:
                    bot.sendMessage(chat_id, "Hi " + name + ", you have joined the game. There's already enough number of players to play. To start the game, send /start@Undercover_bot")
            
            elif player_id in players:
                bot.sendMessage(chat_id, name + " is already in the game")

            elif count == 16:
                bot.sendMessage(chat_id, "Sorry " + name + ", the game is already full")
        if command == "/poll@Undercover_bot":
            bot.sendMessage(chat_id, name + ", Start a game first.")

        if command == "/start@Undercover_bot":
            if count < 4:
                bot.sendMessage(chat_id, "Not enough players")
            else:
                bot.sendMessage(chat_id, "Game will be started")
                bot.sendMessage(chat_id, "How many undercovers?")
                step = 1
                return
                
                

    #Step 1 determining number of undercovers
    if step == 1:
        step = 1.5
        try:
            undercover_n = int(command)
            assert undercover_n > 0
            assert undercover_n < len(players)/2
            bot.sendMessage(chat_id, "Which source for the words do you want? \nMode options: \n1. Random \n2. Very random \n3. High-level \n4. Really similar \n5. Normal \n\n(Enter number between 1 - 5)")
            step = 2
            return
        except:
            bot.sendMessage(chat_id, "Wrong input. Try Again.")
            step = 1
            
    #Step 2 determining words source
    if step == 2:
        step = 2.5
        try:
            diff = int(command)
            print(diff)
            assert diff == 1 or diff == 2 or diff == 3 or diff == 4 or diff == 5
            print(diff)
            [a,b] = synonym.synword(diff)
            print([a,b])
            step = 3
        except:
            bot.sendMessage(chat_id, "wrong input, try again.")
            step = 2

    #Step 3 is at the start of the round, when bot sent essential info.
    if step == 3:
        step = 3.5
        intro_text = "Players names are : "
        for i in range(0,len(players)):
            intro_text = intro_text + "\n" + str(i+1) + ". " + players_name[i]
        bot.sendMessage(chat_id, intro_text)

        words = [a]*(count-undercover_n)+[b]*(undercover_n)          
        random.shuffle(words)
        
        for i in range(0,len(players)):
            bot.sendMessage(players[i], 'Your word is ' + words[i])
        for tempvar in range(0,len(words)):
            if words[tempvar] == b:
                undercover_name.append(players_name[tempvar])
                
        print(undercover_name)
        undercover_name_fix = undercover_name
        bot.sendMessage(chat_id, "Description turn.")
        step = 4

    #Step 4 for the describing
    if step == 4:
        try:
            assert desc_turn < len(players)
            assert a_var == 0
            bot.sendMessage(chat_id, "It's " + players_name[0] + "'s turn to describe (Type @Undercover_bot then your description).")
            a_var+=1

        except:
            None
        finally:
            if desc_turn == len(players):
                bot.sendMessage(chat_id, "To start the polling, send /poll@Undercover_bot")
                step = 5
                return
            
    #Step 5 for polling
    if step == 5:
        if command == "/poll@Undercover_bot":
            vote = [0]*len(players)
            keyboard = inline_polling
            vote_text_list = [0]*len(players)
            for namename in players_name:
                vote_text_list[players_name.index(namename)] = namename + ' ' + str(vote[players_name.index(namename)]) + ' voters\n'
            voting_text = ''
            for a in range(len(players)):
                voting_text = voting_text + str(vote_text_list[a])
            polling_keyboard = bot.sendMessage (chat_id, voting_text , reply_markup = keyboard)
            
            cid, mid = telepot.message_identifier(polling_keyboard)
        if len(voters) == len(players):
            if command.lower() == "continue":
                step = 6
    

    if step == 6:
        print(vote)
        print(players_name)
        kicked = players_name[vote.index(max(vote))]
        print(kicked)
        compare_max = max(vote)
        vote.remove(max(vote))
        if compare_max in vote:
            step = 5
            voters = list()
            bot.sendMessage(chat_id, "It's a draw! Vote Again.\nSend /poll@Undercover_bot again.")
            return
        bot.sendMessage(chat_id, "Voting has ended. " + kicked + " died")
        
        if kicked not in undercover_name:
            print(msg)
            bot.sendMessage(chat_id, "You killed the wrong guy....")
            players.remove(players[players_name.index(kicked)])
            players_name.remove(kicked)
            count = count - 1
            step = 7
        else:
            bot.sendMessage(chat_id,"Undercover Killed!!!")
            players.remove(players[players_name.index(kicked)])
            players_name.remove(kicked)
            undercover_name.remove(kicked)
            count = count - 1
            undercover_n = undercover_n - 1
            bot.sendMessage(chat_id, "Undercover Left = " + str(undercover_n))
            step = 7

    if step == 7:
        if undercover_n == 0:
            bot.sendMessage(chat_id, "Civilian Wins!\n\n\
Game has finished. Join a new game.")
            count           = 0
            step            = 0
            players         = list()
            players_name    = list()
            voters          = list()
            describer       = list()
            words           = list()
            vote            = list()
            vote_text_list  = list()
            undercover_name = list()
            voting_text     = ''
            voting_turn     = ''
            desc_turn       = 0
            desc_list       = list()
        elif undercover_n == len(players)/2:
            bot.sendMessage(chat_id, "Undercover Wins!\n" + "Undercover : " + ", ".join(undercover_name_fix) + "\n\n\
Game has finished. Join a new game.")
            count           = 0
            step            = 0
            players         = list()
            players_name    = list()
            voters          = list()
            describer       = list()
            words           = list()
            vote            = list()
            vote_text_list  = list()
            undercover_name = list()
            voting_text     = ''
            voting_turn     = ''
            desc_turn       = 0
            desc_list       = list()
        else:
            bot.sendMessage(chat_id, "to poll again, send poll. To describe again, send desc")
            if command == "poll":
                step = 5
                voters          = list()
                describer       = list()
                vote            = list()
                vote_text_list  = list()
                voting_text     = ''
                voting_turn     = ''
                desc_turn       = 0
                desc_list       = list()
                
            if command == "desc":
                step = 4
                voters          = list()
                describer       = list()
                vote            = list()
                vote_text_list  = list()
                voting_text     = ''
                voting_turn     = ''
                desc_turn       = 0
                desc_list       = list()





def on_callback_query(msg):
    global count, step, undercover_n, players, players_name, voters, describer_id, words, inline_polling
    global desc_turn, desc_list, cid, mid, diff, words, a, b, vote, vote_text_list, voting_text, voting_turn, chat_id
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)
    
    #Voting
    if from_id in voters:
        bot.answerCallbackQuery(query_id, text = "You have voted already")
    elif from_id in players:
        for namename in players_name:
            if query_data == namename + "_Voted":
                vote[players_name.index(namename)] += 1
            
        for namename in players_name:
            vote_text_list[players_name.index(namename)] = namename + ' ' + str(vote[players_name.index(namename)]) + ' voters\n'
        voting_text = ''
        for a in range(len(players)):
            voting_text = voting_text + str(vote_text_list[a])
        voters.append(from_id)


        bot.editMessageText((cid,mid), voting_text, reply_markup = inline_polling)
    if len(voters) == len(players):
        bot.sendMessage(chat_id, "Send 'continue' to process the voting.")
    



def on_inline_query(msg):
    global desc_turn, step
    query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
    step = 4.5
    def compute():
        query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
        print('Inline Query:', query_id, from_id, query_string)

        articles = [InlineQueryResultArticle(
                        id='abc',
                        title=query_string,
                        input_message_content=InputTextMessageContent(
                            message_text=query_string
                        )
                   )]

        return articles
    if from_id == players[desc_turn]:
        answerer.answer(msg, compute)
        



def on_chosen_inline_result(msg):
    global desc_turn, description_list, step
    result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
    print ('Chosen Inline Result:', result_id, from_id, query_string)
    desc_list.append(query_string)
    desc_turn += 1
    try:
        bot.sendMessage(chat_id, "It's " + players_name[desc_turn] + "'s turn to describe(Using inline query).")
    except:
        step = 4
    finally:
        if desc_turn == len(players):
            bot.sendMessage(chat_id, "To start the polling, send /poll@Undercover_bot")
            step = 5
    

TOKEN = '281001642:AAF53-CK5s979529LDAx3xN8unO5v80l0tA'            
            
bot = telepot.Bot(TOKEN)
answerer = telepot.helper.Answerer(bot)
bot.message_loop({'chat': on_chat_message,
                  'callback_query': on_callback_query,
                  'inline_query': on_inline_query,
                  'chosen_inline_result': on_chosen_inline_result},
                 run_forever='Listening ...')


