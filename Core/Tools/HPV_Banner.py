from shutil import get_terminal_size as gts
from colorama import Fore
from time import sleep



HPV_TEAM = f'''
+-----------------------------------------+
| Blum Automation Fucking  |
+-----------------------------------------+
| Fuck The system |
+-------------------------------+
| chal bhag |
+-----------------------+
| V2.14 |
+-------+
'''



def HPV_Banner():
    '''Displaying a banner'''

    for HPV in HPV_TEAM.split('\n'): # Вывод баннера
        print(Fore.MAGENTA + HPV.center(gts()[0], ' '))
        sleep(0.025)


