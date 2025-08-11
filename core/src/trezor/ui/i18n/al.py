class App:
    account = "حساب"
    scan = "مسح المعاملات"
    nft = "معرض NFT"
    guide = "دليل الاستخدام"
    security = "أمان"
    setting = "إعدادات"


#### Setting App
class Setting:
    bluetooth = "بلوتوث"
    language = "اللغة"
    vibration = "ردود الفعل اللمسية"
    brightness = "سطوع الشاشة"
    auto_lock = "القفل التلقائي"
    auto_shutdown = "الإغلاق التلقائي"
    animation = "الرسوم المتحركة الانتقالية"
    wallpaper = "خلفية الشاشة"
    power_off = "إيقاف التشغيل"
    restart = "إعادة التشغيل"
    restart_tip = "نصيحة إعادة التشغيل"

#### Security App
class Security:
    change_pin = "تغيير رمز PIN"
    backup_mnemonic = "نسخ عبارة الاستعادة احتياطياً"
    check_mnemonic = "التحقق من عبارة الاستعادة"
    wipe_device = "مسح الجهاز"

#### guide App
class Guide:
    about = "عن Digital Shield"
    terms_of_use = 'شروط الاستخدام'
    device_info = 'معلومات الجهاز'
    firmware_update = 'ترقية البرنامج الثابت'
    terms_title_terms_us = 'شروط استخدام Digit Shield'
    terms_describe_terms_us = 'للوصول إلى النسخة الكاملة من شروط الاستخدام، يرجى زيارة الرابط التالي:\nhttp://digitshield.com/terms'

    terms_title_product_services = 'منتجات وخدمات Digit Shield'
    terms_describe_product_services = 'تساعد محفظتنا الأمنية في إدارة العملات المشفرة بأمان'
    terms_title_risks = 'المخاطر'
    terms_describe_risks = 'يرجى ملاحظة المخاطر المرتبطة بالعملات المشفرة والثغرات التقنية.'
    terms_title_disclaimers = 'إخلاء المسؤولية'
    terms_describe_disclaimers = 'المعلومات المقدمة ليست نصيحة مالية. يرجى استشارة خبير قبل اتخاذ أي قرارات.'
    terms_title_contact_us = 'اتصل بنا'
    terms_describe_contact_us = 'إذا كان لديك أي استفسارات أو مخاوف، يرجى إرسال بريد إلكتروني إلينا على www.ds.pro@gmail.com'
    
    accept_tems = 'قبول الشروط'
    use_range = '1. نطاق التطبيق'
    range_include = 'تطبق هذه البنود على جميع الخدمات التي تقدمها محفظة Digital Shield، بما في ذلك:'
    range_include_1 = 'شراء وإلغاء تنشيط خدمات ما بعد البيع للجهاز المادي؛ تنزيل وتثبيت تطبيقات Digital Shield للهواتف المحمولة (Android/iOS/Goolg) واستخدام الميزات؛ خدمات ترقية البرامج الثابتة (بما في ذلك التصحيحات الأمنية والإصدارات التي تزيد من الميزات)；إدارة الأصول الرقمية المتعددة السلاسل (دعم تخزين وتحويل أكثر من 3000 رمز، مثل BTC و ETH، وما إلى ذلك)؛ الدعم الفني (فحص أعطال الأجهزة، معالجة حالات عدم تطابق توقيعات المعاملات، وما إلى ذلك).'
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
    attention_events = "تنبيهات"
    firmware_title_1 = '1. يرجى التأكد من أن شحن الجهاز أكثر من 20%'
    firmware_title_2 = '2. استخدم كابل USB-C لتوصيل الجهاز بالكمبيوتر'
    firmware_title_3 = '3. اضغط على "تحديث البرنامج الثابت"'
    firmware_title_caution = 'تحذير'
    firmware_describe_caution = 'أثناء التحديث، يرجى التأكد من اتصال USB'
    equipment_info = 'معلومات الجهاز'
    equipment_name = 'اسم الجهاز'
    equipment_version = 'إصدار الجهاز'

class Nft:
    nft_item ="{} عنصر"
    nft_items ="{} عناصر"
