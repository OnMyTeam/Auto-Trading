import configparser
from autotrading.pusher.base_pusher import Pusher
from telethon import TelegramClient



class PushTelegram(Pusher):

    def __init__(self):

        config = configparser.ConfigParser()
        config.read('../conf/config.ini')
        api_id = config['TELEGRAM']['api_id']
        api_hash = config['TELEGRAM']['api_hash']
        print(api_id,' ',api_hash)
        self.telegram = TelegramClient("BitCoinDev", api_id, api_hash)

        self.telegram.connect()
        if not self.telegram.is_user_authorized():
            self.telegram.send_code_request('+821097950344')
            self.telegram.sign_in('+821097950344',  input('Enter the code: '))


    def send_message(self, username = None, message = None):
        self.telegram.send_message(username, message)



if __name__ == "__main__":
    abc = PushTelegram()
