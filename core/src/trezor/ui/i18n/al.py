class App:
    account = "الحساب"
    scan = "مسح الصفقات"
    nft = "صالة العرض NFT"
    guide = "تعليمات الاستخدام"
    security = "الأمان"
    setting = "الإعدادات"


#### Setting App
class Setting:
    bluetooth = "بلوتوث"
    language = "اللغة"
    vibration = "ردود الفعل عند اللمس"
    brightness = "سطوع الشاشة"
    auto_lock = "قفل تلقائي"
    auto_shutdown = "إيقاف تلقائي"
    animation = "رسوم انتقالية"
    wallpaper = "خلفية الشاشة"
    power_off = "إيقاف التشغيل"
    restart = "إعادة التشغيل"

#### Security App
class Security:
    change_pin = "تغيير الرقم السري"
    backup_mnemonic = "نسخ احتياطي للكلمات المفردة"
    check_mnemonic = "فحص الكلمات المفردة"
    wipe_device = "مسح الجهاز"

#### guide App
class Guide:
    about = "حول Digit Shield"
    terms_of_use = 'شروط الاستخدام'
    device_info = 'معلومات الجهاز'
    firmware_update = 'تحديث البرنامج الثابت'
    terms_title_terms_us = 'شروط استخدام Digit Shield'
    terms_describe_terms_us = 'للوصول إلى النسخة الكاملة لشروط الاستخدام، يرجى زيارة الرابط التالي:\n http://digitshield.com/terms'

    terms_title_product_services = 'منتجات وخدمات Digit Shield'
    terms_describe_product_services = 'تدير محافظنا المادية العملات المشفرة بأمان'
    terms_title_risks = ' المخاطر'
    terms_describe_risks = 'يرجى الانتباه إلى المخاطر المتعلقة بالعملات المشفرة والثغرات التقنية.'
    terms_title_disclaimers = 'إخلاء المسؤولية'
    terms_describe_disclaimers = 'المعلومات المقدمة ليست نصيحة مالية. يرجى طلب المشورة المهنية قبل اتخاذ أي قرار.'
    terms_title_contact_us = 'اتصل بنا'
    terms_describe_contact_us = 'إذا كان لديك أي أسئلة أو مخاوف، فأرسل لنا بريدًا إلكترونيًا على www.ds.pro@gmail.com'
    
    accept_tems = 'قبول الشروط'
    use_range = '1. نطاق التطبيق'
    range_include = 'تطبق هذه البنود على جميع الخدمات التي تقدمها محفظة Digital Shield، بما في ذلك:'
    range_include_1 = 'شراء وإلغاء تنشيط خدمات ما بعد البيع للجهاز المادي؛ تنزيل وتثبيت تطبيقات Digital Shield للهواتف المحمولة (Android/iOS/Goolg)和使用 الميزات؛ خدمات ترقية البرامج الثابتة (بما في ذلك التصحيحات الأمنية والإصدارات التي تزيد من الميزات)；إدارة الأصول الرقمية المتعددة السلاسل (دعم تخزين وتحويل أكثر من 3000 رمز، مثل BTC و ETH، وما إلى ذلك)؛ الدعم الفني (فحص أعطال الأجهزة، معالجة حالات عدم تطابق توقيعات المعاملات، وما إلى ذلك).'
    user_qualification = '2. مؤهلات المستخدم'
    ability_include = 'أنت تؤكد أنك تبلغ من العمر 18 عامًا على الأقل ولديك القدرة على القيام بجميع الأعمال القانونية؛'
    ability_include_1 = 'المنطقة القضائية التي تقيم فيها لا تمنع استخدام العملات المشفرة والأجهزة المادية ذات الصلة (على سبيل المثال، يجب على المستخدمين في الصين القارية تحمل المخاطر المرتبطة باستخدامها بأنفسهم)؛'
    terms_update_infor = '3. تحديث الشروط والإشعار'
    update_infor_content = 'نحتفظ بالحق في تعديل الشروط jednostronnie، سيتم نشر محتوى المراجعة في لوحة الإعلانات على الموقع الرسمي، وتاريخ السريان سيكون وفقًا للإعلان. إذا واصلت استخدام الخدمات، يعتبر ذلك موافقة على الشروط المراجعة؛ إذا كنت لا توافق، يجب عليك إخطارنا كتابيًا وقف استخدامها قبل تاريخ السريان.'

    wallet_buy_iterms = '2. شروط شراء المحفظة المادية'
    order_process = '1. عملية الطلب'
    payment_confirmation = 'تأكيد الدفع: بعد نجاح دفع الطلب (يتم تأكيده بواسطة شبكة البلوكشين أو وصول البنك)، سيقوم النظام بتحديث الحالة في غضون 24 ساعة؛'
    inventory_shortage = 'نقص المخزون: إذا كان المخزون غير كافٍ، يمكن للمستخدمين الاختيار:'
    inventory_shortage_1 = 'a. الانتظار لاستلام البضائع (ما يصل إلى 30 يومًا، سيتم رد الأموال تلقائيًا في حالة تجاوز المدة)؛'
    inventory_shortage_2 = 'b. رد الأموال بالكامل على الطريقة الأصلية (سيتم حساب طلبات العملات المشفرة وفقًا لسعر الصرف في وقت الدفع).'
    return_and_exchange_policy = '2. سياسة الاسترجاع والتبادل'
    return_and_exchange_condi = 'شروط الاسترجاع:'
    return_and_exchange_condi_con = 'a. يجب على الأجهزة غير المفعلة الاحتفاظ بالملصق المختوم من المصنع (رقم الطلب متوافق) والملحقات الكاملة (كابل USB، الكتيب، بطاقة الكلمات المميزة)؛ b. يجب تقديم طلب الاسترجاع في غضون 7 أيام من الاستلام، في حالة التأخير سيتم اعتبارها كقبول الجودة؛ c. يتحمل المستخدم تكاليف الشحن المرتجعة (باستثناء المشكلات الجودة).'
    warranty_scope = 'نطاق الضمان:'
    warranty_scope_1 = 'a. يغطي الأعطال غير الناجمة عن الإنسان، مثل أعطال الرقاقة الأمنية، والشاشة العرضية غير الطبيعية، وفقدان وظيفة الأزرار؛'
    warranty_scope_2 = 'b. يجب تقديم دليل الشراء (رقم الطلب) ودليل العطل (يجب أن يظهر الفيديو رقم SN للجهاز والظواهر غير الطبيعية بوضوح)؛'
    warranty_scope_3 = 'c. الأضرار الناجمة عن الإنسان (مثل السقوط في الماء، والسقوط) ليست ضمن نطاق الضمان، يمكن إجراء الصيانة المدفوعة.'

    disclaimer = '3. الإخلاء من المسؤولية'
    product_risk = '1. مخاطر المنتج'
    physical_risk = 'المخاطر المادية:'
    physical_risk_1 = 'a. قد يتعطل الجهاز في البيئات ذات الحرارة العالية (>60℃)、الرطوبة العالية (>90% RH)、والحقول المغناطيسية القوية (>100mT)؛'
    physical_risk_2 = 'b. قد يؤدي عدم الشحن لفترة طويلة إلى تلف البطارية (يوصى بشحن البطارية مرة واحدة كل شهر).'
    supply_chain_risk = 'مخاطر سلسلة التوريد:'
    supply_chain_risk_1 = 'a. يوفر الموقع الرسمي أدوات التحقق من الأصالة، يمكن فحص الأجهزة عن طريق مسح رمز QR للجهاز؛'
    supply_chain_risk_2 = 'b. إذا اشتبهت في أن الجهاز تم التلاعب به، يجب عليك الاتصال بخدمة العملاء على الفور和解عنها.'
    service_interruption = '2. انقطاع الخدمة'
    service_interruption_1 = 'سيتم إخطار الصيانة المخططة قبل 48 ساعة عن طريق لوحة الإعلانات على الموقع الرسمي، قد يتم تعليق الخدمة بدون إشعار مسبق في حالة الصيانة الطارئة؛'
    service_interruption_2 = 'نحن لا نتحمل المسؤولية عن فقدان البيانات الناجم عن العوامل القاهرة.'
    
    device_label = "اسم الجهاز"
    device_title_firmware_version = 'إصدار البرنامج الثابت'
    device_title_serial_number = 'الرقم التسلسلي'
    bluetooth_name = "اسم البلوتوث"
    bluetooth_version = "إصدار البلوتوث"
    firmware_title_1 = '1. تأكد أن بطارية الجهاز أعلى من 20%'
    firmware_title_2 = '2. قم بتوصيل الجهاز بالكمبيوتر باستخدام كابل USB-C'
    firmware_title_3 = '3. انقر فوق "تحديث البرنامج الثابت"'
    firmware_title_caution = 'تحذير'
    firmware_describe_caution = 'خلال التحديث، يرجى التأكد من توصيل USB'