class Title:
    enter_old_pin = "الرجاء إدخال رمز PIN القديم"
    enter_new_pin = "الرجاء إدخال رمز PIN الجديد"
    enter_pin = "الرجاء إدخال رمز PIN"
    enter_pin_again = "الرجاء إدخال رمز PIN مرة أخرى"
    select_language = "اللغة"
    create_wallet = "إنشاء محفظة"
    wallet = "المحفظة"
    import_wallet = "استيراد المحفظة"
    restore_wallet = "استعادة المحفظة"
    select_word_count = "اختر عدد الكلمات"
    wallet_security = "أمان المحفظة"
    pin_security = "نصائح أمان رمز PIN"
    mnemonic_security = "نصائح أمان عبارة الاستعادة"
    backup_mnemonic = "نسخ عبارة الاستعادة احتياطياً"
    enter_mnemonic = "الرجاء إدخال عبارة الاستعادة"
    check_mnemonic = "التحقق من عبارة الاستعادة"
    success = "نجاح"
    operate_success = "تمت العملية بنجاح"
    theme_success = "تم تغيير السمة بنجاح"
    warning = "تحذير"
    error = "خطأ"
    invalid_mnemonic = "عبارة استعادة غير صالحة"
    pin_not_match = "رمز PIN غير متطابق"
    check_recovery_mnemonic = "التحقق من عبارة الاستعادة"
    power_off = "إيقاف التشغيل"
    restart = "إعادة التشغيل"
    change_language = "تغيير اللغة"
    wipe_device = "مسح الجهاز"
    bluetooth_pairing = "إقران البلوتوث"
    address="{} عنوان"
    public_key = "المفتاح العام {}"
    xpub = "XPub {}"
    transaction = "معاملة {}"
    transaction_detail = "تفاصيل المعاملة"
    confirm_transaction = "تأكيد المعاملة"
    confirm_message = "تأكيد الرسالة"
    signature = "نتيجة التوقيع"
    wrong_pin = "رمز PIN خاطئ"
    pin_changed = "تم تغيير رمز PIN"
    pin_enabled = "تم تفعيل رمز PIN"
    pin_disabled = "تم تعطيل رمز PIN"
    unknown_token = "رمز غير معروف"
    view_data = "عرض البيانات"
    sign_message = "توقيع رسالة {}"
    verify_message = "التحقق من توقيع رسالة {}"
    typed_data = "بيانات منظمة {}"
    typed_hash = "تجزئة منظمة {}"
    system_update = "تحديث النظام"
    entering_boardloader = "الدخول إلى لوحة التحميل"
    remove_credential = "إزالة بيانات الاعتماد"
    list_credentials = "عرض بيانات الاعتماد"
    authorize_coinjoin = "تفويض CoinJoin"
    multisig_address_m_of_n = "عنوان متعدد التوقيعات {}\n({} من {})"
    u2f_register = "تسجيل U2F"
    u2f_unregister = "إلغاء تسجيل U2F"
    u2f_authenticate = "مصادقة U2F"
    fido2_register = "تسجيل FIDO2"
    fido2_unregister = "إلغاء تسجيل FIDO2"
    fido2_authenticate = "مصادقة FIDO2"
    finalize_transaction = "إتمام المعاملة"
    meld_transaction = "دمج المعاملة"
    update_transaction = "تحديث المعاملة"
    high_fee = "رسوم المعاملة مرتفعة"
    fee_is_high = "رسوم المعاملة مرتفعة"
    confirm_locktime = "تأكيد وقت القفل"
    view_transaction = "عرض المعاملة"
    x_confirm_payment = "{} تأكيد الدفع"
    confirm_replacement = "تأكيد استبدال المعاملة"
    x_transaction = "{} معاملة"
    x_joint_transaction = "{} معاملة مشتركة"
    change_label = "تغيير اسم الجهاز"
    enable_passphrase = "تفعيل عبارة المرور"
    disable_passphrase = "تعطيل عبارة المرور"
    passphrase_source = "إعدادات إدخال عبارة المرور"
    enable_safety_checks ="تفعيل الفحوصات الأمنية"
    disable_safety_checks ="تعطيل الفحوصات الأمنية"
    experimental_mode = "وضع التجارب"
    set_as_homescreen = "تعيين كشاشة رئيسية"
    get_next_u2f_counter = "الحصول على عداد U2F التالي"
    set_u2f_counter = "ضبط عداد U2F"
    encrypt_value = "تشفير البيانات"
    decrypt_value = "فك تشفير البيانات"
    confirm_entropy = "تصدير الإنتروبيا"
    memo = "ملاحظة"
    import_credential = "استيراد بيانات الاعتماد"
    export_credential = "تصدير بيانات الاعتماد"
    asset = "الأصول"
    unimplemented = "غير مطبق"
    invalid_data="تنسيق بيانات غير صالح"
    low_power = "بطارية منخفضة"
    collect_nft = "جمع NFT"
    verify_device = "تحقق من الجهاز"
    update_bootloader = "تحديث برنامج التحميل الأولي"
    update_resource = "تحديث الموارد"

    words_num = "كلمة #{}"
    download_digital = "تحميل"
    connect_wallets = "ربط المحافظ"
    start_setup = "بدء الإعداد"
    prepare_create = "تحضير الإنشاء"
    prepare_import = "تحضير الاستيراد"
    prepare_check = "التحضير للتحقق"
    input_words = "إدخال عبارة الاستعادة"
    has_sub = "تم الإرسال"
    reatart = "إعادة البدء"
    invalid_words = "عبارة الاستعادة غير صالحة"
    stop_checking = "إيقاف التحقق"
    correct_words = "عبارة الاستعادة صحيحة"
    mnemonic_not_match = "عبارة الاستعادة غير متطابقة"
    wallet_created = "تم إنشاء المحفظة"
    check_words = "التحقق من عبارة الاستعادة"
    verified = "تم التحقق"
    wallet_is_ready = "المحفظة جاهزة"

    prepare_backup = "التحضير للنسخ الاحتياطي"
    mnemonic_word = "عبارة الاستعادة"
    error_mnemonic_word = "كلمة غير صحيحة"
    right_word = "صحيح"
    wrong_word = "خطأ"

    pin_not_match = "غير متطابق"
    has_reset = "تم إعادة ضبط الجهاز"
    has_wipe = "تم مسح الجهاز"
    screen_bright = "سطوع الشاشة"
    download_app = "تحميل التطبيق"
    official_website = "الموقع الرسمي"
    scan_ercode = "امسح رمز الاستجابة السريعة المعروض في التطبيق"
    wipe_notice = "قبل مسح الجهاز، يرجى التأكد من معرفتك بذلك:"
    receive_tips = "يدعم فقط استقبال أصول {}"
    sign_fail = "فشل التوقيع"
    select_network = "اختر الشبكة"
    preview = "معاينة"
    go_link = "يرجى زيارة الرابط:"
    connect_again = "يرجى محاولة إعادة الاتصال."

