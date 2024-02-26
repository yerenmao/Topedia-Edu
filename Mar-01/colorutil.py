import sys
from io import StringIO

class Color:

    class fg:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'
        white = '\033[97m'

    class bg:
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'
    
    def print(*args, sep=' ', end='\n', file=sys.stdout, flush=False, fg='', bg=''):
        strio = StringIO()
        print(*args, sep=sep, end=end, file=strio)
        payload = strio.getvalue().replace("\n", f"\033[00m\n{fg}{bg}")
        print(f'{fg}{bg}{payload}\033[00m', end='', file=file, flush=flush)
        
