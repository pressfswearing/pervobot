import telebot
import random

bot = telebot.TeleBot("6665386471:AAHumfgLJo1G5K3LXf4x38BRNM0prAzUB7U")


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "тут приветственное сообщение")


@bot.message_handler(commands=["create_profile"])
def create_profile(message):
    directionss = open("directions.png", "rb")
    data = bot.send_message(
        message.chat.id,
        "Выбери свою будущую аватарку из галереи и в подписи к ней напиши свою анкету в таком формате:\n\n\
\
Имя\n\
Пол (М или Ж)\n\
Возраст\n\
Направление (одно)\n\
Статус (в будущем его можно будет поменять)\n\
Что-то о себе",
    )
    bot.send_photo(message.chat.id, directionss, "Вот список направлений.")
    bot.register_next_step_handler(data, create_profile1)


def create_profile1(message):
    photo = max(message.photo, key=lambda x: x.height)
    if not photo:
        bot.send_message(message.chat.id, 'Ты не прикреплил аватарку. Запусти /create_profile заново.')
        break
    bot.send_message(message.chat.id, "Вот твоя анкета:")
    bot.send_photo(message.chat.id, photo.file_id, message.caption)
    bot.send_message(
        message.chat.id,
        "Проверь, все ли данные ты правильно ввел и в правильном ли формате. Если что-то не так, запусти /create_profile заново.\n\
Если всё нормально, запусти /register.",
    )


@bot.message_handler(commands=["register"])
def register(message):
    data = bot.send_message(
        message.chat.id,
        "Скопируй свою анкету, прикрепи ту же фотку, которая была отправлена раньше, и отправь её ещё раз сейчас. Таким образом ты зарегистрируешься.",
    )
    bot.register_next_step_handler(data, register1)


def register1(message):
    profile = str(message.caption)
    photo = max(message.photo, key=lambda x: x.height)
    if not photo:
        bot.send_message(message.chat.id, 'Ты не прикрепил аватарку. Запусти /create_profile заново.')
    else:
        profile_split = profile.split("\n")
        name = profile_split[0]
        sex = profile_split[1]
        age = profile_split[2]
        direction = profile_split[3]
        status = profile_split[4]
        bio = profile_split[5]
        profile_join = "@".join(profile_split)
        general_file = open("general_data.txt", "a+", encoding="utf-8")
        ids_file = open("ids.txt", "a+", encoding="utf-8")
        general_file.write(
            "\n"
            + str(profile_join)
            + "@"
            + photo.file_id
            + "@"
            + message.from_user.username
        )
        ids_file.write("\n" + str(message.from_user.id) + "@" + message.from_user.username)
        bot.send_message(
            message.chat.id,
            "Теперь ты зарегистрирован! Запусти /show_profile, чтобы увидеть свой профиль!",
        )


@bot.message_handler(commands=["login"])
def login(message):
    general_file = open("general_data.txt", "r", encoding="utf-8")
    line = general_file.read()
    array = line.split("\n")
    for i in array:
        if message.from_user.username in i:
            profile_split = i.split("@")
            name = profile_split[0]
            sex = profile_split[1]
            age = profile_split[2]
            direction = profile_split[3]
            status = "Статус: " + profile_split[4]
            bio = profile_split[5]
            photo_id = profile_split[6]
            username = profile_split[7]
            caption = (
                name
                + "\n"
                + sex
                + "\n"
                + age
                + "\n"
                + direction
                + "\n"
                + status
                + "\n"
                + bio
                + "\n"
                + "@"
                + username
            )
            bot.send_message(
                message.chat.id, "Готово, ты вошёл в бота! Вот твой профиль:"
            )
            bot.send_photo(message.chat.id, photo_id, caption)
            break
    bot.send_message(
        message.chat.id,
        'Если тебе не выпало сообщение об удачном входе, то ты ещё не зарегистрирован в боте. Выполни /start заново и зарегистрируйся.\nОно выглядит так: "Готово, ты вошёл в бота!"',
    )


@bot.message_handler(commands=["new_friends"])
def new_friends(message):
    bot.send_message(
        message.chat.id,
        "Как будем искать?\nРандомно - /randomnewfriends\nПо интересам - /interestsnewfriends",
    )


