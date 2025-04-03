class App:
    account = "賬戶"
    scan = "掃描交易"
    nft = "NFT 陳列室"
    guide = "使用說明"
    security = "安全"
    setting = "設定"


#### Setting App
class Setting:
    bluetooth = "藍牙"
    language = "語言"
    vibration = "觸摸反饋"
    brightness = "螢幕亮度"
    auto_lock = "自動鎖定"
    auto_shutdown = "自動關機"
    animation = "過場動畫"
    wallpaper = "壁紙"
    power_off = "關機"
    restart = "重新啟動"

#### Security App
class Security:
    change_pin = "更改PIN碼"
    backup_mnemonic = "備份助記詞"
    check_mnemonic = "檢查助記詞"
    wipe_device = "抹掉裝置"

#### guide App
class Guide:
    about = "關於Digit Shield"
    terms_of_use = '使用條款'
    device_info = '裝置資訊'
    firmware_update = '韌體升級'
    terms_title_terms_us = 'Digit Shield使用條款'
    terms_describe_terms_us = '要訪問使用條款的完整版本，請訪問以下具體連結:\n http://digitshield.com/terms'

    terms_title_product_services = 'Digit Shield產品和服務'
    terms_describe_product_services = '我們的硬體錢包安全的管理加密貨幣'
    terms_title_risks = '風險'
    terms_describe_risks = '請注意與加密貨幣和技術漏洞相關的風險.'
    terms_title_disclaimers = '免責聲明'
    terms_describe_disclaimers = '提供的訊息不是財務建議。在做出任何決定前，請尋求專業建議。'
    terms_title_contact_us = '聯絡我們'
    terms_describe_contact_us = '如果您有任何疑問或疑慮，請給我們傳送電子郵件至support@digitshield.com'

    accept_tems = '一、接受條款'
    use_range = '1、適用範圍'
    range_include = '本條款適用於通過 Digital Shield 錢包提供的所有服務，包括：'
    range_include_1 = '硬體錢包的購買、激活及售後服務；Digital Shield 移動端應用程式（Android/iOS/Goolg）的下載、安裝及功能使用；固件升級服務（包括安全補丁、功能增強版本）；多鏈數字資產管理（支援 BTC、ETH 等 3000 + 代幣的存儲與轉賬）；技術支援（設備故障排查、交易簽名異常處理等）。'
    user_qualification = '2、用戶資格'
    ability_include = '您確認已年滿 18 週歲，並具備完全民事行為能力；'
    ability_include_1 = '您所在司法轄區未禁止加密貨幣及相關硬體設備的使用（例如中國內地用戶需自行承擔使用風險）；'
    terms_update_infor = '3、條款更新與通知'
    update_infor_content = '我們保留單方修改條款的權利，修訂內容通過官網公告欄發佈，生效日期以公告為準； 若您繼續使用服務，視為接受修訂後的條款；若不同意，應在生效日期前書面通知並終止使用。'

    wallet_buy_iterms = '二、硬體錢包購買條款'
    order_process = '1. 訂單流程'
    payment_confirmation = '支付確認：訂單支付成功（以區塊鏈網路確認或銀行到賬為準）後，系統將在 24 小時內更新狀態；'
    inventory_shortage = '庫存缺貨：若庫存不足，用戶可選擇：'
    inventory_shortage_1 = 'a. 等待補貨（最長 30 日，超期自動退款）；'
    inventory_shortage_2 = 'b. 全額原路退款（加密貨幣訂單按支付時匯率折算）。'
    return_and_exchange_policy = '2. 退換政策'
    return_and_exchange_condi = '退貨條件：'
    return_and_exchange_condi_con = 'a. 未激活設備需保留原廠密封貼紙（編號與訂單一致）及完整配件（USB 線、說明書、助記詞卡片）； b. 退貨申請需在簽收後 7 日內提交，逾期視為驗收合格； c. 退回運費由用戶承擔（質量問題除外）。'
    warranty_scope = '保修範圍：'
    warranty_scope_1 = 'a. 覆蓋安全晶片故障、螢幕顯示異常、按鍵失靈等非人為損壞；'
    warranty_scope_2 = 'b. 需提供購買憑證（訂單號）及故障證明（視頻需清晰展示設備 SN 碼及異常現象）；'
    warranty_scope_3 = 'c. 人為損壞（如進水、摔落）不在保修範圍內，可付費維修。'

    disclaimer = '三、免責聲明'
    product_risk = '1. 產品風險'
    physical_risk = '物理風險：'
    physical_risk_1 = 'a. 設備在高溫（>60℃）、高濕（>90% RH）、強磁場（>100mT）環境下可能失效；'
    physical_risk_2 = 'b. 長期未充電可能導致電池損壞（建議每個月充電一次）。'
    supply_chain_risk = '供應鏈風險：'
    supply_chain_risk_1 = 'a. 官網提供防偽驗證工具，掃描設備二維碼可查驗真偽；'
    supply_chain_risk_2 = 'b. 若懷疑設備被調包，應立即聯繫客服並報警處理。'
    service_interruption = '2. 服務中斷'
    service_interruption_1 = '計劃維護將提前 48 小時通過官網公告通知，緊急維護可能無預警暫停服務；'
    service_interruption_2 = '不可抗力因素導致數據丟失，我們不承擔賠償責任。'

    device_label = "設備名称"
    device_title_firmware_version = '韌體版本'
    device_title_serial_number = '序號'
    bluetooth_name = "藍牙名稱"
    bluetooth_version = "藍牙版本"
    firmware_title_1 = '1.請確保裝置電量高於20%'
    firmware_title_2 = '2.使用USB-C線將裝置連結至電腦'
    firmware_title_3 = '3.單擊「韌體升級」'
    firmware_title_caution = '警告'
    firmware_describe_caution = '升級中，請確保USB連結'
    equipment_info = '設備資訊'
    equipment_name = '設備名稱'
    equipment_version = '設備版本'

