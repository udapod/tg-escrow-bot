"""
Мультиязычная система переводов для HandshakeDealBot.
Поддерживаемые языки: ru (русский), uz (o'zbek), kk (қазақша).
"""

LANGS = {
    "ru": "🇷🇺 Русский",
    "uz": "🇺🇿 O'zbek",
    "kk": "🇰🇿 Қазақша",
    "tr": "🇹🇷 Türkçe",
    "tg": "🇹🇯 Тоҷикӣ",
    "ky": "🇰🇬 Кыргызча",
    "en": "🇺🇸 English",
}

# ————— Все переводы —————

TEXTS = {
    # ===== КНОПКИ МЕНЮ =====
    "btn_catalog": {
        "ru": "📋 Каталог",
        "uz": "📋 Katalog",
        "kk": "📋 Каталог",
        "tr": "📋 Katalog",
        "tg": "📋 Каталог",
        "ky": "📋 Каталог",
    },
    "btn_create_listing": {
        "ru": "➕ Создать объявление",
        "uz": "➕ E'lon yaratish",
        "kk": "➕ Хабарландыру жасау",
        "tr": "➕ İlan oluştur",
        "tg": "➕ Эълон сохтан",
        "ky": "➕ Жарнама түзүү",
    },
    "btn_my_deals": {
        "ru": "📦 Мои сделки",
        "uz": "📦 Bitimlarim",
        "kk": "📦 Мәмілелерім",
        "tr": "📦 İşlemlerim",
        "tg": "📦 Муомилаҳоям",
        "ky": "📦 Келишимдерим",
    },
    "btn_my_listings": {
        "ru": "📝 Мои объявления",
        "uz": "📝 E'lonlarim",
        "kk": "📝 Хабарландыруларым",
        "tr": "📝 İlanlarım",
        "tg": "📝 Эълонҳоям",
        "ky": "📝 Жарнамаларым",
    },
    "btn_vip": {
        "ru": "👑 VIP-подписка",
        "uz": "👑 VIP-obuna",
        "kk": "👑 VIP-жазылым",
        "tr": "👑 VIP-abonelik",
        "tg": "👑 VIP-обуна",
        "ky": "👑 VIP-жазылуу",
    },
    "btn_profile": {
        "ru": "👤 Профиль",
        "uz": "👤 Profil",
        "kk": "👤 Профиль",
        "tr": "👤 Profil",
        "tg": "👤 Профил",
        "ky": "👤 Профиль",
    },
    "btn_search": {
        "ru": "🔍 Поиск",
        "uz": "🔍 Qidirish",
        "kk": "🔍 Іздеу",
        "tr": "🔍 Arama",
        "tg": "🔍 Ҷустуҷӯ",
        "ky": "🔍 Издөө",
    },
    "btn_help": {
        "ru": "ℹ️ Помощь",
        "uz": "ℹ️ Yordam",
        "kk": "ℹ️ Көмек",
        "tr": "ℹ️ Yardım",
        "tg": "ℹ️ Кӯмак",
        "ky": "ℹ️ Жардам",
    },

    # ===== КНОПКИ INLINE =====
    "btn_start_deal": {
        "ru": "🤝 Начать сделку",
        "uz": "🤝 Bitim boshlash",
        "kk": "🤝 Мәміле бастау",
    },
    "btn_seller_profile": {
        "ru": "👤 Профиль продавца",
        "uz": "👤 Sotuvchi profili",
        "kk": "👤 Сатушы профилі",
    },
    "btn_i_sent_usdt": {
        "ru": "💰 Я отправил USDT на эскроу",
        "uz": "💰 USDT eskroga yubordim",
        "kk": "💰 USDT эскроуға жібердім",
    },
    "btn_cancel_deal": {
        "ru": "❌ Отменить сделку",
        "uz": "❌ Bitimni bekor qilish",
        "kk": "❌ Мәмілені болдырмау",
    },
    "btn_order_done": {
        "ru": "📦 Заказ выполнен / Товар отправлен",
        "uz": "📦 Buyurtma bajarildi / Tovar yuborildi",
        "kk": "📦 Тапсырыс орындалды / Тауар жіберілді",
    },
    "btn_open_dispute": {
        "ru": "⚠️ Открыть спор",
        "uz": "⚠️ Da'vo ochish",
        "kk": "⚠️ Дау ашу",
    },
    "btn_confirm_received": {
        "ru": "✅ Подтверждаю получение",
        "uz": "✅ Qabul qildim",
        "kk": "✅ Алғанымды растаймын",
    },
    "btn_leave_review": {
        "ru": "⭐ Оставить отзыв",
        "uz": "⭐ Sharh qoldirish",
        "kk": "⭐ Пікір қалдыру",
    },
    "btn_yes": {
        "ru": "✅ Да",
        "uz": "✅ Ha",
        "kk": "✅ Иә",
    },
    "btn_no": {
        "ru": "❌ Нет",
        "uz": "❌ Yo'q",
        "kk": "❌ Жоқ",
    },
    "btn_delete_listing": {
        "ru": "🗑 Удалить объявление",
        "uz": "🗑 E'lonni o'chirish",
        "kk": "🗑 Хабарландыруды жою",
    },
    "btn_back_menu": {
        "ru": "⬅️ В меню",
        "uz": "⬅️ Menyu",
        "kk": "⬅️ Мәзірге",
    },
    "btn_buy_vip": {
        "ru": "👑 Купить VIP-подписку",
        "uz": "👑 VIP-obuna sotib olish",
        "kk": "👑 VIP-жазылым сатып алу",
    },
    "btn_i_paid_vip": {
        "ru": "💰 Я оплатил VIP",
        "uz": "💰 VIP uchun to'ladim",
        "kk": "💰 VIP үшін төледім",
    },
    "btn_cancel": {
        "ru": "❌ Отмена",
        "uz": "❌ Bekor qilish",
        "kk": "❌ Болдырмау",
    },

    # ===== КАТЕГОРИИ =====
    "cat_goods": {
        "ru": "🛒 Товары",
        "uz": "🛒 Tovarlar",
        "kk": "🛒 Тауарлар",
    },
    "cat_services": {
        "ru": "🔧 Услуги",
        "uz": "🔧 Xizmatlar",
        "kk": "🔧 Қызметтер",
    },

    # ===== /start =====
    "welcome": {
        "ru": (
            "🤝 <b>Добро пожаловать в HandshakeDeal!</b>\n\n"
            "🔐 <b>Надёжный эскроу-гарант</b> для P2P-сделок.\n"
            "Покупайте и продавайте товары и услуги без риска!\n\n"
            "🛡 <b>Как это работает:</b>\n"
            "1️⃣ Продавец создаёт объявление\n"
            "2️⃣ Покупатель отправляет USDT на <b>эскроу-кошелёк бота</b>\n"
            "3️⃣ 🔓 Контакты разблокируются — можно договориться о встрече\n"
            "4️⃣ Покупатель подтверждает получение\n"
            "5️⃣ Средства отправляются продавцу ⭐\n\n"
            "🎁 <b>Первая сделка без комиссии!</b>\n"
            "❗ При отмене после оплаты удерживается штраф 2%.\n\n"
            "Используйте меню ниже 👇"
        ),
        "uz": (
            "🤝 <b>HandshakeDeal'ga xush kelibsiz!</b>\n\n"
            "🔐 <b>Ishonchli eskrou-kafolat</b> P2P-bitimlar uchun.\n"
            "Tovar va xizmatlarni xavfsiz sotib oling va soting!\n\n"
            "🛡 <b>Qanday ishlaydi:</b>\n"
            "1️⃣ Sotuvchi e'lon yaratadi\n"
            "2️⃣ Xaridor USDT ni <b>bot eskrou-hamyoniga</b> yuboradi\n"
            "3️⃣ 🔓 Kontaktlar ochiladi — uchrashuvni kelishish mumkin\n"
            "4️⃣ Xaridor qabul qilganini tasdiqlaydi\n"
            "5️⃣ Mablag' sotuvchiga yuboriladi ⭐\n\n"
            "🎁 <b>Birinchi bitim komissiyasiz!</b>\n"
            "❗ To'lovdan keyin bekor qilinsa 2% jarima ushlanadi.\n\n"
            "Quyidagi menyudan foydalaning 👇"
        ),
        "kk": (
            "🤝 <b>HandshakeDeal-ға қош келдіңіз!</b>\n\n"
            "🔐 <b>Сенімді эскроу-кепілдік</b> P2P-мәмілелер үшін.\n"
            "Тауарлар мен қызметтерді қауіпсіз сатып алыңыз!\n\n"
            "🛡 <b>Қалай жұмыс істейді:</b>\n"
            "1️⃣ Сатушы хабарландыру жасайды\n"
            "2️⃣ Сатып алушы USDT-ні <b>бот эскроу-әмиянына</b> жібереді\n"
            "3️⃣ 🔓 Байланыстар ашылады — кездесуді келісуге болады\n"
            "4️⃣ Сатып алушы алғанын растайды\n"
            "5️⃣ Қаражат сатушыға жіберіледі ⭐\n\n"
            "🎁 <b>Бірінші мәміле комиссиясыз!</b>\n"
            "❗ Төлемнен кейін болдырмаса 2% айыппұл ұсталады.\n\n"
            "Төмендегі мәзірді пайдаланыңыз 👇"
        ),
    },

    # ===== Выбор языка =====
    "choose_lang": {
        "ru": "🌐 Выберите язык / Tilni tanlang / Тілді таңдаңыз:",
        "uz": "🌐 Выберите язык / Tilni tanlang / Тілді таңдаңыз:",
        "kk": "🌐 Выберите язык / Tilni tanlang / Тілді таңдаңыз:",
    },
    "lang_set": {
        "ru": "✅ Язык установлен: Русский",
        "uz": "✅ Til tanlandi: O'zbek",
        "kk": "✅ Тіл таңдалды: Қазақша",
        "tr": "✅ Dil seçildi: Türkçe",
        "tg": "✅ Забон интихоб шуд: Тоҷикӣ",
        "ky": "✅ Тил тандалды: Кыргызча",
    },

    # ===== ВЫБОР МЕСТОПОЛОЖЕНИЯ =====
    "choose_country": {
        "ru": "🌍 Выберите вашу страну:",
        "uz": "🌍 Davlatingizni tanlang:",
        "kk": "🌍 Еліңізді таңдаңыз:",
    },
    "choose_city": {
        "ru": "🏙 Выберите ваш город ({country}):",
        "uz": "🏙 Shahringizni tanlang ({country}):",
        "kk": "🏙 Қалаңызды таңдаңыз ({country}):",
    },
    "city_other": {
        "ru": "📝 Другой город",
        "uz": "📝 Boshqa shahar",
        "kk": "📝 Басқа қала",
    },
    "enter_city_manual": {
        "ru": "✏️ Введите название вашего города:",
        "uz": "✏️ Shahringiz nomini kiriting:",
        "kk": "✏️ Қалаңыздың атын енгізіңіз:",
    },
    "city_too_short": {
        "ru": "❗ Слишком короткое название. Введите название города (2-50 символов):",
        "uz": "❗ Nom juda qisqa. Shahar nomini kiriting (2-50 belgi):",
        "kk": "❗ Атауы тым қысқа. Қала атын енгізіңіз (2-50 таңба):",
    },
    "location_set": {
        "ru": "📍 Местоположение: {country}, {city}",
        "uz": "📍 Joylashuv: {country}, {city}",
        "kk": "📍 Орналасқан жері: {country}, {city}",
    },
    "btn_change_location": {
        "ru": "📍 Сменить город",
        "uz": "📍 Shaharni o'zgartirish",
        "kk": "📍 Қаланы өзгерту",
        "tr": "📍 Şehir değiştir",
        "tg": "📍 Шаҳрро иваз кардан",
        "ky": "📍 Шаарды өзгөртүү",
    },
    "profile_location": {
        "ru": "📍 Город",
        "uz": "📍 Shahar",
        "kk": "📍 Қала",
    },
    "location_not_set": {
        "ru": "не указан",
        "uz": "ko'rsatilmagan",
        "kk": "көрсетілмеген",
    },
    "set_location_first": {
        "ru": "📍 Сначала укажите местоположение — нажмите /location",
        "uz": "📍 Avval joylashuvni ko'rsating — /location bosing",
        "kk": "📍 Алдымен орналасуды көрсетіңіз — /location басыңыз",
    },
    "listing_city": {
        "ru": "📍 Город",
        "uz": "📍 Shahar",
        "kk": "📍 Қала",
    },
    "all_cities": {
        "ru": "🌐 Все города",
        "uz": "🌐 Barcha shaharlar",
        "kk": "🌐 Барлық қалалар",
    },

    # ===== ЧАТ СДЕЛКИ =====
    "btn_chat": {
        "ru": "💬 Чат сделки",
        "uz": "💬 Bitim chati",
        "kk": "💬 Мәміле чаты",
    },
    "chat_role_seller": {
        "ru": "продавцом",
        "uz": "sotuvchi",
        "kk": "сатушымен",
    },
    "chat_role_buyer": {
        "ru": "покупателем",
        "uz": "xaridor",
        "kk": "сатып алушымен",
    },
    "chat_msg_from_buyer": {
        "ru": "💬 <b>Покупатель</b> (сделка #{id}):\n{text}",
        "uz": "💬 <b>Xaridor</b> (bitim #{id}):\n{text}",
        "kk": "💬 <b>Сатып алушы</b> (мәміле #{id}):\n{text}",
    },
    "chat_msg_from_seller": {
        "ru": "💬 <b>Продавец</b> (сделка #{id}):\n{text}",
        "uz": "💬 <b>Sotuvchi</b> (bitim #{id}):\n{text}",
        "kk": "💬 <b>Сатушы</b> (мәміле #{id}):\n{text}",
    },
    "chat_contact_blocked": {
        "ru": "🚫 Контактные данные (телефон, @username, ссылки) заблокированы до оплаты на эскроу.\nПосле оплаты они будут разблокированы автоматически.",
        "uz": "🚫 Kontakt ma'lumotlari (telefon, @username, havolalar) to'lovgacha bloklangan.\nTo'lovdan keyin avtomatik ochiladi.",
        "kk": "🚫 Байланыс деректері (телефон, @username, сілтемелер) төлемге дейін бұғатталған.\nТөлемнен кейін автоматты түрде ашылады.",
    },
    "chat_sent": {
        "ru": "✅ Отправлено",
        "uz": "✅ Yuborildi",
        "kk": "✅ Жіберілді",
    },
    "chat_exited": {
        "ru": "👋 Вы вышли из чата сделки.",
        "uz": "👋 Siz bitim chatidan chiqdingiz.",
        "kk": "👋 Сіз мәміле чатынан шықтыңыз.",
    },
    "chat_no_deal": {
        "ru": "❗ Сделка не найдена или уже завершена.",
        "uz": "❗ Bitim topilmadi yoki tugallangan.",
        "kk": "❗ Мәміле табылмады немесе аяқталған.",
    },
    "chat_history_title": {
        "ru": "📜 <b>История переписки — сделка #{id}</b>\n",
        "uz": "📜 <b>Yozishmalar tarixi — bitim #{id}</b>\n",
        "kk": "📜 <b>Хат алмасу тарихы — мәміле #{id}</b>\n",
    },
    "chat_history_empty": {
        "ru": "📜 Переписка по сделке #{id} пуста.",
        "uz": "📜 Bitim #{id} bo'yicha yozishmalar yo'q.",
        "kk": "📜 Мәміле #{id} бойынша хат алмасу жоқ.",
    },
    "btn_view_chat_history": {
        "ru": "📜 Переписка",
        "uz": "📜 Yozishmalar",
        "kk": "📜 Хат алмасу",
    },

    # ===== ВСТРЕЧА =====
    "btn_propose_meet": {
        "ru": "📍 Предложить встречу",
        "uz": "📍 Uchrashuv taklif qilish",
        "kk": "📍 Кездесу ұсыну",
    },
    "meet_enter_location": {
        "ru": "📍 Укажите место встречи (адрес, ориентир, ТЦ и т.д.):",
        "uz": "📍 Uchrashuv joyini kiriting (manzil, mo'ljal, SM va h.k.):",
        "kk": "📍 Кездесу орнын көрсетіңіз (мекенжай, бағдар, СО т.б.):",
    },
    "meet_enter_datetime": {
        "ru": "🕐 Укажите дату и время встречи (например: завтра в 15:00, 20.03 в 12:00):",
        "uz": "🕐 Uchrashuv sanasi va vaqtini kiriting (masalan: ertaga 15:00, 20.03 da 12:00):",
        "kk": "🕐 Кездесу күні мен уақытын көрсетіңіз (мысалы: ертең 15:00, 20.03 12:00):",
    },
    "meet_proposal_sent": {
        "ru": "✅ Предложение о встрече отправлено!",
        "uz": "✅ Uchrashuv taklifi yuborildi!",
        "kk": "✅ Кездесу ұсынысы жіберілді!",
    },
    "meet_proposal_card": {
        "ru": (
            "📍 <b>Предложение встречи — сделка #{id}</b>\n\n"
            "🏠 Место: <b>{location}</b>\n"
            "🕐 Время: <b>{datetime}</b>\n\n"
            "Ответьте в чате сделки, если хотите изменить время/место."
        ),
        "uz": (
            "📍 <b>Uchrashuv taklifi — bitim #{id}</b>\n\n"
            "🏠 Joy: <b>{location}</b>\n"
            "🕐 Vaqt: <b>{datetime}</b>\n\n"
            "Vaqt/joyni o'zgartirmoqchi bo'lsangiz, bitim chatida javob yozing."
        ),
        "kk": (
            "📍 <b>Кездесу ұсынысы — мәміле #{id}</b>\n\n"
            "🏠 Орын: <b>{location}</b>\n"
            "🕐 Уақыт: <b>{datetime}</b>\n\n"
            "Уақытты/орынды өзгерткіңіз келсе, мәміле чатында жауап жазыңыз."
        ),
    },
    "meet_cancelled": {
        "ru": "❌ Предложение встречи отменено. Вы вернулись в чат.",
        "uz": "❌ Uchrashuv taklifi bekor qilindi. Chatga qaytdingiz.",
        "kk": "❌ Кездесу ұсынысы бас тартылды. Чатқа оралдыңыз.",
    },
    "chat_enter": {
        "ru": (
            "💬 <b>Чат сделки #{id}</b>\n\n"
            "Вы общаетесь с {role} анонимно.\n"
            "Пишите сообщения — бот перешлёт их.\n\n"
            "📍 /meet — предложить встречу\n"
            "/endchat — выйти из чата"
        ),
        "uz": (
            "💬 <b>Bitim chati #{id}</b>\n\n"
            "Siz {role} bilan anonim muloqot qilmoqdasiz.\n"
            "Xabar yozing — bot uzatadi.\n\n"
            "📍 /meet — uchrashuv taklif qilish\n"
            "/endchat — chatdan chiqish"
        ),
        "kk": (
            "💬 <b>Мәміле чаты #{id}</b>\n\n"
            "Сіз {role} анонимді сөйлесесіз.\n"
            "Хабар жазыңыз — бот жібереді.\n\n"
            "📍 /meet — кездесу ұсыну\n"
            "/endchat — чаттан шығу"
        ),
    },

    # ===== /help =====
    "help": {
        "ru": (
            "📖 <b>Правила и условия HandshakeDeal</b>\n\n"
            "📝 <b>Основные функции:</b>\n"
            "📋 <b>Каталог</b> — просмотр объявлений в вашем городе\n"
            "➕ <b>Создать объявление</b> — разместить товар/услугу\n"
            "📦 <b>Мои сделки</b> — текущие и завершённые сделки\n"
            "👤 <b>Профиль</b> — рейтинг, кошелёк, статистика\n\n"

            "🔐 <b>Эскроу-гарант:</b>\n"
            "• Покупатель отправляет USDT на кошелёк бота\n"
            "• Деньги заморожены до подтверждения получения\n"
            "• Продавец получает средства только после завершения\n"
            "• Авто-завершение через 72ч если нет спора\n"
            "• Спор = заморозка до решения админа\n\n"

            "💰 <b>Комиссии (прогрессивная шкала):</b>\n"
            "• 🎁 Первая сделка — <b>без комиссии (0%)</b>\n"
            "• 20–100 USDT — <b>3%</b> (мин. 2 USDT)\n"
            "• 100–500 USDT — <b>2%</b>\n"
            "• 500+ USDT — <b>1.5%</b>\n"
            "• 👑 VIP — вдвое меньше: 1.5% / 1% / 0.75% (мин. 1 USDT)\n"
            "• 👑 VIP-подписка — <b>10 USDT</b>/мес\n"
            "• Минимальная сумма сделки — <b>20 USDT</b>\n\n"

            "💬 <b>Чат сделки:</b>\n"
            "• До оплаты — анонимный чат (контакты заблокированы)\n"
            "• После оплаты — 🔓 контакты разблокированы\n"
            "• Можно обмениваться телефонами, адресами\n"
            "• 📍 /meet — предложить встречу\n\n"

            "⚠️ <b>Отмена сделки:</b>\n"
            "• До оплаты — бесплатна\n"
            "• После оплаты — <b>штраф 2%</b> от суммы эскроу\n"
            "• Остаток возвращается покупателю\n\n"

            "💱 Все транзакции в USDT (TRC-20).\n"
            "📱 /qr — QR-код для приглашения друзей\n"
            "Поддержка: /support"
        ),
        "uz": (
            "📖 <b>HandshakeDeal qoidalari va shartlari</b>\n\n"
            "📝 <b>Asosiy funksiyalar:</b>\n"
            "📋 <b>Katalog</b> — shahringizdagi e'lonlarni ko'rish\n"
            "➕ <b>E'lon yaratish</b> — tovar/xizmat joylashtirish\n"
            "📦 <b>Bitimlarim</b> — joriy va tugallangan bitimlar\n"
            "👤 <b>Profil</b> — reyting, hamyon, statistika\n\n"

            "🔐 <b>Eskrou-kafolat:</b>\n"
            "• Xaridor USDT ni bot hamyoniga yuboradi\n"
            "• Pul qabul qilingunga qadar muzlatiladi\n"
            "• Sotuvchi faqat bitim tugagandan keyin pul oladi\n"
            "• 72 soatdan keyin avtomatik tugallanadi\n"
            "• Da'vo = admin qaroriga qadar muzlatish\n\n"

            "💰 <b>Komissiya (progressiv shkala):</b>\n"
            "• 🎁 Birinchi bitim — <b>komissiyasiz (0%)</b>\n"
            "• 20–100 USDT — <b>3%</b> (min. 2 USDT)\n"
            "• 100–500 USDT — <b>2%</b>\n"
            "• 500+ USDT — <b>1.5%</b>\n"
            "• 👑 VIP — ikki baravar kam: 1.5% / 1% / 0.75% (min. 1 USDT)\n"
            "• 👑 VIP-obuna — <b>10 USDT</b>/oy\n"
            "• Minimal bitim summasi — <b>20 USDT</b>\n\n"

            "💬 <b>Bitim chati:</b>\n"
            "• To'lovdan oldin — anonim chat (kontaktlar bloklangan)\n"
            "• To'lovdan keyin — 🔓 kontaktlar ochiq\n"
            "• Telefon, manzil almashish mumkin\n"
            "• 📍 /meet — uchrashuv taklif qilish\n\n"

            "⚠️ <b>Bitimni bekor qilish:</b>\n"
            "• To'lovdan oldin — bepul\n"
            "• To'lovdan keyin — <b>2% jarima</b>\n"
            "• Qolgan mablag' xaridorga qaytariladi\n\n"

            "💱 Barcha tranzaksiyalar USDT (TRC-20) da.\n"
            "📱 /qr — Do'stlarni taklif qilish uchun QR-kod\n"
            "Qo'llab-quvvatlash: /support"
        ),
        "kk": (
            "📖 <b>HandshakeDeal ережелері мен шарттары</b>\n\n"
            "📝 <b>Негізгі функциялар:</b>\n"
            "📋 <b>Каталог</b> — қалаңыздағы хабарландыруларды қарау\n"
            "➕ <b>Хабарландыру жасау</b> — тауар/қызмет орналастыру\n"
            "📦 <b>Мәмілелерім</b> — ағымдағы және аяқталған мәмілелер\n"
            "👤 <b>Профиль</b> — рейтинг, әмиян, статистика\n\n"

            "🔐 <b>Эскроу-кепілдік:</b>\n"
            "• Сатып алушы USDT-ні бот әмиянына жібереді\n"
            "• Ақша алғанша мұздатылады\n"
            "• Сатушы тек мәміле аяқталғаннан кейін ақша алады\n"
            "• 72 сағаттан кейін автоматты аяқталады\n"
            "• Дау = әкімші шешіміне дейін мұздату\n\n"

            "💰 <b>Комиссия (прогрессивті шкала):</b>\n"
            "• 🎁 Бірінші мәміле — <b>комиссиясыз (0%)</b>\n"
            "• 20–100 USDT — <b>3%</b> (мин. 2 USDT)\n"
            "• 100–500 USDT — <b>2%</b>\n"
            "• 500+ USDT — <b>1.5%</b>\n"
            "• 👑 VIP — екі есе аз: 1.5% / 1% / 0.75% (мин. 1 USDT)\n"
            "• 👑 VIP-жазылым — <b>10 USDT</b>/ай\n"
            "• Минималды мәміле сомасы — <b>20 USDT</b>\n\n"

            "💬 <b>Мәміле чаты:</b>\n"
            "• Төлемге дейін — аноним чат (байланыстар бұғатталған)\n"
            "• Төлемнен кейін — 🔓 байланыстар ашық\n"
            "• Телефон, мекенжай алмасуға болады\n"
            "• 📍 /meet — кездесу ұсыну\n\n"

            "⚠️ <b>Мәмілені болдырмау:</b>\n"
            "• Төлемге дейін — тегін\n"
            "• Төлемнен кейін — <b>2% айыппұл</b>\n"
            "• Қалған қаражат сатып алушыға қайтарылады\n\n"

            "💱 Барлық транзакциялар USDT (TRC-20).\n"
            "📱 /qr — Достарды шақыру үшін QR-код\n"
            "Қолдау: /support"
        ),
    },

    # ===== Профиль =====
    "profile_title": {
        "ru": "👤 <b>Ваш профиль</b>",
        "uz": "👤 <b>Sizning profilingiz</b>",
        "kk": "👤 <b>Сіздің профиліңіз</b>",
    },
    "profile_vip_status": {
        "ru": "👑 Статус: <b>Верифицирован (VIP)</b>",
        "uz": "👑 Status: <b>Tasdiqlangan (VIP)</b>",
        "kk": "👑 Мәртебе: <b>Расталған (VIP)</b>",
    },
    "profile_id": {"ru": "🆔 ID", "uz": "🆔 ID", "kk": "🆔 ID"},
    "profile_name": {"ru": "📛 Имя", "uz": "📛 Ism", "kk": "📛 Аты"},
    "profile_rating": {"ru": "⭐ Рейтинг", "uz": "⭐ Reyting", "kk": "⭐ Рейтинг"},
    "profile_deals": {
        "ru": "📦 Завершённых сделок",
        "uz": "📦 Tugallangan bitimlar",
        "kk": "📦 Аяқталған мәмілелер",
    },
    "profile_wallet": {
        "ru": "💰 USDT-кошелёк (TRC-20)",
        "uz": "💰 USDT-hamyon (TRC-20)",
        "kk": "💰 USDT-әмиян (TRC-20)",
    },
    "profile_reviews": {"ru": "📝 Отзывов", "uz": "📝 Sharhlar", "kk": "📝 Пікірлер"},
    "wallet_not_set": {"ru": "❌ Не указан", "uz": "❌ Ko'rsatilmagan", "kk": "❌ Көрсетілмеген"},
    "wallet_hint": {
        "ru": "Чтобы указать/сменить кошелёк:\n/wallet <code>ВАШ_TRC20_АДРЕС</code>",
        "uz": "Hamyonni ko'rsatish/o'zgartirish:\n/wallet <code>TRC20_MANZILINGIZ</code>",
        "kk": "Әмиянды көрсету/ауыстыру:\n/wallet <code>TRC20_МЕКЕНЖАЙЫҢЫЗ</code>",
    },
    "wallet_prompt": {
        "ru": "❗ Укажите ваш TRC-20 USDT кошелёк:\n/wallet <code>T...</code>",
        "uz": "❗ TRC-20 USDT hamyoningizni ko'rsating:\n/wallet <code>T...</code>",
        "kk": "❗ TRC-20 USDT әмияныңызды көрсетіңіз:\n/wallet <code>T...</code>",
    },
    "wallet_invalid": {
        "ru": "❌ Неверный формат TRC-20 адреса. Адрес должен начинаться с T и содержать 34 символа.",
        "uz": "❌ TRC-20 manzil formati noto'g'ri. Manzil T bilan boshlanishi va 34 belgidan iborat bo'lishi kerak.",
        "kk": "❌ TRC-20 мекенжай форматы қате. Мекенжай T-мен басталып, 34 таңбадан тұруы керек.",
    },
    "wallet_saved": {
        "ru": "✅ Кошелёк сохранён",
        "uz": "✅ Hamyon saqlandi",
        "kk": "✅ Әмиян сақталды",
    },

    # ===== Просмотр чужого профиля =====
    "profile_view_title": {
        "ru": "👤 <b>Профиль пользователя</b>",
        "uz": "👤 <b>Foydalanuvchi profili</b>",
        "kk": "👤 <b>Пайдаланушы профилі</b>",
    },
    "profile_since": {"ru": "📅 В системе с", "uz": "📅 Tizimda", "kk": "📅 Жүйеде"},
    "profile_deals_count": {"ru": "📦 Сделок", "uz": "📦 Bitimlar", "kk": "📦 Мәмілелер"},

    # ===== Объявления =====
    "press_start_first": {
        "ru": "Сначала нажмите /start",
        "uz": "Avval /start bosing",
        "kk": "Алдымен /start басыңыз",
    },
    "account_banned": {
        "ru": "⛔ Ваш аккаунт заблокирован.",
        "uz": "⛔ Hisobingiz bloklangan.",
        "kk": "⛔ Аккаунтыңыз бұғатталған.",
    },
    "set_wallet_first": {
        "ru": "❗ Сначала укажите ваш USDT-кошелёк (TRC-20):\n/wallet <code>ВАШ_АДРЕС</code>",
        "uz": "❗ Avval USDT-hamyoningizni (TRC-20) ko'rsating:\n/wallet <code>MANZILINGIZ</code>",
        "kk": "❗ Алдымен USDT-әмияныңызды (TRC-20) көрсетіңіз:\n/wallet <code>МЕКЕНЖАЙЫҢЫЗ</code>",
    },
    "choose_category": {
        "ru": "Выберите категорию:",
        "uz": "Kategoriyani tanlang:",
        "kk": "Санатты таңдаңыз:",
    },
    "invalid_category": {
        "ru": "Неверная категория",
        "uz": "Noto'g'ri kategoriya",
        "kk": "Қате санат",
    },
    "enter_title": {
        "ru": "📝 Введите название (до 100 символов):",
        "uz": "📝 Nomini kiriting (100 belgigacha):",
        "kk": "📝 Атауын енгізіңіз (100 таңбаға дейін):",
    },
    "title_error": {
        "ru": "❗ Название от 3 до 100 символов. Попробуйте ещё раз:",
        "uz": "❗ Nom 3 dan 100 belgigacha. Qaytadan urinib ko'ring:",
        "kk": "❗ Атауы 3-тен 100 таңбаға дейін. Қайталап көріңіз:",
    },
    "enter_description": {
        "ru": "📋 Введите описание (до 500 символов):",
        "uz": "📋 Tavsifni kiriting (500 belgigacha):",
        "kk": "📋 Сипаттамасын енгізіңіз (500 таңбаға дейін):",
    },
    "desc_error": {
        "ru": "❗ Описание от 10 до 500 символов. Попробуйте ещё раз:",
        "uz": "❗ Tavsif 10 dan 500 belgigacha. Qaytadan urinib ko'ring:",
        "kk": "❗ Сипаттама 10-нан 500 таңбаға дейін. Қайталап көріңіз:",
    },
    "enter_price": {
        "ru": "💰 Укажите цену в USDT (число):",
        "uz": "💰 USDT da narxni kiriting (raqam):",
        "kk": "💰 USDT бағасын енгізіңіз (сан):",
    },
    "enter_photo": {
        "ru": "📸 Отправьте фото товара/услуги или нажмите /skip чтобы пропустить:",
        "uz": "📸 Tovar/xizmat rasmini yuboring yoki o'tkazib yuborish uchun /skip bosing:",
        "kk": "📸 Тауар/қызмет фотосын жіберіңіз немесе өткізіп жіберу үшін /skip басыңыз:",
    },
    "price_min_error": {
        "ru": "❗ Минимальная сумма сделки — {amount} USDT. Укажите цену выше:",
        "uz": "❗ Minimal bitim summasi — {amount} USDT. Yuqoriroq narx kiriting:",
        "kk": "❗ Мәміленің ең аз сомасы — {amount} USDT. Жоғарырақ баға енгізіңіз:",
    },
    "price_error": {
        "ru": "❗ Введите корректную цену (от 0.01 до 1 000 000 USDT):",
        "uz": "❗ To'g'ri narx kiriting (0.01 dan 1 000 000 USDT gacha):",
        "kk": "❗ Дұрыс баға енгізіңіз (0.01 — 1 000 000 USDT):",
    },
    "listing_created": {
        "ru": "✅ Объявление #{id} создано!\n\n📂 {cat}\n📌 {title}\n💰 {price} USDT\n\nОно появится в каталоге.",
        "uz": "✅ #{id}-e'lon yaratildi!\n\n📂 {cat}\n📌 {title}\n💰 {price} USDT\n\nU katalogda paydo bo'ladi.",
        "kk": "✅ #{id} хабарландыру жасалды!\n\n📂 {cat}\n📌 {title}\n💰 {price} USDT\n\nОл каталогта пайда болады.",
    },
    "no_listings_in_cat": {
        "ru": "В категории <b>{cat}</b> пока нет объявлений.",
        "uz": "<b>{cat}</b> kategoriyasida hali e'lon yo'q.",
        "kk": "<b>{cat}</b> санатында әлі хабарландыру жоқ.",
    },
    "listings_found": {
        "ru": "📋 <b>{cat}</b> — найдено {count}:",
        "uz": "📋 <b>{cat}</b> — {count} ta topildi:",
        "kk": "📋 <b>{cat}</b> — {count} табылды:",
    },
    "seller": {"ru": "Продавец", "uz": "Sotuvchi", "kk": "Сатушы"},
    "price_label": {"ru": "Цена", "uz": "Narx", "kk": "Бағасы"},
    "unknown_seller": {"ru": "Неизвестен", "uz": "Noma'lum", "kk": "Белгісіз"},
    "no_my_listings": {
        "ru": "У вас пока нет объявлений. Нажмите «➕ Создать объявление».",
        "uz": "Sizda hali e'lon yo'q. «➕ E'lon yaratish» bosing.",
        "kk": "Сізде әлі хабарландыру жоқ. «➕ Хабарландыру жасау» басыңыз.",
    },
    "listing_active": {"ru": "✅ Активно", "uz": "✅ Faol", "kk": "✅ Белсенді"},
    "listing_inactive": {"ru": "❌ Неактивно", "uz": "❌ Faol emas", "kk": "❌ Белсенді емес"},
    "status_label": {"ru": "Статус", "uz": "Status", "kk": "Мәртебесі"},
    "confirm_delete_listing": {
        "ru": "Удалить объявление #{id} «{title}»?",
        "uz": "#{id} «{title}» e'lonni o'chirasizmi?",
        "kk": "#{id} «{title}» хабарландыруды жоясыз ба?",
    },
    "listing_deleted": {
        "ru": "✅ Объявление удалено.",
        "uz": "✅ E'lon o'chirildi.",
        "kk": "✅ Хабарландыру жойылды.",
    },
    "action_cancelled": {
        "ru": "↩️ Действие отменено.",
        "uz": "↩️ Amal bekor qilindi.",
        "kk": "↩️ Әрекет болдырылмады.",
    },

    # ===== Сделки =====
    "listing_unavailable": {
        "ru": "Объявление недоступно",
        "uz": "E'lon mavjud emas",
        "kk": "Хабарландыру қол жетімсіз",
    },
    "cant_buy_own": {
        "ru": "Нельзя купить у самого себя!",
        "uz": "O'zingizdan sotib ololmaysiz!",
        "kk": "Өзіңізден сатып ала алмайсыз!",
    },
    "min_deal_amount": {
        "ru": "⚠️ Минимальная сумма сделки — {amount} USDT",
        "uz": "⚠️ Minimal bitim summasi — {amount} USDT",
        "kk": "⚠️ Мәміленің ең аз сомасы — {amount} USDT",
    },
    "seller_no_wallet": {
        "ru": "У продавца не указан кошелёк",
        "uz": "Sotuvchining hamyoni ko'rsatilmagan",
        "kk": "Сатушының әмияны көрсетілмеген",
    },
    "deal_created": {
        "ru": (
            "🤝 <b>Сделка #{id} создана!</b>\n\n"
            "{vip_note}"
            "📌 {title}\n"
            "💰 Цена: {price} USDT\n"
            "📊 Комиссия бота ({rate}%): {commission} USDT\n"
            "💵 <b>Итого к оплате: {total} USDT</b>\n\n"
            "🔐 <b>ЭСКРОУ-ГАРАНТ:</b>\n"
            "Ваши деньги будут заморожены на кошельке бота до тех пор,\n"
            "пока вы не подтвердите получение товара/услуги.\n\n"
            "📋 <b>Переведите {total} USDT</b> на эскроу-кошелёк бота:\n"
            "<code>{wallet}</code>\n\n"
            "⚠️ Сеть: <b>TRC-20</b>\n"
            "После перевода нажмите «💰 Я отправил USDT на эскроу»"
        ),
        "uz": (
            "🤝 <b>#{id}-bitim yaratildi!</b>\n\n"
            "{vip_note}"
            "📌 {title}\n"
            "💰 Narx: {price} USDT\n"
            "📊 Bot komissiyasi ({rate}%): {commission} USDT\n"
            "💵 <b>Jami to'lov: {total} USDT</b>\n\n"
            "🔐 <b>ESKROU-KAFOLAT:</b>\n"
            "Pulingiz siz tovar/xizmatni qabul qilganingizni\n"
            "tasdiqlamaguncha bot hamyonida muzlatiladi.\n\n"
            "📋 <b>{total} USDT</b> ni bot eskrou-hamyoniga o'tkazing:\n"
            "<code>{wallet}</code>\n\n"
            "⚠️ Tarmoq: <b>TRC-20</b>\n"
            "O'tkazgandan keyin «💰 USDT eskroga yubordim» bosing"
        ),
        "kk": (
            "🤝 <b>#{id} мәміле жасалды!</b>\n\n"
            "{vip_note}"
            "📌 {title}\n"
            "💰 Бағасы: {price} USDT\n"
            "📊 Бот комиссиясы ({rate}%): {commission} USDT\n"
            "💵 <b>Жалпы төлем: {total} USDT</b>\n\n"
            "🔐 <b>ЭСКРОУ-КЕПІЛДІК:</b>\n"
            "Сіз тауар/қызметті алғаныңызды растағанша\n"
            "ақшаңыз бот әмиянында мұздатылады.\n\n"
            "📋 <b>{total} USDT</b> бот эскроу-әмиянына аударыңыз:\n"
            "<code>{wallet}</code>\n\n"
            "⚠️ Желі: <b>TRC-20</b>\n"
            "Аударғаннан кейін «💰 USDT эскроуға жібердім» басыңыз"
        ),
    },
    "deal_new_seller_notify": {
        "ru": (
            "🔔 <b>Новая сделка #{id}!</b>\n\n"
            "📌 {title}\n💰 {price} USDT\n"
            "👤 Покупатель: {buyer}\n\n"
            "🔐 Покупатель переводит средства на эскроу бота.\n"
            "Когда деньги будут заморожены — вам придёт уведомление."
        ),
        "uz": (
            "🔔 <b>Yangi #{id}-bitim!</b>\n\n"
            "📌 {title}\n💰 {price} USDT\n"
            "👤 Xaridor: {buyer}\n\n"
            "🔐 Xaridor mablag'ni bot eskrousiga o'tkazmoqda.\n"
            "Pul muzlatilganda sizga xabar keladi."
        ),
        "kk": (
            "🔔 <b>Жаңа #{id} мәміле!</b>\n\n"
            "📌 {title}\n💰 {price} USDT\n"
            "👤 Сатып алушы: {buyer}\n\n"
            "🔐 Сатып алушы қаражатты бот эскроуына аударуда.\n"
            "Ақша мұздатылғанда сізге хабарлама келеді."
        ),
    },
    "deal_not_found": {
        "ru": "Сделка не найдена",
        "uz": "Bitim topilmadi",
        "kk": "Мәміле табылмады",
    },
    "deal_status_locked": {
        "ru": "Нельзя изменить статус этой сделки",
        "uz": "Bu bitim statusini o'zgartirib bo'lmaydi",
        "kk": "Бұл мәміленің мәртебесін өзгерту мүмкін емес",
    },
    "enter_tx_hash": {
        "ru": (
            "📋 <b>Сделка #{id}</b>\n\n"
            "Введите хэш (TxID) вашей транзакции для подтверждения:\n\n"
            "💡 Хэш выглядит так:\n"
            "<code>a1b2c3d4e5f6...</code> (64 символа)"
        ),
        "uz": (
            "📋 <b>#{id}-bitim</b>\n\n"
            "Tasdiqlash uchun tranzaksiya xeshini (TxID) kiriting:\n\n"
            "💡 Xesh shunday ko'rinadi:\n"
            "<code>a1b2c3d4e5f6...</code> (64 belgi)"
        ),
        "kk": (
            "📋 <b>#{id} мәміле</b>\n\n"
            "Растау үшін транзакция хэшін (TxID) енгізіңіз:\n\n"
            "💡 Хэш мынадай болады:\n"
            "<code>a1b2c3d4e5f6...</code> (64 таңба)"
        ),
    },
    "tx_hash_invalid": {
        "ru": "❗ Неверный формат TxID.\nХэш транзакции TRON содержит 64 символа, например:\n<code>a1b2c3d4e5f6...</code>\nВведите корректный TxID:",
        "uz": "❗ TxID formati noto'g'ri.\nTRON tranzaksiya xeshi 64 ta belgidan iborat, masalan:\n<code>a1b2c3d4e5f6...</code>\nTo'g'ri TxID kiriting:",
        "kk": "❗ TxID форматы қате.\nTRON транзакция хэші 64 таңбадан тұрады, мысалы:\n<code>a1b2c3d4e5f6...</code>\nДұрыс TxID енгізіңіз:",
    },
    "tx_already_used": {
        "ru": "🚫 Этот TxID уже использован в другой сделке. Введите уникальный TxID:",
        "uz": "🚫 Bu TxID boshqa bitimda ishlatilgan. Boshqa TxID kiriting:",
        "kk": "🚫 Бұл TxID басқа мәмілеге қолданылған. Басқа TxID енгізіңіз:",
    },
    "listing_unavailable": {
        "ru": "❌ Это объявление уже недоступно.",
        "uz": "❌ Bu e'lon endi mavjud emas.",
        "kk": "❌ Бұл хабарландыру қол жетімсіз.",
    },
    "message_too_long": {
        "ru": "⚠️ Сообщение слишком длинное (макс. 2000 символов).",
        "uz": "⚠️ Xabar juda uzun (maks. 2000 belgi).",
        "kk": "⚠️ Хабарлама тым ұзын (макс. 2000 таңба).",
    },
    "invalid_category": {
        "ru": "❌ Некорректная категория.",
        "uz": "❌ Noto'g'ri kategoriya.",
        "kk": "❌ Қате санат.",
    },
    "tx_verifying": {
        "ru": "⏳ Проверяю транзакцию в блокчейне TRON...",
        "uz": "⏳ TRON blokcheyinda tranzaksiyani tekshirmoqdaman...",
        "kk": "⏳ TRON блокчейнінде транзакцияны тексеруде...",
    },
    "tx_not_found": {
        "ru": "❌ Транзакция не найдена в блокчейне.\nПроверьте TxID и попробуйте ещё раз (подождите пару минут — транзакция может ещё обрабатываться):",
        "uz": "❌ Tranzaksiya blokcheyinda topilmadi.\nTxID ni tekshiring va qaytadan urinib ko'ring (bir necha daqiqa kuting):",
        "kk": "❌ Транзакция блокчейнде табылмады.\nTxID тексеріңіз және қайталап көріңіз (бірнеше минут күтіңіз):",
    },
    "tx_wrong_wallet": {
        "ru": "❌ Транзакция найдена, но получатель — не кошелёк бота.\nПереведите USDT на правильный адрес и введите новый TxID:",
        "uz": "❌ Tranzaksiya topildi, lekin qabul qiluvchi bot hamyoni emas.\nUSDT ni to'g'ri manzilga o'tkazing va yangi TxID kiriting:",
        "kk": "❌ Транзакция табылды, бірақ алушы бот әмияны емес.\nUSDT дұрыс мекенжайға аударыңыз және жаңа TxID енгізіңіз:",
    },
    "tx_amount_mismatch": {
        "ru": "❌ Сумма транзакции ({received} USDT) меньше требуемой ({expected} USDT).\nПереведите точную сумму и введите новый TxID:",
        "uz": "❌ Tranzaksiya summasi ({received} USDT) talab qilinganidan ({expected} USDT) kam.\nAniq summani o'tkazing va yangi TxID kiriting:",
        "kk": "❌ Транзакция сомасы ({received} USDT) қажеттіден ({expected} USDT) аз.\nДәл соманы аударыңыз және жаңа TxID енгізіңіз:",
    },
    "tx_not_usdt": {
        "ru": "❌ Это не USDT TRC-20 перевод на кошелёк бота.\nОтправьте USDT (TRC-20) и введите правильный TxID:",
        "uz": "❌ Bu bot hamyoniga USDT TRC-20 o'tkazmasi emas.\nUSDT (TRC-20) yuboring va to'g'ri TxID kiriting:",
        "kk": "❌ Бұл бот әмиянына USDT TRC-20 аударымы емес.\nUSDT (TRC-20) жіберіңіз және дұрыс TxID енгізіңіз:",
    },
    "tx_network_error": {
        "ru": "⚠️ Не удалось проверить транзакцию (ошибка сети). Попробуйте ещё раз через минуту:",
        "uz": "⚠️ Tranzaksiyani tekshirib bo'lmadi (tarmoq xatosi). Bir daqiqadan keyin qaytadan urinib ko'ring:",
        "kk": "⚠️ Транзакцияны тексеру мүмкін болмады (желі қатесі). Бір минуттан кейін қайталаңыз:",
    },
    "tx_verified": {
        "ru": "✅ Транзакция подтверждена блокчейном!",
        "uz": "✅ Tranzaksiya blokcheyn tomonidan tasdiqlandi!",
        "kk": "✅ Транзакция блокчейнмен расталды!",
    },
    "tx_admin_verified": {
        "ru": (
            "✅ <b>Платёж подтверждён</b>\n\n"
            "🆔 Сделка: #{id}\n"
            "� Товар: {title}\n"
            "👤 Покупатель: {buyer_id}\n"
            "👥 Продавец: {seller_id}\n"
            "💵 Сумма товара: {price} USDT\n"
            "💰 Эскроу (с комиссией): {amount} USDT\n"
            "🔗 TxHash: <code>{tx}</code>"
        ),
        "uz": (
            "✅ <b>To'lov tasdiqlandi</b>\n\n"
            "🆔 Bitim: #{id}\n"
            "📋 Tovar: {title}\n"
            "👤 Xaridor: {buyer_id}\n"
            "👥 Sotuvchi: {seller_id}\n"
            "💵 Tovar narxi: {price} USDT\n"
            "💰 Escrow (komissiya bilan): {amount} USDT\n"
            "🔗 TxHash: <code>{tx}</code>"
        ),
        "kk": (
            "✅ <b>Төлем расталды</b>\n\n"
            "🆔 Мәміле: #{id}\n"
            "📋 Тауар: {title}\n"
            "👤 Сатып алушы: {buyer_id}\n"
            "👥 Сатушы: {seller_id}\n"
            "💵 Тауар бағасы: {price} USDT\n"
            "💰 Эскроу (комиссиямен): {amount} USDT\n"
            "🔗 TxHash: <code>{tx}</code>"
        ),
    },
    "tx_admin_failed": {
        "ru": (
            "⚠️ <b>Неудачная верификация TxHash</b>\n\n"
            "🆔 Сделка: #{id}\n"
            "� Товар: {title}\n"
            "👤 Покупатель: {buyer_id}\n"
            "👥 Продавец: {seller_id}\n"
            "💰 Эскроу: {amount} USDT\n"
            "❌ Причина: {reason}\n"
            "🔗 TxHash: <code>{tx}</code>\n"
            "🔄 Попытка: {attempt}/3"
        ),
        "uz": (
            "⚠️ <b>TxHash tekshiruvi muvaffaqiyatsiz</b>\n\n"
            "🆔 Bitim: #{id}\n"
            "📋 Tovar: {title}\n"
            "👤 Xaridor: {buyer_id}\n"
            "👥 Sotuvchi: {seller_id}\n"
            "💰 Escrow: {amount} USDT\n"
            "❌ Sabab: {reason}\n"
            "🔗 TxHash: <code>{tx}</code>\n"
            "🔄 Urinish: {attempt}/3"
        ),
        "kk": (
            "⚠️ <b>TxHash тексеруі сәтсіз</b>\n\n"
            "🆔 Мәміле: #{id}\n"
            "📋 Тауар: {title}\n"
            "👤 Сатып алушы: {buyer_id}\n"
            "👥 Сатушы: {seller_id}\n"
            "💰 Эскроу: {amount} USDT\n"
            "❌ Себебі: {reason}\n"
            "🔗 TxHash: <code>{tx}</code>\n"
            "🔄 Әрекет: {attempt}/3"
        ),
    },
    "tx_blocked": {
        "ru": "🚫 Слишком много неудачных попыток. Сделка заблокирована — обратитесь к администратору.",
        "uz": "🚫 Muvaffaqiyatsiz urinishlar juda ko'p. Bitim bloklandi — administratorga murojaat qiling.",
        "kk": "🚫 Сәтсіз әрекеттер тым көп. Мәміле бұғатталды — әкімшіге хабарласыңыз.",
    },
    "tx_admin_blocked": {
        "ru": (
            "🚫 <b>Сделка заблокирована</b>\n\n"
            "🆔 Сделка: #{id}\n"
            "� Товар: {title}\n"
            "👤 Покупатель: {buyer_id}\n"
            "👥 Продавец: {seller_id}\n"
            "💰 Эскроу: {amount} USDT\n"
            "❌ 3 неудачных попытки верификации TxHash\n"
            "⚡ Требуется ручная проверка"
        ),
        "uz": (
            "🚫 <b>Bitim bloklandi</b>\n\n"
            "🆔 Bitim: #{id}\n"
            "📋 Tovar: {title}\n"
            "👤 Xaridor: {buyer_id}\n"
            "👥 Sotuvchi: {seller_id}\n"
            "💰 Escrow: {amount} USDT\n"
            "❌ 3 muvaffaqiyatsiz TxHash tekshiruvi\n"
            "⚡ Qo'lda tekshirish kerak"
        ),
        "kk": (
            "🚫 <b>Мәміле бұғатталды</b>\n\n"
            "🆔 Мәміле: #{id}\n"
            "📋 Тауар: {title}\n"
            "👤 Сатып алушы: {buyer_id}\n"
            "👥 Сатушы: {seller_id}\n"
            "💰 Эскроу: {amount} USDT\n"
            "❌ 3 сәтсіз TxHash тексеруі\n"
            "⚡ Қолмен тексеру қажет"
        ),
    },
    "deal_paid": {
        "ru": (
            "✅ <b>Сделка #{id} — оплата зафиксирована!</b>\n\n"
            "📌 {title}\n"
            "💰 {total} USDT заморожены на эскроу\n"
            "🔗 TxID: <code>{tx}</code>\n\n"
            "⏳ Ожидаем выполнение заказа продавцом...\n\n"
            "После получения товара/услуги нажмите «✅ Подтверждаю получение»."
        ),
        "uz": (
            "✅ <b>#{id}-bitim — to'lov qabul qilindi!</b>\n\n"
            "📌 {title}\n"
            "💰 {total} USDT eskrouda muzlatildi\n"
            "🔗 TxID: <code>{tx}</code>\n\n"
            "⏳ Sotuvchi buyurtmani bajarishini kutmoqdamiz...\n\n"
            "Tovar/xizmatni olgach «✅ Qabul qildim» bosing."
        ),
        "kk": (
            "✅ <b>#{id} мәміле — төлем тіркелді!</b>\n\n"
            "📌 {title}\n"
            "💰 {total} USDT эскроуда мұздатылды\n"
            "🔗 TxID: <code>{tx}</code>\n\n"
            "⏳ Сатушының тапсырысты орындауын күтудеміз...\n\n"
            "Тауар/қызметті алғаннан кейін «✅ Алғанымды растаймын» басыңыз."
        ),
    },
    "deal_escrow_seller_notify": {
        "ru": (
            "💰 <b>Сделка #{id} — средства на эскроу!</b>\n\n"
            "📌 {title}\n"
            "💵 {total} USDT заморожены на кошельке бота.\n"
            "🔗 TxID покупателя: <code>{tx}</code>\n\n"
            "✅ Покупатель оплатил. Выполните заказ и нажмите\n"
            "«📦 Заказ выполнен» когда будете готовы."
        ),
        "uz": (
            "💰 <b>#{id}-bitim — mablag' eskrouda!</b>\n\n"
            "📌 {title}\n"
            "💵 {total} USDT bot hamyonida muzlatildi.\n"
            "🔗 Xaridor TxID: <code>{tx}</code>\n\n"
            "✅ Xaridor to'ladi. Buyurtmani bajaring va\n"
            "«📦 Buyurtma bajarildi» bosing."
        ),
        "kk": (
            "💰 <b>#{id} мәміле — қаражат эскроуда!</b>\n\n"
            "📌 {title}\n"
            "💵 {total} USDT бот әмиянында мұздатылды.\n"
            "🔗 Сатып алушы TxID: <code>{tx}</code>\n\n"
            "✅ Сатып алушы төледі. Тапсырысты орындаңыз және\n"
            "«📦 Тапсырыс орындалды» басыңыз."
        ),
    },
    "deal_delivered_seller": {
        "ru": (
            "📦 <b>Сделка #{id} — заказ выполнен!</b>\n\n"
            "Ожидаем подтверждения от покупателя.\n\n"
            "⏳ Если покупатель не подтвердит и не откроет спор\n"
            "в течение <b>{hours}ч</b> — сделка завершится автоматически,\n"
            "а средства будут отправлены вам."
        ),
        "uz": (
            "📦 <b>#{id}-bitim — buyurtma bajarildi!</b>\n\n"
            "Xaridordan tasdiqlashni kutmoqdamiz.\n\n"
            "⏳ Agar xaridor <b>{hours} soat</b> ichida tasdiqlamasa\n"
            "va da'vo ochmasa — bitim avtomatik tugallanadi\n"
            "va mablag' sizga yuboriladi."
        ),
        "kk": (
            "📦 <b>#{id} мәміле — тапсырыс орындалды!</b>\n\n"
            "Сатып алушының растауын күтудеміз.\n\n"
            "⏳ Егер сатып алушы <b>{hours} сағат</b> ішінде растамаса\n"
            "және дау ашпаса — мәміле автоматты аяқталады,\n"
            "ал қаражат сізге жіберіледі."
        ),
    },
    "deal_delivered_buyer_notify": {
        "ru": (
            "📦 <b>Сделка #{id} — продавец выполнил заказ!</b>\n\n"
            "📌 {title}\n👤 Продавец: {seller}\n\n"
            "Если вы получили товар/услугу — подтвердите,\n"
            "и средства автоматически уйдут продавцу.\n\n"
            "⚠️ Если есть проблема — откройте спор.\n"
            "⏳ Авто-завершение через <b>{hours}ч</b> если нет ответа."
        ),
        "uz": (
            "📦 <b>#{id}-bitim — sotuvchi buyurtmani bajardi!</b>\n\n"
            "📌 {title}\n👤 Sotuvchi: {seller}\n\n"
            "Agar tovar/xizmatni olgan bo'lsangiz — tasdiqlang,\n"
            "mablag' avtomatik sotuvchiga yuboriladi.\n\n"
            "⚠️ Muammo bo'lsa — da'vo oching.\n"
            "⏳ Javob bo'lmasa <b>{hours} soat</b>da avtomatik tugallanadi."
        ),
        "kk": (
            "📦 <b>#{id} мәміле — сатушы тапсырысты орындады!</b>\n\n"
            "📌 {title}\n👤 Сатушы: {seller}\n\n"
            "Егер тауар/қызметті алсаңыз — растаңыз,\n"
            "қаражат автоматты сатушыға жіберіледі.\n\n"
            "⚠️ Мәселе болса — дау ашыңыз.\n"
            "⏳ Жауап болмаса <b>{hours} сағатта</b> автоматты аяқталады."
        ),
    },
    "deal_completed_buyer": {
        "ru": (
            "🎉 <b>Сделка #{id} завершена!</b>\n\n"
            "📌 {title}\n"
            "💵 {payout} USDT будут отправлены продавцу.\n"
            "📊 Комиссия {commission} USDT удержана ботом.\n\n"
            "Спасибо за доверие! Оставьте отзыв:"
        ),
        "uz": (
            "🎉 <b>#{id}-bitim tugallandi!</b>\n\n"
            "📌 {title}\n"
            "💵 {payout} USDT sotuvchiga yuboriladi.\n"
            "📊 {commission} USDT komissiya bot tomonidan ushlab qolindi.\n\n"
            "Ishonchingiz uchun rahmat! Sharh qoldiring:"
        ),
        "kk": (
            "🎉 <b>#{id} мәміле аяқталды!</b>\n\n"
            "📌 {title}\n"
            "💵 {payout} USDT сатушыға жіберіледі.\n"
            "📊 {commission} USDT комиссия бот ұстап қалды.\n\n"
            "Сеніміңіз үшін рахмет! Пікір қалдырыңыз:"
        ),
    },
    "deal_completed_seller_notify": {
        "ru": (
            "🎉 <b>Сделка #{id} завершена!</b>\n\n"
            "📌 {title}\n"
            "✅ Покупатель подтвердил получение.\n"
            "💵 <b>{payout} USDT</b> будут отправлены на ваш кошелёк:\n"
            "<code>{wallet}</code>\n\n"
            "Оставьте отзыв покупателю:"
        ),
        "uz": (
            "🎉 <b>#{id}-bitim tugallandi!</b>\n\n"
            "📌 {title}\n"
            "✅ Xaridor qabul qilganini tasdiqladi.\n"
            "💵 <b>{payout} USDT</b> hamyoningizga yuboriladi:\n"
            "<code>{wallet}</code>\n\n"
            "Xaridor haqida sharh qoldiring:"
        ),
        "kk": (
            "🎉 <b>#{id} мәміле аяқталды!</b>\n\n"
            "📌 {title}\n"
            "✅ Сатып алушы алғанын растады.\n"
            "💵 <b>{payout} USDT</b> әмияныңызға жіберіледі:\n"
            "<code>{wallet}</code>\n\n"
            "Сатып алушыға пікір қалдырыңыз:"
        ),
    },
    "deal_cancelled": {
        "ru": "❌ Сделка #{id} отменена.",
        "uz": "❌ #{id}-bitim bekor qilindi.",
        "kk": "❌ #{id} мәміле болдырылмады.",
    },
    "deal_cancelled_seller_notify": {
        "ru": "❌ Сделка #{id} отменена покупателем (до оплаты).",
        "uz": "❌ #{id}-bitim xaridor tomonidan bekor qilindi (to'lovdan oldin).",
        "kk": "❌ #{id} мәміле сатып алушы тарапынан болдырылмады (төлемге дейін).",
    },
    "cancel_only_before_pay": {
        "ru": "Отмена возможна только до оплаты на эскроу",
        "uz": "Bekor qilish faqat eskrouga to'lovdan oldin mumkin",
        "kk": "Болдырмау тек эскроуға төлемге дейін мүмкін",
    },
    "cancel_not_available": {
        "ru": "Отмена сейчас недоступна",
        "uz": "Bekor qilish hozir mumkin emas",
        "kk": "Болдырмау қазір қолжетімсіз",
    },
    "deal_cancelled_penalty": {
        "ru": (
            "❌ <b>Сделка #{id} отменена после оплаты</b>\n\n"
            "🔻 Штраф за отмену ({penalty_pct}%): <b>{penalty} USDT</b>\n"
            "💸 К возврату: <b>{refund} USDT</b>\n\n"
            "Администратор вернёт средства за вычетом штрафа."
        ),
        "uz": (
            "❌ <b>#{id}-bitim to'lovdan keyin bekor qilindi</b>\n\n"
            "🔻 Bekor qilish jarimasi ({penalty_pct}%): <b>{penalty} USDT</b>\n"
            "💸 Qaytarish: <b>{refund} USDT</b>\n\n"
            "Administrator jarima chegirib mablag'ni qaytaradi."
        ),
        "kk": (
            "❌ <b>#{id} мәміле төлемнен кейін болдырылмады</b>\n\n"
            "🔻 Болдырмау айыппұлы ({penalty_pct}%): <b>{penalty} USDT</b>\n"
            "💸 Қайтару: <b>{refund} USDT</b>\n\n"
            "Әкімші айыппұлды ұстап қаражатты қайтарады."
        ),
    },
    "deal_cancelled_seller_after_pay": {
        "ru": "❌ Сделка #{id} ({title}) отменена покупателем после оплаты. Средства возвращаются покупателю.",
        "uz": "❌ #{id}-bitim ({title}) xaridor tomonidan to'lovdan keyin bekor qilindi. Mablag' xaridorga qaytarilmoqda.",
        "kk": "❌ #{id} мәміле ({title}) сатып алушы тарапынан төлемнен кейін болдырылмады. Қаражат сатып алушыға қайтарылады.",
    },
    "first_deal_free_note": {
        "ru": "🎁 <b>Первая сделка без комиссии!</b>\n",
        "uz": "🎁 <b>Birinchi bitim komissiyasiz!</b>\n",
        "kk": "🎁 <b>Бірінші мәміле комиссиясыз!</b>\n",
    },
    "chat_contacts_unlocked": {
        "ru": "🔓 Оплата подтверждена — обмен контактами разрешён!\nТеперь вы можете обменяться телефоном и адресом для встречи.",
        "uz": "🔓 To'lov tasdiqlandi — kontakt almashish ruxsat etildi!\nEndi telefon va manzil almashishingiz mumkin.",
        "kk": "🔓 Төлем расталды — байланыс алмасуға рұқсат!\nЕнді телефон және мекенжай алмасуға болады.",
    },

    # ===== Споры =====
    "dispute_opened": {
        "ru": (
            "⚠️ <b>Спор по сделке #{id} открыт!</b>\n\n"
            "🔐 Средства заморожены на эскроу.\n"
            "Администратор рассмотрит спор и вынесет решение.\n\n"
            "Никто не получит деньги до разрешения спора."
        ),
        "uz": (
            "⚠️ <b>#{id}-bitim bo'yicha da'vo ochildi!</b>\n\n"
            "🔐 Mablag' eskrouda muzlatildi.\n"
            "Administrator da'voni ko'rib chiqadi.\n\n"
            "Da'vo hal qilinmaguncha hech kim pul olmaydi."
        ),
        "kk": (
            "⚠️ <b>#{id} мәміле бойынша дау ашылды!</b>\n\n"
            "🔐 Қаражат эскроуда мұздатылды.\n"
            "Әкімші дауды қарастырып шешім шығарады.\n\n"
            "Дау шешілгенше ешкім ақша алмайды."
        ),
    },
    "dispute_other_notify": {
        "ru": "⚠️ По сделке #{id} открыт спор.\n🔐 Средства заморожены на эскроу до решения администратора.",
        "uz": "⚠️ #{id}-bitim bo'yicha da'vo ochildi.\n🔐 Mablag' admin qaroriga qadar muzlatildi.",
        "kk": "⚠️ #{id} мәміле бойынша дау ашылды.\n🔐 Қаражат әкімші шешіміне дейін мұздатылды.",
    },
    "dispute_only_escrow": {
        "ru": "Спор возможен только когда средства на эскроу",
        "uz": "Da'vo faqat mablag' eskrouda bo'lganda mumkin",
        "kk": "Дау тек қаражат эскроуда болғанда мүмкін",
    },
    "no_access": {
        "ru": "Нет прав",
        "uz": "Ruxsat yo'q",
        "kk": "Рұқсат жоқ",
    },

    # ===== Отзывы =====
    "review_only_completed": {
        "ru": "Отзыв можно оставить только после завершения сделки",
        "uz": "Sharh faqat bitim tugagandan keyin qoldiriladi",
        "kk": "Пікір тек мәміле аяқталғаннан кейін қалдырылады",
    },
    "review_not_participant": {
        "ru": "Вы не участник этой сделки",
        "uz": "Siz bu bitim ishtirokchisi emassiz",
        "kk": "Сіз бұл мәміленің қатысушысы емессіз",
    },
    "review_rate": {
        "ru": "⭐ Оцените сделку #{id}:",
        "uz": "⭐ #{id}-bitimni baholang:",
        "kk": "⭐ #{id} мәмілені бағалаңыз:",
    },
    "review_comment": {
        "ru": "💬 Напишите комментарий (или отправьте «-» чтобы пропустить):",
        "uz": "💬 Izoh yozing (yoki o'tkazib yuborish uchun «-» yuboring):",
        "kk": "💬 Пікір жазыңыз (немесе өткізіп жіберу үшін «-» жіберіңіз):",
    },
    "review_comment_too_long": {
        "ru": "❗ Комментарий до 300 символов. Попробуйте ещё раз:",
        "uz": "❗ Izoh 300 belgigacha. Qaytadan urinib ko'ring:",
        "kk": "❗ Пікір 300 таңбаға дейін. Қайталап көріңіз:",
    },
    "review_saved": {
        "ru": "✅ Отзыв сохранён!",
        "uz": "✅ Sharh saqlandi!",
        "kk": "✅ Пікір сақталды!",
    },

    # ===== Мои сделки =====
    "no_deals": {
        "ru": "У вас пока нет сделок.",
        "uz": "Sizda hali bitimlar yo'q.",
        "kk": "Сізде әлі мәмілелер жоқ.",
    },
    "my_deals_title": {
        "ru": "📦 <b>Ваши сделки:</b>",
        "uz": "📦 <b>Sizning bitimlaringiz:</b>",
        "kk": "📦 <b>Сіздің мәмілелеріңіз:</b>",
    },
    "role_buyer": {"ru": "🛒 Покупатель", "uz": "🛒 Xaridor", "kk": "🛒 Сатып алушы"},
    "role_seller": {"ru": "🏪 Продавец", "uz": "🏪 Sotuvchi", "kk": "🏪 Сатушы"},
    "deal_status_created": {
        "ru": "🕐 Ожидает оплату на эскроу",
        "uz": "🕐 Eskroga to'lovni kutmoqda",
        "kk": "🕐 Эскроуға төлемді күтуде",
    },
    "deal_status_paid": {
        "ru": "🔐 Средства на эскроу (выполняется)",
        "uz": "🔐 Mablag' eskrouda (bajarilmoqda)",
        "kk": "🔐 Қаражат эскроуда (орындалуда)",
    },
    "deal_status_delivered": {
        "ru": "📦 Доставлено (ждём подтверждения)",
        "uz": "📦 Yetkazildi (tasdiqlashni kutmoqda)",
        "kk": "📦 Жеткізілді (растауды күтуде)",
    },
    "deal_status_completed": {"ru": "🎉 Завершена", "uz": "🎉 Tugallandi", "kk": "🎉 Аяқталды"},
    "deal_status_disputed": {
        "ru": "⚠️ Спор (средства заморожены)",
        "uz": "⚠️ Da'vo (mablag' muzlatilgan)",
        "kk": "⚠️ Дау (қаражат мұздатылған)",
    },
    "deal_status_cancelled": {"ru": "❌ Отменена", "uz": "❌ Bekor qilingan", "kk": "❌ Болдырылмаған"},
    "deal_status_refunded": {"ru": "💸 Возврат", "uz": "💸 Qaytarish", "kk": "💸 Қайтару"},

    # ===== VIP =====
    "vip_active": {
        "ru": (
            "👑 <b>У вас активная VIP-подписка!</b>\n\n"
            "✅ Статус: Верифицированный продавец\n"
            "📅 Действует до: <b>{expires}</b>\n"
            "💰 Ваша комиссия: <b>{vip_rate}%</b> (вместо {rate}%)\n\n"
            "🛡 Преимущества:\n"
            "• ✅ Галочка «Верифицирован» в профиле\n"
            "• 📌 Приоритет в каталоге\n"
            "• 💰 Сниженная комиссия {vip_rate}%\n"
            "• ⭐ Повышенное доверие покупателей"
        ),
        "uz": (
            "👑 <b>Sizda faol VIP-obuna bor!</b>\n\n"
            "✅ Status: Tasdiqlangan sotuvchi\n"
            "📅 Amal qiladi: <b>{expires}</b>\n"
            "💰 Komissiyangiz: <b>{vip_rate}%</b> ({rate}% o'rniga)\n\n"
            "🛡 Afzalliklar:\n"
            "• ✅ Profilda «Tasdiqlangan» belgisi\n"
            "• 📌 Katalogda ustuvorlik\n"
            "• 💰 Kam komissiya {vip_rate}%\n"
            "• ⭐ Xaridorlar ishonchi yuqori"
        ),
        "kk": (
            "👑 <b>Сізде белсенді VIP-жазылым бар!</b>\n\n"
            "✅ Мәртебе: Расталған сатушы\n"
            "📅 Жарамды: <b>{expires}</b>\n"
            "💰 Комиссияңыз: <b>{vip_rate}%</b> ({rate}% орнына)\n\n"
            "🛡 Артықшылықтар:\n"
            "• ✅ Профильде «Расталған» белгісі\n"
            "• 📌 Каталогта басымдық\n"
            "• 💰 Төмендетілген комиссия {vip_rate}%\n"
            "• ⭐ Сатып алушылардың жоғары сенімі"
        ),
    },
    "vip_offer": {
        "ru": (
            "👑 <b>VIP-подписка</b>\n\n"
            "Станьте верифицированным продавцом и получите:\n\n"
            "✅ Галочка «Верифицирован» рядом с именем\n"
            "📌 Приоритет показа в каталоге\n"
            "💰 Сниженная комиссия: <b>{vip_rate}%</b> вместо {rate}%\n"
            "⭐ Повышенное доверие покупателей\n\n"
            "💵 Стоимость: <b>{price} USDT / {days} дней</b>"
        ),
        "uz": (
            "👑 <b>VIP-obuna</b>\n\n"
            "Tasdiqlangan sotuvchi bo'ling va quyidagilarni oling:\n\n"
            "✅ Ism yonida «Tasdiqlangan» belgisi\n"
            "📌 Katalogda ustuvorlik\n"
            "💰 Kam komissiya: <b>{vip_rate}%</b> ({rate}% o'rniga)\n"
            "⭐ Xaridorlar ishonchi yuqori\n\n"
            "💵 Narxi: <b>{price} USDT / {days} kun</b>"
        ),
        "kk": (
            "👑 <b>VIP-жазылым</b>\n\n"
            "Расталған сатушы болыңыз және алыңыз:\n\n"
            "✅ Аттың жанында «Расталған» белгісі\n"
            "📌 Каталогта басымдық\n"
            "💰 Төмендетілген комиссия: <b>{vip_rate}%</b> ({rate}% орнына)\n"
            "⭐ Сатып алушылардың жоғары сенімі\n\n"
            "💵 Бағасы: <b>{price} USDT / {days} күн</b>"
        ),
    },
    "vip_already_active": {
        "ru": "У вас уже есть активная VIP-подписка!",
        "uz": "Sizda allaqachon faol VIP-obuna bor!",
        "kk": "Сізде қазірдің өзінде белсенді VIP-жазылым бар!",
    },
    "vip_payment": {
        "ru": (
            "👑 <b>Оплата VIP-подписки</b>\n\n"
            "💵 Сумма: <b>{price} USDT</b>\n"
            "📅 Срок: {days} дней\n\n"
            "📋 Переведите <b>{price} USDT</b> на кошелёк бота:\n"
            "<code>{wallet}</code>\n\n"
            "⚠️ Сеть: <b>TRC-20</b>\n\n"
            "После перевода нажмите «💰 Я оплатил VIP»"
        ),
        "uz": (
            "👑 <b>VIP-obuna to'lovi</b>\n\n"
            "💵 Summa: <b>{price} USDT</b>\n"
            "📅 Muddat: {days} kun\n\n"
            "📋 <b>{price} USDT</b> ni bot hamyoniga o'tkazing:\n"
            "<code>{wallet}</code>\n\n"
            "⚠️ Tarmoq: <b>TRC-20</b>\n\n"
            "O'tkazgandan keyin «💰 VIP uchun to'ladim» bosing"
        ),
        "kk": (
            "👑 <b>VIP-жазылым төлемі</b>\n\n"
            "💵 Сома: <b>{price} USDT</b>\n"
            "📅 Мерзімі: {days} күн\n\n"
            "📋 <b>{price} USDT</b> бот әмиянына аударыңыз:\n"
            "<code>{wallet}</code>\n\n"
            "⚠️ Желі: <b>TRC-20</b>\n\n"
            "Аударғаннан кейін «💰 VIP үшін төледім» басыңыз"
        ),
    },
    "vip_enter_tx": {
        "ru": "📋 <b>VIP-подписка — подтверждение оплаты</b>\n\nВведите хэш (TxID) вашей транзакции:",
        "uz": "📋 <b>VIP-obuna — to'lovni tasdiqlash</b>\n\nTranzaksiya xeshini (TxID) kiriting:",
        "kk": "📋 <b>VIP-жазылым — төлемді растау</b>\n\nТранзакция хэшін (TxID) енгізіңіз:",
    },
    "vip_activated": {
        "ru": (
            "🎉 <b>VIP-подписка активирована!</b>\n\n"
            "👑 Вы теперь верифицированный продавец!\n"
            "📅 Действует {days} дней\n"
            "💰 Ваша комиссия: {vip_rate}%\n"
            "✅ Галочка верификации уже на вашем профиле\n\n"
            "🔗 TxID: <code>{tx}</code>"
        ),
        "uz": (
            "🎉 <b>VIP-obuna faollashtirildi!</b>\n\n"
            "👑 Siz endi tasdiqlangan sotuvchisiz!\n"
            "📅 {days} kun amal qiladi\n"
            "💰 Komissiyangiz: {vip_rate}%\n"
            "✅ Tasdiqlash belgisi profilingizda\n\n"
            "🔗 TxID: <code>{tx}</code>"
        ),
        "kk": (
            "🎉 <b>VIP-жазылым белсендірілді!</b>\n\n"
            "👑 Сіз енді расталған сатушысыз!\n"
            "📅 {days} күн жарамды\n"
            "💰 Комиссияңыз: {vip_rate}%\n"
            "✅ Растау белгісі профиліңізде\n\n"
            "🔗 TxID: <code>{tx}</code>"
        ),
    },
    "vip_cancelled": {
        "ru": "❌ Покупка VIP отменена.",
        "uz": "❌ VIP sotib olish bekor qilindi.",
        "kk": "❌ VIP сатып алу болдырылмады.",
    },
    "vip_seller_note": {
        "ru": "👑 Продавец верифицирован (VIP)\n",
        "uz": "👑 Sotuvchi tasdiqlangan (VIP)\n",
        "kk": "👑 Сатушы расталған (VIP)\n",
    },

    # ===== Главное меню =====
    "main_menu": {
        "ru": "Главное меню 👇",
        "uz": "Asosiy menyu 👇",
        "kk": "Басты мәзір 👇",
    },
    "error_try_again": {
        "ru": "Ошибка. Попробуйте начать заново.",
        "uz": "Xatolik. Qaytadan boshlang.",
        "kk": "Қате. Қайтадан бастаңыз.",
    },
    "deal_status_changed": {
        "ru": "Сделка не найдена или статус изменился.",
        "uz": "Bitim topilmadi yoki statusi o'zgardi.",
        "kk": "Мәміле табылмады немесе мәртебесі өзгерді.",
    },
    "cant_confirm_now": {
        "ru": "Нельзя подтвердить на этом этапе",
        "uz": "Bu bosqichda tasdiqlab bo'lmaydi",
        "kk": "Бұл кезеңде растау мүмкін емес",
    },
    "deal_not_at_execution": {
        "ru": "Нельзя отметить — сделка не на этапе выполнения",
        "uz": "Belgilab bo'lmaydi — bitim bajarilish bosqichida emas",
        "kk": "Белгілеу мүмкін емес — мәміле орындау кезеңінде емес",
    },

    # ===== Удаление аккаунта =====
    "btn_delete_account": {
        "ru": "🗑 Удалить аккаунт",
        "uz": "🗑 Hisobni o'chirish",
        "kk": "🗑 Аккаунтты жою",
        "tr": "🗑 Hesabı sil",
        "tg": "🗑 Ҳисобро нест кардан",
        "ky": "🗑 Аккаунтту жок кылуу",
    },
    "delete_account_confirm": {
        "ru": (
            "⚠️ <b>Вы уверены, что хотите удалить аккаунт?</b>\n\n"
            "Будут удалены:\n"
            "• Ваш профиль и кошелёк\n"
            "• Все ваши объявления\n"
            "• VIP-подписка\n\n"
            "❗ Активные сделки не будут затронуты.\n"
            "Это действие <b>необратимо</b>!"
        ),
        "uz": (
            "⚠️ <b>Hisobni o'chirishga ishonchingiz kommi?</b>\n\n"
            "O'chiriladi:\n"
            "• Profil va hamyon\n"
            "• Barcha e'lonlaringiz\n"
            "• VIP-obuna\n\n"
            "❗ Faol bitimlar ta'sirlanmaydi.\n"
            "Bu amal <b>qaytarilmas</b>!"
        ),
        "kk": (
            "⚠️ <b>Аккаунтты жоюға сенімдісіз бе?</b>\n\n"
            "Жойылады:\n"
            "• Профиль және әмиян\n"
            "• Барлық хабарландыруларыңыз\n"
            "• VIP-жазылым\n\n"
            "❗ Белсенді мәмілелер әсер етпейді.\n"
            "Бұл әрекет <b>қайтарылмайды</b>!"
        ),
    },
    "account_deleted": {
        "ru": "✅ Ваш аккаунт удалён. Все данные стёрты.\nДля повторной регистрации нажмите /start",
        "uz": "✅ Hisobingiz o'chirildi. Barcha ma'lumotlar o'chirildi.\nQayta ro'yxatdan o'tish uchun /start bosing",
        "kk": "✅ Аккаунтыңыз жойылды. Барлық деректер жойылды.\nҚайта тіркелу үшін /start басыңыз",
    },
    "delete_account_has_active_deals": {
        "ru": "❌ Нельзя удалить аккаунт — у вас есть активные сделки. Завершите или отмените их сначала.",
        "uz": "❌ Hisobni o'chirib bo'lmaydi — sizda faol bitimlar bor. Avval ularni tugating yoki bekor qiling.",
        "kk": "❌ Аккаунтты жою мүмкін емес — сізде белсенді мәмілелер бар. Алдымен оларды аяқтаңыз немесе болдырмаңыз.",
    },

    # ===== Поддержка /support =====
    "support_prompt": {
        "ru": "📩 Напишите ваше сообщение для службы поддержки:",
        "uz": "📩 Qo'llab-quvvatlash xizmatiga xabar yozing:",
        "kk": "📩 Қолдау қызметіне хабарлама жазыңыз:",
        "tr": "📩 Destek ekibine mesajınızı yazın:",
        "tg": "📩 Паёмро барои хадамоти дастгирӣ нависед:",
        "ky": "📩 Колдоо кызматына кабарыңызды жазыңыз:",
    },
    "support_sent": {
        "ru": "✅ Ваше сообщение отправлено администратору. Ожидайте ответа.",
        "uz": "✅ Xabaringiz administratorga yuborildi. Javobni kuting.",
        "kk": "✅ Хабарламаңыз әкімшіге жіберілді. Жауапты күтіңіз.",
        "tr": "✅ Mesajınız yöneticiye gönderildi. Yanıt bekleyin.",
        "tg": "✅ Паёми шумо ба администратор фиристода шуд. Ҷавобро интизор шавед.",
        "ky": "✅ Кабарыңыз администраторго жөнөтүлдү. Жооп күтүңүз.",
    },
    "support_too_long": {
        "ru": "❗ Сообщение слишком длинное (макс. 1000 символов).",
        "uz": "❗ Xabar juda uzun (maks. 1000 belgi).",
        "kk": "❗ Хабарлама тым ұзын (макс. 1000 таңба).",
    },
    "support_cancelled": {
        "ru": "↩️ Обращение отменено.",
        "uz": "↩️ Murojaat bekor qilindi.",
        "kk": "↩️ Өтініш болдырылмады.",
    },

    # ===== Пагинация =====
    "page_label": {
        "ru": "стр.",
        "uz": "bet",
        "kk": "бет",
        "tr": "sayfa",
        "tg": "саҳ.",
        "ky": "бет",
    },

    # ===== Поиск =====
    "search_prompt": {
        "ru": "🔍 Введите запрос для поиска (название или описание товара/услуги):",
        "uz": "🔍 Qidiruv so'rovini kiriting (tovar/xizmat nomi yoki tavsifi):",
        "kk": "🔍 Іздеу сұранысын енгізіңіз (тауар/қызмет атауы немесе сипаттамасы):",
        "tr": "🔍 Arama sorgusu girin (ürün/hizmet adı veya açıklaması):",
        "tg": "🔍 Дархости ҷустуҷӯро ворид кунед (номи мол/хидмат ё тавсифи он):",
        "ky": "🔍 Издөө сурамын жазыңыз (товар/кызмат аты же сүрөттөмөсү):",
    },
    "search_too_short": {
        "ru": "❗ Запрос слишком короткий. Введите от 2 символов.",
        "uz": "❗ So'rov juda qisqa. Kamida 2 ta belgi kiriting.",
        "kk": "❗ Сұраныс тым қысқа. Кемінде 2 таңба енгізіңіз.",
    },
    "search_results": {
        "ru": "🔍 По запросу <b>{query}</b> найдено {count}:",
        "uz": "🔍 <b>{query}</b> so'rovi bo'yicha {count} ta topildi:",
        "kk": "🔍 <b>{query}</b> сұранысы бойынша {count} табылды:",
    },
    "search_no_results": {
        "ru": "🔍 По запросу <b>{query}</b> ничего не найдено.",
        "uz": "🔍 <b>{query}</b> so'rovi bo'yicha hech narsa topilmadi.",
        "kk": "🔍 <b>{query}</b> сұранысы бойынша ештеңе табылмады.",
    },
    "search_cancelled": {
        "ru": "↩️ Поиск отменён.",
        "uz": "↩️ Qidiruv bekor qilindi.",
        "kk": "↩️ Іздеу болдырылмады.",
    },

    # ===== Просмотр отзывов =====
    "btn_view_reviews": {
        "ru": "📝 Отзывы",
        "uz": "📝 Sharhlar",
        "kk": "📝 Пікірлер",
        "tr": "📝 Yorumlar",
        "tg": "📝 Шарҳҳо",
        "ky": "📝 Сын-пикирлер",
    },
    "reviews_title": {
        "ru": "📝 <b>Отзывы о {name}</b>  (⭐ {rating})\n\n",
        "uz": "📝 <b>{name} haqida sharhlar</b>  (⭐ {rating})\n\n",
        "kk": "📝 <b>{name} туралы пікірлер</b>  (⭐ {rating})\n\n",
    },
    "no_reviews": {
        "ru": "У этого пользователя пока нет отзывов.",
        "uz": "Bu foydalanuvchida hali sharhlar yo'q.",
        "kk": "Бұл пайдаланушыда әлі пікірлер жоқ.",
    },
    "review_item": {
        "ru": "{'⭐' * rating}  — <i>{comment}</i>\n📅 {date}\n\n",
        "uz": "{'⭐' * rating}  — <i>{comment}</i>\n📅 {date}\n\n",
        "kk": "{'⭐' * rating}  — <i>{comment}</i>\n📅 {date}\n\n",
    },
    # ——— QR-код ———
    "qr_bot_caption": {
        "ru": "📱 QR-код для перехода в бот\nОтсканируйте или перешлите друзьям!",
        "uz": "📱 Botga o'tish uchun QR-kod\nSkanerlang yoki do'stlaringizga yuboring!",
        "kk": "📱 Ботқа өту үшін QR-код\nСканерлеңіз немесе достарыңызға жіберіңіз!",
        "tr": "📱 Bota geçiş için QR kod\nTarayın veya arkadaşlarınıza gönderin!",
        "tg": "📱 QR-код барои гузариш ба бот\nСканер кунед ё ба дӯстонатон фиристед!",
        "ky": "📱 Ботко өтүү үчүн QR-код\nСканерлеңиз же досторуңузга жөнөтүңүз!",
    },
    "qr_wallet_caption": {
        "ru": "📋 QR-код эскроу-кошелька для оплаты сделки #{id}",
        "uz": "📋 #{id}-bitim uchun eskrou-hamyon QR-kodi",
        "kk": "📋 #{id} мәміле үшін эскроу-әмиян QR-коды",
        "tr": "📋 #{id} anlaşması için emanet cüzdan QR kodu",
        "tg": "📋 QR-коди ҳамёни эскроу барои аҳдномаи #{id}",
        "ky": "📋 #{id} келишим үчүн эскроу-капчыгынын QR-коду",
    },

    # ===== РЕФЕРАЛЬНАЯ ПРОГРАММА =====
    "referral_welcome_bonus": {
        "ru": "🎁 Вас пригласил пользователь! Добро пожаловать в HandshakeDeal!",
        "uz": "🎁 Sizni foydalanuvchi taklif qildi! HandshakeDeal'ga xush kelibsiz!",
        "kk": "🎁 Сізді пайдаланушы шақырды! HandshakeDeal-ға қош келдіңіз!",
    },
    "referral_new_user_notify": {
        "ru": "🎉 По вашей реферальной ссылке зарегистрировался новый пользователь: <b>{name}</b>!",
        "uz": "🎉 Sizning referal havolangiz orqali yangi foydalanuvchi ro'yxatdan o'tdi: <b>{name}</b>!",
        "kk": "🎉 Сіздің реферал сілтемеңіз арқылы жаңа пайдаланушы тіркелді: <b>{name}</b>!",
    },
    "referral_info": {
        "ru": (
            "👥 <b>Реферальная программа</b>\n\n"
            "Ваша ссылка:\n<code>{link}</code>\n\n"
            "📊 Приглашено: <b>{total}</b>\n"
            "✅ Совершили сделку: <b>{active}</b>\n\n"
            "🎁 Приглашённый получает <b>первую сделку без комиссии</b>.\n"
            "Делитесь ссылкой и развивайте площадку!"
        ),
        "uz": (
            "👥 <b>Referal dasturi</b>\n\n"
            "Sizning havolangiz:\n<code>{link}</code>\n\n"
            "📊 Taklif qilingan: <b>{total}</b>\n"
            "✅ Bitim qilgan: <b>{active}</b>\n\n"
            "🎁 Taklif qilingan foydalanuvchi <b>birinchi bitimni komissiyasiz</b> oladi.\n"
            "Havolani ulashing va platformani rivojlantiring!"
        ),
        "kk": (
            "👥 <b>Реферал бағдарламасы</b>\n\n"
            "Сіздің сілтемеңіз:\n<code>{link}</code>\n\n"
            "📊 Шақырылған: <b>{total}</b>\n"
            "✅ Мәміле жасаған: <b>{active}</b>\n\n"
            "🎁 Шақырылған пайдаланушы <b>бірінші мәмілені комиссиясыз</b> алады.\n"
            "Сілтемені бөлісіңіз және платформаны дамытыңыз!"
        ),
    },
    "btn_referral": {
        "ru": "👥 Реферальная программа",
        "uz": "👥 Referal dasturi",
        "kk": "👥 Реферал бағдарламасы",
        "tr": "👥 Referans programı",
        "tg": "👥 Барномаи реферал",
        "ky": "👥 Реферал программасы",
    },

    # ===== СИСТЕМА РЕПУТАЦИИ =====
    "reputation_level": {
        "ru": "{emoji} Уровень: <b>{name}</b>",
        "uz": "{emoji} Daraja: <b>{name}</b>",
        "kk": "{emoji} Деңгей: <b>{name}</b>",
    },
    "reputation_discount_note": {
        "ru": "📉 Скидка на комиссию за репутацию: <b>−{discount}%</b>",
        "uz": "📉 Obro' uchun komissiya chegirmasi: <b>−{discount}%</b>",
        "kk": "📉 Беделге комиссия жеңілдігі: <b>−{discount}%</b>",
    },
    "reputation_bronze": {"ru": "Бронза", "uz": "Bronza", "kk": "Қола"},
    "reputation_silver": {"ru": "Серебро", "uz": "Kumush", "kk": "Күміс"},
    "reputation_gold": {"ru": "Золото", "uz": "Oltin", "kk": "Алтын"},

    # ===== ФОТО-ОТЗЫВЫ =====
    "review_photo_prompt": {
        "ru": "📸 Прикрепите фото (товара, результата и т.д.) или нажмите /skip чтобы пропустить:",
        "uz": "📸 Rasm biriktiring (tovar, natija va h.k.) yoki o'tkazib yuborish uchun /skip bosing:",
        "kk": "📸 Фото тіркеңіз (тауар, нәтиже т.б.) немесе өткізіп жіберу үшін /skip басыңыз:",
    },

    # ===== ИЗБРАННОЕ / ПОДПИСКА НА ПРОДАВЦА =====
    "btn_follow_seller": {
        "ru": "⭐ Подписаться",
        "uz": "⭐ Obuna bo'lish",
        "kk": "⭐ Жазылу",
    },
    "btn_unfollow_seller": {
        "ru": "💔 Отписаться",
        "uz": "💔 Obunani bekor qilish",
        "kk": "💔 Жазылудан бас тарту",
    },
    "btn_favorites": {
        "ru": "⭐ Избранное",
        "uz": "⭐ Sevimlilar",
        "kk": "⭐ Таңдаулылар",
        "tr": "⭐ Favoriler",
        "tg": "⭐ Дӯстдоштаҳо",
        "ky": "⭐ Тандалмалар",
    },
    "followed_seller": {
        "ru": "⭐ Вы подписались на продавца <b>{name}</b>. Вы получите уведомление о новых объявлениях.",
        "uz": "⭐ Siz <b>{name}</b> sotuvchisiga obuna bo'ldingiz. Yangi e'lonlar haqida xabar olasiz.",
        "kk": "⭐ Сіз <b>{name}</b> сатушысына жазылдыңыз. Жаңа хабарландырулар туралы хабарлама аласыз.",
    },
    "unfollowed_seller": {
        "ru": "💔 Вы отписались от продавца <b>{name}</b>.",
        "uz": "💔 Siz <b>{name}</b> sotuvchisidan obunani bekor qildingiz.",
        "kk": "💔 Сіз <b>{name}</b> сатушысынан жазылудан бас тарттыңыз.",
    },
    "favorites_empty": {
        "ru": "⭐ У вас пока нет подписок на продавцов.\nПодпишитесь на продавца через его профиль в каталоге.",
        "uz": "⭐ Sizda hali sotuvchilarga obuna yo'q.\nKatalogdagi profili orqali obuna bo'ling.",
        "kk": "⭐ Сізде әлі сатушыларға жазылым жоқ.\nКаталогтағы профилі арқылы жазылыңыз.",
    },
    "favorites_list_title": {
        "ru": "⭐ <b>Ваши подписки:</b>\n",
        "uz": "⭐ <b>Sizning obunalaringiz:</b>\n",
        "kk": "⭐ <b>Сіздің жазылымдарыңыз:</b>\n",
    },
    "new_listing_notify_follower": {
        "ru": (
            "🔔 Новое объявление от продавца, на которого вы подписаны!\n\n"
            "👤 {seller}\n"
            "📌 <b>{title}</b>\n"
            "💰 {price} USDT\n"
            "📍 {city}"
        ),
        "uz": (
            "🔔 Obuna bo'lgan sotuvchidan yangi e'lon!\n\n"
            "👤 {seller}\n"
            "📌 <b>{title}</b>\n"
            "💰 {price} USDT\n"
            "📍 {city}"
        ),
        "kk": (
            "🔔 Жазылған сатушыдан жаңа хабарландыру!\n\n"
            "👤 {seller}\n"
            "📌 <b>{title}</b>\n"
            "💰 {price} USDT\n"
            "📍 {city}"
        ),
    },
    "cant_follow_self": {
        "ru": "❌ Нельзя подписаться на себя",
        "uz": "❌ O'zingizga obuna bo'lolmaysiz",
        "kk": "❌ Өзіңізге жазыла алмайсыз",
    },
    "profile_followers": {
        "ru": "👥 Подписчиков",
        "uz": "👥 Obunachilar",
        "kk": "👥 Жазылушылар",
    },
    "profile_referrals": {
        "ru": "👥 Рефералов",
        "uz": "👥 Referallar",
        "kk": "👥 Рефералдар",
    },
    "action_cancelled": {
        "ru": "❌ Действие отменено.",
        "uz": "❌ Amal bekor qilindi.",
        "kk": "❌ Әрекет тоқтатылды.",
    },
    "create_listing_cancelled": {
        "ru": "❌ Создание объявления отменено.",
        "uz": "❌ E'lon yaratish bekor qilindi.",
        "kk": "❌ Хабарландыру жасау тоқтатылды.",
    },
    "support_cancelled": {
        "ru": "❌ Обращение отменено.",
        "uz": "❌ Murojaat bekor qilindi.",
        "kk": "❌ Өтініш тоқтатылды.",
    },
    "city_input_cancelled": {
        "ru": "❌ Ввод города отменён.",
        "uz": "❌ Shahar kiritish bekor qilindi.",
        "kk": "❌ Қала енгізу тоқтатылды.",
    },
    "support_rate_limit": {
        "ru": "⏳ Подождите немного перед следующим обращением.",
        "uz": "⏳ Keyingi murojaat uchun biroz kuting.",
        "kk": "⏳ Келесі өтініш үшін біраз күтіңіз.",
    },
    "resolve_confirm_seller": {
        "ru": (
            "⚠️ <b>Подтвердите решение спора #{id}</b>\n\n"
            "Действие: выплата продавцу\n"
            "💰 Сумма: {payout} USDT → <code>{wallet}</code>\n\n"
            "Вы уверены?"
        ),
        "uz": (
            "⚠️ <b>Nizoni hal qilishni tasdiqlang #{id}</b>\n\n"
            "Harakat: sotuvchiga to'lov\n"
            "💰 Summa: {payout} USDT → <code>{wallet}</code>\n\n"
            "Ishonchingiz komilmi?"
        ),
        "kk": (
            "⚠️ <b>Дау шешімін растаңыз #{id}</b>\n\n"
            "Әрекет: сатушыға төлем\n"
            "💰 Сома: {payout} USDT → <code>{wallet}</code>\n\n"
            "Сенімдісіз бе?"
        ),
    },
    "resolve_confirm_buyer": {
        "ru": (
            "⚠️ <b>Подтвердите решение спора #{id}</b>\n\n"
            "Действие: возврат покупателю\n"
            "💰 Сумма: {total} USDT\n\n"
            "Вы уверены?"
        ),
        "uz": (
            "⚠️ <b>Nizoni hal qilishni tasdiqlang #{id}</b>\n\n"
            "Harakat: xaridorga qaytarish\n"
            "💰 Summa: {total} USDT\n\n"
            "Ishonchingiz komilmi?"
        ),
        "kk": (
            "⚠️ <b>Дау шешімін растаңыз #{id}</b>\n\n"
            "Әрекет: сатып алушыға қайтару\n"
            "💰 Сома: {total} USDT\n\n"
            "Сенімдісіз бе?"
        ),
    },
    "followers_notified": {
        "ru": "📣 Уведомлено подписчиков: {count}",
        "uz": "📣 Xabardor qilingan obunachilar: {count}",
        "kk": "📣 Хабарландырылған жазылушылар: {count}",
    },
    "account_banned": {
        "ru": "🚫 Ваш аккаунт заблокирован. Обратитесь в поддержку: /support",
        "uz": "🚫 Hisobingiz bloklangan. Qo'llab-quvvatlash: /support",
        "kk": "🚫 Аккаунтыңыз бұғатталған. Қолдау қызметі: /support",
    },
    "btn_change_lang": {
        "ru": "🌐 Сменить язык",
        "uz": "🌐 Tilni o'zgartirish",
        "kk": "🌐 Тілді ауыстыру",
    },
    "vip_days_left": {
        "ru": "⏳ Осталось дней: <b>{days}</b>",
        "uz": "⏳ Qolgan kunlar: <b>{days}</b>",
        "kk": "⏳ Қалған күндер: <b>{days}</b>",
    },
}

# ————— Подключение внешних переводов —————
from _lang_tr import TR
from _lang_tg import TG
from _lang_ky import KY
from _lang_en import EN

for _lang_code, _translations in [("tr", TR), ("tg", TG), ("ky", KY), ("en", EN)]:
    for _key, _val in _translations.items():
        if _key in TEXTS:
            TEXTS[_key][_lang_code] = _val


def t(lang: str, key: str, **kwargs) -> str:
    """Получить перевод по ключу и языку."""
    entry = TEXTS.get(key, {})
    text = entry.get(lang, entry.get("ru", key))
    if kwargs:
        text = text.format(**kwargs)
    return text


def get_category_name(key: str, lang: str) -> str:
    """Название категории на нужном языке."""
    cat_key = f"cat_{key}"
    entry = TEXTS.get(cat_key, {})
    return entry.get(lang, entry.get("ru", key))


def btn(lang: str, key: str) -> str:
    """Текст кнопки на нужном языке."""
    return t(lang, key)


def all_btn_texts(key: str) -> list[str]:
    """Все языковые варианты кнопки — для F.text.in_()."""
    entry = TEXTS.get(key, {})
    return list(entry.values())