@bot.message_handler(commands=["randomnewfriends"])
def randomnewfriends(message):
    general_file = open("general_data.txt", "r", encoding="utf-8")
    line = general_file.read()
    array = line.split("\n")
    temp = random.randint(0, len(array) - 1)
    tempp = array[temp]
    tempp_split = tempp.split("@")
    name = tempp_split[0]
    sex = tempp_split[1]
    age = tempp_split[2]
    direction = tempp_split[3]
    status = "Статус: " + tempp_split[4]
    bio = tempp_split[5]
    photo_id = tempp_split[6]
    username = tempp_split[7]
    caption = (
        name
        + "\n"
        + sex
        + "\n"
        + age
        + "\n"
        + direction
        + "\n"
        + status
        + "\n"
        + bio
        + "\n"
        + "@"
        + username
    )
    bot.send_photo(message.chat.id, photo_id, caption)


@bot.message_handler(commands=["interestsnewfriends"])
def interestsnewfriends(message):
    bot.send_message(
        message.chat.id,
        "Выбери интерес:\n\
  Образование и знания - /education\n\
  Наука и технологии - /technology\n\
  Труд, профессия и своё дело - /profession\n\
  Культура и искусство - /culture\n\
  Волонтёрство и добровольченство - /volunteer\n\
  Патриотизм и историческая память - /patriotism\n\
  Спорт - /sport\n\
  Здоровый образ жизни - /healthyhealth\n\
  Медиа и коммуникации - /media\n\
  Дипломатизм и международные отношения - /diplomatism\n\
  Экология и охрана природы - /ecology\n\
  Туризм и путешествия - /tourism",
    )


@bot.message_handler(commands=["education"])
def education(message):
    general_file = open("general_data.txt", "r", encoding="utf-8")
    line = general_file.read()
    array = line.split("\n")
    for i in array:
        temp = random.randint(0, len(array) - 1)
        tempp = array[temp]
        tempp_split = tempp.split("@")
        name = tempp_split[0]
        sex = tempp_split[1]
        age = tempp_split[2]
        direction = tempp_split[3]
        status = "Статус: " + tempp_split[4]
        bio = tempp_split[5]
        photo_id = tempp_split[6]
        username = tempp_split[7]
        caption = (
            name
            + "\n"
            + sex
            + "\n"
            + age
            + "\n"
            + direction
            + "\n"
            + status
            + "\n"
            + bio
            + "\n"
            + "@"
            + username
        )
        if direction == "Образование и знания":
            bot.send_photo(message.chat.id, photo_id, caption)
            bot.send_message(message.chat.id, 'Если хочешь повторить поиск - /education. Для возврата в меню знакомств - /new_friends.')
            break


@bot.message_handler(commands=["technology"])
def technology(message):
    general_file = open("general_data.txt", "r", encoding="utf-8")
    line = general_file.read()
    array = line.split("\n")
    for i in array:
        temp = random.randint(0, len(array) - 1)
        tempp = array[temp]
        tempp_split = tempp.split("@")
        name = tempp_split[0]
        sex = tempp_split[1]
        age = tempp_split[2]
        direction = tempp_split[3]
        status = "Статус: " + tempp_split[4]
        bio = tempp_split[5]
        photo_id = tempp_split[6]
        username = tempp_split[7]
        caption = (
            name
            + "\n"
            + sex
            + "\n"
            + age
            + "\n"
            + direction
            + "\n"
            + status
            + "\n"
            + bio
            + "\n"
            + "@"
            + username
        )
        if direction == "Наука и технологии":
            bot.send_photo(message.chat.id, photo_id, caption)
            bot.send_message(message.chat.id, 'Если хочешь повторить поиск - /technology. Для возврата в меню знакомств - /new_friends.')
            break


@bot.message_handler(commands=["profession"])
def profession(message):
    general_file = open("general_data.txt", "r", encoding="utf-8")
    line = general_file.read()
    array = line.split("\n")
    for i in array:
        temp = random.randint(0, len(array) - 1)
        tempp = array[temp]
        tempp_split = tempp.split("@")
        name = tempp_split[0]
        sex = tempp_split[1]
        age = tempp_split[2]
        direction = tempp_split[3]
        status = "Статус: " + tempp_split[4]
        bio = tempp_split[5]
        photo_id = tempp_split[6]
        username = tempp_split[7]
        caption = (
            name
            + "\n"
            + sex
            + "\n"
            + age
            + "\n"
            + direction
            + "\n"
            + status
            + "\n"
            + bio
            + "\n"
            + "@"
            + username
        )
        if direction == "Труд, профессия и своё дело":
            bot.send_photo(message.chat.id, photo_id, caption)
            bot.send_message(message.chat.id, 'Если хочешь повторить поиск - /profession. Для возврата в меню знакомств - /new_friends.')
            break