class Text:
    start_setup = "ابدأ إعداد محفظة جديدة بعبارة استعادة، أو استورد نسخة احتياطية موجودة لاستعادة المحفظة."
    select_word_count = "يرجى اختيار عدد كلمات عبارة الاستعادة."
    input_words = "يرجى إدخال كلمات عبارة الاستعادة بالترتيب، والتأكد من تطابقها مع النسخة الاحتياطية لديك."
    invalid_words = "عبارة الاستعادة التي أدخلتها غير صالحة، اضغط على الكلمة لتعديلها أو ابدأ من جديد."
    stop_checking = "سيتم فقدان جميع التقدم بعد الإيقاف، هل أنت متأكد من الإيقاف؟"
    import_wallet = "أدخل عبارة الاستعادة الخاصة بك لاستعادة المحفظة."
    correct_words = "عبارة الاستعادة التي أدخلتها صحيحة ومتطابقة مع المخزنة في الجهاز."
    mnemonic_not_match = "عبارة الاستعادة التي أدخلتها صحيحة لكنها لا تتطابق مع المخزنة في الجهاز."
    wallet_created = "تم إنشاء المحفظة الجديدة بنجاح، يرجى عمل نسخة احتياطية فوراً."
    mnemonic_word_tips = "يرجى نسخ الكلمات التالية وعددها {} بالترتيب."
    select_words = "يرجى اختيار الكلمات الصحيحة"
    error_mnemonic_word = "الكلمة غير صحيحة، يرجى مراجعة عبارة الاستعادة والمحاولة مرة أخرى."
    has_reset = "تم إدخال رمز PIN بشكل خاطئ عدة مرات، تم مسح مساحة التخزين."
    restart_countdown = "سيتم إعادة التشغيل بعد {} ثانية"
    has_wipe = "تم مسح بيانات الجهاز بنجاح، يرجى إعادة تشغيل الجهاز."
    download_digital_tips = "يرجى تنزيل تطبيق Digital Shield من: \n{}"
    sign_fail = "لقد ألغيت التوقيع، تم إلغاء المعاملة."
    sign_success = "تم توقيع المعاملة"
    check_words_tips = "يرجى اتباع الإرشادات والتحقق من الكلمات واحدة تلو الأخرى وفقًا لنسخة الاسترداد الخاصة بك."
    backup_verified = "لقد أكملت التحقق من عبارة الاستعادة."
    create_success = "تم نسخ عبارة الاستعادة بنجاح وإنشاء المحفظة"
    tap_to_unlock = "اضغط لفتح القفل"
    unlocking = "جاري فتح قفل الجهاز..."

    str_words = "#FFFFFF {}# كلمات"
    backup_manual = "اكتب عبارة الاستعادة يدوياً واحفظها في مكان آمن"
    check_manual = "اضغط على الكلمات بالترتيب أدناه"
    backup_invalid = "عبارة الاستعادة التي أدخلتها غير صحيحة، يرجى مراجعة النسخة الاحتياطية والمحاولة مرة أخرى"
    pin_not_match = "رمز PIN غير متطابق، يرجى المحاولة مرة أخرى."
    please_wait = "يرجى الانتظار"
    wiping_device = "جاري مسح بيانات الجهاز..."
    create_wallet = "إنشاء مجموعة جديدة من عبارة الاستعادة لإنشاء محفظة جديدة"
    restore_wallet = "استعادة المحفظة من عبارة الاستعادة التي قمت بنسخها احتياطياً"
    restore_mnemonic_match = "عبارة الاستعادة الخاصة بك متطابقة، النسخة الاحتياطية صحيحة"
    restore_success = "تم استيراد عبارة الاستعادة الخاصة بك، وتم استعادة المحفظة بنجاح."
    check_recovery_mnemonic = "يرجى مراجعة عبارة الاستعادة والتأكد من تطابقها تماماً"
    invalid_recovery_mnemonic = "عبارة الاستعادة التي أدخلتها غير صالحة، يرجى مراجعتها والمحاولة مرة أخرى"
    check_recovery_not_match = "عبارة الاستعادة التي أدخلتها صالحة ولكنها لا تتطابق مع العبارة في الجهاز"
    shutting_down = "جارٍ إيقاف التشغيل..."
    restarting = "جارٍ إعادة التشغيل..."
    never = "أبداً"
    second = "ثانية"
    seconds = "ثواني"
    minute = "دقيقة"
    minutes = "دقائق"
    changing_language = "أنت تقوم بتغيير اللغة إلى {}، سيؤدي تطبيق هذا الإعداد إلى إعادة تشغيل الجهاز"
    change_pin = "قم بتعيين رمز PIN يتكون من 4 إلى 16 رقمًا."
    wipe_device = "استعادة الجهاز إلى إعدادات المصنع.\nتحذير: سيتم مسح جميع البيانات من جهازك."
    wipe_device_check = [
        "مسح الجهاز سيزيل جميع البيانات",
        "لا يمكن استعادة البيانات",
        "تم عمل نسخة احتياطية من عبارة الاستعادة",
    ]
    wipe_device_success = "تم مسح بيانات الجهاز بنجاح\nجارٍ إعادة التشغيل..."
    bluetooth_pair = "الرجاء إدخال رمز الاقتران على جهازك"
    bluetooth_pair_failed = "فشل اقتران البلوتوث"
    path = "مسار الاشتقاق:"
    chain_id = "معرف السلسلة:"
    send = "إرسال"
    to = "إلى"
    amount = "المبلغ"
    from_ = "من"
    receiver = "المستلم"
    fee = "الرسوم"
    max_fee = "الرسوم القصوى"
    max_priority_fee_per_gas = "الرسوم القصوى لكل غاز"
    max_fee_per_gas = "الحد الأقصى للرسوم لكل غاز"
    max_gas_limit = "حد أقصى لكمية الغاز"
    gas_unit_price = "سعر وحدة الغاز"
    max_gas_limit = "الحد الأقصى لكمية الغاز"
    gas_unit_price= "سعر وحدة الغاز"
    gas_price = "سعر الغاز"
    total = "المبلغ الإجمالي"
    do_sign_this_transaction = "هل تريد توقيع معاملة {} هذه؟"
    transaction_signed = "تم توقيع المعاملة"
    address = 'العنوان:'
    public_key = "المفتاح العام:"
    xpub = "XPub:"
    unknown_tx_type = "نوع معاملة غير معروف، يرجى التحقق من بيانات الإدخال"
    unknown_function = "الوظيفة غير معروفة"
    use_app_scan_this_signature = "الرجاء استخدام تطبيق المحفظة لمسح التوقيع"
    internal_error = "خطأ داخلي"
    tap_switch_to_airgap = "اضغط على رمز الاستجابة السريعة للتبديل إلى عنوان Airgap"
    tap_switch_to_receive = "اضغط على رمز الاستجابة السريعة للتبديل إلى عنوان استقبال المحفظة"
    incorrect_pin_times_left = "PIN غير صحيح، متبقي {} محاولات"
    incorrect_pin_last_time = "PIN غير صحيح، لديك محاولة أخيرة"
    wrong_pin = "رمز PIN المدخل غير صحيح"
    seedless = "لا يوجد بذرة"
    backup_failed = "فشل النسخ الاحتياطي!"
    need_backup = "يحتاج إلى نسخ احتياطي!"
    pin_not_set = "لم يتم تعيين PIN!"
    experimental_mode = "وضع التجارب"
    pin_change_success = "تم تغيير رمز PIN بنجاح"
    pin_enable_success = "تم تفعيل رمز PIN بنجاح"
    pin_disable_success = "تم تعطيل رمز PIN بنجاح"
    contract = "عقد:"
    new_contract = "عقد جديد?"
    bytes_ = "{} بايت"
    message = "رسالة:"
    no_message = "لا تحتوي على رسالة"
    contains_x_key = "يحتوي على {} مفتاح"
    array_of_x_type = "مصفوفة من نوع {} {}"
    do_sign_712_typed_data = "هل تريد توقيع معاملة البيانات المنظمة هذه؟"
    do_sign_typed_hash = "هل تريد توقيع معاملة الهاش المنظم هذه؟"
    domain_hash = "هاش النطاق:"
    message_hash = "هاش الرسالة:"
    switch_to_update_mode = "التبديل إلى وضع التحديث"
    switch_to_boardloader = "التبديل إلى وضع لوحة التحميل"
    list_credentials = "هل تريد تصدير معلومات الاعتمادات المخزنة على هذا الجهاز؟"
    coinjoin_at_x = "هل تريد المشاركة في معاملة Coinjoin التالية:\n{}"
    signature_is_valid = "التوقيع صالح"
    signature_is_invalid = "التوقيع غير صالح"
    u2f_already_registered = "U2F مسجل بالفعل"
    u2f_not_registered = "U2F غير مسجل"
    fido2_already_registered_x = "FIDO2 مسجل بالفعل {}"
    fido2_verify_user = "FIDO2 التحقق من المستخدم"
    device_already_registered_x = "الجهاز مسجل بالفعل {}"
    device_verify_user = "الجهاز يتحقق من المستخدم"
    fee_is_unexpectedly_high = "الرسوم مرتفعة بشكل غير متوقع"
    too_many_change_outputs = "هناك الكثير من مخرجات الصرف"
    change_count = "عدد التغييرات"
    locktime_will_have_no_effect = "وقت القفل لن يكون له تأثير"
    confirm_locktime_for_this_transaction = "تأكيد وقت القفل لهذه المعاملة"
    block_height = "ارتفاع الكتلة"
    time = "الوقت"
    amount_increased = "زيادة المبلغ"
    amount_decreased = "انخفاض المبلغ"
    fee_unchanged = "الرسوم لم تتغير"
    fee_increased = "زيادة الرسوم"
    fee_decreased = "انخفاض الرسوم"
    your_spend = "مصروفاتك"
    change_label_to_x = "تغيير التسمية إلى {}"
    enable_passphrase = "هل تريد تمكين تشفير عبارة المرور؟"
    disable_passphrase = "هل تريد تعطيل تشفير عبارة المرور؟"
    enable_passphrase_always = "إدخال عبارة المرور دائماً على الجهاز؟"
    revoke_enable_passphrase_always = "هل تريد إلغاء إعداد إدخال عبارة المرور دائماً؟"
    auto_lock_x = "تأكيد القفل التلقائي للجهاز بعد {}؟"
    enable_safety_checks = "هل تريد تنفيذ فحوصات أمان صارمة؟ سيؤدي هذا إلى توفير حماية أمان أكثر شمولاً."
    disable_safety_checks = "هل أنت متأكد من تعطيل فحوصات الأمان؟ يرجى العلم بالمخاطر الأمنية المحتملة قبل المتابعة."
    enable_experiment_mode = "هل تريد تمكين وضع التجارب؟"
    set_as_homescreen = "هل تريد تغيير الشاشة الرئيسية؟"
    replace_homescreen = "هل تريد استبدال الشاشة الرئيسية؟ سيؤدي هذا إلى حذف خلفية الشاشة الأولى التي تم تحميلها."
    confirm_replace_wallpaper = "هل أنت متأكد من رغبتك في استبدال ورق الحائط للشاشة الرئيسية؟"
    get_next_u2f_counter = "هل تريد الحصول على عداد U2F التالي؟"
    set_u2f_counter_x = "هل تريد ضبط عداد U2F على {}؟"
    confirm_entropy = "هل تريد تصدير الإنتروبيا؟ يرجى فهم ما تفعله قبل المتابعة!"
    bandwidth = "عرض النطاق الترددي"
    energy = "الطاقة"
    sender = "المرسل"
    recipient = "المستلم"
    resource = "المورد"
    frozen_balance = "الرصيد المجمد"
    unfrozen_balance = "الرصيد غير المجمد"
    delegated_balance = "الرصيد المفوض"
    undelegated_balance = "الرصيد غير المفوض"
    you_are_freezing = "أنت تقوم بتجميد الأصول"
    you_are_unfreezing = "أنت تقوم بإلغاء تجميد الأصول"
    you_are_delegating = "أنت تقوم بتفويض الأصول"
    you_are_undelegating = "أنت تقوم بإلغاء تفويض الأصول"
    duration = "المدة"
    lock = "قفل"
    unlock = "فتح القفل"
    all = "الكل"
    source = "المصدر"
    tip = "نصيحة"
    keep_alive = "إبقاء نشطاً"
    invalid_ur = "نوع رمز الاستجابة السريعة غير مدعوم، يرجى المحاولة مرة أخرى"
    sequence_number = "رقم التسلسل"
    expiration_time = "وقت الانتهاء"
    argument_x = "وسيطة #{}"
    low_power_message = "تبقى {}% من البطارية\nيرجى الشحن"
    collect_nft = "هل أنت متأكد من جمع هذه NFT؟"
    replace_nft = "هل تريد جمع هذه NFT؟ لقد وصلت إلى الحد الأقصى للمخزن، وسيتسبب هذا في إزالة أقدم NFT يتم تحميلها."
    verify_device = "هل أنت متأكد من مصادقة جهازك على خادم DigitShield؟ اضغط على تأكيد للتحقق مما إذا كان جهازك أصيل وغير مزعوم."
    update_bootloader = "هل تريد تحديث برنامج التحميل الأولي؟"
    update_resource = "هل تريد تحديث موارد الجهاز؟"

