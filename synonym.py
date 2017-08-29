### THIS MODULE IS CRETED BY TEAM CUNTUM OF NTU ###


from nltk.corpus import wordnet
import random
import sys
import time
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
import urllib.request
import html5lib
import lxml
import re

def synword(method):
    
    # Method 1 : Use --- https://www.randomlists.com/things --- to random 1st word
    #            Use --- http://www.similar-word.com/default.asp --- to find synonym
    #
    # Method 2 : Use --- https://www.randomlists.com/things --- to random 1st word
    #            Use --- nltk module (Wordnet) --- to find synonym
    #
    # Method 3 : Use --- http://www.paulnoll.com/Books/Synonyms/index.html --- to finf both words
    #            Contain 2307 words and 426 sets of words
    #
    # Method 4 : Use --- http://www.enhancemyvocabulary.com/similar-words.html --- to find pair of synonym words
    #            Contain 277 pair of words
    #
    # Method 5 : Use words from the Undercover^^ app in ios.
    #          : Contain the best pair of words

    ###################################
    #   METHOD USING WEB SIMULATION   #
    ###################################

    if int(method) == 1 or int(method) == 2:

        # Start firefox for simulation
        driver = webdriver.Firefox()

        while True:

            ########################################
            #   This part for searching 1st word   #
            ########################################

            # Open the site
            url = "https://www.randomlists.com/things"
            driver.get(url)
            driver.implicitly_wait(10)

            # Inputting the number of words to find in the bar on the site
            quantity_input = driver.find_element_by_xpath("/html/body/div/div[1]/main/div[2]/div[1]/form/table/tbody/tr[2]/td[2]/input")
            quantity_input.clear()
            quantity_input.send_keys('1')
            quantity_input.send_keys(Keys.RETURN)

            # Getting the 1st word provided by the site
            time.sleep(3)
            result = driver.find_element_by_xpath("/html/body/div/div[1]/main/div[1]/ol/li/div/span[2]")
            word1  = result.text
            
            if int(method) == 1:
                
                ###########################################################
                #   This part for searching similar words using website   #
                ###########################################################

                # Open the site
                url = "http://www.similar-word.com/default.asp"
                driver.get(url)
                driver.implicitly_wait(90)

                # Inputting the 1st word to the search bar to find its synonym
                word_box = driver.find_element_by_xpath("/html/body/div[1]/div[4]/div[2]/div/form/div[1]/div[2]/input[1]")
                word_box.clear()
                word_box.send_keys(word1)
                word_box.send_keys(Keys.RETURN)

                # The site takes too long to load
                time.sleep(5)
                list_of_words = list()
                driver.implicitly_wait(90)
                
                # Getting the 2nd word
                for similar_words in driver.find_elements_by_xpath("/html/body/div[1]/div[4]/div[3]/div/div"):
                    list_of_words.append(similar_words.text)
                try:
                    assert 'mismatch' not in list_of_words[0]
                    synonym_str  = list_of_words[0].replace("Similar word to ","")
                    try:
                        word1_mod = word1 + ', '
                        synonym_str  = synonym_str.replace(word1_mod,'')
                    except:
                        None
                    try:
                        word1_mod = ', ' + word1
                        synonym_str  = synonym_str.replace(word1_mod,'')
                    except:
                        None
                    synonym_str  = synonym_str.replace(word1,'')
                    synonym_str  = synonym_str.replace(':\n\n', '')
                    synonym_list = synonym_str.split(',')
                    driver.quit()
                    x = random.randint(0,len(synonym_list))
                    word2 = synonym_list[x]
                    pair = [word1 , word2]
                    return pair
                    break    
                except:
                    None

            
            if int(method) == 2:

            
                ########################################
                #   This part for synonym using nltk   #
                ########################################

                

                # Finding list of words that have nearly the same lemmas with the first word base on nltk
                try:
                    synonyms = []
                    Word_test = word1
                    for syn in wordnet.synsets(Word_test):
                        for l in syn.lemmas():
                            if l.name() not in synonyms:
                                synonyms.append(l.name())
                                
                    synonyms.remove(Word_test)
                    x = random.randint(0,len(synonyms))
                    Set = [Word_test, synonyms[x]]
                    driver.quit()
                    return Set
                    break
                except:
                    None

            # Both Method will change the 1st word if there's no synonym found

            
    #####################################
    #   METHOD WITHOUT WEB SIMULATION   #
    #####################################




    if int(method) == 3:


        #################################################
        #   This part for getting both words from the   #
        #          datas provided by paulnoll           #
        #################################################
        
        a = random.randint(1,36)
        if a < 10:
            page = "0"+str(a)
        else:
            page = str(a)
        
        url = "http://www.paulnoll.com/Books/Synonyms/synonym-choices-" + page + ".html"
        html = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html, 'lxml')
        
        sets_x = soup.find_all(href=re.compile("synonym-"))
        sets_x.remove(sets_x[len(sets_x)-1])
        sets_x.remove(sets_x[len(sets_x)-1])

        x = random.randint(0, len(sets_x)-1)
        Sets = sets_x[x]
        Sets = str(Sets)
        try:
            Sets = re.search('html">(.+?).</a>', Sets).group(1)
        except AttributeError:
            Sets = re.search('html">(.+?). </a>', Sets).group(1)
        except:
            None
        finally:
            Sets = Sets.split(", ")
            while True:
                a = random.randint(0, len(Sets)-1)
                b = random.randint(0, len(Sets)-1)
                if not a == b:
                    break
            synonyms = [Sets[a], Sets[b]]
            return(synonyms)



    if int(method) == 4:
        

        #################################################
        #   This part for getting both words from the   #
        #     datas provided by enhancemyvocabulary     #
        #################################################

        # Getting html date of the site using BeautifulSoup
        url = "http://www.enhancemyvocabulary.com/similar-words.html"
        html = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html, 'lxml')

        # Kill all script and style elements
        
        for script in soup(["script", "style"]):
            script.extract()    # rip it out

        # Get text
        text = soup.get_text()
    
        # Break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        
        # Drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)

        # Get the string of the untagged words
        final_result = text.encode('utf-8')

        # Delete all non necessary string
        text_list = list(text)
        text_list[0:975] = []
        text_list[4893:] = []
        for capital_word in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            if capital_word in text_list:
                try:
                    text_list.remove(capital_word)
                except:
                    None
        text = "".join(text_list)
        
        for capital_word in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            text.replace(capital_word+'\n', "")
    
        text_list = text.split("\n")
        qwerty = text_list[31]
        for i in range(22):
            text_list.remove(qwerty)

        # Get random pair of synonyms still in string
        x = random.randint(0,277)
        chosen_row = text_list[x]
        # Split the string into a list of two elements
        words_list = chosen_row.split(', ')
        return words_list

    if int(method) == 5:
        good_list = [["Butterfly", "bird"],
                     ["KFC", "McDonald's"],
                     ["The Shawshank Redemption", "The Godfather"],
                     ["Cat", "pikachu"],
                     ["Menu", "buffet"],
                     ["Throat", "lake"],
                     ["Pepper", "wasabi"],
                     ["Bacon", "sausage"],
                     ["Beach", "desert"],
                     ["New York", "Manhattan"],
                     ["Whale", "submarine"],
                     ["Parrote", "tomato"],
                     ["Ice cream", "frozen yogurt"],
                     ["Zoo", "aquarium"],
                     ["Cabbage", "salad"],
                     ["Fog", "Steam"],
                     ["The Hobbit", "Harry Potter"],
                     ["Sea", "ocean"],
                     ["Kongfu", "karate"],
                     ["Chicken", "muscle"],
                     ["Sky", "cloud"],
                     ["Santa claus", "christmas"],
                     ["Camping", "picnic"],
                     ["Salsa", "tango"],
                     ["Eye", "camera"],
                     ["Glass", "mirror"],
                     ["Talk", "sing"],
                     ["Guinness", "heineken"],
                     ["Youtube", "CNN"],
                     ["USA", "European Union"],
                     ["Colorado", "Amazon"],
                     ["Secret", "privacy"],
                     ["Kiss", "hug"],
                     ["James Bond", "Sherlock Holmes"],
                     ["Basketball", "football"],
                     ["Penguin", "panda"],
                     ["Twitter", "Facebook"],
                     ["Halloween", "carnival"],
                     ["Burger", "pancake"],
                     ["Post office", "email"],
                     ["Llama", "ostrich"],
                     ["Chinese", "Japanese"],
                     ["Clock", "watch"],
                     ["Music", "art"],
                     ["Ben&Jerry's", "Häagen-dazs"],
                     ["Ice Age", "Madagascar"],
                     ["Movie", "story"],
                     ["Fire", "sun"],
                     ["Gray", "black"],
                     ["Orange", "clementine"],
                     ["Mouse", "guinea pig"],
                     ["Point(.)", "comma(,)"]]
        x = random.randint(0,51)
        return(good_list[x])