@bot.message_handler(commands=["culture"])
def culture(message):
    general_file = open("general_data.txt", "r", encoding="utf-8")
    line = general_file.read()
    array = line.split("\n")
    for i in array:
        temp = random.randint(0, len(array) - 1)
        tempp = array[temp]
        tempp_split = tempp.split("@")
        name = tempp_split[0]
        sex = tempp_split[1]
        age = tempp_split[2]
        direction = tempp_split[3]
        status = "Статус: " + tempp_split[4]
        bio = tempp_split[5]
        photo_id = tempp_split[6]
        username = tempp_split[7]
        caption = (
            name
            + "\n"
            + sex
            + "\n"
            + age
            + "\n"
            + direction
            + "\n"
            + status
            + "\n"
            + bio
            + "\n"
            + "@"
            + username
        )
        if direction == "Культура и искусство":
            bot.send_photo(message.chat.id, photo_id, caption)
            bot.send_message(message.chat.id, 'Если хочешь повторить поиск - /culture. Для возврата в меню знакомств - /new_friends.')
            break


@bot.message_handler(commands=["volunteer"])
def volunteer(message):
    general_file = open("general_data.txt", "r", encoding="utf-8")
    line = general_file.read()
    array = line.split("\n")
    for i in array:
        temp = random.randint(0, len(array) - 1)
        tempp = array[temp]
        tempp_split = tempp.split("@")
        name = tempp_split[0]
        sex = tempp_split[1]
        age = tempp_split[2]
        direction = tempp_split[3]
        status = "Статус: " + tempp_split[4]
        bio = tempp_split[5]
        photo_id = tempp_split[6]
        username = tempp_split[7]
        caption = (
            name
            + "\n"
            + sex
            + "\n"
            + age
            + "\n"
            + direction
            + "\n"
            + status
            + "\n"
            + bio
            + "\n"
            + "@"
            + username
        )
        if direction == "Волонтёрство и добровольчество":
            bot.send_photo(message.chat.id, photo_id, caption)
            bot.send_message(message.chat.id, 'Если хочешь повторить поиск - /volunteer. Для возврата в меню знакомств - /new_friends.')
            break


@bot.message_handler(commands=["patriotism"])
def patriotism(message):
    general_file = open("general_data.txt", "r", encoding="utf-8")
    line = general_file.read()
    array = line.split("\n")
    for i in array:
        temp = random.randint(0, len(array) - 1)
        tempp = array[temp]
        tempp_split = tempp.split("@")
        name = tempp_split[0]
        sex = tempp_split[1]
        age = tempp_split[2]
        direction = tempp_split[3]
        status = "Статус: " + tempp_split[4]
        bio = tempp_split[5]
        photo_id = tempp_split[6]
        username = tempp_split[7]
        caption = (
            name
            + "\n"
            + sex
            + "\n"
            + age
            + "\n"
            + direction
            + "\n"
            + status
            + "\n"
            + bio
            + "\n"
            + "@"
            + username
        )
        if direction == "Патриотизм и историческая память":
            bot.send_photo(message.chat.id, photo_id, caption)
            bot.send_message(message.chat.id, 'Если хочешь повторить поиск - /patriotism. Для возврата в меню знакомств - /new_friends.')
            break


@bot.message_handler(commands=["sport"])
def sport(message):
    general_file = open("general_data.txt", "r", encoding="utf-8")
    line = general_file.read()
    array = line.split("\n")
    for i in array:
        temp = random.randint(0, len(array) - 1)
        tempp = array[temp]
        tempp_split = tempp.split("@")
        name = tempp_split[0]
        sex = tempp_split[1]
        age = tempp_split[2]
        direction = tempp_split[3]
        status = "Статус: " + tempp_split[4]
        bio = tempp_split[5]
        photo_id = tempp_split[6]
        username = tempp_split[7]
        caption = (
            name
            + "\n"
            + sex
            + "\n"
            + age
            + "\n"
            + direction
            + "\n"
            + status
            + "\n"
            + bio
            + "\n"
            + "@"
            + username
        )
        if direction == "Спорт":
            bot.send_photo(message.chat.id, photo_id, caption)
            bot.send_message(message.chat.id, 'Если хочешь повторить поиск - /sport. Для возврата в меню знакомств - /new_friends.')
            break


