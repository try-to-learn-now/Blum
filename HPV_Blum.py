from requests import post, get
from threading import Thread, Lock
from os import system as sys
from platform import system as s_name
from time import sleep
from random import randint
from colorama import Fore
from typing import Literal
from datetime import datetime, timedelta
from urllib.parse import unquote
from itertools import cycle

from Core.Tools.HPV_Getting_File_Paths import HPV_Get_Accounts
from Core.Tools.HPV_User_Agent import HPV_User_Agent
from Core.Tools.HPV_Proxy import HPV_Proxy_Checker

from Core.Config.HPV_Config import *







class HPV_Blum:
    '''
    AutoBot Ferma /// HPV
    ---------------------
    [1] - `Получение ежедневной награды`
    
    [2] - `Сбор монет`
    
    [3] - `Запуск фарма монет`
    
    [4] - `Сбор монет за рефералов`
    
    [5] - `Получение кол-ва доступных игр и запуск их прохождения`
    
    [6] - `Ожидание от 8 до 9 часов`
    
    [7] - `Повторение действий через 8-9 часов`
    '''



    def __init__(self, Name: str, URL: str, Proxy: dict) -> None:
        self.Name = Name                     # Ник аккаунта
        self.URL = self.URL_Clean(URL)       # Уникальная ссылка для авторизации в mini app
        self.Proxy = Proxy                   # Прокси (при наличии)
        self.UA = HPV_User_Agent()           # Генерация уникального User Agent
        self.Token = self.Authentication()   # Токен аккаунта



    def URL_Clean(self, URL: str) -> str:
        '''Очистка уникальной ссылки от лишних элементов'''

        try:
            return unquote(URL.split('#tgWebAppData=')[1].split('&tgWebAppVersion')[0])
        except:
            return ''



    def Current_Time(self) -> str:
        '''Текущее время'''

        return Fore.BLUE + f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'



    def Logging(self, Type: Literal['Success', 'Warning', 'Error'], Name: str, Smile: str, Text: str) -> None:
        '''Логирование'''

        with Console_Lock:
            COLOR = Fore.GREEN if Type == 'Success' else Fore.YELLOW if Type == 'Warning' else Fore.RED # Цвет текста
            DIVIDER = Fore.BLACK + ' | '   # Разделитель

            Time = self.Current_Time()     # Текущее время
            Name = Fore.MAGENTA + Name     # Ник аккаунта
            Smile = COLOR + str(Smile)     # Смайлик
            Text = COLOR + Text            # Текст лога

            print(Time + DIVIDER + Smile + DIVIDER + Text + DIVIDER + Name)



    def Authentication(self) -> str:
        '''Аутентификация аккаунта'''

        URL = 'https://gateway.blum.codes/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP'
        Headers = {'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Android WebView";v="122"', 'Accept': 'application/json, text/plain, */*', 'Content-Type': 'application/json', 'sec-ch-ua-mobile': '?1', 'User-Agent': self.UA, 'sec-ch-ua-platform': '"Android"', 'Origin': 'https://telegram.blum.codes', 'x-requested-with': 'org.telegram.plus', 'sec-fetch-site': 'same-site', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'}
        Json = {'query': self.URL}

        try:
            Token = post(URL, headers=Headers, json=Json, proxies=self.Proxy).json()['token']['access']
            self.Logging('Success', self.Name, '🟢', 'Инициализация успешна!')
            return Token
        except:
            self.Logging('Error', self.Name, '🔴', 'Ошибка инициализации!')
            return ''



    def ReAuthentication(self) -> None:
        '''Повторная аутентификация аккаунта'''

        self.Token = self.Authentication()



    def Get_Info(self) -> dict:
        '''Получение информации о балансе и наличии доступных игр'''

        URL = 'https://game-domain.blum.codes/api/v1/user/balance'
        Headers = {'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Android WebView";v="122"', 'accept': 'application/json, text/plain, */*', 'sec-ch-ua-mobile': '?1', 'authorization': f'Bearer {self.Token}', 'user-agent': self.UA, 'sec-ch-ua-platform': 'Android', 'origin': 'https://telegram.blum.codes', 'x-requested-with': 'org.telegram.plus', 'sec-fetch-site': 'same-site', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'ru,ru-RU;q=0.9,en-US;q=0.8,en;q=0.7'}

        try:
            HPV = get(URL, headers=Headers, proxies=self.Proxy).json()

            Balance = HPV['availableBalance'] # Текущий баланс
            Plays = HPV['playPasses'] # Доступное кол-во игр

            return {'Balance': f'{float(Balance):,.0f}', 'Plays': Plays}
        except:
            return None



    def Daily_Reward(self) -> bool:
        '''Получение ежедневной награды'''

        URL = 'https://game-domain.blum.codes/api/v1/daily-reward?offset=-300'
        Headers = {'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Android WebView";v="122"', 'accept': 'application/json, text/plain, */*', 'sec-ch-ua-mobile': '?1', 'authorization': f'Bearer {self.Token}', 'user-agent': self.UA, 'sec-ch-ua-platform': '"Android"', 'origin': 'https://telegram.blum.codes', 'x-requested-with': 'org.telegram.plus', 'sec-fetch-site': 'same-site', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'ru,ru-RU;q=0.9,en-US;q=0.8,en;q=0.7'}

        try:
            HPV = post(URL, headers=Headers, proxies=self.Proxy)

            if HPV.text == 'OK':
                return True
            else:
                return False
        except:
            return False



    def Claim(self) -> None:
        '''Сбор монет'''

        URL = 'https://game-domain.blum.codes/api/v1/farming/claim'
        Headers = {'Host': 'game-domain.blum.codes', 'Content-Length': '0', 'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Android WebView";v="122"', 'Accept': 'application/json, text/plain, */*', 'sec-ch-ua-mobile': '?1', 'Authorization': f'Bearer {self.Token}', 'User-Agent': self.UA, 'sec-ch-ua-platform': '"Android"', 'Origin': 'https://telegram.blum.codes', 'x-requested-with': 'org.telegram.plus', 'sec-fetch-site': 'same-site', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'}

        try:
            post(URL, headers=Headers, proxies=self.Proxy).json()['availableBalance']
            self.Logging('Success', self.Name, '🟢', 'Монеты собраны!')
        except:
            self.Logging('Error', self.Name, '🔴', 'Монеты не собраны!')



    def Start_Farm(self) -> None:
        '''Запуск фарма монет'''

        URL = 'https://game-domain.blum.codes/api/v1/farming/start'
        Headers = {'Host': 'game-domain.blum.codes', 'Content-Length': '0', 'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Android WebView";v="122"', 'Accept': 'application/json, text/plain, */*', 'sec-ch-ua-mobile': '?1', 'Authorization': f'Bearer {self.Token}', 'User-Agent': self.UA, 'sec-ch-ua-platform': '"Android"', 'Origin': 'https://telegram.blum.codes', 'x-requested-with': 'org.telegram.plus', 'sec-fetch-site': 'same-site', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'}

        try:
            HPV = post(URL, headers=Headers, proxies=self.Proxy)

            try:
                HPV.json()['startTime']
                self.Logging('Success', self.Name, '🟢', 'Фарм монет запущен!')
            except:
                self.Logging('Warning', self.Name, '🟡', 'Фарм монет уже запущен!')
        except:
            self.Logging('Error', self.Name, '🔴', 'Фарм монет не запущен!')



    def Referal_Claim(self) -> bool:
        '''Сбор монет за рефералов'''

        URL = 'https://gateway.blum.codes/v1/friends/claim'
        Headers = {'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Android WebView";v="122"', 'Accept': 'application/json, text/plain, */*', 'sec-ch-ua-mobile': '?1', 'Authorization': f'Bearer {self.Token}', 'User-Agent': self.UA, 'sec-ch-ua-platform': '"Android"', 'Origin': 'https://telegram.blum.codes', 'x-requested-with': 'org.telegram.plus', 'sec-fetch-site': 'same-site', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'}

        try:
            post(URL, headers=Headers, proxies=self.Proxy).json()['claimBalance']
            return True
        except:
            return False



    def Play(self) -> None:
        '''Запуск игры'''

        URL_1 = 'https://game-domain.blum.codes/api/v1/game/play'
        URL_2 = 'https://game-domain.blum.codes/api/v1/game/claim'
        Headers_1 = {'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Android WebView";v="122"', 'Accept': 'application/json, text/plain, */*', 'sec-ch-ua-mobile': '?1', 'Authorization': f'Bearer {self.Token}', 'User-Agent': self.UA, 'sec-ch-ua-platform': '"Android"', 'Origin': 'https://telegram.blum.codes', 'x-requested-with': 'org.telegram.plus', 'sec-fetch-site': 'same-site', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'}
        Headers_2 = {'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Android WebView";v="122"', 'Accept': 'application/json, text/plain, */*', 'Content-Type': 'application/json', 'sec-ch-ua-mobile': '?1', 'Authorization': f'Bearer {self.Token}', 'User-Agent': self.UA, 'sec-ch-ua-platform': '"Android"', 'Origin': 'https://telegram.blum.codes', 'x-requested-with': 'org.telegram.plus', 'sec-fetch-site': 'same-site', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'}

        try:
            GID = post(URL_1, headers=Headers_1, proxies=self.Proxy).json()['gameId'] # Запуск и получение ID игры
            _COINS = randint(COINS[0], COINS[1]) # Желаемое кол-во получения монет
            sleep(30) # Ожидание 30 секунд, для показа реальности игры

            post(URL_2, headers=Headers_2, json={'gameId': str(GID), 'points': _COINS}, proxies=self.Proxy)
            self.Logging('Success', self.Name, '🟢', f'Игра сыграна! +{_COINS}!')
        except:
            self.Logging('Error', self.Name, '🔴', 'Игра не сыграна!')



    def Run(self) -> None:
        '''Активация бота'''

        while True:
            try:
                if self.Token: # Если аутентификация успешна

                    if self.Daily_Reward(): # Получение ежедневной награды
                        self.Logging('Success', self.Name, '🟢', 'Ежедневная награда получена!')
                        sleep(randint(33, 103)) # Промежуточное ожидание

                    self.Claim() # Сбор монет
                    sleep(randint(33, 103)) # Промежуточное ожидание
                    self.Start_Farm() # Запуск фарма монет

                    if self.Referal_Claim(): # Сбор монет за рефералов
                        self.Logging('Success', self.Name, '🟢', 'Монеты за рефералов собраны!')
                        sleep(randint(33, 103)) # Промежуточное ожидание

                    self.Logging('Success', self.Name, '💰', f'Текущий баланс: {self.Get_Info()["Balance"]}')

                    # Получение кол-ва доступных игр и запуск их прохождения
                    Get_plays = self.Get_Info()['Plays'] 
                    if Get_plays > 0:
                        self.Logging('Success', self.Name, '🎮', f'Игр доступно: {Get_plays}!')
                        for _ in range(Get_plays):
                            self.Play()
                            sleep(randint(12, 23))

                        self.Logging('Success', self.Name, '💰', f'Баланс после игр: {self.Get_Info()["Balance"]}')

                    Waiting = randint(29_000, 32_500) # Значение времени в секундах для ожидания
                    Waiting_STR = (datetime.now() + timedelta(seconds=Waiting)).strftime('%Y-%m-%d %H:%M:%S') # Значение времени в читаемом виде

                    self.Logging('Warning', self.Name, '⏳', f'Следующий сбор: {Waiting_STR}!')

                    sleep(Waiting) # Ожидание от 8 до 9 часов
                    self.ReAuthentication() # Повторная аутентификация аккаунта

                else: # Если аутентификация не успешна
                    sleep(randint(33, 66)) # Ожидание от 33 до 66 секунд
                    self.ReAuthentication() # Повторная аутентификация аккаунта
            except:
                pass







if __name__ == '__main__':
    sys('cls') if s_name() == 'Windows' else sys('clear')

    Console_Lock = Lock()
    Proxy = HPV_Proxy_Checker()

    def Start_Thread(Account, URL, Proxy = None):
        Blum = HPV_Blum(Account, URL, Proxy)
        Blum.Run()

    for Account, URL in HPV_Get_Accounts().items():
        if Proxy:
            Proxy = cycle(Proxy)
            Thread(target=Start_Thread, args=(Account, URL, next(Proxy),)).start()
        else:
            Thread(target=Start_Thread, args=(Account, URL,)).start()


