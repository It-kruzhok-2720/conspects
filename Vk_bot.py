import vk_api 
import settings

from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

class Vk_bot:
    def __init__(self):
        #Инициализируем бота
        vk_session = vk_api.VkApi(token=settings.api_key)
        self.vk = vk_session.get_api()
        self.longpoll = VkLongPoll(vk_session)

    def start(self):
        print("Bot starts")
        #Слушаем сообщения
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    msg = self.vk.messages.getById(message_ids=event.message_id)
                    #В случае, если мы хотим дистанционно выключить бота, админ пишет Стоп
                    if id == settings.admin_id:
                        if msg["items"][0]["text"] == "Стоп":
                            break
                    self.vk.messages.markAsRead(peer_id=msg["items"][0]["from_id"])
                    print(msg)
        print("Bot has stopped")
        self.send_message("Bot has stopped", settings.admin_id)

        def download_photo():
            pass


    def send_message(sefl, msg, id, attachments="", keyboard=""):
        sefl.vk.messages.send(user_id=id, message=msg, random_id=get_random_id(), keyboard=keyboard, attachments=attachments)