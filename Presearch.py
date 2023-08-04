# !/usr/bin/env python -*- coding: utf-8 -*-

from cgitb import text
import os
import time
import sys
import math
import random
from winsound import PlaySound
from selenium import webdriver
from playsound import playsound
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

######################################################1
#Init Browser


def searcher(sword):

    time.sleep(2)

    search_input = browser.find_element(By.XPATH,'/html/body/div/div[2]/div[3]/div[1]/dic/div[2]/div[1]/div/form/div/input')

    print("Clear Search Box")
    for element in range(0, len(sword) + 4):
        search_input.send_keys(Keys.BACK_SPACE)
        time.sleep(0.5)

    print(sword + " Typed")
    search_input.send_keys(sword)

    time.sleep(4)

    print("Pressing Enter")
    search_input.send_keys(Keys.ENTER)

    time.sleep(4)

acFile = open("Accounts.txt", "r")

accountFile = acFile.readlines()

lastAccount = open("LastAccount.txt", "r+")

lastAccountNumber = int(lastAccount.readline())

accountNumberFile = open("AccountNumber.txt", "r")

accountNumber = int(accountNumberFile.readline())

accountNumberFile.close()

for s in range(lastAccountNumber, accountNumber) :
    
    # os.system('color 0' +  random.choice(['a', 'b', 'c', 'd', 'e', 'f']))

    startTime = time.time()    

    options = Options()

    options.add_argument("--width=650");

    options.add_argument("--height=640");

    options.set_preference('profile', 'C:\\Users\\Admin\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\x2gpmyrg.default-release')

    service = Service('C:\\geco\\geckodriver')

    browser = webdriver.Firefox(options=options, service=service)

    browser.get('https://engine.presearch.org/search?q=Pre')

    loginBtn = browser.find_element(By.XPATH,'/html/body/div/div[2]/div[3]/div[1]/dic/div[2]/div[3]/div[1]/div[5]/div/div[2]/div')

    loginBtn.click()

    time.sleep(6)

    main_page = browser.current_window_handle

    # changing the handles to access login page
    for handle in browser.window_handles:
        if handle != main_page:
            login_page = handle
            break
            
    # change the control to signin page       
    browser.switch_to.window(login_page)

    email = browser.find_element(By.XPATH,'/html/body/div[1]/div[3]/div[1]/form/div[1]/input')

    password = browser.find_element(By.XPATH,'/html/body/div[1]/div[3]/div[1]/form/div[2]/div/input')

    email.send_keys(accountFile[lastAccountNumber*3])

    password.send_keys(accountFile[(lastAccountNumber*3) + 1])

    playsound('audio.mp3')
    
    time.sleep(3)

    lastAccountNumber = lastAccountNumber + 1

    time.sleep(40)
    print("Sleep Over")


    print("Switch To Main Page")
    browser.switch_to.window(main_page)

    time.sleep(2)

    with open("NewSearch.txt", "r") as file:
        allWords = file.read()
        words = list(map(str, allWords.split()))
    
    wordNumberFile = open("WordNumber.txt", "r")

    wordNumber = int(wordNumberFile.readline())

    wordNumberFile.close()

    for kounter in range(1, wordNumber + 1):
        sword = random.choice(words)
        searcher(sword)

        time.sleep(5)

        precoins = browser.find_element(By.CSS_SELECTOR,'div.items-start:nth-child(2) > div:nth-child(3) > div:nth-child(1) > span:nth-child(1)')

        print(" ")

        if kounter == 1 :
            firstPrecoins = round(float(precoins.get_attribute("innerHTML")), 4)

        print("Your Balance After " + str(kounter) + " Search In This Session : " + precoins.get_attribute("innerHTML"))

        print(" ")
        earnedCoins = round(float(precoins.get_attribute("innerHTML")) - firstPrecoins, 4)
        print("You Earn " + str(earnedCoins) + " Token, So Far, For This Session")
        print(" ")

    lastAccount.seek(0, os.SEEK_SET)
    lastAccount.write(str(lastAccountNumber))

    earnedCoins = round(float(precoins.text[0:6]) - firstPrecoins, 4)
    file.close()
    browser.close()

    print("Closing Browser For Next Account \n")
    print("You Earn " + str(earnedCoins) + " From This Account : " + accountFile[(lastAccountNumber - 1)*3])
    print("^^^^^^^^^^^ Account Number ^^^^^^^^^^^ -> " + str(lastAccountNumber - 1) + " <- ^^^^^^^^^^^ Account Number ^^^^^^^^^^^")
    endTime = time.time()
    print(" ")
    print("Process Time For This Account -->> : %s" % (endTime - startTime) + " Seconds")
    print(" ")

acFile.close()

lastAccount.close()
input()



