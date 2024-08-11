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
from pytz import timezone

from Core.Tools.HPV_Banner import HPV_Banner
from Core.Tools.HPV_Config_Check import HPV_Config_Check
from Core.Tools.HPV_Getting_File_Paths import HPV_Get_Config, HPV_Get_Empty_Request, HPV_Get_Accept_Language

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
    
    [6] - `Выполнение всех доступных заданий`
    
    [7] - `Ожидание от 9 до 11 часов`
    
    [8] - `Повторение действий через 9-11 часов`
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
        '''Очистка уникальной ссылки от лишних элементов'''

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
        '''Получение языкового параметра, подходящего под IP'''

        Accept_Language = HPV_Get_Accept_Language() # Получение данных с языковыми заголовками

        # Определение кода страны по IP
        try:
            COUNTRY = self.HPV_PRO.get('https://ipwho.is/', proxies=self.Proxy).json()['country_code'].upper()
        except:
            COUNTRY = ''

        return Accept_Language.get(COUNTRY, 'en-US,en;q=0.9')



    def Authentication(self) -> str:
        '''Аутентификация аккаунта'''

        URL = 'https://gateway.blum.codes/v1/auth/provider/PROVIDER_TELEGRAM_MINI_APP'
        HEADERS = {'User-Agent': self.USER_AGENT, 'Accept': 'application/json, text/plain, */*', 'Content-Type': 'application/json', 'sec-ch-ua': self.SEC_CH_UA, 'sec-ch-ua-mobile': self.SEC_CH_UA_MOBILE, 'sec-ch-ua-platform': self.SEC_CH_UA_PLATFORM, 'origin': 'https://telegram.blum.codes', 'x-requested-with': self.X_REQUESTED_WITH, 'sec-fetch-site': 'same-site', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'accept-language': self.ACCEPT_LANGUAGE}
        JSON = {'query': self.URL}

        self.Empty_Request('Authentication_1') # Пустой запрос
        self.Empty_Request('Authentication_2') # Пустой запрос

        try:
            Token = self.HPV_PRO.post(URL, headers=HEADERS, json=JSON, proxies=self.Proxy).json()['token']['access']
            self.Logging('Success', '🟢', 'Инициализация успешна!')
            return Token
        except:
            self.Logging('Error', '🔴', 'Ошибка инициализации!')
            return ''



    def ReAuthentication(self) -> None:
        '''Повторная аутентификация аккаунта'''

        self.Token = self.Authentication()



    def Empty_Request(self, Empty: str) -> None:
        '''Отправка пустых запросов с подгрузкой дополнений сайта, чтобы казаться человеком'''

        Request: dict = HPV_Get_Empty_Request()[Empty]

        if Request['Headers'].get('User-Agent'):
            Request['Headers']['User-Agent'] = self.USER_AGENT

        if Request['Headers'].get('sec-ch-ua'):
            Request['Headers']['sec-ch-ua'] = self.SEC_CH_UA

        if Request['Headers'].get('sec-ch-ua-mobile'):
            Request['Headers']['sec-ch-ua-mobile'] = self.SEC_CH_UA_MOBILE

        if Request['Headers'].get('authorization'):
            Request['Headers']['authorization'] = f'Bearer {self.Token}'

        if Request['Headers'].get('sec-ch-ua-platform'):
            Request['Headers']['sec-ch-ua-platform'] = self.SEC_CH_UA_PLATFORM

        if Request['Headers'].get('x-requested-with'):
            Request['Headers']['x-requested-with'] = self.X_REQUESTED_WITH

        if Request['Headers'].get('accept-language'):
            Request['Headers']['accept-language'] = self.ACCEPT_LANGUAGE

        try:
            self.HPV_PRO.request(Request['Method'], Request['Url'], Request.get('Params'), Request.get('Data'), Request.get('Headers'), proxies=self.Proxy)
        except:
            pass



    def Time_Check(self) -> bool:
        '''Проверка времени'''

        # Получение текущего времени по МСК
        CURRENT = datetime.now(timezone('Europe/Moscow'))

        # Определение времени начала и конца интервала
        START = CURRENT.replace(hour=20, minute=0, second=0)
        END = CURRENT.replace(hour=21, minute=30, second=0)

        return START <= CURRENT <= END



    def Get_Info(self) -> dict:
        '''Получение информации о балансе и наличии доступных игр'''

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
        '''Получение ежедневной награды'''

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
            self.Logging('Success', '🟢', 'Монеты собраны!')
        except:
            self.Logging('Error', '🔴', 'Монеты не собраны!')



    def Start_Farm(self) -> None:
        '''Запуск фарма монет'''

        URL = 'https://game-domain.blum.codes/api/v1/farming/start'
        HEADERS = {'User-Agent': self.USER_AGENT, 'Accept': 'application/json, text/plain, */*', 'sec-ch-ua': self.SEC_CH_UA, 'sec-ch-ua-mobile': self.SEC_CH_UA_MOBILE, 'authorization': f'Bearer {self.Token}', 'sec-ch-ua-platform': self.SEC_CH_UA_PLATFORM, 'origin': 'https://telegram.blum.codes', 'x-requested-with': self.X_REQUESTED_WITH, 'sec-fetch-site': 'same-site', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'accept-language': self.ACCEPT_LANGUAGE}

        self.Empty_Request('tribe_my_options') # Пустой запрос
        self.Empty_Request('tribe_my_get') # Пустой запрос
        self.Empty_Request('farming_start_options') # Пустой запрос

        try:
            self.HPV_PRO.post(URL, headers=HEADERS, proxies=self.Proxy).json()['startTime']
            self.Logging('Success', '🟢', 'Фарм монет запущен!')
        except:
            self.Logging('Error', '🔴', 'Фарм монет не запущен!')



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
                    self.Logging('Success', '🟢', 'Монеты за рефералов собраны!')

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
            self.Logging('Success', '🟢', f'Игра сыграна! +{_COINS}!')
        except:
            self.Logging('Error', '🔴', 'Игра не сыграна!')



    def AutoPlay(self) -> None:
        '''Автоматическое получение кол-ва доступных игр и запуск их прохождения'''

        try:
            Get_plays = self.Get_Info()['Plays'] 
            if Get_plays > 0:
                self.Logging('Success', '🎮', f'Игр доступно: {Get_plays}!')
                for _ in range(Get_plays):
                    self.Play()
                    self.Empty_Request('friends_balance_options') # Пустой запрос
                    self.Empty_Request('tribe_my_options') # Пустой запрос
                    self.Empty_Request('tribe_my_get') # Пустой запрос
                    self.Empty_Request('tribe_leaderboard_options') # Пустой запрос
                    self.Empty_Request('tribe_leaderboard_get') # Пустой запрос
                    self.Empty_Request('friends_balance_get') # Пустой запрос
                    sleep(randint(4, 6))

                self.Logging('Success', '💰', f'Баланс после игр: {self.Get_Info()["Balance"]}')
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
        '''Автоматическое выполнение всех доступных заданий'''

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
                                self.Logging('Success', '⚡️', f'Задание выполнено! +{Claim_Tasks["Reward"]}')
                                sleep(randint(3, 5)) # Промежуточное ожидание

                    elif _Task['status'] == 'READY_FOR_CLAIM': # Если задание уже начато
                        Claim_Tasks = self.Claim_Tasks(_Task['id'])
                        if Claim_Tasks['Status']:
                            self.Logging('Success', '⚡️', f'Задание выполнено! +{Claim_Tasks["Reward"]}')
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
                    self.Logging('Success', '💰', f'Текущий баланс: {self.Get_Info()["Balance"]}')


                    if self.Daily_Reward(): # Получение ежедневной награды
                        self.Logging('Success', '🟢', 'Ежедневная награда получена!')
                        sleep(randint(3, 5)) # Промежуточное ожидание


                    self.Empty_Request('user_balance_options') # Пустой запрос

                    # Проверка окончания фарминга
                    try:
                        URL = 'https://game-domain.blum.codes/api/v1/user/balance'
                        HEADERS = {'User-Agent': self.USER_AGENT, 'Accept': 'application/json, text/plain, */*', 'sec-ch-ua': self.SEC_CH_UA, 'sec-ch-ua-mobile': self.SEC_CH_UA_MOBILE, 'authorization': f'Bearer {self.Token}', 'sec-ch-ua-platform': self.SEC_CH_UA_PLATFORM, 'origin': 'https://telegram.blum.codes', 'x-requested-with': self.X_REQUESTED_WITH, 'sec-fetch-site': 'same-site', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty', 'accept-language': self.ACCEPT_LANGUAGE}
                        Farming = float(self.HPV_PRO.get(URL, headers=HEADERS, proxies=self.Proxy).json()['farming']['balance'])
                    except:
                        Farming = False

                    self.Empty_Request('tribe_my_options') # Пустой запрос
                    self.Empty_Request('user_balance_get') # Пустой запрос
                    self.Empty_Request('tribe_my_get') # Пустой запрос
                    self.Empty_Request('tribe_leaderboard_options') # Пустой запрос
                    self.Empty_Request('tribe_leaderboard_get') # Пустой запрос


                    if Farming: # Если фарминг ещё продолжается
                        _Waiting = 28_800 - Farming/0.002 + randint(1*60*60, 3*60*60) # Значение времени в секундах для ожидания
                        Waiting_STR = (datetime.now() + timedelta(seconds=_Waiting)).strftime('%Y-%m-%d %H:%M:%S') # Значение времени в читаемом виде

                        self.Logging('Warning', '⏳', f'Сбор уже производился! Следующий сбор: {Waiting_STR}!')

                        # Ожидание конца майнинга
                        for _ in range(_Waiting):
                            if self.Time_Check(): # Проверка времени, является ли сейчас время от 20:00 до 21:30 по МСК
                                return
                            sleep(1)
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
                    for _ in range(Waiting):
                        if self.Time_Check(): # Проверка времени, является ли сейчас время от 20:00 до 21:30 по МСК
                            return
                        sleep(1)
                    self.ReAuthentication() # Повторная аутентификация аккаунта

                else: # Если аутентификация не успешна
                    if self.Time_Check(): # Проверка времени, является ли сейчас время от 20:00 до 21:30 по МСК
                        return
                    sleep(randint(33, 66)) # Ожидание от 33 до 66 секунд
                    self.ReAuthentication() # Повторная аутентификация аккаунта

            except:
                if self.Time_Check(): # Проверка времени, является ли сейчас время от 20:00 до 21:30 по МСК
                    return







if __name__ == '__main__':

    sys('cls' if s_name() == 'Windows' else 'clear') # Очистка терминала

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


