#import Telegram_bot as telegram_bot
from Vk_bot.Vk_bot import Vk_bot
from Conspects_storage import Conspects_storage

def main():
    conspects = Conspects_storage()
    vk_bot = Vk_bot(conspects)
    vk_bot.start()

if __name__ == '__main__':
    main()