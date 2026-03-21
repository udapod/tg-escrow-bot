"""Турецкие (tr) переводы — все 222 ключа."""

TR = {
    # ===== КНОПКИ МЕНЮ =====
    "btn_catalog": "📋 Katalog",
    "btn_create_listing": "➕ İlan oluştur",
    "btn_my_deals": "📦 İşlemlerim",
    "btn_my_listings": "📝 İlanlarım",
    "btn_vip": "👑 VIP-abonelik",
    "btn_profile": "👤 Profil",
    "btn_search": "🔍 Arama",
    "btn_help": "ℹ️ Yardım",

    # ===== КНОПКИ INLINE =====
    "btn_start_deal": "🤝 İşlem başlat",
    "btn_seller_profile": "👤 Satıcı profili",
    "btn_i_sent_usdt": "💰 USDT emanete gönderdim",
    "btn_cancel_deal": "❌ İşlemi iptal et",
    "btn_order_done": "📦 Sipariş tamamlandı / Ürün gönderildi",
    "btn_open_dispute": "⚠️ İtiraz aç",
    "btn_confirm_received": "✅ Teslim aldığımı onaylıyorum",
    "btn_leave_review": "⭐ Yorum bırak",
    "btn_yes": "✅ Evet",
    "btn_no": "❌ Hayır",
    "btn_delete_listing": "🗑 İlanı sil",
    "btn_back_menu": "⬅️ Menüye",
    "btn_buy_vip": "👑 VIP-abonelik satın al",
    "btn_i_paid_vip": "💰 VIP için ödedim",
    "btn_cancel": "❌ İptal",

    # ===== КАТЕГОРИИ =====
    "cat_goods": "🛒 Ürünler",
    "cat_services": "🔧 Hizmetler",

    # ===== /start =====
    "welcome": (
        "🤝 <b>HandshakeDeal'e hoş geldiniz!</b>\n\n"
        "🔐 <b>Güvenilir emanet garantisi</b> P2P işlemler için.\n"
        "Ürün ve hizmetleri risksiz alıp satın!\n\n"
        "🛡 <b>Nasıl çalışır:</b>\n"
        "1️⃣ Satıcı ilan oluşturur\n"
        "2️⃣ Alıcı USDT'yi <b>bot emanet cüzdanına</b> gönderir\n"
        "3️⃣ 🔓 İletişim bilgileri açılır — buluşma ayarlanabilir\n"
        "4️⃣ Alıcı teslim aldığını onaylar\n"
        "5️⃣ Fonlar satıcıya gönderilir ⭐\n\n"
        "🎁 <b>İlk işlem komisyonsuz!</b>\n"
        "❗ Ödemeden sonra iptal edilirse %2 ceza kesilir.\n\n"
        "Aşağıdaki menüyü kullanın 👇"
    ),

    # ===== Выбор языка =====
    "choose_lang": "🌐 Dil seçin / Выберите язык / Choose language:",
    "lang_set": "✅ Dil seçildi: Türkçe",

    # ===== МЕСТОПОЛОЖЕНИЕ =====
    "choose_country": "🌍 Ülkenizi seçin:",
    "choose_city": "🏙 Şehrinizi seçin ({country}):",
    "city_other": "📝 Başka şehir",
    "enter_city_manual": "✏️ Şehir adını girin:",
    "city_too_short": "❗ Ad çok kısa. Şehir adını girin (2-50 karakter):",
    "location_set": "📍 Konum: {country}, {city}",
    "btn_change_location": "📍 Şehir değiştir",
    "profile_location": "📍 Şehir",
    "location_not_set": "belirtilmemiş",
    "set_location_first": "📍 Önce konumunuzu belirtin — /location",
    "listing_city": "📍 Şehir",
    "all_cities": "🌐 Tüm şehirler",

    # ===== ЧАТ СДЕЛКИ =====
    "btn_chat": "💬 İşlem sohbeti",
    "chat_role_seller": "satıcı",
    "chat_role_buyer": "alıcı",
    "chat_msg_from_buyer": "💬 <b>Alıcı</b> (işlem #{id}):\n{text}",
    "chat_msg_from_seller": "💬 <b>Satıcı</b> (işlem #{id}):\n{text}",
    "chat_contact_blocked": (
        "🚫 İletişim bilgileri (telefon, @kullanıcıadı, bağlantılar) emanet ödemesine kadar engellenmiştir.\n"
        "Ödemeden sonra otomatik olarak açılacaktır."
    ),
    "chat_sent": "✅ Gönderildi",
    "chat_exited": "👋 İşlem sohbetinden çıktınız.",
    "chat_no_deal": "❗ İşlem bulunamadı veya zaten tamamlandı.",
    "chat_history_title": "📜 <b>Yazışma geçmişi — işlem #{id}</b>\n",
    "chat_history_empty": "📜 İşlem #{id} yazışması boş.",
    "btn_view_chat_history": "📜 Yazışmalar",

    # ===== ВСТРЕЧА =====
    "btn_propose_meet": "📍 Buluşma teklif et",
    "meet_enter_location": "📍 Buluşma yerini belirtin (adres, AVM vb.):",
    "meet_enter_datetime": "🕐 Buluşma tarih ve saatini belirtin (örn: yarın 15:00, 20.03 12:00):",
    "meet_proposal_sent": "✅ Buluşma teklifi gönderildi!",
    "meet_proposal_card": (
        "📍 <b>Buluşma teklifi — işlem #{id}</b>\n\n"
        "🏠 Yer: <b>{location}</b>\n"
        "🕐 Zaman: <b>{datetime}</b>\n\n"
        "Saat/yeri değiştirmek isterseniz işlem sohbetinde yanıt yazın."
    ),
    "meet_cancelled": "❌ Buluşma teklifi iptal edildi. Sohbete döndünüz.",
    "chat_enter": (
        "💬 <b>İşlem sohbeti #{id}</b>\n\n"
        "Anonim olarak {role} ile iletişimdesiniz.\n"
        "Mesaj yazın — bot iletecektir.\n\n"
        "📍 /meet — buluşma teklif et\n"
        "/endchat — sohbetten çık"
    ),

    # ===== /help =====
    "help": (
        "📖 <b>HandshakeDeal Kuralları ve Koşulları</b>\n\n"
        "📝 <b>Ana özellikler:</b>\n"
        "📋 <b>Katalog</b> — şehrinizdeki ilanları görüntüleme\n"
        "➕ <b>İlan oluştur</b> — ürün/hizmet yayınla\n"
        "📦 <b>İşlemlerim</b> — mevcut ve tamamlanmış işlemler\n"
        "👤 <b>Profil</b> — puan, cüzdan, istatistikler\n\n"
        "🔐 <b>Emanet garantisi:</b>\n"
        "• Alıcı USDT'yi bot cüzdanına gönderir\n"
        "• Para, teslim alınana kadar dondurulur\n"
        "• Satıcı yalnızca işlem tamamlandıktan sonra ödeme alır\n"
        "• 72 saat sonra otomatik tamamlanır\n"
        "• İtiraz = yönetici kararına kadar dondurma\n\n"
        "💰 <b>Komisyonlar (kademeli ölçek):</b>\n"
        "• 🎁 İlk işlem — <b>komisyonsuz (0%)</b>\n"
        "• 20–100 USDT — <b>%3</b> (min. 2 USDT)\n"
        "• 100–500 USDT — <b>%2</b>\n"
        "• 500+ USDT — <b>%1,5</b>\n"
        "• 👑 VIP — yarı yarıya: %1,5 / %1 / %0,75 (min. 1 USDT)\n"
        "• 👑 VIP abonelik — <b>10 USDT</b>/ay\n"
        "• Minimum işlem tutarı — <b>20 USDT</b>\n\n"
        "💬 <b>İşlem sohbeti:</b>\n"
        "• Ödemeden önce — anonim sohbet (iletişim bilgileri engelli)\n"
        "• Ödemeden sonra — 🔓 iletişim bilgileri açık\n"
        "• Telefon, adres paylaşılabilir\n"
        "• 📍 /meet — buluşma teklif et\n\n"
        "⚠️ <b>İşlem iptali:</b>\n"
        "• Ödemeden önce — ücretsiz\n"
        "• Ödemeden sonra — <b>%2 ceza</b>\n"
        "• Kalan tutar alıcıya iade edilir\n\n"
        "💱 Tüm işlemler USDT (TRC-20) ile yapılır.\n"
        "📱 /qr — arkadaşlarınızı davet etmek için QR kod\n"
        "Destek: /support"
    ),

    # ===== Профиль =====
    "profile_title": "👤 <b>Profiliniz</b>",
    "profile_vip_status": "👑 Durum: <b>Doğrulanmış (VIP)</b>",
    "profile_id": "🆔 ID",
    "profile_name": "📛 Ad",
    "profile_rating": "⭐ Puan",
    "profile_deals": "📦 Tamamlanan işlemler",
    "profile_wallet": "💰 USDT cüzdanı (TRC-20)",
    "profile_reviews": "📝 Yorumlar",
    "wallet_not_set": "❌ Belirtilmemiş",
    "wallet_hint": "Cüzdan belirtmek/değiştirmek için:\n/wallet <code>TRC20_ADRESİNİZ</code>",
    "wallet_prompt": "❗ TRC-20 USDT cüzdanınızı belirtin:\n/wallet <code>T...</code>",
    "wallet_invalid": "❌ Geçersiz TRC-20 adres formatı. Adres T ile başlamalı ve 34 karakter olmalıdır.",
    "wallet_saved": "✅ Cüzdan kaydedildi",

    # ===== Чужой профиль =====
    "profile_view_title": "👤 <b>Kullanıcı profili</b>",
    "profile_since": "📅 Sistemde",
    "profile_deals_count": "📦 İşlemler",

    # ===== Объявления =====
    "press_start_first": "Önce /start basın",
    "account_banned": "🚫 Hesabınız engellendi. Destek: /support",
    "set_wallet_first": "❗ Önce USDT cüzdanınızı (TRC-20) belirtin:\n/wallet <code>ADRESİNİZ</code>",
    "choose_category": "Kategori seçin:",
    "invalid_category": "❌ Geçersiz kategori.",
    "enter_title": "📝 Başlık girin (en fazla 100 karakter):",
    "title_error": "❗ Başlık 3-100 karakter arası olmalıdır. Tekrar deneyin:",
    "enter_description": "📋 Açıklama girin (en fazla 500 karakter):",
    "desc_error": "❗ Açıklama 10-500 karakter arası olmalıdır. Tekrar deneyin:",
    "enter_price": "💰 USDT cinsinden fiyat belirtin (sayı):",
    "enter_photo": "📸 Ürün/hizmet fotoğrafı gönderin veya atlamak için /skip basın:",
    "price_min_error": "❗ Minimum işlem tutarı — {amount} USDT. Daha yüksek fiyat belirtin:",
    "price_error": "❗ Geçerli fiyat girin (0,01 — 1.000.000 USDT):",
    "listing_created": "✅ #{id} numaralı ilan oluşturuldu!\n\n📂 {cat}\n📌 {title}\n💰 {price} USDT\n\nKatalogda görünecektir.",
    "no_listings_in_cat": "<b>{cat}</b> kategorisinde henüz ilan yok.",
    "listings_found": "📋 <b>{cat}</b> — {count} bulundu:",
    "seller": "Satıcı",
    "price_label": "Fiyat",
    "unknown_seller": "Bilinmeyen",
    "no_my_listings": "Henüz ilanınız yok. «➕ İlan oluştur» basın.",
    "listing_active": "✅ Aktif",
    "listing_inactive": "❌ Pasif",
    "status_label": "Durum",
    "confirm_delete_listing": "#{id} «{title}» ilanını silmek istiyor musunuz?",
    "listing_deleted": "✅ İlan silindi.",
    "action_cancelled": "❌ İşlem iptal edildi.",

    # ===== Сделки =====
    "listing_unavailable": "❌ Bu ilan artık mevcut değil.",
    "cant_buy_own": "Kendinizden satın alamazsınız!",
    "min_deal_amount": "⚠️ Minimum işlem tutarı — {amount} USDT",
    "seller_no_wallet": "Satıcının cüzdanı belirtilmemiş",
    "deal_created": (
        "🤝 <b>İşlem #{id} oluşturuldu!</b>\n\n"
        "{vip_note}"
        "📌 {title}\n"
        "💰 Fiyat: {price} USDT\n"
        "📊 Bot komisyonu ({rate}%): {commission} USDT\n"
        "💵 <b>Toplam ödeme: {total} USDT</b>\n\n"
        "🔐 <b>EMANET GARANTİSİ:</b>\n"
        "Paranız, ürün/hizmeti teslim aldığınızı onaylayana kadar\n"
        "bot cüzdanında dondurulacaktır.\n\n"
        "📋 <b>{total} USDT</b>'yi bot emanet cüzdanına gönderin:\n"
        "<code>{wallet}</code>\n\n"
        "⚠️ Ağ: <b>TRC-20</b>\n"
        "Gönderdikten sonra «💰 USDT emanete gönderdim» basın"
    ),
    "deal_new_seller_notify": (
        "🔔 <b>Yeni işlem #{id}!</b>\n\n"
        "📌 {title}\n💰 {price} USDT\n"
        "👤 Alıcı: {buyer}\n\n"
        "🔐 Alıcı fonları bot emanetine gönderiyor.\n"
        "Para dondurulduğunda size bildirim gelecektir."
    ),
    "deal_not_found": "İşlem bulunamadı",
    "deal_status_locked": "Bu işlemin durumu değiştirilemez",
    "enter_tx_hash": (
        "📋 <b>İşlem #{id}</b>\n\n"
        "Onay için işlem hash'ini (TxID) girin:\n\n"
        "💡 Hash şu şekilde görünür:\n"
        "<code>a1b2c3d4e5f6...</code> (64 karakter)"
    ),
    "tx_hash_invalid": "❗ Geçersiz TxID formatı.\nTRON işlem hash'i 64 karakter içerir, örn.:\n<code>a1b2c3d4e5f6...</code>\nGeçerli TxID girin:",
    "tx_already_used": "🚫 Bu TxID başka bir işlemde kullanıldı. Farklı TxID girin:",
    "message_too_long": "⚠️ Mesaj çok uzun (maks. 2000 karakter).",
    "tx_verifying": "⏳ TRON blok zincirinde işlem kontrol ediliyor...",
    "tx_not_found": "❌ İşlem blok zincirinde bulunamadı.\nTxID'yi kontrol edin ve tekrar deneyin (birkaç dakika bekleyin):",
    "tx_wrong_wallet": "❌ İşlem bulundu, ancak alıcı bot cüzdanı değil.\nUSDT'yi doğru adrese gönderin ve yeni TxID girin:",
    "tx_amount_mismatch": "❌ İşlem tutarı ({received} USDT) gerekenden ({expected} USDT) az.\nTam tutarı gönderin ve yeni TxID girin:",
    "tx_not_usdt": "❌ Bu bot cüzdanına USDT TRC-20 transferi değil.\nUSDT (TRC-20) gönderin ve doğru TxID girin:",
    "tx_network_error": "⚠️ İşlem kontrol edilemedi (ağ hatası). Bir dakika sonra tekrar deneyin:",
    "tx_verified": "✅ İşlem blok zinciri tarafından onaylandı!",
    "tx_admin_verified": (
        "✅ <b>Ödeme onaylandı</b>\n\n"
        "🆔 İşlem: #{id}\n"
        "📋 Ürün: {title}\n"
        "👤 Alıcı: {buyer_id}\n"
        "👥 Satıcı: {seller_id}\n"
        "💵 Ürün fiyatı: {price} USDT\n"
        "💰 Emanet (komisyonlu): {amount} USDT\n"
        "🔗 TxHash: <code>{tx}</code>"
    ),
    "tx_admin_failed": (
        "⚠️ <b>TxHash doğrulaması başarısız</b>\n\n"
        "🆔 İşlem: #{id}\n"
        "📋 Ürün: {title}\n"
        "👤 Alıcı: {buyer_id}\n"
        "👥 Satıcı: {seller_id}\n"
        "💰 Emanet: {amount} USDT\n"
        "❌ Neden: {reason}\n"
        "🔗 TxHash: <code>{tx}</code>\n"
        "🔄 Deneme: {attempt}/3"
    ),
    "tx_blocked": "🚫 Çok fazla başarısız deneme. İşlem engellendi — yöneticiye başvurun.",
    "tx_admin_blocked": (
        "🚫 <b>İşlem engellendi</b>\n\n"
        "🆔 İşlem: #{id}\n"
        "📋 Ürün: {title}\n"
        "👤 Alıcı: {buyer_id}\n"
        "👥 Satıcı: {seller_id}\n"
        "💰 Emanet: {amount} USDT\n"
        "❌ 3 başarısız TxHash doğrulaması\n"
        "⚡ Manuel kontrol gerekli"
    ),
    "deal_paid": (
        "✅ <b>İşlem #{id} — ödeme kaydedildi!</b>\n\n"
        "📌 {title}\n"
        "💰 {total} USDT emanette donduruldu\n"
        "🔗 TxID: <code>{tx}</code>\n\n"
        "⏳ Satıcının siparişi yerine getirmesini bekliyoruz...\n\n"
        "Ürün/hizmeti teslim aldıktan sonra «✅ Teslim aldığımı onaylıyorum» basın."
    ),
    "deal_escrow_seller_notify": (
        "💰 <b>İşlem #{id} — fonlar emanette!</b>\n\n"
        "📌 {title}\n"
        "💵 {total} USDT bot cüzdanında donduruldu.\n"
        "🔗 Alıcı TxID: <code>{tx}</code>\n\n"
        "✅ Alıcı ödedi. Siparişi tamamlayın ve\n"
        "«📦 Sipariş tamamlandı» basın."
    ),
    "deal_delivered_seller": (
        "📦 <b>İşlem #{id} — sipariş tamamlandı!</b>\n\n"
        "Alıcıdan onay bekleniyor.\n\n"
        "⏳ Alıcı <b>{hours} saat</b> içinde onaylamazsa\n"
        "ve itiraz açmazsa — işlem otomatik tamamlanır,\n"
        "fonlar size gönderilir."
    ),
    "deal_delivered_buyer_notify": (
        "📦 <b>İşlem #{id} — satıcı siparişi tamamladı!</b>\n\n"
        "📌 {title}\n👤 Satıcı: {seller}\n\n"
        "Ürün/hizmeti teslim aldıysanız — onaylayın,\n"
        "fonlar otomatik satıcıya gönderilir.\n\n"
        "⚠️ Sorun varsa — itiraz açın.\n"
        "⏳ Yanıt olmazsa <b>{hours} saat</b> içinde otomatik tamamlanır."
    ),
    "deal_completed_buyer": (
        "🎉 <b>İşlem #{id} tamamlandı!</b>\n\n"
        "📌 {title}\n"
        "💵 {payout} USDT satıcıya gönderilecek.\n"
        "📊 {commission} USDT komisyon bot tarafından kesildi.\n\n"
        "Güveniniz için teşekkürler! Yorum bırakın:"
    ),
    "deal_completed_seller_notify": (
        "🎉 <b>İşlem #{id} tamamlandı!</b>\n\n"
        "📌 {title}\n"
        "✅ Alıcı teslim aldığını onayladı.\n"
        "💵 <b>{payout} USDT</b> cüzdanınıza gönderilecek:\n"
        "<code>{wallet}</code>\n\n"
        "Alıcı hakkında yorum bırakın:"
    ),
    "deal_cancelled": "❌ İşlem #{id} iptal edildi.",
    "deal_cancelled_seller_notify": "❌ İşlem #{id} alıcı tarafından iptal edildi (ödemeden önce).",
    "cancel_only_before_pay": "İptal yalnızca emanet ödemesinden önce mümkündür",
    "cancel_not_available": "İptal şu anda mevcut değil",
    "deal_cancelled_penalty": (
        "❌ <b>İşlem #{id} ödemeden sonra iptal edildi</b>\n\n"
        "🔻 İptal cezası ({penalty_pct}%): <b>{penalty} USDT</b>\n"
        "💸 İade: <b>{refund} USDT</b>\n\n"
        "Yönetici cezayı keserek fonları iade edecek."
    ),
    "deal_cancelled_seller_after_pay": "❌ İşlem #{id} ({title}) alıcı tarafından ödemeden sonra iptal edildi. Fonlar alıcıya iade ediliyor.",
    "first_deal_free_note": "🎁 <b>İlk işlem komisyonsuz!</b>\n",
    "chat_contacts_unlocked": "🔓 Ödeme onaylandı — iletişim bilgisi paylaşımı açık!\nArtık telefon ve adres paylaşabilirsiniz.",

    # ===== Споры =====
    "dispute_opened": (
        "⚠️ <b>İşlem #{id} hakkında itiraz açıldı!</b>\n\n"
        "🔐 Fonlar emanette donduruldu.\n"
        "Yönetici itirazı inceleyip karar verecek.\n\n"
        "İtiraz çözülene kadar kimse ödeme almaz."
    ),
    "dispute_other_notify": "⚠️ İşlem #{id} hakkında itiraz açıldı.\n🔐 Fonlar yönetici kararına kadar donduruldu.",
    "dispute_only_escrow": "İtiraz yalnızca fonlar emanetteyken mümkündür",
    "no_access": "Erişim yok",

    # ===== Отзывы =====
    "review_only_completed": "Yorum yalnızca işlem tamamlandıktan sonra bırakılabilir",
    "review_not_participant": "Bu işlemin katılımcısı değilsiniz",
    "review_rate": "⭐ İşlem #{id}'yi puanlayın:",
    "review_comment": "💬 Yorum yazın (atlamak için «-» gönderin):",
    "review_comment_too_long": "❗ Yorum en fazla 300 karakter. Tekrar deneyin:",
    "review_saved": "✅ Yorum kaydedildi!",

    # ===== Мои сделки =====
    "no_deals": "Henüz işleminiz yok.",
    "my_deals_title": "📦 <b>İşlemleriniz:</b>",
    "role_buyer": "🛒 Alıcı",
    "role_seller": "🏪 Satıcı",
    "deal_status_created": "🕐 Emanet ödemesi bekleniyor",
    "deal_status_paid": "🔐 Fonlar emanette (yürütülüyor)",
    "deal_status_delivered": "📦 Teslim edildi (onay bekleniyor)",
    "deal_status_completed": "🎉 Tamamlandı",
    "deal_status_disputed": "⚠️ İtiraz (fonlar donduruldu)",
    "deal_status_cancelled": "❌ İptal edildi",
    "deal_status_refunded": "💸 İade",

    # ===== VIP =====
    "vip_active": (
        "👑 <b>Aktif VIP aboneliğiniz var!</b>\n\n"
        "✅ Durum: Doğrulanmış satıcı\n"
        "📅 Geçerlilik: <b>{expires}</b>\n"
        "💰 Komisyonunuz: <b>{vip_rate}%</b> ({rate}% yerine)\n\n"
        "🛡 Avantajlar:\n"
        "• ✅ Profilde «Doğrulanmış» rozeti\n"
        "• 📌 Katalogda öncelik\n"
        "• 💰 Düşük komisyon {vip_rate}%\n"
        "• ⭐ Alıcıların yüksek güveni"
    ),
    "vip_offer": (
        "👑 <b>VIP Abonelik</b>\n\n"
        "Doğrulanmış satıcı olun ve kazanın:\n\n"
        "✅ Adınızın yanında «Doğrulanmış» rozeti\n"
        "📌 Katalogda öncelik\n"
        "💰 Düşük komisyon: <b>{vip_rate}%</b> ({rate}% yerine)\n"
        "⭐ Alıcıların yüksek güveni\n\n"
        "💵 Fiyat: <b>{price} USDT / {days} gün</b>"
    ),
    "vip_already_active": "Zaten aktif VIP aboneliğiniz var!",
    "vip_payment": (
        "👑 <b>VIP Abonelik Ödemesi</b>\n\n"
        "💵 Tutar: <b>{price} USDT</b>\n"
        "📅 Süre: {days} gün\n\n"
        "📋 <b>{price} USDT</b>'yi bot cüzdanına gönderin:\n"
        "<code>{wallet}</code>\n\n"
        "⚠️ Ağ: <b>TRC-20</b>\n\n"
        "Gönderdikten sonra «💰 VIP için ödedim» basın"
    ),
    "vip_enter_tx": "📋 <b>VIP Abonelik — ödeme onayı</b>\n\nİşlem hash'ini (TxID) girin:",
    "vip_activated": (
        "🎉 <b>VIP abonelik etkinleştirildi!</b>\n\n"
        "👑 Artık doğrulanmış satıcısınız!\n"
        "📅 {days} gün geçerli\n"
        "💰 Komisyonunuz: {vip_rate}%\n"
        "✅ Doğrulama rozeti profilinizde\n\n"
        "🔗 TxID: <code>{tx}</code>"
    ),
    "vip_cancelled": "❌ VIP satın alma iptal edildi.",
    "vip_seller_note": "👑 Satıcı doğrulanmış (VIP)\n",

    # ===== Главное меню =====
    "main_menu": "Ana menü 👇",
    "error_try_again": "Hata. Yeniden başlayın.",
    "deal_status_changed": "İşlem bulunamadı veya durumu değişti.",
    "cant_confirm_now": "Bu aşamada onaylama yapılamaz",
    "deal_not_at_execution": "İşaretlenemez — işlem yürütme aşamasında değil",

    # ===== Удаление аккаунта =====
    "btn_delete_account": "🗑 Hesabı sil",
    "delete_account_confirm": (
        "⚠️ <b>Hesabınızı silmek istediğinizden emin misiniz?</b>\n\n"
        "Silinecekler:\n"
        "• Profiliniz ve cüzdanınız\n"
        "• Tüm ilanlarınız\n"
        "• VIP abonelik\n\n"
        "❗ Aktif işlemler etkilenmeyecektir.\n"
        "Bu işlem <b>geri alınamaz</b>!"
    ),
    "account_deleted": "✅ Hesabınız silindi. Tüm veriler silindi.\nYeniden kayıt için /start basın",
    "delete_account_has_active_deals": "❌ Hesap silinemez — aktif işlemleriniz var. Önce bunları tamamlayın veya iptal edin.",

    # ===== Поддержка =====
    "support_prompt": "📩 Destek ekibine mesajınızı yazın:",
    "support_sent": "✅ Mesajınız yöneticiye gönderildi. Yanıt bekleyin.",
    "support_too_long": "❗ Mesaj çok uzun (maks. 1000 karakter).",
    "support_cancelled": "❌ Başvuru iptal edildi.",

    # ===== Пагинация =====
    "page_label": "sayfa",

    # ===== Поиск =====
    "search_prompt": "🔍 Arama sorgusu girin (ürün/hizmet adı veya açıklaması):",
    "search_too_short": "❗ Sorgu çok kısa. En az 2 karakter girin.",
    "search_results": "🔍 <b>{query}</b> sorgusu için {count} bulundu:",
    "search_no_results": "🔍 <b>{query}</b> sorgusu için hiçbir şey bulunamadı.",
    "search_cancelled": "↩️ Arama iptal edildi.",

    # ===== Отзывы (просмотр) =====
    "btn_view_reviews": "📝 Yorumlar",
    "reviews_title": "📝 <b>{name} hakkında yorumlar</b>  (⭐ {rating})\n\n",
    "no_reviews": "Bu kullanıcının henüz yorumu yok.",
    "review_item": "{'⭐' * rating}  — <i>{comment}</i>\n📅 {date}\n\n",

    # ===== QR =====
    "qr_bot_caption": "📱 Bota geçiş için QR kod\nTarayın veya arkadaşlarınıza gönderin!",
    "qr_wallet_caption": "📋 İşlem #{id} ödemesi için emanet cüzdanı QR kodu",

    # ===== Реферальная программа =====
    "referral_welcome_bonus": "🎁 Bir kullanıcı sizi davet etti! HandshakeDeal'e hoş geldiniz!",
    "referral_new_user_notify": "🎉 Referans bağlantınızla yeni kullanıcı kaydoldu: <b>{name}</b>!",
    "referral_info": (
        "👥 <b>Referans Programı</b>\n\n"
        "Bağlantınız:\n<code>{link}</code>\n\n"
        "📊 Davet edilen: <b>{total}</b>\n"
        "✅ İşlem yapan: <b>{active}</b>\n\n"
        "🎁 Davet edilen kullanıcı <b>ilk işlemi komisyonsuz</b> alır.\n"
        "Bağlantınızı paylaşın ve platformu geliştirin!"
    ),
    "btn_referral": "👥 Referans programı",

    # ===== Репутация =====
    "reputation_level": "{emoji} Seviye: <b>{name}</b>",
    "reputation_discount_note": "📉 İtibar komisyon indirimi: <b>−{discount}%</b>",
    "reputation_bronze": "Bronz",
    "reputation_silver": "Gümüş",
    "reputation_gold": "Altın",

    # ===== Фото-отзывы =====
    "review_photo_prompt": "📸 Fotoğraf ekleyin (ürün, sonuç vb.) veya atlamak için /skip basın:",

    # ===== Избранное =====
    "btn_follow_seller": "⭐ Takip et",
    "btn_unfollow_seller": "💔 Takibi bırak",
    "btn_favorites": "⭐ Favoriler",
    "followed_seller": "⭐ <b>{name}</b> satıcısını takip ediyorsunuz. Yeni ilanlar hakkında bildirim alacaksınız.",
    "unfollowed_seller": "💔 <b>{name}</b> satıcısının takibini bıraktınız.",
    "favorites_empty": "⭐ Henüz takip ettiğiniz satıcı yok.\nKatalogdaki profili üzerinden takip edin.",
    "favorites_list_title": "⭐ <b>Takip ettikleriniz:</b>\n",
    "new_listing_notify_follower": (
        "🔔 Takip ettiğiniz satıcıdan yeni ilan!\n\n"
        "👤 {seller}\n"
        "📌 <b>{title}</b>\n"
        "💰 {price} USDT\n"
        "📍 {city}"
    ),
    "cant_follow_self": "❌ Kendinizi takip edemezsiniz",
    "profile_followers": "👥 Takipçiler",
    "profile_referrals": "👥 Referanslar",

    # ===== Отмена / прочее =====
    "create_listing_cancelled": "❌ İlan oluşturma iptal edildi.",
    "city_input_cancelled": "❌ Şehir girişi iptal edildi.",
    "support_rate_limit": "⏳ Sonraki başvurudan önce biraz bekleyin.",
    "resolve_confirm_seller": (
        "⚠️ <b>İtiraz kararını onaylayın #{id}</b>\n\n"
        "İşlem: satıcıya ödeme\n"
        "💰 Tutar: {payout} USDT → <code>{wallet}</code>\n\n"
        "Emin misiniz?"
    ),
    "resolve_confirm_buyer": (
        "⚠️ <b>İtiraz kararını onaylayın #{id}</b>\n\n"
        "İşlem: alıcıya iade\n"
        "💰 Tutar: {total} USDT\n\n"
        "Emin misiniz?"
    ),
    "followers_notified": "📣 Bildirilen takipçiler: {count}",
    "btn_change_lang": "🌐 Dil değiştir",
    "vip_days_left": "⏳ Kalan günler: <b>{days}</b>",
}
