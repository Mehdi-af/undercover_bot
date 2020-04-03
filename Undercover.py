##############################################################################
## README                                                                   ##
##                                                                          ##
## This program requires:                                                   ##
## Selenium                                                                 ##
## NLTK                                                                     ##
## Telepot                                                                  ##
## Requests                                                                 ##
## lxml                                                                     ##
## Beautifulsoup                                                            ##
## Geckodriver                                                              ##
##                                                                          ##
##############################################################################

import telepot, random, sys, time
from pprint import pprint
from statistics import mode
sys.path.append('SYNONYM.PY file PATH') #Insert synonym.py path here so that it can be imported
import synonym
from telepot.namedtuple import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton
from random import randint
from math import floor
import pdb

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
    # pprint(msg)
    global chat_id, desc_turn, desc_list, cid, mid, diff, words, a, b, vote, vote_text_list, voting_text, voting_turn, a_var
    
    content_type, chat_type, chat_id = telepot.glance(msg)
    command = msg['text']
    player_id = msg['from']['id']
    name = msg['from']['first_name']
    global count, step, white_n, white_name, undercover_n, players, players_name, voters, describer_id, words, inline_polling, undercover_name, undercover_name_fix, civilian_word
    global kicked_white_name, white_name_fix
    print(step)
    if str(command) == 'a': 
        [a,b] = synonym.synword(3)
        civilian_word = a
    pdb.set_trace()


    #Inline Keyboard
    inline_polling  = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text= namename, callback_data = namename + "_Voted")] for namename in players_name
                ])

    if player_id == chat_id:
        if command == "/help":
            bot.sendMessage(chat_id, Help_Text)
            bot.sendMessage(chat_id, "Add this bot to your group to start playing.")

    #For command /help
    if command == "/help":
        bot.sendMessage(chat_id, Help_Text)

    if step > 0 and command == "/join":
        bot.sendMessage(chat_id, name + ", you no longer can join. The game has already started.")

    if command == "/restart":
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
        white_name      = list()
        voting_text     = ''
        voting_turn     = ''
        desc_turn       = 0
        desc_list       = list()        
        bot.sendMessage(chat_id, "The game has been restarted, please join to start.")


    #For command /quit    
    if command == "/quit":
        if player_id in players:
            players.remove(player_id)
            count = count-1
            players_name.remove(name)
            bot.sendMessage(chat_id, name + ", just left the game.")
        else:
            bot.sendMessage(chat_id, name + ", you're not in the game.")


    #Step 0 means nothing happened yet. In this section, players will join and start the game.
    if step == 0:
        if command == "/join":
            if player_id not in players and count < 16:
                players.append(player_id)
                players_name.append(name)
                count = count + 1
                if count < 4:
                    bot.sendMessage(chat_id, "Hi " + name + ", you have joined the game. Waiting for at least " + str(4-count) + " more players \n\nMake sure you had clicked start on the private chat")
                else:
                    bot.sendMessage(chat_id, "Hi " + name + ", you have joined the game. There's already enough number of players to play. To start the game, send /start")
            
            elif player_id in players:
                bot.sendMessage(chat_id, name + " is already in the game")

            elif count == 16:
                bot.sendMessage(chat_id, "Sorry " + name + ", the game is already full")
        if command == "/poll":
            bot.sendMessage(chat_id, name + ", Start a game first.")

        if command == "/start":
            if count < 4:
                bot.sendMessage(chat_id, "Not enough players")
            else:
                bot.sendMessage(chat_id, "Game will be started")
                bot.sendMessage(chat_id, "How many undercovers? (0 for Random)")
                step = 1
                return
                
                

    #Step 1 determining number of undercovers
    if step == 1:
        step = 1.5
        try:
            if int(command) == 0:
                undercover_n = randint(1,floor(len(players)/2.0))
                white_n = randint(0, undercover_n)
                undercover_n = undercover_n - white_n
            elif int(command) < floor(len(players)/2.0):
                undercover_n = int(command)
                white_n = randint(0, undercover_n)
                undercover_n = undercover_n - white_n
            else:
                step = 1
            assert undercover_n > 0
            assert undercover_n < len(players)/2
            if step == 1.5:
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
            # print(diff)
            assert diff == 1 or diff == 2 or diff == 3 or diff == 4 or diff == 5
            print(diff)
            [a,b] = synonym.synword(diff)
            civilian_word = a
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

        words = ['-']*(white_n) + [a]*(count-undercover_n-white_n) + [b]*(undercover_n)        
        civilian_word = a
        while words[0] == '-':
            random.shuffle(words)

        c = list(zip(players,players_name))
        random.shuffle(c)
        players, players_name = zip(*c)
        
        for i in range(0,len(players)):
            if not words[i] == '-':
                bot.sendMessage(players[i], 'Your word is ' + words[i])
            else:
                bot.sendMessage(players[i], 'You have no words; you are a White!')

        for tempvar in range(0,len(words)):
            if words[tempvar] == b:
                undercover_name.append(players_name[tempvar])
            elif words[tempvar] == '-':
                white_name.append(players_name[tempvar])
                
        print('UnderCover is ' + str(undercover_name))
        if white_n > 0:
            print('White is ' + str(white_name))
        undercover_name_fix = undercover_name
        white_name_fix = white_name
        bot.sendMessage(chat_id, "Description turn.")
        step = 4

    #Step 4 for the describing
    if step == 4:
        message_to_send = 'Players should play in the following order.\n\n'
        for c, players_name_order in enumerate(players_name):
            message_to_send = message_to_send + 'Player ' + str(c+1) + ' is ' + players_name_order + '.\n'
        bot.sendMessage(chat_id, message_to_send)
        bot.sendMessage(chat_id, "To start the polling, send /poll")
        step = 5
            
    #Step 5 for polling
    if step == 5:
        if command == "/poll":
            vote = [0]*len(players)
            keyboard = inline_polling
            vote_text_list = [0]*len(players)
            vote_sum = 0
            for namename in players_name:
                vote_text_list[players_name.index(namename)] = namename + ' ' + str(vote[players_name.index(namename)]) + ' voters\n'
                vote_sum += vote[players_name.index(namename)]
            voting_text = ''
            for a in range(len(players)):
                voting_text = voting_text + str(vote_text_list[a])
            voting_text = 'Voting in Progress.\n\n Total number of Votes :' + str(vote_sum)
            polling_keyboard = bot.sendMessage (chat_id, voting_text , reply_markup = keyboard)
            
            cid, mid = telepot.message_identifier(polling_keyboard)
        if len(voters) == len(players):
            # if command.lower() == "continue":
            for namename in players_name:
                vote_text_list[players_name.index(namename)] = namename + ' ' + str(vote[players_name.index(namename)]) + ' voters\n'
            voting_text = ''
            for a in range(len(players)):
                voting_text = voting_text + str(vote_text_list[a])
            bot.sendMessage (chat_id, voting_text)
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
            bot.sendMessage(chat_id, "It's a draw! Vote Again.\nSend /poll again.")
            return
        bot.sendMessage(chat_id, "Voting has ended. " + kicked + " died")
        
        if kicked not in undercover_name:
            if kicked not in white_name:
                print(msg)
                bot.sendMessage(chat_id, "You killed the wrong guy....")
                players.remove(players[players_name.index(kicked)])
                players_name.remove(kicked)
                count = count - 1
                step = 7
            else:
                print(msg)
                bot.sendMessage(chat_id, "You killed the white!!!")
                bot.sendMessage(chat_id, "White should guess the Civilian Word. (In this format -> guess:***)")
                players.remove(players[players_name.index(kicked)])
                players_name.remove(kicked)
                kicked_white_name = kicked
                count = count - 1
                white_n = white_n - 1
                step = 8
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
        if undercover_n + white_n == 0:
            bot.sendMessage(chat_id, "Civilian Wins!\n\n\Game has finished. Join a new game.")
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
            white_name      = list()
            voting_text     = ''
            voting_turn     = ''
            desc_turn       = 0
            desc_list       = list()
        elif (len(players) - white_n - undercover_n == 1):
            bot.sendMessage(chat_id, "Undercover Wins!\n" + "Undercover : " + ", ".join(undercover_name_fix))
            bot.sendMessage(chat_id, "Whites : " + ", ".join(white_name_fix) + "\n\n\
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
            white_name      = list()
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
                
            else:
                step = 4
                voters          = list()
                describer       = list()
                vote            = list()
                vote_text_list  = list()
                voting_text     = ''
                voting_turn     = ''
                desc_turn       = 0
                desc_list       = list()

    if step == 8:
        if name == kicked_white_name:
            if 'guess' in command.lower():
                if civilian_word in command.lower():
                    bot.sendMessage(chat_id, 'Mr. White Won!!!')
                    bot.sendMessage(chat_id, "Undercover : " + ", ".join(undercover_name_fix) + "\n\n\Game has finished. Join a new game.")
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
                    white_name      = list()
                    voting_text     = ''
                    voting_turn     = ''
                    desc_turn       = 0
                    desc_list       = list()                
                else:
                    bot.sendMessage(chat_id, 'Continue the game! Wrong guess!')
                step = 7
            else:
                bot.sendMessage(chat_id, 'Hey White, please make a guess in this format (guess:****)')
        else:
            bot.sendMessage(chat_id, 'It is ' + str(kicked_white_name) + '\'s turn to make a guess.')






def on_callback_query(msg):
    global count, step, undercover_n, players, players_name, voters, describer_id, words, inline_polling
    global desc_turn, desc_list, cid, mid, diff, words, a, b, vote, vote_text_list, voting_text, voting_turn, chat_id
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    #print('Callback Query:', query_id, from_id, query_data)
    
    #Voting
    if from_id in voters:
        bot.answerCallbackQuery(query_id, text = "You have voted already")
    elif from_id in players:
        for namename in players_name:
            if query_data == namename + "_Voted":
                vote[players_name.index(namename)] += 1
                # bot.sendMessage(chat_id, text = update.message.from_user['first_name'])
        vote_sum = 0            
        for namename in players_name:
            vote_text_list[players_name.index(namename)] = namename + ' ' + str(vote[players_name.index(namename)]) + ' voters\n'
            vote_sum += vote[players_name.index(namename)]
        voting_text = ''
        for a in range(len(players)):
            voting_text = voting_text + str(vote_text_list[a])
        voting_text = 'Voting in Progress.\n\n Total number of Votes : ' + str(vote_sum)
        voters.append(from_id)


        bot.editMessageText((cid,mid), voting_text, reply_markup = inline_polling)
    if len(voters) == len(players):
        # if command.lower() == "continue":
        for namename in players_name:
            vote_text_list[players_name.index(namename)] = namename + ' ' + str(vote[players_name.index(namename)]) + ' voters\n'
        voting_text = ''
        for a in range(len(players)):
            voting_text = voting_text + str(vote_text_list[a])
        bot.sendMessage (chat_id, voting_text)
        step = 6
    



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
    bot.sendMessage(chat_id, "It's " + players_name[desc_turn] + "'s turn to describe(Using inline query).")
    bot.sendMessage(chat_id, "To start the polling, send /poll")
    step = 5        

    

TOKEN = '<YOUR-TOKEN>'            
            
bot = telepot.Bot(TOKEN)
answerer = telepot.helper.Answerer(bot)
bot.message_loop({'chat': on_chat_message,
                  'callback_query': on_callback_query,
                  'inline_query': on_inline_query,
                  'chosen_inline_result': on_chosen_inline_result},
                 run_forever='Listening ...')