@bot.message_handler(commands=["healthyhealth"])
def healthyhealth(message):
    general_file = open("general_data.txt", "r", encoding="utf-8")
    line = general_file.read()
    array = line.split("\n")
    for i in array:
        temp = random.randint(0, len(array) - 1)
        tempp = array[temp]
        tempp_split = tempp.split("@")
        name = tempp_split[0]
        sex = tempp_split[1]
        age = tempp_split[2]
        direction = tempp_split[3]
        status = "Статус: " + tempp_split[4]
        bio = tempp_split[5]
        photo_id = tempp_split[6]
        username = tempp_split[7]
        caption = (
            name
            + "\n"
            + sex
            + "\n"
            + age
            + "\n"
            + direction
            + "\n"
            + status
            + "\n"
            + bio
            + "\n"
            + "@"
            + username
        )
        if direction == "Здоровый образ жизни":
            bot.send_photo(message.chat.id, photo_id, caption)
            bot.send_message(message.chat.id, 'Если хочешь повторить поиск - /healthyhealth. Для возврата в меню знакомств - /new_friends.')
            break


@bot.message_handler(commands=["media"])
def media(message):
    general_file = open("general_data.txt", "r", encoding="utf-8")
    line = general_file.read()
    array = line.split("\n")
    for i in array:
        temp = random.randint(0, len(array) - 1)
        tempp = array[temp]
        tempp_split = tempp.split("@")
        name = tempp_split[0]
        sex = tempp_split[1]
        age = tempp_split[2]
        direction = tempp_split[3]
        status = "Статус: " + tempp_split[4]
        bio = tempp_split[5]
        photo_id = tempp_split[6]
        username = tempp_split[7]
        caption = (
            name
            + "\n"
            + sex
            + "\n"
            + age
            + "\n"
            + direction
            + "\n"
            + status
            + "\n"
            + bio
            + "\n"
            + "@"
            + username
        )
        if direction == "Медиа и коммуникации":
            bot.send_photo(message.chat.id, photo_id, caption)
            bot.send_message(message.chat.id, 'Если хочешь повторить поиск - /media. Для возврата в меню знакомств - /new_friends.')
            break


@bot.message_handler(commands=["diplomatism"])
def diplomatism(message):
    general_file = open("general_data.txt", "r", encoding="utf-8")
    line = general_file.read()
    array = line.split("\n")
    for i in array:
        temp = random.randint(0, len(array) - 1)
        tempp = array[temp]
        tempp_split = tempp.split("@")
        name = tempp_split[0]
        sex = tempp_split[1]
        age = tempp_split[2]
        direction = tempp_split[3]
        status = "Статус: " + tempp_split[4]
        bio = tempp_split[5]
        photo_id = tempp_split[6]
        username = tempp_split[7]
        caption = (
            name
            + "\n"
            + sex
            + "\n"
            + age
            + "\n"
            + direction
            + "\n"
            + status
            + "\n"
            + bio
            + "\n"
            + "@"
            + username
        )
        if direction == "Дипломатизм и международные отношения":
            bot.send_photo(message.chat.id, photo_id, caption)
            bot.send_message(message.chat.id, 'Если хочешь повторить поиск - /diplomatism. Для возврата в меню знакомств - /new_friends.')
            break


@bot.message_handler(commands=["ecology"])
def ecology(message):
    general_file = open("general_data.txt", "r", encoding="utf-8")
    line = general_file.read()
    array = line.split("\n")
    for i in array:
        temp = random.randint(0, len(array) - 1)
        tempp = array[temp]
        tempp_split = tempp.split("@")
        name = tempp_split[0]
        sex = tempp_split[1]
        age = tempp_split[2]
        direction = tempp_split[3]
        status = "Статус: " + tempp_split[4]
        bio = tempp_split[5]
        photo_id = tempp_split[6]
        username = tempp_split[7]
        caption = (
            name
            + "\n"
            + sex
            + "\n"
            + age
            + "\n"
            + direction
            + "\n"
            + status
            + "\n"
            + bio
            + "\n"
            + "@"
            + username
        )
        if direction == "Экология и охрана природы":
            bot.send_photo(message.chat.id, photo_id, caption)
            bot.send_message(message.chat.id, 'Если хочешь повторить поиск - /ecology. Для возврата в меню знакомств - /new_friends.')
            break


