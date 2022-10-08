import vk_api 
import settings
import Vk_bot.Keyboards_vk as Keyboards

from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

class Vk_bot:
    def __init__(self, conspects):
        #Инициализируем бота
        vk_session = vk_api.VkApi(token=settings.VK_API_KEY)
        self.vk = vk_session.get_api()
        self.longpoll = VkLongPoll(vk_session)
        self.conspects = conspects
        
    def start(self):
        print('Bot starts')
        #Слушаем сообщения
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    msg = self.vk.messages.getById(message_ids=event.message_id)
                    #В случае, если мы хотим дистанционно выключить бота, админ пишет Стоп
                    if id == settings.ADMIN_ID_VK:
                        if msg['items'][0]['text'] == 'Стоп':
                            break
                    #Помечаем сообщение как прочитанное            
                    self.vk.messages.markAsRead(peer_id=msg['items'][0]['from_id'])
                    
                    #Для дэбагов
                    #print(msg)

                    #Отправляем клавиатуру для регистрации (тесты)
                    self.send_message('Выберите группу:', msg['items'][0]['from_id'], keyboard=Keyboards.Registration_menu())
            
                    if msg['items'][0].get('payload') != None:
                        user_get = self.vk.users.get(user_ids = msg['items'][0]['from_id'])
                        user_get = user_get[0]
                        first_name = user_get['first_name']
                        last_name = user_get['last_name']
                        full_name = first_name+' '+last_name

                        self.registrate_new_user(full_name, '')
                        
        print("Bot has stopped")
        self.send_message("Bot has stopped", settings.ADMIN_ID_VK)

    def download_photo():
        pass

    def registrate_new_user(self, username, group):
        #Создаём отдельную папку для пользователя и папки для предметов
        user_folder_id = self.conspects.create_new_folder(username)['id']
        self.conspects.create_new_folder('Алгебра', user_folder_id)
        self.conspects.create_new_folder('Биология', user_folder_id)
        self.conspects.create_new_folder('Геометрия', user_folder_id)
        self.conspects.create_new_folder('Информатика', user_folder_id)
        self.conspects.create_new_folder('История', user_folder_id)
        self.conspects.create_new_folder('Обществознание', user_folder_id)
        self.conspects.create_new_folder('Физика', user_folder_id)
        self.conspects.create_new_folder('Химия', user_folder_id)

    def send_message(sefl, msg, id, attachments="", keyboard=""):
        sefl.vk.messages.send(user_id=id, message=msg, random_id=get_random_id(), keyboard=keyboard, attachments=attachments)