class Nft:
    nft_item ="عنصر {}"
    nft_items ="{} عناصر"
class Title:
    enter_old_pin = "الرجاء إدخال الرقم السري القديم"
    enter_new_pin = "الرجاء إدخال الرقم السري الجديد"
    enter_pin = "الرجاء إدخال الرقم السري"
    enter_pin_again = "أدخل الرقم السري مرة أخرى"
    select_language = "اختيار اللغة"
    create_wallet = "إنشاء محفظة"
    wallet = "محفظة"
    import_wallet = "استيراد محفظة"
    restore_wallet = "استعادة محفظة"
    wallet_is_ready = "المحفظة جاهزة"
    select_word_count = "اختيار عدد الكلمات"
    wallet_security = "أمان المحفظة"
    pin_security = "تلميح الأمان للرقم السري"
    mnemonic_security = "تلميح الأمان للكلمات المفردة"
    backup_mnemonic = "نسخ احتياطي للكلمات المفردة"
    enter_mnemonic = "الرجاء إدخال الكلمات المفردة"
    check_mnemonic = "فحص الكلمات المفردة"
    success = "نجاح"
    operate_success = "نجاح العملية"
    theme_success = "نجاح تبديل السمة"
    warning = "تحذير"
    error = "خطأ"
    verified = "اكتمل نسخ احتياطي للكلمات المفردة"
    invalid_mnemonic = "الكلمات المفردة غير صالحة"
    pin_not_match = "الرقم السري غير متطابق"
    check_recovery_mnemonic = "فحص الكلمات المفردة للاستعادة"
    mnemonic_not_match = "الكلمات المفردة غير متطابقة"
    power_off = "إيقاف التشغيل"
    restart = "إعادة التشغيل"
    change_language = "تغيير اللغة"
    wipe_device = "مسح الجهاز"
    bluetooth_pairing = "توصيل البلوتوث"
    address="{} العنوان"
    public_key = "{} المفتاح العام"
    xpub = "{} XPub"
    transaction = "{} الصفقة"
    transaction_detail = "تفاصيل الصفقة"
    confirm_transaction = "تأكيد الصفقة"
    confirm_message = "تأكيد الرسالة"
    signature = "نتيجة التوقيع"
    wrong_pin = "الرقم السري خاطئ"
    pin_changed = "تم تغيير الرقم السري"
    pin_enabled = "تم تمكين الرقم السري"
    pin_disabled = "تم تعطيل الرقم السري"
    unknown_token = "رمز غير معروف"
    view_data = "عرض البيانات"
    sign_message = "{} توقيع الرسالة"
    verify_message = "{} التحقق من الرسالة"
    typed_data = "{} البيانات المنظمة"
    typed_hash = "{} التجزئة المنظمة"
    system_update = "تحديث النظام"
    entering_boardloader = "الدخول إلى Boardloader"
    remove_credential = "حذف البطاقة"
    list_credentials = "سرد البطاقات"
    authorize_coinjoin = "تفويض CoinJoin"
    multisig_address_m_of_n = "{} عنوان التوقيع المتعدد\n({} من {})"
    u2f_register = "تسجيل U2F"
    u2f_unregister = "إلغاء تسجيل U2F"
    u2f_authenticate = "مصادقة U2F"
    fido2_register = "تسجيل FIDO2"
    fido2_unregister = "إلغاء تسجيل FIDO2"
    fido2_authenticate = "مصادقة FIDO2"
    fee_is_high = "رسوم عالية"
    confirm_locktime = "تأكيد وقت القفل"
    view_transaction = "عرض الصفقة"
    x_confirm_payment = "{} تأكيد الدفع"
    confirm_replacement = "تأكيد استبدال الصفقة"
    x_transaction = "{} الصفقة"
    x_joint_transaction = "{} الصفقة المشتركة"
    change_label = "تغيير اسم الجهاز"
    enable_passphrase = "تفعيل عبارة المرور"
    disable_passphrase = "تعطيل عبارة المرور"
    passphrase_source = "إعداد إدخال عبارة المرور"
    enable_safety_checks ="تفعيل الفحوصات الأمنية"
    disable_safety_checks ="تعطيل الفحوصات الأمنية"
    experiment_mode = "الوضع التجريبي"
    set_as_homescreen = "تعيين كشاشة رئيسية"
    get_next_u2f_counter = "الحصول على العداد التالي لـ U2F"
    set_u2f_counter = "تعيين عداد U2F"
    encrypt_value = "تشفير البيانات"
    decrypt_value = "فك تشفير البيانات"
    confirm_entropy = "تصدير الكمية العشوائية"
    memo = "ملاحظة"
    import_credential = "استيراد البطاقة"
    export_credential = "تصدير البطاقة"
    asset = "الأصول"
    unimplemented = "لم يتم التنفيذ"
    invalid_data="تنسيق البيانات غير صالح"
    low_power = "الطاقة منخفضة"