@bot.message_handler(commands=["tourism"])
def tourism(message):
    general_file = open("general_data.txt", "r", encoding="utf-8")
    line = general_file.read()
    array = line.split("\n")
    for i in array:
        temp = random.randint(0, len(array) - 1)
        tempp = array[temp]
        tempp_split = tempp.split("@")
        name = tempp_split[0]
        sex = tempp_split[1]
        age = tempp_split[2]
        direction = tempp_split[3]
        status = "Статус: " + tempp_split[4]
        bio = tempp_split[5]
        photo_id = tempp_split[6]
        username = tempp_split[7]
        caption = (
            name
            + "\n"
            + sex
            + "\n"
            + age
            + "\n"
            + direction
            + "\n"
            + status
            + "\n"
            + bio
            + "\n"
            + "@"
            + username
        )
        if direction == "Туризм и путешествия":
            bot.send_photo(message.chat.id, photo_id, caption)
            bot.send_message(message.chat.id, 'Если хочешь повторить поиск - /tourism. Для возврата в меню знакомств - /new_friends.')
            break


@bot.message_handler(commands=["show_profile"])
def show_profile(message):
    general_file = open("general_data.txt", "r", encoding="utf-8")
    username = message.from_user.username
    temp = ""
    line = general_file.read()
    array = line.split("\n")
    for i in array:
        if username in i:
            temp = i
    profile_split = temp.split("@")
    name = profile_split[0]
    sex = profile_split[1]
    age = profile_split[2]
    direction = profile_split[3]
    status = "Статус: " + profile_split[4]
    bio = profile_split[5]
    photo_id = profile_split[6]
    caption = (
        name
        + "\n"
        + sex
        + "\n"
        + age
        + "\n"
        + direction
        + "\n"
        + status
        + "\n"
        + bio
        + "\n"
        + "@"
        + username
    )
    bot.send_photo(message.chat.id, photo_id, caption)


@bot.message_handler(commands=["contacts"])
def contacts(message):
    bot.send_message(
        message.chat.id,
        "Тут контакты тех, к кому ты можешь обратиться по любому вопросу, они всегда помогут!\
	\n\nАнастасия Аксенова - комьюнити-менеджер сообщества - @hey_nastyaaa\
	\nАнастасия Елецкая - старший комьюнити-менеджер - @EletskayaN\
	\nСевда Миралиева - координатор акселератора - @s_miralieva\
	\n\nКоманда Хранителей атмосферы чата:\
	\nМатвей - @MtBb11\
	\nСоня - @sonysska\
	\nVioletta - @Violettzzz\
	\nАрсений - @chelovek0125\
	\nМария - @majezepr\
	\nНадежда - @Googbeste\
	\nАриша - @rinvilo\
	\n\nИ, конечно же, команда разработчиков бота:\
	\nДима - разработчик бота - @chuuuchin\
	\nВика - старший администратор - @wisac\
	\nРегина - менеджер - @rrrrrrega\
	\nМатвей - @MtBb11",
    )


@bot.message_handler(commands=["links"])
def links(message):
    bot.send_message(
        message.chat.id,
        'Основной чат "Движение первых | Москва" - https://t.me/mypervie77_chat\
                    \nОфициальный канал "Движение Первых" - https://t.me/rddm_official\
                    \nОфициальное сообщество ВК - https://vk.com/rddm_official\
                    \nНавигация по чату - https://t.me/mypervie77_chat/79626/120868\
                    \nЧто можно, а что нельзя размещать в чате - https://t.me/mypervie77_chat/79626/126733\
                    \nПравила чата - https://t.me/mypervie77_chat/79626/126737\
                    \nХэштеги Движения - \
                    \nВступить в Движение - https://будьвдвижении.рф/',
    )


@bot.message_handler(commands=["update_status"])
def update_status(message):
    general_file = open("general_data.txt", "r", encoding="utf-8")
    line = general_file.read()
    array = line.split("\n")
    for i in array:
        if message.from_user.username in i:
            temp = i.split("@")
            status = temp[4]
            new_status = bot.send_message(
                message.chat.id,
                "Сейчас твой статус такой: "
                + status
                + ". В следующем сообщении напиши, на что ты его хочешь поменять.",
            )
            bot.register_next_step_handler(new_status, update_status1)