class Nft:
    nft_item ="{} item"
    nft_items ="{} items"
class Title:
    enter_old_pin = "請輸入舊PIN碼"
    enter_new_pin = "請輸入新PIN碼"
    enter_pin = "請輸入PIN碼"
    enter_pin_again = "請再次輸入PIN碼"
    select_language = "語言"
    create_wallet = "建立錢包"
    wallet = "錢包"
    import_wallet = "導入钱包"
    restore_wallet = "恢復錢包"
    wallet_is_ready = "錢包準備就緒"
    select_word_count = "選擇單詞數量"
    wallet_security = "錢包安全"
    pin_security = "PIN 安全提示"
    mnemonic_security = "助記詞安全提示"
    backup_mnemonic = "備份助記詞"
    enter_mnemonic = "請輸入助記詞"
    check_mnemonic = "檢查助記詞"
    success = "成功"
    operate_success = "操作成功"
    theme_success = "主題切換成功"
    warning = "警告"
    error = "錯誤"
    verified = "助記詞備份完成"
    invalid_mnemonic = "無效的助記詞"
    pin_not_match = "PIN 不匹配"
    check_recovery_mnemonic = "檢查恢復助記詞"
    mnemonic_not_match = "助記詞不匹配"
    power_off = "關機"
    restart = "重新啟動"
    change_language = "更改語言"
    wipe_device = "抹掉裝置"
    bluetooth_pairing = "藍牙配對"
    address="{} 地址"
    public_key = "{} 公鑰"
    xpub = "{} XPub"
    transaction = "{} 交易"
    transaction_detail = "交易詳情"
    confirm_transaction = "確認交易"
    confirm_message = "確認訊息"
    signature = "簽名結果"
    wrong_pin = "PIN錯誤"
    pin_changed = "PIN已修改"
    pin_enabled = "PIN已啟用"
    pin_disabled = "PIN已停用"
    unknown_token = "未知代幣"
    view_data = "查看數據"
    sign_message = "{} 訊息簽名"
    verify_message = "{} 訊息驗簽"
    typed_data = "{} 結構化數據"
    typed_hash = "{} 結構化哈希"
    system_update = "系統升級"
    entering_boardloader = "Entering Boardloader"
    remove_credential = "刪除憑證"
    list_credentials = "列出憑證"
    authorize_coinjoin = "授權CoinJoin"
    multisig_address_m_of_n = "{} 多重簽名地址\n({} of {})"
    u2f_register = "U2F 註冊"
    u2f_unregister = "U2F 註銷"
    u2f_authenticate = "U2F 認證"
    fido2_register = "FIDO2 註冊"
    fido2_unregister = "FIDO2 註銷"
    fido2_authenticate = "FIDO2 認證"
    fee_is_high = "手續費過高"
    confirm_locktime = "確認鎖定時間"
    view_transaction = "查看交易"
    x_confirm_payment = "{} 確認付款"
    confirm_replacement = "確認替換交易"
    x_transaction = "{} 交易"
    x_joint_transaction = "{} 聯合交易"
    change_label = "修改裝置名稱"
    enable_passphrase = "啟用 Passphrase"
    disable_passphrase = "停用 Passphrase"
    passphrase_source = "Passphrase 輸入設定"
    enable_safety_checks ="啟用安全檢查"
    disable_safety_checks ="停用安全檢查"
    experiment_mode = "實驗模式"
    set_as_homescreen = "設為主屏幕"
    get_next_u2f_counter = "獲取U2F計數器"
    set_u2f_counter = "設定U2F計數器"
    encrypt_value = "加密數據"
    decrypt_value = "解密數據"
    confirm_entropy = "導出熵"
    memo = "備註"
    import_credential = "導入憑證"
    export_credential = "導出憑證"
    asset = "資產"
    unimplemented = "未實現"
    invalid_data="無效的數據格式"
    low_power = "電量低"