class Text:
    # tap_to_unlock = "Tap to unlock"
    tap_to_unlock = "انقر للفتح"
    unlocking = "جاري فتح الجهاز..."
    # str_words = "#18794E {}# words"
    str_words = "#FFFFFF {}# كلمات"
    backup_manual = "اكتب الكلمات المميزة يدويًا واحتفظ بها في مكان آمن"
    check_manual = "انقر على الكلمات أدناه بالترتيب"
    backup_verified = "لقد أكملت نسخ احتياطي للكلمات المفردة، احفظها جيدًا ولا تشاركها مع أي شخص"
    backup_invalid = "الكلمات المفردة التي أدخلتها غير صحيحة، يرجى فحص نسخة النسخ الاحتياطي للكلمات المفردة ثم المحاولة مرة أخرى"
    pin_not_match = "الرقم السري الذي أدخلته غير صحيح، يرجى المحاولة مرة أخرى"
    please_wait = "يرجى الانتظار"
    wiping_device = "جاري مسح بيانات الجهاز..."
    create_wallet = "إنشاء مجموعة جديدة من الكلمات المفردة لإنشاء محفظة جديدة"
    restore_wallet = "استعادة المحفظة من الكلمات المفردة التي قمت بنسخها احتياطيًا"
    restore_mnemonic_match = "تطابق الكلمات المفردة التي أدخلتها، نسخة النسخ الاحتياطي للكلمات المفردة صحيحة"
    restore_success = "استعادة المحفظة بنجاح"
    create_success = "لقد تم نسخ احتياطي للكلمات المفردة بنجاح، تم إنشاء المحفظة"
    check_recovery_mnemonic = "يرجى فحص الكلمات المفردة، تأكيد أنها تطابق تمامًا"
    invalid_recovery_mnemonic = "الكلمات المفردة التي أدخلتها غير صالحة، يرجى فحص الكلمات المفردة ثم المحاولة مرة أخرى"
    check_recovery_not_match = "الكلمات المفردة التي أدخلتها صالحة، لكنها لا تطابق الكلمات المفردة الموجودة في الجهاز"
    shutting_down = "جاري إيقاف التشغيل..."
    restarting = "جاري إعادة التشغيل..."
    never = "أبدًا"
    second = "ثانية"
    seconds = "ثواني"
    minute = "دقيقة"
    minutes = "دقائق"
    changing_language = "أنت بصدد تغيير اللغة\nسيؤدي تطبيق هذه الإعدادات إلى إعادة تشغيل الجهاز"
    change_pin = "حدد رقم سري يتراوح بين 4 إلى 16 رقمًا لحماية جهازك"
    wipe_device = "اعادة تعيين الجهاز إلى إعدادات المصنع.\nتحذير: سيؤدي هذا إلى مسح جميع البيانات من جهازك."
    wipe_device_check = [
        "مسح الجهاز سيحذف جميع البيانات",
        "لن تتمكن من استعادة البيانات",
        "لقد قمت بنسخ احتياطي للكلمات المفردة",
    ]
    wipe_device_success = "تم مسح بيانات الجهاز بنجاح\n جاري إعادة تشغيل الجهاز ..."
    bluetooth_pair = "يرجى إدخال رمز التوصيل على جهازك"
    bluetooth_pair_failed = "فشل توصيل البلوتوث"
    path = "مسار التوريث:"
    chain_id = "Chain ID:"
    send = "إرسال"
    to = "إلى"
    amount = "المبلغ"
    from_ = "المرسل"
    receiver = "المستقبل"
    fee = "الرسوم"
    max_fee = "الرسوم القصوى"
    max_priority_fee_per_gas = "الرسوم القصوى للغاز"
    max_fee_per_gas = "الحد الأقصى لرسوم الغاز لكل وحدة غاز"
    max_gas_limit = "الحد الأقصى لكمية الغاز"
    gas_unit_price= "سعر وحدة الغاز"
    gas_price = "سعر الوقود"
    total = "المجموع"
    do_sign_this_transaction = "هل تريد توقيع هذه الصفقة {}"
    transaction_signed = "تم توقيع الصفقة"
    address = 'العنوان:'
    public_key = "المفتاح العام:"
    xpub = "XPub:"
    unknown_tx_type = "نوع الصفقة غير معروف، يرجى فحص بيانات الإدخال"
    unknown_function = "الوظيفة غير معروفة"
    use_app_scan_this_signature = "يرجى استخدام تطبيق المحفظة لمسح نتيجة التوقيع"
    internal_error = "خطأ داخلي"
    tap_switch_to_airgap = "انقر على رمز QR للتبديل إلى عرض عنوان Airgap"
    tap_switch_to_receive = "انقر على رمز QR للتبديل إلى عرض عنوان الاستلام"
    incorrect_pin_times_left = "الرقم السري غير صحيح، تبقى {} محاولات"
    incorrect_pin_last_time = "الرقم السري غير صحيح، هذه هي المحاولة الأخيرة"
    wrong_pin = "الرقم السري الذي أدخلته غير صحيح"
    seedless = "نقص البذور"
    backup_failed = "فشل النسخ الاحتياطي!"
    need_backup = "يحتاج إلى النسخ الاحتياطي!"
    pin_not_set = "لم يتم تعيين الرقم السري!"
    experimental_mode = "الوضع التجريبي"
    pin_change_success = "تم تغيير الرقم السري بنجاح"
    pin_enable_success = "تم تمكين الرقم السري بنجاح"
    pin_disable_success = "تم تعطيل الرقم السري بنجاح"
    contract = "العقد:"
    new_contract = "عقد جديد?"
    bytes_ = "{} بايت"
    message = "الرسالة:"
    no_message = "لا تحتوي على رسالة"
    contains_x_key = "تحتوي على {} مفتاح"
    array_of_x_type = "نوع المصفوفة {} {}"
    do_sign_712_typed_data = "هل تريد توقيع هذه الصفقة بالبيانات المنظمة؟"
    do_sign_typed_hash = "هل تريد توقيع هذه الصفقة بالتجزئة المنظمة؟"
    domain_hash = "تجزئة المجال:"
    message_hash = "تجزئة الرسالة:"
    switch_to_update_mode = "التبديل إلى وضع التحديث"
    switch_to_boardloader = "التبديل إلى وضع Boardloader"
    list_credentials = "هل تريد تصدير معلومات البطاقات المخزنة على هذا الجهاز؟"
    coinjoin_at_x = "هل تريد المشاركة في الصفقة Coinjoin التالية:\n{}"
    signature_is_valid = "التوقيع صالح"
    signature_is_invalid = "التوقيع غير صالح"
    u2f_already_registered = "U2F مسجل بالفعل"
    u2f_not_registered = "U2F غير مسجل"
    fido2_already_registered_x = "FIDO2 مسجل {}"
    fido2_verify_user = "تحقق من المستخدم FIDO2"
    device_already_registered_x = "الجهاز مسجل {}"
    device_verify_user = "تحقق من المستخدم الجهاز"
    finalize_transaction = "إكمال الصفقة"
    meld_transaction = "دمج الصفقة"
    update_transaction = "تحديث الصفقة"
    fee_is_unexpectedly_high = "الرسوم مرتفعة للغاية"
    change_count = "عدد الفكة"
    locktime_will_have_no_effect = "لن يكون لوقت القفل أي تأثير"
    confirm_locktime_for_this_transaction = "تأكيد وقت القفل لهذه الصفقة"
    block_height = "ارتفاع الكتلة"
    time = "الوقت"
    amount_increased = "زيادة المبلغ"
    amount_decreased = "تقليل المبلغ"
    fee_unchanged = "لم تتغير الرسوم"
    fee_increased = "زيادة الرسوم"
    fee_decreased = "تقليل الرسوم"
    your_spend = "نفقاتك"
    change_label_to_x = "تغيير التسمية إلى {}"
    enable_passphrase = "هل تريد تفعيل تشفير عبارة المرور؟"
    disable_passphrase = "هل تريد تعطيل تشفير عبارة المرور؟"
    enable_passphrase_always = "هل تريد دائمًا إدخال عبارة المرور على هذا الجهاز؟"
    revoke_enable_passphrase_always = "هل تريد سحب تفعيل إدخال عبارة المرور دائمًا؟"
    auto_lock_x = "هل أنت متأكد من رغبتك في قفل الجهاز تلقائيًا بعد {}؟"
    enable_safety_checks = "هل تريد تنفيذ فحوصات أمنية صارمة؟ سيوفر ذلك حماية أكثر شمولاً."
    disable_safety_checks = "هل أنت متأكد من رغبتك في تعطيل الفحوصات الأمنية؟ قبل المتابعة، يرجى العلم بالمخاطر الأمنية المحتملة لهذا الإجراء."
    enable_experiment_mode = "هل تريد تفعيل الوضع التجريبي؟"
    set_as_homescreen = "هل أنت متأكد من رغبتك في تغيير الشاشة الرئيسية؟"
    replace_homescreen = "هل أنت متأكد من رغبتك في استبدال الشاشة الرئيسية؟ سيؤدي ذلك إلى حذف أول ورقة حائط تم رفعها."
    confirm_replace_wallpaper = "هل أنت متأكد من رغبتك في استبدال ورق الحائط للشاشة الرئيسية؟"
    get_next_u2f_counter = "هل تريد الحصول على العداد التالي لـ U2F؟"
    set_u2f_counter_x = "هل أنت متأكد من رغبتك في تعيين عداد U2F على {}؟"
    confirm_entropy = "هل أنت متأكد من رغبتك في تصدير الكمية العشوائية؟ قبل المتابعة، يرجى العلم بما تفعله!"
    bandwidth = "عرض النطاق"
    energy = "الطاقة"
    sender = "المرسل"
    recipient = "المستقبل"
    resource = "المورد"
    frozen_balance = "الرصيد المجمد"
    unfrozen_balance = "الرصيد غير المجمد"
    delegated_balance = "الرصيد المفوض"
    undelegated_balance = "الرصيد غير المفوض"
    you_are_freezing = "أنت بصدد تجميد الأصول"
    you_are_unfreezing = "أنت بصدد إلغاء تجميد الأصول"
    you_are_delegating = "أنت بصدد تفويض الأصول"
    you_are_undelegating = "أنت بصدد إلغاء تفويض الأصول"
    duration = "المدة"
    lock = "قفل"
    unlock = "فك القفل"
    all = "الكل"
    source = "المصدر"
    tip = "تلميح"
    keep_alive = "Keep alive"
    invalid_ur = "نوع رمز QR غير مدعوم، يرجى المحاولة مرة أخرى"
    sequence_number = "رقم التسلسل"
    expiration_time = "وقت الانتهاء"
    argument_x = "المعامل #{}"
    low_power_message = "البطارية المتبقية {}%.\nيرجى الشحن"