class Tip:
    swipe_down_to_close = "اسحب لأسفل للإغلاق"
class Button:
    done = "تم"
    ok = "موافق"
    confirm = "تأكيد"
    reject = "رفض"
    next = "التالي"
    cancel = "إلغاء"
    redo = "إعادة إنشاء"
    continue_ = "متابعة"
    try_again = "حاول مرة أخرى"
    power_off = "الضغط المطول للإيقاف"
    hold_to_power_off = "اضغط مع الاستمرار لإيقاف التشغيل"
    restart = "إعادة التشغيل"
    hold = "اضغط مع الاستمرار"
    address = "العنوان"
    qr_code = "رمز الاستجابة السريعة"
    view_detail = "عرض التفاصيل"
    hold_to_sign = "اضغط مع الاستمرار للتوقيع"
    hold_to_wipe = "اضغط مع الاستمرار للمسح"
    receive = "عنوان الاستلام"
    airgap = "Airgap"
    sign = "توقيع"
    verify = "تحقق"
    view_full_array = "عرض المصفوفة الكاملة"
    view_full_struct = "عرض الهيكل الكامل"
    view_full_message = "عرض الرسالة الكاملة"
    view_data = "عرض البيانات"
    view_more = "عرض المزيد"
    update = "تحديث"
class WalletSecurity:
    header = "اكتب عبارة الاستعادة الخاصة بك على ورقة واحفظها في مكان آمن"
    tips = [
        {
            "level": "info",
            "msgs": [
                "#00001F يجب تخزين عبارة الاستعادة بشكل آمن#",
                "#18794E * احفظها في خزنة بنكية#",
                "#18794E * احفظها في صندوق أمانات#", 
                "#18794E * احفظها في عدة أماكن سرية#",
            ]
        },
        {
            "level": "warning",
            "msgs": [
                "#00001F انتبه جيداً#",
                "#CD2B31 * تذكر مكان حفظ عبارة الاستعادة#",
                "#CD2B31 * لا تفقدها#",
                "#CD2B31 * لا تخبر أحداً بها#",
                "#CD2B31 * لا تخزنها على الإنترنت#",
                "#CD2B31 * لا تخزنها على الكمبيوتر#",
            ]
        },
    ]