class Text:
    tap_to_unlock = "點擊以解鎖"
    unlocking = "正在解鎖裝置..."
    # str_words = "#18794E {}# 個單詞"
    str_words = "#FFFFFF {}# 個單詞"
    backup_manual = "手動寫下助記詞並存放在安全的地方"
    check_manual = "按順序依次點擊下面的單詞"
    backup_verified = "您已完成助記詞的備份，請妥善保存，不要與任何人分享"
    backup_invalid = "您輸入的助記詞不正確，請檢查備份的助記詞，再次嘗試"
    pin_not_match = "您輸入的PIN碼不正確，請再次嘗試"
    please_wait = "請稍等"
    wiping_device = "正在清除裝置數據..."
    create_wallet = "生成一組新的助記詞，建立新錢包"
    restore_wallet = "從您備份的助記詞恢復錢包"
    restore_mnemonic_match = "您的助記詞匹配，您的助記詞備份正確"
    restore_success = "恢復錢包成功"
    create_success = "您的助記詞已成功備份，錢包已建立"
    check_recovery_mnemonic = "請檢查您的助記詞，確認是否完全匹配"
    invalid_recovery_mnemonic = "您輸入的助記詞無效，請檢查您的助記詞，再次嘗試"
    check_recovery_not_match = "您輸入的助記詞是有效的，但是與裝置中的助記詞不匹配"
    shutting_down = "正在關機..."
    restarting = "正在重新啟動..."
    never = "從不"
    second = "秒"
    seconds = "秒"
    minute = "分鐘"
    minutes = "分鐘"
    changing_language = "您正在更改語言\n應用此設定將重新啟動裝置"
    change_pin = "設定一個長度為4~16位的PIN碼，保護您的裝置"
    wipe_device = "將裝置恢復到出廠狀態。\n警告： 這將從您的裝置中抹掉所有數據。"
    wipe_device_check = [
        "抹掉裝置會清除所有數據",
        "數據將無法恢復",
        "已經備份了助記詞",
    ]
    wipe_device_success = "裝置已成功清除數據\n 正在重啟裝置 ..."
    bluetooth_pair = "請在您的裝置上輸入配對碼"
    bluetooth_pair_failed = "藍牙配對失敗"
    path = "派生路徑:"
    chain_id = "Chain ID:"
    send = "傳送"
    to = "至"
    amount = "金額"
    from_ = "來自"
    receiver = "接收者"
    fee = "手續費"
    max_fee = "最大手續費"
    max_priority_fee_per_gas = "最大優先級手續費"
    max_fee_per_gas = "單位Gas的交易費上限"
    gas_price = "燃料價格"
    total = "總金額"
    do_sign_this_transaction = "是否簽名這筆{}交易"
    transaction_signed = "交易已簽名"
    address = '地址:'
    public_key = "公鑰:"
    xpub = "XPub:"
    unknown_tx_type = "未知交易類型，請檢查輸入數據"
    use_app_scan_this_signature = "請使用錢包 APP 掃描簽名結果"
    internal_error = "內部錯誤"
    tap_switch_to_airgap = "點擊二維碼切換為展示Airgap地址"
    tap_switch_to_receive = "點擊二維碼切換為展示錢包收款地址"
    incorrect_pin_times_left = "PIN不正確，剩餘 {} 次重試機會"
    incorrect_pin_last_time = "PIN不正確，還有最後一次機會"
    wrong_pin = "輸入的PIN碼不正確"
    seedless = "缺少種子"
    backup_failed = "備份失敗！"
    need_backup = "需要備份！"
    pin_not_set = "沒有設定PIN！"
    experimental_mode = "實驗模式"
    pin_change_success = "PIN碼已成功更改"
    pin_enable_success = "PIN碼已成功啟用"
    pin_disable_success = "PIN碼已成功停用"
    contract = "合約:"
    new_contract = "新合約?"
    bytes_ = "{} 位元組"
    message = "訊息:"
    no_message = "不包含訊息"
    contains_x_key = "包含 {} 鍵"
    array_of_x_type = "陣列類型 {} {}"
    do_sign_712_typed_data = "是否簽署這筆結構化數據交易？"
    do_sign_typed_hash = "是否簽署這筆結構化哈希交易？"
    domain_hash = "Domain 哈希:"
    message_hash = "訊息 哈希:"
    switch_to_update_mode = "切換到更新模式"
    switch_to_boardloader = "Switch to board loader mode"
    list_credentials = "是否要導出有關存儲在此裝置上的憑證訊息？"
    coinjoin_at_x = "是否要參加下面的Coinjoin交易:\n{}"
    signature_is_valid = "簽名有效"
    signature_is_invalid = "簽名無效"
    u2f_already_registered = "U2F 已經註冊"
    u2f_not_registered = "U2F 未註冊"
    fido2_already_registered_x = "FIDO2 已註冊 {}"
    fido2_verify_user = "FIDO2 驗證用戶"
    device_already_registered_x = "裝置已註冊 {}"
    device_verify_user = "裝置驗證用戶"
    finalize_transaction = "完成交易"
    meld_transaction = "融合交易"
    update_transaction = "更新交易"
    fee_is_unexpectedly_high = "手續費過高"
    change_count = "找零數量"
    locktime_will_have_no_effect = "鎖定時間將不會有影響"
    confirm_locktime_for_this_transaction = "確認交易的鎖定時間"
    block_height = "區塊高度"
    time = "時間"
    amount_increased = "金額增加"
    amount_decreased = "金額減少"
    fee_unchanged = "手續費未改變"
    fee_increased = "手續費增加"
    fee_decreased = "手續費減少"
    your_spend = "你的花費"
    change_label_to_x = "修改標籤為 {}"
    enable_passphrase = "要啟用 Passphrase 加密嗎？"
    disable_passphrase = "要停用 Passphrase 加密嗎？"
    enable_passphrase_always = "總是在本機輸入 Passphrase 嗎？"
    revoke_enable_passphrase_always = "要撤銷總是在本機輸入 Passphrase 的設定嗎？"
    auto_lock_x = "確定要在 {} 之後自動鎖定裝置嗎？"
    enable_safety_checks = "要執行嚴格的安全檢查嗎？這將提供更全面的安全保護。"
    disable_safety_checks = "確定要停用安全檢查嗎？繼續操作前，請知悉該行為的潛在安全風險。"
    enable_experiment_mode = "是否啟用實驗模式？"
    set_as_homescreen = "確定要更改主屏幕嗎？"
    replace_homescreen = "確定要替換主屏幕嗎？這將會刪除最早上傳的壁紙。"
    get_next_u2f_counter = "確定要獲取下一個U2F計數器嗎？"
    set_u2f_counter_x = "確定要設定U2F計數器為 {} 嗎？"
    confirm_entropy = "確定要導出熵嗎？繼續操作之前請明白你在做什麼！"
    bandwidth = "頻寬"
    energy = "能量"
    sender = "傳送者"
    recipient = "接收者"
    resource = "資源"
    frozen_balance = "凍結的金額"
    unfrozen_balance = "解凍的金額"
    delegated_balance = "委託的金額"
    undelegated_balance = "撤銷委託的金額"
    you_are_freezing = "你正在凍結資產"
    you_are_unfreezing = "你正在解凍資產"
    you_are_delegating = "你正在委託資產"
    you_are_undelegating = "你正在撤銷委託"
    duration = "持續時間"
    lock = "鎖定"
    unlock = "解鎖"
    all = "全部"
    source = "來源"
    tip = "提示"
    keep_alive = "Keep alive"
    invalid_ur = "不支援的二維碼類型，請重試"
    sequence_number = "序號"
    expiration_time = "過期時間"
    argument_x = "參數 #{}"
    low_power_message = "電量還剩餘 {}%\n請充電"