class Tip:
    swipe_down_to_close = "اسحب لأسفل للإغلاق"
class Button:
    done = "تم"
    ok = "حسنًا"
    confirm = "تأكيد"
    reject = "رفض"
    next = "التالي"
    cancel = "إلغاء"
    redo = "إعادة إنشاء"
    continue_ = "متابعة"
    try_again = "إعادة المحاولة"
    power_off = "إيقاف التشغيل"
    restart = "إعادة التشغيل"
    hold = "اضغط"
    address = "العنوان"
    qr_code = "رمز QR"
    view_detail = "عرض التفاصيل"
    hold_to_sign = "اضغط للتوقيع"
    hold_to_wipe = "اضغط لمسح"
    receive = "عنوان الاستلام"
    airgap = "Airgap"
    sign = "توقيع"
    verify = "تحقق"
    view_full_array = "عرض المصفوفة الكاملة"
    view_full_struct = "عرض الهيكل الكامل"
    view_full_message = "عرض الرسالة الكاملة"
    view_data = "عرض البيانات"
    view_more = "عرض المزيد"
class WalletSecurity:
    header = "الكلمات المفردة هي مجموعة من الكلمات تستخدم لاستعادة أصول المحفظة، امتلاك الكلمات المفردة يعني أنه يمكنك استخدام أصولك، احفظها جيدًا"

    tips = [
        "1. يرجى فحص سلامة البيئة، التأكد من عدم وجود مراقبين أو كاميرات",
        "2. يرجى نسخ الكلمات المفردة بالترتيب الصحيح، ولا تشارك الكلمات المفردة مع أي شخص",
        "3. يرجى حفظ الكلمات المفردة في مكان آمن دون اتصال بالإنترنت، لا تقم بنسخ الكلمات المفردة إلكترونيًا، ولا تقم بتحميلها على الإنترنت",
    ]