def update_status1(message):
    new_status = message.text
    general_file = open("general_data.txt", "r", encoding="utf-8")
    line = general_file.read()
    array = line.split("\n")
    for i in array:
        if message.from_user.username in i:
            temp = i.split("@")
            old_status = temp[4]
            general_file_write = open("general_data.txt", "wt", encoding="utf-8")
            i = i.replace(str(old_status), str(new_status))
            general_file_write.write(i)
            bot.send_message(
                message.chat.id, "Готово! Теперь твой статус такой: " + new_status
            )


@bot.message_handler(commands=["faq"])
def faq(message):
    bot.send_message(
        message.chat.id,
        "1. В: Что делать, если у меня неполадки с ботом?\nО: Писать менеджерам, вот их контакты: @wisac, @rrrrrrega, @nyusha_tsukiri.\
  \n\n2. В: Где можно посмотреть новые проекты Движения?\nО: Следи за обновлениями и новыми проектами Движения можно в нашем чате движения первых: будьвдвижении.рф.\
  \n\n3. В: Как искать новых друзей?\nО: Найти друзей можно через команду /new_friends. Там ты сможешь выбрать, как именно искать друзей: анонимно, по полу или по интересам.\
  \n\n4. В: Как поменять информацию о себе?\nО: Для этого вызови функцию /edit_data и выбери, что именно ты хочешь поменять.",
    )


@bot.message_handler(commands=["feedback"])
def feedback(message):
    question = bot.send_message(
        message.chat.id,
        "В сообщении напиши свой вопрос, предложение или пожелание, и оно попадёт к разработчикам!",
    )
    bot.register_next_step_handler(question, feedback1)


def feedback1(message):
    bot.send_message(
        -1001958306887,
        "Вопрос, пожелание или предложение: "
        + message.text
        + ", "
        + str(message.from_user.id),
    )
    bot.send_message(message.chat.id, "Готово, твой вопрос отправился к разработчикам!")


@bot.message_handler(commands=["answer"])
def answer(message):
    if (
        message.from_user.username == "chuuuchin"
        or message.from_user.username == "wisac"
        or message.from_user.username == "rrrrrrega"
    ):
        answer = bot.send_message(
            message.chat.id,
            "В первой строчке введи id пользователя, во второй - ответ на вопрос.",
        )
        bot.register_next_step_handler(answer, answer1)
    else:
        bot.send_message(
            message.chat.id,
            "Ты не можешь использовать эту команду, т.к. ты не админ. Если ты админ, но команда не работает, сделай фидбэк и включи в него @chuuuchin. Таким образом, главный разработчик увидит твой вопрос с вероятностью 100%.",
        )


def answer1(message):
    data = message.text
    answer_data = data.split("\n")
    idd = answer_data[0]
    answerr = answer_data[1]
    bot.send_message(message.chat.id, str(answerr))
    bot.send_message(idd, answerr)


@bot.message_handler(commands=["edit_data"])
def edit_data(message):
    bot.send_message(
        message.chat.id,
        "Напиши, что ты хочешь изменить в своём профиле, в таком формате:\n\
Хочу изменить\n\
Ваше имя пользователя (@...)\n\
Имя/Возраст/Направление/Биография\n\
Новое имя/возраст/направление/биография",
    )
    data = bot.send_message(
        message.chat.id,
        "Если хочешь изменить аватарку, то запусти /change_profile_photo",
    )
    bot.register_next_step_handler(data, edit_data1)


def edit_data1(message):
    bot.send_message(-1001958306887, message.text)
    bot.send_message(
        message.chat.id,
        "Твоя заявка отправилась модераторам, скоро твой профиль изменится!",
    )


@bot.message_handler(commands=["change_profile_photo"])
def change_profile_picture(message):
    data = bot.send_message(
        message.chat.id,
        "Выбери свою новую аватарку из галереи и в подписи напиши своё имя пользователя (@...).",
    )
    bot.register_next_step_handler(data, change_profile_picture1)


def change_profile_picture1(message):
    nick = str(message.caption)
    photo = max(message.photo, key=lambda x: x.height)
    bot.send_photo(-1001958306887, photo.file_id, nick)
    bot.send_message(
        message.chat.id,
        "Твоя заявка отправилась модераторам, скоро твоя аватарка изменится!",
    )


bot.polling(none_stop=True, interval=0)