class Tip:
    swipe_down_to_close = "向下滑動以關閉"
class Button:
    done = "完成"
    ok = "好的"
    confirm = "確認"
    reject = "拒絕"
    next = "下一步"
    cancel = "取消"
    redo = "重新生成"
    continue_ = "繼續"
    try_again = "重試"
    power_off = "關機"
    restart = "重新啟動"
    hold = "按住"
    address = "地址"
    qr_code = "二維碼"
    view_detail = "查看詳情"
    hold_to_sign = "長按簽名"
    hold_to_wipe = "長按抹掉"
    receive = "收款地址"
    airgap = "Airgap"
    sign = "簽名"
    verify = "驗證"
    view_full_array = "查看完整陣列"
    view_full_struct = "查看完整結構"
    view_full_message = "查看完整訊息"
    view_data = "查看數據"
    view_more = "查看更多"
class WalletSecurity:
    header = "在一張紙上寫下您的助記詞並將其存放在安全的地方"
    tips = [
        {
            "level": "info",
            "msgs": [
                "#00001F 助記詞需要安全存放#",
                "#18794E * 存放在銀行金庫中#",
                "#18794E * 存放在保險箱中#",
                "#18794E * 存放在多個秘密地點#",
            ]
        },
        {
            "level": "warning",
            "msgs": [
                "#00001F 一定要注意#",
                "#CD2B31 * 謹記保存的助記詞#",
                "#CD2B31 * 不要丟失#",
                "#CD2B31 * 不要告訴別人#",
                "#CD2B31 * 不要存儲在網路上#",
                "#CD2B31 * 不要存儲在電腦上#",
            ]
        },
    ]

