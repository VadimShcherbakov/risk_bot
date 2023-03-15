import requests
import time


def send_bot_message():
    # Отправляет собщение в чат бот и получает ответ  от бота 'Ура! Классный апдейт!'
    API_URL: str = 'https://api.telegram.org/bot'
    BOT_TOKEN: str = '5443763132:AAHwrgf4WPPFBOXl9Gs1HL6ejTsO4-wgWAk'
    TEXT: str = 'Ура! Классный апдейт!'
    MAX_COUNTER: int = 5

    #мы делаем offset равным -2, чтобы при запуске программы, во время первого запроса на сервер,
    # запрос уходил с параметром offset равным -1 (requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json())
    # и мы получали от сервера только самый последний апдейт.
    offset: int = -2
    counter: int = 0
    chat_id: int

    while counter < MAX_COUNTER:

        print('attempt =', counter)  # Чтобы видеть в консоли, что код живет

        #Телеграм хранит апдейты для бота в течение некоторого промежутка времени (не более 24 часов),
        # поэтому если просто использовать метод getUpdates без параметра offset, то будут приходить все апдейты
        # за этот период времени столько раз, сколько мы будем вызывать данный метод.
        #У каждого апдейта есть свой ID - некоторое целое число. Каждый следующий апдейт больше предыдущего на единицу.
        # Передав, в качестве параметра в offset, номер последнего апдейта плюс 1, сервер будет отправлять нам только те апдейты, которые идут за последним, полученным
        # нами до очередного запроса апдейтов. Мы как бы сообщаем серверу Telegram номер апдейта, начиная с которого хотим дальше эти апдейты получать(последний апдейт).
        updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json()

        #нужно проверить есть ли у словаря по ключу 'result' непустое значение и если есть - надо пройтись в цикле по всем полученным апдейтам,
        # получить из них update_id (номер апдейта) и chat_id (номер чата из которого пришел апдейт).
        print(updates)
        if updates['result']:
            for result in updates['result']:
                offset = result['update_id']
                chat_id = result['message']['from']['id']
                #отправляем запрос на сервер Телеграм с методом sendMessage и указанием chat_id, из которого пришел апдейт.
                requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={TEXT}')

        #Засыпаем на одну секунду, чтобы не травмировать сервер слишком частыми запросами.
        time.sleep(1)
        #Увеличиваем счетчик итераций на единицу и повторяем цикл снова.
        counter += 1


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    send_bot_message()