class MnemonicSecurity:
    header = "عبارة الاستعادة هي مجموعة من الكلمات القصيرة تستخدم لاسترداد أصول المحفظة. امتلاك عبارة الاستعادة يعني القدرة على استخدام أصولك، يرجى الحفاظ عليها بعناية"

    tips = [
        "1. يرجى التحقق من أمان البيئة المحيطة والتأكد من عدم وجود مراقبين أو كاميرات",
        "2. يرجى نسخ عبارة الاستعادة بالترتيب الصحيح للكلمات، ولا تشاركها مع أي شخص",
        "3. يرجى حفظ عبارة الاستعادة في مكان آمن دون اتصال بالإنترنت، ولا تستخدم طرقًا إلكترونية لنسخها احتياطيًا، ولا تقم برفعها على الإنترنت",
    ]

class PinSecurity:
    header = "رمز PIN هو كلمة مرور للوصول إلى الجهاز، يُستخدم للسماح بالوصول إلى الجهاز الحالي. يرجى اتباع الإرشادات التالية لاستخدام رمز PIN بشكل صحيح"
    tips = [
        "1. عند تعيين أو إدخال رمز PIN، يرجى التحقق من أمان البيئة والتأكد من عدم وجود مراقبين أو كاميرات",
        "2. يرجى تعيين رمز PIN قوي مكون من 4-16 رقمًا، وتجنب استخدام الأرقام المتتالية أو المكررة",
        "3. الحد الأقصى لمحاولات إدخال رمز PIN هو 10 مرات، بعد 10 محاولات خاطئة سيتم إعادة ضبط الجهاز",
        "4. يرجى الحفاظ على رمز PIN الخاص بك بشكل آمن وعدم مشاركته مع أي شخص",
    ]
class DownloadDigital:
    #header = "يرجى تنزيل وتثبيت تطبيق DigitShield للتحقق من الجهاز"
    tips = [
        "1. اضغط على \"ربط المحافظ\"",
        "2. قم بتوصيل الجهاز:",
        "3. انتظر قليلاً، سيقوم تطبيق DigitalShield باستعادة الحسابات التي استخدمتها سابقاً.",
    ]
class Solana:
    ata_reciver = "المستلم (حساب الرمز المميز المرتبط)"
    ata_sender = "المرسل (حساب الرمز المميز المرتبط)"
    source_owner = "موقع المعاملة"
    fee_payer = "مدفوع الرسوم"