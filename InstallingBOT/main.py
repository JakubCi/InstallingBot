from distutils.log import ERROR
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
import keyboard
from translate import Translator
import translators as ts
import random
import numpy as np
import os


########## ZMIENNE ##########

translator= Translator(to_lang="English")
driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))
new_word=''
sessions=True
exception_2=True
saved=False

#############################


########### SESJA ###########

def session():
    global sessions,new_word,exception_2
    findByXpath('/html/body/div[1]/div[2]/div/p[1]/a').click()
    element=driver.find_element('xpath','/html/body/div/div[5]/div[2]/h4')
    element2=driver.find_element('xpath','/html/body/div/div[3]/div/h4')
    time.sleep(1)
    displayed=True
    while displayed==True:
        time.sleep(0.5)
        if element.is_displayed():
            element.click()
            displayed=False
        elif element2.is_displayed():
            element2.click()
            displayed=False
           
    while driver.find_element('xpath','/html/body/div/div[9]/div[4]'):
        sessions=True
        while sessions==True:
            time.sleep(np.random.uniform(3,6))
            word= findByXpath('/html/body/div/div[8]/div[1]/div[2]/div[2]').get_attribute('textContent')
            while len(word)==0:
                time.sleep(0.5)
                word=driver.find_element('xpath','/html/body/div/div[8]/div[1]/div[2]/div[2]').get_attribute('textContent')
            f1=open('words.txt','r',encoding='utf-8')
            lines=f1.readlines()
            for rows in lines:
                print('Sprawdzam',rows)
                if rows.find(word.lower())==0:
                    print('plik')
                    translate=rows.split(':')
                    print(translate[1])
                    findByXpath('/html/body/div/div[8]/div[2]/table/tbody/tr/td/input').send_keys(translate[1])
                    time.sleep(1)
                    
                    # if driver.find_element('xpath','//div[@id=\"check\"]')!=0:
                    #     findByXpath('//div[@id=\"check\"]').click()
                    time.sleep(1)
                    findByXpath('//div[@id=\"nextword\"]').click()
                    print(translate[1])
                    exception_2=False
                    sessions=False 
                    break
                else:
                    exception_2=True
            if exception_2==True:
                print('wyjatek')
                time.sleep(np.random.uniform(3,6))
                word= findByXpath('/html/body/div/div[8]/div[1]/div[2]/div[2]').get_attribute('textContent')
                new_word=ts.google(word).lower()
                exception=True
                findByXpath('/html/body/div/div[8]/div[2]/table/tbody/tr/td/input').send_keys(new_word)
                while exception==True:
                    if len('/html/body/div/div[9]/div[2]/h4/div')!=0:
                        print('pierwsze')
                        findByXpath('/html/body/div/div[8]/div[2]/div[1]').click()
                        time.sleep(1)
                        if 'wielkość' in (driver.find_element('xpath','/html/body/div/div[9]/div[2]/h4/div')).get_attribute('textContent'):

                            findByXpath('/html/body/div/div[9]/div[4]').click()
                            exception=False
                            break
                        else:
                            word2=findByXpath('/html/body/div/div[9]/div[1]/div[2]').get_attribute('textContent')
                            word1=findByXpath('/html/body/div/div[9]/div[1]/div[3]/div[2]').get_attribute('textContent')
                            while len(word2)==0:
                                time.sleep(0.5)
                                word2=findByXpath('/html/body/div/div[9]/div[1]/div[2]').get_attribute('textContent')
                                word1=findByXpath('/html/body/div/div[9]/div[1]/div[3]/div[2]').get_attribute('textContent')
                                print('petla\n',word1,'\n',word2)
                            with open('words.txt','a',encoding='utf-8') as f:
                                f.write('\n'+word1+':'+word2)
                            findByXpath('/html/body/div/div[9]/div[4]').click()
                            exception=False
                            sessions=False
                            break
                    else:
                        print('drugie')
                        findByXpath('/html/body/div/div[8]/div[2]/div[1]').click()
                        findByXpath('/html/body/div/div[9]/div[4]').click()
                        exception=False
                        sessions=False
    findByXpath('/html/body/div/div[12]/div[2]').click()

######################################################################


########### FUNCKJA SPRAWDZAJĄCA POPRAWNOŚĆ HASŁA I LOGINU ###########

def check():
    global driver,saved,password,login
    elementy=driver.find_elements("xpath",'/html/body/div/div[3]/form/div/div[1]/p')
    while len(elementy)!=0:
        time.sleep(0.5)
        print("Błędne loginy!\n")
        login=input("Podaj ponownie swój login:\n")
        password=input("\nPodaj ponownie swoje hasło:\n")
        findByXpath('//input[@name=\"log_email\"]').clear()
        findByXpath('//input[@name=\"log_password\"]').clear()
        findByXpath('//input[@name=\"log_email\"]').send_keys(login)
        findByXpath('//input[@name=\"log_password\"]').send_keys(password)
        findByXpath('//button[@class=\"btn btn-primary w-100 mt-3 mb-3\"]').click()
        elementy=driver.find_elements("xpath",'/html/body/div/div[3]/form/div/div[1]/p')
    print('zalogowano!')
    
    if saved==False:
        agree=input('\nCzy chcesz zapisać swoje dane?\nWpisz tak/nie\n')
        if 'tak' in agree:
            with open('pass.txt','a',encoding='utf-8') as f:
                print('Password:'+password, file=f)
                print('Login:'+login,file=f)
                print('saved',file=f)
    session()

######################################################################


################ FUNCKJA SZUKAJĄCA ELEMENTU NA STRONIE ###############

def findByXpath(xpath):
    global driver
    elementy=driver.find_elements("xpath",xpath)
    while len(elementy)==0:
        time.sleep(0.5)
        print('.')
        elementy=driver.find_elements("xpath",xpath)
    return elementy[0]

######################################################################


############## FORMULARZ DO WYPEŁNIANIA LOGINU I HASŁA ###############

def form():
    global saved,login,password
    driver.get('https://instaling.pl/teacher.php?page=login')
    if os.path.exists('pass.txt'):
        print('File exists')
    else:
        f = open("pass.txt", "x")
        print('Password:',file=f)
        print('Login:',file=f)

    with open('pass.txt','r',encoding='utf-8') as f1:
        linie=f1.readlines()
        for rows in linie:
            if rows.find('saved'):
                saved=True
    if saved==False:
        password=input('Podaj swoje hasło:\n')
        login=input('\nPodaj swój login:\n')
        findByXpath('//input[@name=\"log_email\"]').clear()
        findByXpath('//input[@name=\"log_email\"]').send_keys(login)
        findByXpath('//input[@name=\"log_password\"]').clear()
        findByXpath('//input[@name=\"log_password\"]').send_keys(password)
        findByXpath('/html/body/div/div[3]/form/div/div[3]/button').click()
    else:
        with open('pass.txt','r',encoding='utf-8') as f:
            linia=f.readlines()
            password=linia[0].split(':')[1]
            login=linia[1].split(':')[1]
        findByXpath('//input[@name=\"log_email\"]').clear()
        findByXpath('//input[@name=\"log_email\"]').send_keys(login)
        findByXpath('//input[@name=\"log_password\"]').clear()
        findByXpath('//input[@name=\"log_password\"]').send_keys(password)
    check()

######################################################################

form()

while True:
    if keyboard.is_pressed('c'):
        exit()