class MnemonicSecurity:
    header = "الكلمات المفردة هي مجموعة من الكلمات تستخدم لاستعادة أصول المحفظة، امتلاك الكلمات المفردة يعني أنه يمكنك استخدام أصولك، احفظها جيدًا"

    tips = [
        "1. يرجى فحص سلامة البيئة، التأكد من عدم وجود مراقبين أو كاميرات",
        "2. يرجى نسخ الكلمات المفردة بالترتيب الصحيح، ولا تشارك الكلمات المفردة مع أي شخص",
        "3. يرجى حفظ الكلمات المفردة في مكان آمن دون اتصال بالإنترنت، لا تقم بنسخ الكلمات المفردة إلكترونيًا، ولا تقم بتحميلها على الإنترنت",
    ]

class PinSecurity:
    header = "الرقم السري هو كلمة المرور للوصول إلى الجهاز، يستخدم للسماح بالوصول إلى الجهاز الحالي. يرجى استخدام تلميحات الأمان التالية لاستخدام الرقم السري بشكل صحيح"
    tips = [
        "1. عند تعيين أو إدخال الرقم السري، يرجى فحص سلامة البيئة، التأكد من عدم وجود مراقبين أو كاميرات",
        "2. يرجى تعيين رقم سري قوي يتراوح بين 4 إلى 16 رقمًا، تجنب استخدام الأرقام المتتالية أو المتكررة",
        "3. عدد المحاولات القصوى للرقم السري هو 10 مرات، عند الخطأ 10 مرات، سيتم إعادة تعيين الجهاز",
        "4. يرجى الاحتفاظ بالرقم السري جيدًا، ولا تشارك الرقم السري مع أي شخص",
    ]

class Solana:
    ata_reciver = "المستقبل (حساب العملة المشفرة المرتبط)"
    ata_sender = "المرسل (حساب العملة المشفرة المرتبط)"
    source_owner = "مؤشر الصفقة"
    fee_payer = "دافع الرسوم"