class MnemonicSecurity:
    header = "助記詞是一組用來恢復錢包資產的短語，擁有助記詞就意味著可以使用您的資產，請妥善保管"

    tips = [
        "1. 請檢查環境安全，確保沒有旁觀者或攝像頭",
        "2. 請按短語的正確順序備份助記詞，切勿與任何人分享您的助記詞",
        "3. 請在安全的地方離線保存助記詞，切勿使用電子方式備份助記詞，切勿上傳網路",
    ]

class PinSecurity:
    # 定义类属性header，用于描述PIN码的作用和使用提示
    header = "PIN碼是裝置訪問的密碼，用於授權訪問當前裝置。請按照以下提示正確使用PIN碼"
    # 定义类属性tips，用于存储PIN码使用的具体提示信息
    tips = [
        "1. 設定或錄入PIN時請檢查環境安全，確保沒有旁觀者或攝像頭",  # 提示1：设置或输入PIN码时请检查环境安全，确保没有旁观者或摄像头
        "2. 請設定長度為4-16位的高強度的PIN碼，避免使用連續或重複的數字",
        "3. PIN碼的最大重試次數為10次，當錯誤10次後裝置將會被重置",
        "4. 請妥善保管PIN碼，不要和任何人分享您的PIN碼",
    ]

class Solana:
    ata_reciver = "接收者(關聯代幣帳戶)"
    ata_sender = "發送者(關聯代幣帳戶)"
    source_owner = "交易簽署者"
    fee_payer = "手續費支付者"    