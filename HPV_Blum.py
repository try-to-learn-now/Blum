from requests import Session
from threading import Thread, Lock
from os import system as sys
from platform import system as s_name
from time import sleep
from random import randint, shuffle
from colorama import Fore
from typing import Literal
from datetime import datetime, timedelta
from urllib.parse import unquote

from Core.Tools.HPV_Banner import HPV_Banner
from Core.Tools.HPV_Config_Check import HPV_Config_Check
from Core.Tools.HPV_Upgrade import HPV_Upgrade_Alert
from Core.Tools.HPV_Getting_File_Paths import HPV_Get_Config, HPV_Get_Empty_Request, HPV_Get_Accept_Language

from Core.Config.HPV_Config import *







class HPV_Blum:
    '''
    AutoBot Ferma /// HPV
    ---------------------
    [1] - `Receiving daily reward`
    
    [2] - `Coin collection`
    
    [3] - `Launch of coin farming`
    
    [4] - `Collecting coins for referrals`
    
    [5] - `Getting the number of available games and starting their passage`
    
    [6] - `Completing all available tasks`
    
    [7] - `Waiting time from 9 to 11 hours`
    
    [8] - `Repeat actions after 9-11 hours`
    '''



    def __init__(self, Name: str, URL: str, Proxy: dict, Headers: dict) -> None:
        self.HPV_PRO = Session()           # Создание `requests` сессии
        self.Name = Name                   # Ник аккаунта
        self.URL = self.URL_Clean(URL)     # Уникальная ссылка для авторизации в mini app
        self.Proxy = Proxy                 # Прокси (при наличии)

        # Уникальные параметров для Headers
        self.USER_AGENT = Headers['USER_AGENT']
        self.SEC_CH_UA = Headers['SEC_CH_UA']
        self.SEC_CH_UA_MOBILE = Headers['SEC_CH_UA_MOBILE']
        self.SEC_CH_UA_PLATFORM = Headers['SEC_CH_UA_PLATFORM']
        self.X_REQUESTED_WITH = Headers['X_REQUESTED_WITH']
        self.ACCEPT_LANGUAGE = self.Get_Accept_Language()

        self.Token = self.Authentication() # Токен аккаунта



    def URL_Clean(self, URL: str) -> str:
        '''Cleaning a unique link from unnecessary elements'''

        try:
            return unquote(URL.split('#tgWebAppData=')[1].split('&tgWebAppVersion')[0])
        except:
            return ''



    def Current_Time(self) -> str:
        '''Текущее время'''

        return Fore.BLUE + f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'



    def Logging(self, Type: Literal['Success', 'Warning', 'Error'], Smile: str, Text: str) -> None:
        '''Логирование'''

        with Console_Lock:
            COLOR = Fore.GREEN if Type == 'Success' else Fore.YELLOW if Type == 'Warning' else Fore.RED # Цвет текста
            DIVIDER = Fore.BLACK + ' | '   # Разделитель

            Time = self.Current_Time()        # Текущее время
            Name = Fore.MAGENTA + self.Name   # Ник аккаунта
            Smile = COLOR + str(Smile)        # Смайлик
            Text = COLOR + Text               # Текст лога

            print(Time + DIVIDER + Smile + DIVIDER + Text + DIVIDER + Name)



    def Get_Accept_Language(self) -> str:
        '''Getting the language parameter that matches the IP'''

        Accept_Language = HPV_Get_Accept_Language() # Получение данных с языковыми заголовками

        # Определение кода страны по IP
        try:
            COUNTRY = self.HPV_PRO.get('https://ipwho.is/', proxies=self.Proxy).json()['country_code'].upper()
        except:
            COUNTRY = ''

        return Accept_Language.get(COUNTRY, 'en-US,en;q=0.9')



    def Authentication(self) -> str:
        '''Account authentication'''

        URL = 'https://gateway.blum.codes/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP'
        HEADERS = {'User-Agent': self.USER_AGENT, 'Accept': 'application/json, text/plain, */*', 'Content-Type': 'application/json', 'sec-ch-ua': self.SEC_CH_UA, 'sec-ch-ua-mobile': self.SEC_CH_UA_MOBILE, 'sec-ch-ua-platform': self.SEC_CH_UA_PLATFORM, 'origin': 'https://telegram.blum.codes', 'x-requested-with': self.X_REQUESTED_WITH, 'sec-fetch-site': 'same-site', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'accept-language': self.ACCEPT_LANGUAGE}
        JSON = {'query': self.URL}

        self.Empty_Request('Authentication_1') # Пустой запрос
        self.Empty_Request('Authentication_2') # Пустой запрос

        try:
            Token = self.HPV_PRO.post(URL, headers=HEADERS, json=JSON, proxies=self.Proxy).json()['token']['access']
            self.Logging('Success', '🟢', 'Initialization successful!')
            return Token
        except:
            self.Logging('Error', '🔴', 'Initialization error!')
            return ''



    def ReAuthentication(self) -> None:
        '''Re-authenticating your account'''

        self.Token = self.Authentication()



    def Empty_Request(self, Empty: str) -> None:
        '''Sending empty requests with site add-ons loading to appear human'''

        Request: dict = HPV_Get_Empty_Request()[Empty]

        for header_key in list(Request['Headers'].keys()):
            header_key_lower = header_key.lower()

            if header_key_lower == 'user-agent':
                Request['Headers'][header_key] = self.USER_AGENT
            elif header_key_lower == 'sec-ch-ua':
                Request['Headers'][header_key] = self.SEC_CH_UA
            elif header_key_lower == 'sec-ch-ua-mobile':
                Request['Headers'][header_key] = self.SEC_CH_UA_MOBILE
            elif header_key_lower == 'authorization':
                Request['Headers'][header_key] = f'Bearer {self.Token}'
            elif header_key_lower == 'sec-ch-ua-platform':
                Request['Headers'][header_key] = self.SEC_CH_UA_PLATFORM
            elif header_key_lower == 'x-requested-with':
                Request['Headers'][header_key] = self.X_REQUESTED_WITH
            elif header_key_lower == 'accept-language':
                Request['Headers'][header_key] = self.ACCEPT_LANGUAGE

        try:
            self.HPV_PRO.request(method=Request['Method'], url=Request['Url'], params=Request.get('Params'), data=Request.get('Data'), json=Request.get('Json'), headers=Request.get('Headers'), proxies=self.Proxy)
        except:
            pass



    def Get_Info(self) -> dict:
        '''Getting information about the balance and availability of available games'''

        URL = 'https://game-domain.blum.codes/api/v1/user/balance'
        HEADERS = {'User-Agent': self.USER_AGENT, 'Accept': 'application/json, text/plain, */*', 'sec-ch-ua': self.SEC_CH_UA, 'sec-ch-ua-mobile': self.SEC_CH_UA_MOBILE, 'authorization': f'Bearer {self.Token}', 'sec-ch-ua-platform': self.SEC_CH_UA_PLATFORM, 'origin': 'https://telegram.blum.codes', 'x-requested-with': self.X_REQUESTED_WITH, 'sec-fetch-site': 'same-site', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'accept-language': self.ACCEPT_LANGUAGE}

        self.Empty_Request('user_me_get') # Пустой запрос
        self.Empty_Request('time_now_options') # Пустой запрос
        self.Empty_Request('friends_balance_options') # Пустой запрос
        self.Empty_Request('friends_balance_get') # Пустой запрос
        self.Empty_Request('user_balance_options') # Пустой запрос
        self.Empty_Request('daily_reward_options') # Пустой запрос
        self.Empty_Request('tribe_my_options') # Пустой запрос

        try:
            HPV = self.HPV_PRO.get(URL, headers=HEADERS, proxies=self.Proxy).json()

            Balance = HPV['availableBalance'] # Текущий баланс
            Plays = HPV['playPasses'] # Доступное кол-во игр

            return {'Balance': f'{float(Balance):,.0f}', 'Plays': Plays}
        except:
            return None



    def Daily_Reward(self) -> bool:
        '''Receiving daily reward'''

        URL = 'https://game-domain.blum.codes/api/v1/daily-reward?offset=-300'
        HEADERS = {'User-Agent': self.USER_AGENT, 'Accept': 'application/json, text/plain, */*', 'sec-ch-ua': self.SEC_CH_UA, 'sec-ch-ua-mobile': self.SEC_CH_UA_MOBILE, 'authorization': f'Bearer {self.Token}', 'sec-ch-ua-platform': self.SEC_CH_UA_PLATFORM, 'origin': 'https://telegram.blum.codes', 'x-requested-with': self.X_REQUESTED_WITH, 'sec-fetch-site': 'same-site', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'accept-language': self.ACCEPT_LANGUAGE}

        self.Empty_Request('time_now_get') # Пустой запрос
        self.Empty_Request('tribe_my_get') # Пустой запрос

        # Проверка доступности получения ежедневной награды
        try:
            Daily_Reward = False if self.HPV_PRO.get(URL, headers=HEADERS, proxies=self.Proxy).json()['message'] else True
        except:
            Daily_Reward = True

        self.Empty_Request('friends_balance_options') # Пустой запрос
        self.Empty_Request('tribe_leaderboard_options') # Пустой запрос
        self.Empty_Request('friends_balance_get') # Пустой запрос
        self.Empty_Request('tribe_leaderboard_get') # Пустой запрос

        try:
            if Daily_Reward:
                return True if self.HPV_PRO.post(URL, headers=HEADERS, proxies=self.Proxy).text == 'OK' else False
            else:
                return False
        except:
            return False



    def Claim(self) -> None:
        '''Сбор монет'''

        URL = 'https://game-domain.blum.codes/api/v1/farming/claim'
        HEADERS = {'User-Agent': self.USER_AGENT, 'Accept': 'application/json, text/plain, */*', 'sec-ch-ua': self.SEC_CH_UA, 'sec-ch-ua-mobile': self.SEC_CH_UA_MOBILE, 'authorization': f'Bearer {self.Token}', 'sec-ch-ua-platform': self.SEC_CH_UA_PLATFORM, 'origin': 'https://telegram.blum.codes', 'x-requested-with': self.X_REQUESTED_WITH, 'sec-fetch-site': 'same-site', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'accept-language': self.ACCEPT_LANGUAGE}

        self.Empty_Request('farming_claim_options') # Пустой запрос

        try:
            self.HPV_PRO.post(URL, headers=HEADERS, proxies=self.Proxy).json()['availableBalance']
            self.Logging('Success', '🟢', 'Coins collected!')
        except:
            self.Logging('Error', '🔴', 'Coins not collected!')



    def Start_Farm(self) -> None:
        '''Запуск фарма монет'''

        URL = 'https://game-domain.blum.codes/api/v1/farming/start'
        HEADERS = {'User-Agent': self.USER_AGENT, 'Accept': 'application/json, text/plain, */*', 'sec-ch-ua': self.SEC_CH_UA, 'sec-ch-ua-mobile': self.SEC_CH_UA_MOBILE, 'authorization': f'Bearer {self.Token}', 'sec-ch-ua-platform': self.SEC_CH_UA_PLATFORM, 'origin': 'https://telegram.blum.codes', 'x-requested-with': self.X_REQUESTED_WITH, 'sec-fetch-site': 'same-site', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'accept-language': self.ACCEPT_LANGUAGE}

        self.Empty_Request('tribe_my_options') # Пустой запрос
        self.Empty_Request('tribe_my_get') # Пустой запрос
        self.Empty_Request('farming_start_options') # Пустой запрос

        try:
            self.HPV_PRO.post(URL, headers=HEADERS, proxies=self.Proxy).json()['startTime']
            self.Logging('Success', '🟢', 'Coin farming has started!')
        except:
            self.Logging('Error', '🔴', 'Coin farming is not running!')



    def Referal_Claim(self) -> bool:
        '''Сбор монет за рефералов'''

        URL = 'https://gateway.blum.codes/v1/friends/claim'
        HEADERS = {'User-Agent': self.USER_AGENT, 'Accept': 'application/json, text/plain, */*', 'sec-ch-ua': self.SEC_CH_UA, 'sec-ch-ua-mobile': self.SEC_CH_UA_MOBILE, 'authorization': f'Bearer {self.Token}', 'sec-ch-ua-platform': self.SEC_CH_UA_PLATFORM, 'origin': 'https://telegram.blum.codes', 'x-requested-with': self.X_REQUESTED_WITH, 'sec-fetch-site': 'same-site', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'accept-language': self.ACCEPT_LANGUAGE}

        try:
            self.HPV_PRO.post(URL, headers=HEADERS, proxies=self.Proxy).json()['claimBalance']
            return True
        except:
            return False



    def AutoRefClaim(self) -> None:
        '''Автоматический сбор монет за рефералов'''

        try:
            self.Empty_Request('friends_balance_options') # Пустой запрос
            self.Empty_Request('AutoRefClaim_1') # Пустой запрос

            # Проверка наличия реферальных бонусов
            try:
                URL = 'https://gateway.blum.codes/v1/friends/balance'
                HEADERS = {'User-Agent': self.USER_AGENT, 'Accept': 'application/json, text/plain, */*', 'sec-ch-ua': self.SEC_CH_UA, 'sec-ch-ua-mobile': self.SEC_CH_UA_MOBILE, 'authorization': f'Bearer {self.Token}', 'sec-ch-ua-platform': self.SEC_CH_UA_PLATFORM, 'origin': 'https://telegram.blum.codes', 'x-requested-with': self.X_REQUESTED_WITH, 'sec-fetch-site': 'same-site', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'accept-language': self.ACCEPT_LANGUAGE}
                RefClaim = self.HPV_PRO.get(URL, headers=HEADERS, proxies=self.Proxy).json()['canClaim']
            except:
                RefClaim = False

            self.Empty_Request('AutoRefClaim_2') # Пустой запрос

            if RefClaim:
                self.Empty_Request('AutoRefClaim_3') # Пустой запрос
                sleep(randint(1, 3)) # Промежуточное ожидание

                if self.Referal_Claim():
                    self.Logging('Success', '🟢', 'Coins for referrals collected!')

                    self.Empty_Request('friends_balance_options') # Пустой запрос
                    self.Empty_Request('friends_balance_get') # Пустой запрос
                    self.Empty_Request('user_balance_options') # Пустой запрос
                    self.Empty_Request('user_balance_get') # Пустой запрос
        except:pass



    def Play(self) -> None:
        '''Запуск игры'''

        URL_1 = 'https://game-domain.blum.codes/api/v1/game/play'
        URL_2 = 'https://game-domain.blum.codes/api/v1/game/claim'
        HEADERS_1 = {'User-Agent': self.USER_AGENT, 'Accept': 'application/json, text/plain, */*', 'sec-ch-ua': self.SEC_CH_UA, 'sec-ch-ua-mobile': self.SEC_CH_UA_MOBILE, 'authorization': f'Bearer {self.Token}', 'sec-ch-ua-platform': self.SEC_CH_UA_PLATFORM, 'origin': 'https://telegram.blum.codes', 'x-requested-with': self.X_REQUESTED_WITH, 'sec-fetch-site': 'same-site', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'accept-language': self.ACCEPT_LANGUAGE}
        HEADERS_2 = {'User-Agent': self.USER_AGENT, 'Accept': 'application/json, text/plain, */*', 'Content-Type': 'application/json', 'sec-ch-ua': self.SEC_CH_UA, 'sec-ch-ua-mobile': self.SEC_CH_UA_MOBILE, 'authorization': f'Bearer {self.Token}', 'sec-ch-ua-platform': self.SEC_CH_UA_PLATFORM, 'origin': 'https://telegram.blum.codes', 'x-requested-with': self.X_REQUESTED_WITH, 'sec-fetch-site': 'same-site', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'accept-language': self.ACCEPT_LANGUAGE}

        try:
            self.Empty_Request('game_play_options') # Пустой запрос
            self.Logging('Success', '🟢', 'Game started, waiting 30 seconds...')

            GID = self.HPV_PRO.post(URL_1, headers=HEADERS_1, proxies=self.Proxy).json()['gameId'] # Запуск и получение ID игры
            _COINS = randint(COINS[0], COINS[1]) # Желаемое кол-во получения монет

            def Empty_Requests():
                self.Empty_Request('user_balance_options')
                self.Empty_Request('friends_balance_options')
                self.Empty_Request('friends_balance_get')
                self.Empty_Request('user_balance_get')
                self.Empty_Request('game_claim_options')

            Thread(target=Empty_Requests).start() # Пустые запросы

            sleep(30) # Ожидание 30 секунд, для показа реальности игры

            self.Empty_Request('game_webm_get') # Пустой запрос
            self.HPV_PRO.post(URL_2, headers=HEADERS_2, json={'gameId': str(GID), 'points': _COINS}, proxies=self.Proxy)
            self.Logging('Success', '🟢', f'The game is played! +{_COINS}!')
        except:
            self.Logging('Error', '🔴', 'The game is not played!')



    def AutoPlay(self) -> None:
        '''Автоматическое получение кол-ва доступных игр и запуск их прохождения'''

        try:
            Get_plays = self.Get_Info()['Plays'] 
            if Get_plays > 0:
                self.Logging('Success', '🎮', f'Games available: {Get_plays}!')
                for _ in range(Get_plays):
                    self.Play()
                    self.Empty_Request('friends_balance_options') # Пустой запрос
                    self.Empty_Request('tribe_my_options') # Пустой запрос
                    self.Empty_Request('tribe_my_get') # Пустой запрос
                    self.Empty_Request('tribe_leaderboard_options') # Пустой запрос
                    self.Empty_Request('tribe_leaderboard_get') # Пустой запрос
                    self.Empty_Request('friends_balance_get') # Пустой запрос
                    sleep(randint(4, 6))

                self.Logging('Success', '💰', f'Balance after games: {self.Get_Info()["Balance"]}')
        except:pass



    def Get_Tasks(self) -> list:
        '''Список заданий'''

        URL = 'https://game-domain.blum.codes/api/v1/tasks'
        HEADERS_1 = {'User-Agent': self.USER_AGENT, 'Accept': 'application/json, text/plain, */*', 'sec-ch-ua': self.SEC_CH_UA, 'sec-ch-ua-mobile': self.SEC_CH_UA_MOBILE, 'authorization': f'Bearer {self.Token}', 'sec-ch-ua-platform': self.SEC_CH_UA_PLATFORM, 'origin': 'https://telegram.blum.codes', 'x-requested-with': self.X_REQUESTED_WITH, 'sec-fetch-site': 'same-site', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'accept-language': self.ACCEPT_LANGUAGE}
        HEADERS_2 = {'User-Agent': 'HPV TEAM', 'access-control-request-method': 'GET', 'access-control-request-headers': 'authorization', 'origin': 'https://telegram.blum.codes', 'sec-fetch-mode': 'cors', 'x-requested-with': 'HPV TEAM', 'sec-fetch-site': 'same-site', 'sec-fetch-dest': 'empty', 'accept-language': self.ACCEPT_LANGUAGE}

        try:
            try:self.HPV_PRO.options(URL, headers=HEADERS_2, proxies=self.Proxy)
            except:pass

            return self.HPV_PRO.get(URL, headers=HEADERS_1, proxies=self.Proxy).json()
        except:
            return []



    def Start_Tasks(self, ID: str) -> bool:
        '''Запуск задания'''

        URL = f'https://game-domain.blum.codes/api/v1/tasks/{ID}/start'
        HEADERS_1 = {'User-Agent': self.USER_AGENT, 'Accept': 'application/json, text/plain, */*', 'sec-ch-ua': self.SEC_CH_UA, 'sec-ch-ua-mobile': self.SEC_CH_UA_MOBILE, 'authorization': f'Bearer {self.Token}', 'sec-ch-ua-platform': self.SEC_CH_UA_PLATFORM, 'origin': 'https://telegram.blum.codes', 'x-requested-with': self.X_REQUESTED_WITH, 'sec-fetch-site': 'same-site', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'accept-language': self.ACCEPT_LANGUAGE}
        HEADERS_2 = {'User-Agent': self.USER_AGENT, 'access-control-request-method': 'POST', 'access-control-request-headers': 'authorization', 'origin': 'https://telegram.blum.codes', 'sec-fetch-mode': 'cors', 'x-requested-with': self.X_REQUESTED_WITH, 'sec-fetch-site': 'same-site', 'sec-fetch-dest': 'empty', 'accept-language': self.ACCEPT_LANGUAGE}

        try:
            try:self.HPV_PRO.options(URL, headers=HEADERS_2, proxies=self.Proxy)
            except:pass

            return True if self.HPV_PRO.post(URL, headers=HEADERS_1, proxies=self.Proxy).json()['STARTED'] else False
        except:
            return False



    def Claim_Tasks(self, ID: str) -> dict:
        '''Получение награды за выполненное задание'''

        URL = f'https://game-domain.blum.codes/api/v1/tasks/{ID}/claim'
        HEADERS_1 = {'User-Agent': self.USER_AGENT, 'Accept': 'application/json, text/plain, */*', 'sec-ch-ua': self.SEC_CH_UA, 'sec-ch-ua-mobile': self.SEC_CH_UA_MOBILE, 'authorization': f'Bearer {self.Token}', 'sec-ch-ua-platform': self.SEC_CH_UA_PLATFORM, 'origin': 'https://telegram.blum.codes', 'x-requested-with': self.X_REQUESTED_WITH, 'sec-fetch-site': 'same-site', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'accept-language': self.ACCEPT_LANGUAGE}
        HEADERS_2 = {'User-Agent': self.USER_AGENT, 'access-control-request-method': 'POST', 'access-control-request-headers': 'authorization', 'origin': 'https://telegram.blum.codes', 'sec-fetch-mode': 'cors', 'x-requested-with': self.X_REQUESTED_WITH, 'sec-fetch-site': 'same-site', 'sec-fetch-dest': 'empty', 'accept-language': self.ACCEPT_LANGUAGE}

        try:
            try:self.HPV_PRO.options(URL, headers=HEADERS_2, proxies=self.Proxy)
            except:pass

            HPV = self.HPV_PRO.post(URL, headers=HEADERS_1, proxies=self.Proxy).json()

            Status = HPV['status'] # Статус задания
            Reward = HPV['reward'] # Награда

            return {'Status': True, 'Reward': Reward} if Status == 'FINISHED' else {'Status': False}
        except:
            return {'Status': False}



    def AutoTasks(self) -> None:
        '''Automatic execution of all available tasks'''

        try:
            Tasks = self.Get_Tasks() # Список заданий
            sleep(randint(2, 4))

            for Task in Tasks:
                for _Task in Task['tasks']:

                    if _Task['status'] == 'NOT_STARTED': # Если задание ещё не начато
                        if self.Start_Tasks(_Task['id']):
                            sleep(randint(5, 7)) # Промежуточное ожидание
                            self.Get_Tasks() # Пустой запрос
                            sleep(randint(2, 4)) # Промежуточное ожидание
                            Claim_Tasks = self.Claim_Tasks(_Task['id'])
                            if Claim_Tasks['Status']:
                                self.Logging('Success', '⚡️', f'The task is completed! +{Claim_Tasks["Reward"]}')
                                sleep(randint(3, 5)) # Промежуточное ожидание

                    elif _Task['status'] == 'READY_FOR_CLAIM': # Если задание уже начато
                        Claim_Tasks = self.Claim_Tasks(_Task['id'])
                        if Claim_Tasks['Status']:
                            self.Logging('Success', '⚡️', f'The task is completed! +{Claim_Tasks["Reward"]}')
                            sleep(randint(3, 5)) # Промежуточное ожидание
        except:pass



    def Connected_Wallet(self) -> None:
        '''Пустые запросы для просмотра подключённого кошелька'''

        self.Empty_Request('Connected_Wallet_1') # Пустой запрос
        self.Empty_Request('Connected_Wallet_2') # Пустой запрос
        self.Empty_Request('Connected_Wallet_3') # Пустой запрос
        self.Empty_Request('Connected_Wallet_4') # Пустой запрос
        self.Empty_Request('Connected_Wallet_5') # Пустой запрос
        self.Empty_Request('user_balance_options') # Пустой запрос
        self.Empty_Request('user_balance_get') # Пустой запрос



    def Run(self) -> None:
        '''Активация бота'''

        while True:
            try:
                if self.Token: # Если аутентификация успешна
                    self.Logging('Success', '💰', f'Current balance: {self.Get_Info()["Balance"]}')


                    if self.Daily_Reward(): # Получение ежедневной награды
                        self.Logging('Success', '🟢', 'Daily reward received!')
                        sleep(randint(3, 5)) # Промежуточное ожидание


                    self.Empty_Request('user_balance_options') # Пустой запрос

                    # Проверка окончания фарминга
                    try:
                        URL = 'https://game-domain.blum.codes/api/v1/user/balance'
                        HEADERS = {'User-Agent': self.USER_AGENT, 'Accept': 'application/json, text/plain, */*', 'sec-ch-ua': self.SEC_CH_UA, 'sec-ch-ua-mobile': self.SEC_CH_UA_MOBILE, 'authorization': f'Bearer {self.Token}', 'sec-ch-ua-platform': self.SEC_CH_UA_PLATFORM, 'origin': 'https://telegram.blum.codes', 'x-requested-with': self.X_REQUESTED_WITH, 'sec-fetch-site': 'same-site', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'accept-language': self.ACCEPT_LANGUAGE}
                        Request = self.HPV_PRO.get(URL, headers=HEADERS, proxies=self.Proxy).json()['farming']
                        BALANCE = float(Request['balance']) # Намайненный баланс
                        SPEED = float(Request['earningsRate']) # Скорость майнинга
                        if BALANCE == 57.6 or BALANCE == 63.36:
                            Farming = False
                        else:
                            Farming = True
                    except:
                        Farming = False


                    self.Empty_Request('tribe_my_options') # Пустой запрос
                    self.Empty_Request('user_balance_get') # Пустой запрос
                    self.Empty_Request('tribe_my_get') # Пустой запрос
                    self.Empty_Request('tribe_leaderboard_options') # Пустой запрос
                    self.Empty_Request('tribe_leaderboard_get') # Пустой запрос


                    if Farming: # Если фарминг ещё продолжается
                        _Waiting = 8*60*60 - BALANCE/SPEED + randint(1*60*60, 3*60*60) # Значение времени в секундах для ожидания
                        Waiting_STR = (datetime.now() + timedelta(seconds=_Waiting)).strftime('%Y-%m-%d %H:%M:%S') # Значение времени в читаемом виде

                        self.Logging('Warning', '⏳', f'Сбор уже производился! Следующий сбор: {Waiting_STR}!')

                        # Ожидание конца майнинга
                        _Waiting_For_Upgrade = int(_Waiting / (60*30))
                        for _ in range(_Waiting_For_Upgrade):
                            if HPV_Upgrade_Alert(): # Проверка наличия обновления
                                return
                            sleep(60*30)
                        sleep(_Waiting - (_Waiting_For_Upgrade * 60 * 30))
                        self.ReAuthentication() # Повторная аутентификация аккаунта
                        continue

                    else: # Если фарм окончен
                        self.Claim() # Сбор монет
                        sleep(randint(3, 5)) # Промежуточное ожидание
                        self.Start_Farm() # Запуск фарма монет


                    self.Empty_Request('user_balance_options') # Пустой запрос
                    self.Empty_Request('user_balance_get') # Пустой запрос
                    sleep(randint(4, 9)) # Промежуточное ожидание


                    # Рандомное выполнение действий
                    Autos = [self.AutoRefClaim, self.AutoPlay, self.AutoTasks, self.Connected_Wallet]
                    shuffle(Autos) # Перемешивание списока функций
                    for Auto in Autos:
                        Auto() # Запуск случайных действий: сбор монет за рефералов, выполнение заданий, прохождение игр, или просто просмотр привязанного кошелька
                        sleep(randint(3, 5)) # Промежуточное ожидание


                    Waiting = randint(9*60*60, 11*60*60) # Значение времени в секундах для ожидания
                    Waiting_STR = (datetime.now() + timedelta(seconds=Waiting)).strftime('%Y-%m-%d %H:%M:%S') # Значение времени в читаемом виде


                    self.Logging('Success', '💰', f'Текущий баланс: {self.Get_Info()["Balance"]}')
                    self.Logging('Warning', '⏳', f'Следующий сбор: {Waiting_STR}!')


                    # Ожидание от 9 до 11 часов
                    Waiting_For_Upgrade = int(Waiting / (60*30))
                    for _ in range(Waiting_For_Upgrade):
                        if HPV_Upgrade_Alert(): # Проверка наличия обновления
                            return
                        sleep(60*30)
                    sleep(Waiting - (Waiting_For_Upgrade * 60 * 30))
                    self.ReAuthentication() # Повторная аутентификация аккаунта

                else: # Если аутентификация не успешна
                    if HPV_Upgrade_Alert(): # Проверка наличия обновления
                        return
                    sleep(randint(33, 66)) # Ожидание от 33 до 66 секунд
                    self.ReAuthentication() # Повторная аутентификация аккаунта

            except:
                if HPV_Upgrade_Alert(): # Проверка наличия обновления
                    return







if __name__ == '__main__':

    if s_name() == 'Windows':
        sys('cls'); sys('title HPV Blum - V2.14')
    else:
        sys('clear')

    while True:
        HPV_Banner() # Вывод баннера
        HPV_Config_Check() # Проверка конфига на валидность
        print(Fore.MAGENTA + '[HPV]' + Fore.GREEN + ' — Проверка конфига окончена... Скрипт запустится через 5 секунд...\n'); sleep(5)

        Console_Lock = Lock()
        Threads = [] # Список потоков

        def Start_Thread(Name: str, URL: str, Proxy: dict, Headers: dict) -> None:
            Blum = HPV_Blum(Name, URL, Proxy, Headers)
            Blum.Run()

        # Получение конфигурационных данных и запуск потоков
        for Account in HPV_Get_Config(_print=False):
            HPV = Thread(target=Start_Thread, args=(Account['Name'], Account['URL'], Account['Proxy'], Account['Headers'],))
            HPV.start()
            Threads.append(HPV)

        for thread in Threads:
            thread.join()


