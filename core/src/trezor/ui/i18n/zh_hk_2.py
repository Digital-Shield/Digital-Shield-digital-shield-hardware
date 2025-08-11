class App:
    account = "账户"
    scan = "扫描交易"
    nft = "NFT 陈列室"
    guide = "产品说明"
    security = "安全"
    setting = "设定"


#### Setting App
class Setting:
    bluetooth = "蓝牙"
    language = "语言"
    vibration = "触感反馈"
    brightness = "屏幕亮度"
    auto_lock = "自动锁定"
    auto_shutdown = "自动关机"
    animation = "过场动画"
    wallpaper = "壁纸"
    power_off = "关机"
    restart = "重新启动"
    restart_tip = "重启"

#### Security App
class Security:
    change_pin = "更改PIN码"
    backup_mnemonic = "备份助记词"
    check_mnemonic = "核对助记词"
    wipe_device = "抹掉设备"

#### guide App
class Guide:
    about = "关注我们"
    terms_of_use = '使用条款'
    device_info = '设备信息'
    firmware_update = '固件升级'
    #terms_title_terms_us = 'Digit Shield使用条款'
    #terms_describe_terms_us = '要访问使用条款的完整版本，请访问以下具体链接:\n http://digitshield.com/terms'

    # terms_title_product_services = 'Digit Shield產品和服務'
    # terms_describe_product_services = '我們的硬體錢包安全的管理加密貨幣'
    # terms_title_risks = '風險'
    # terms_describe_risks = '請注意與加密貨幣和技術漏洞相關的風險.'
    # terms_title_disclaimers = '免責聲明'
    # terms_describe_disclaimers = '提供的訊息不是財務建議。在做出任何決定前，請尋求專業建議。'
    # terms_title_contact_us = '四、联系我们'
    # terms_describe_contact_us = '如果您有任何疑问或疑虑，请给我们发送电子邮件至www.ds.pro@gmail.com'

    # accept_tems = '一、接受條款'
    # use_range = '1、適用範圍'
    # range_include = '本條款適用於通過 Digital Shield 錢包提供的所有服務，包括：'
    # range_include_1 = '硬體錢包的購買、激活及售後服務；Digital Shield 移動端應用程式（Android/iOS/Goolg）的下載、安裝及功能使用；固件升級服務（包括安全補丁、功能增強版本）；多鏈數字資產管理（支援 BTC、ETH 等 3000 + 代幣的存儲與轉賬）；技術支援（設備故障排查、交易簽名異常處理等）。'
    # user_qualification = '2、用戶資格'
    # ability_include = '您確認已年滿 18 週歲，並具備完全民事行為能力；'
    # ability_include_1 = '您所在司法轄區未禁止加密貨幣及相關硬體設備的使用（例如中國內地用戶需自行承擔使用風險）；'
    # terms_update_infor = '3、條款更新與通知'
    # update_infor_content = '我們保留單方修改條款的權利，修訂內容通過官網公告欄發佈，生效日期以公告為準； 若您繼續使用服務，視為接受修訂後的條款；若不同意，應在生效日期前書面通知並終止使用。'

    # wallet_buy_iterms = '二、硬體錢包購買條款'
    # order_process = '1. 訂單流程'
    # payment_confirmation = '支付確認：訂單支付成功（以區塊鏈網路確認或銀行到賬為準）後，系統將在 24 小時內更新狀態；'
    # inventory_shortage = '庫存缺貨：若庫存不足，用戶可選擇：'
    # inventory_shortage_1 = 'a. 等待補貨（最長 30 日，超期自動退款）；'
    # inventory_shortage_2 = 'b. 全額原路退款（加密貨幣訂單按支付時匯率折算）。'
    # return_and_exchange_policy = '2. 退換政策'
    # return_and_exchange_condi = '退貨條件：'
    # return_and_exchange_condi_con = 'a. 未激活設備需保留原廠密封貼紙（編號與訂單一致）及完整配件（USB 線、說明書、助記詞卡片）； b. 退貨申請需在簽收後 7 日內提交，逾期視為驗收合格； c. 退回運費由用戶承擔（質量問題除外）。'
    # warranty_scope = '保修範圍：'
    # warranty_scope_1 = 'a. 覆蓋安全晶片故障、螢幕顯示異常、按鍵失靈等非人為損壞；'
    # warranty_scope_2 = 'b. 需提供購買憑證（訂單號）及故障證明（視頻需清晰展示設備 SN 碼及異常現象）；'
    # warranty_scope_3 = 'c. 人為損壞（如進水、摔落）不在保修範圍內，可付費維修。'

    # disclaimer = '三、免責聲明'
    # product_risk = '1. 產品風險'
    # physical_risk = '物理風險：'
    # physical_risk_1 = 'a. 設備在高溫（>60℃）、高濕（>90% RH）、強磁場（>100mT）環境下可能失效；'
    # physical_risk_2 = 'b. 長期未充電可能導致電池損壞（建議每個月充電一次）。'
    # supply_chain_risk = '供應鏈風險：'
    # supply_chain_risk_1 = 'a. 官網提供防偽驗證工具，掃描設備二維碼可查驗真偽；'
    # supply_chain_risk_2 = 'b. 若懷疑設備被調包，應立即聯繫客服並報警處理。'
    # service_interruption = '2. 服務中斷'
    # service_interruption_1 = '計劃維護將提前 48 小時通過官網公告通知，緊急維護可能無預警暫停服務；'
    # service_interruption_2 = '不可抗力因素導致數據丟失，我們不承擔賠償責任。'

    device_label = "设备名称"
    device_title_firmware_version = '固件版本'
    device_title_serial_number = '序号'
    bluetooth_name = "蓝牙名称"
    bluetooth_version = "蓝牙版本"
    attention_events = "注意事项"
    firmware_title_1 = '1.请确保设备电量高于20%'
    firmware_title_2 = '2.使用USB-C线将设备连接至电脑'
    firmware_title_3 = '3.单击“固件升级”'
    firmware_title_caution = '警告'
    firmware_describe_caution = '升级中，请确保USB连接'
    equipment_info = '设备信息'
    equipment_name = '设备名称'
    equipment_version = '设备版本'

# class Nft:
#     nft_item ="{} item"
#     nft_items ="{} items"
class Title:
    enter_old_pin = "输入旧PIN码"
    enter_new_pin = "输入新PIN码"
    enter_pin = "请输入PIN码"
    enter_pin_again = "再次输入PIN码"
    select_language = "语言"
    create_wallet = "创建钱包"
    wallet = "钱包"
    import_wallet = "导入钱包"
    restore_wallet = "恢复钱包"
    select_word_count = "选择单词数量"
    wallet_security = "钱包安全"
    pin_security = "启用PIN码保护"
    mnemonic_security = "助记词安全提示"
    backup_mnemonic = "备份助记词"
    enter_mnemonic = "请输入助记词"
    check_mnemonic = "检查助记词"
    success = "成功"
    operate_success = "操作成功"
    theme_success = "主题切换成功"
    warning = "警告"
    error = "错误"
    invalid_mnemonic = "无效的助记词"
    pin_not_match = "PIN 不匹配"
    check_recovery_mnemonic = "检查恢复助记词"
    power_off = "关机"
    restart = "重新启动"
    change_language = "更改语言"
    wipe_device = "抹掉设备"
    bluetooth_pairing = "蓝牙配对"
    address="{} 地址"
    public_key = "{} 公钥"
    xpub = "{} XPub"
    transaction = "{} 交易"
    transaction_detail = "交易详情"
    confirm_transaction = "确认交易"
    confirm_message = "确认消息"
    signature = "签名结果"
    wrong_pin = "PIN错误"
    pin_changed = "PIN已更改"
    pin_enabled = "PIN已启用"
    pin_disabled = "PIN已停用"
    unknown_token = "未知代币"
    view_data = "查看数据"
    sign_message = "{} 消息签名"
    verify_message = "{} 消息验签"
    typed_data = "{} 结构化数据"
    typed_hash = "{} 结构化哈希"
    system_update = "系统升级"
    entering_boardloader = "进入Boardloader"
    remove_credential = "删除凭证"
    list_credentials = "列出凭证"
    authorize_coinjoin = "授权CoinJoin"
    multisig_address_m_of_n = "{} 多重签名地址\n({} of {})"
    u2f_register = "U2F 注册"
    u2f_unregister = "U2F 注销"
    u2f_authenticate = "U2F 认证"
    fido2_register = "FIDO2 注册"
    fido2_unregister = "FIDO2 注销"
    fido2_authenticate = "FIDO2 认证"
    finalize_transaction = "完成交易"
    meld_transaction = "融合交易"
    update_transaction = "更新交易"
    high_fee = "高费用"
    fee_is_high = "手续费过高"
    confirm_locktime = "确认锁定时间"
    view_transaction = "查看交易"
    x_confirm_payment = "{} 确认付款"
    confirm_replacement = "确认替换交易"
    x_transaction = "{} 交易"
    x_joint_transaction = "{} 联合交易"
    change_label = "修改设备名称"
    enable_passphrase = "启用 Passphrase"
    disable_passphrase = "停用 Passphrase"
    passphrase_source = "Passphrase 输入设置"
    enable_safety_checks ="启用安全检查"
    disable_safety_checks ="停用安全检查"
    experimental_mode =  "实验模式"
    set_as_homescreen = "设为主屏幕"
    get_next_u2f_counter = "获取U2F计数器"
    set_u2f_counter = "设置U2F计数器"
    encrypt_value = "加密数据"
    decrypt_value = "解密数据"
    confirm_entropy = "导出熵"
    memo = "备注"
    import_credential = "导入凭证"
    export_credential = "导出凭证"
    asset = "资产"
    unimplemented = "未实现"
    invalid_data = "二维码无效"
    low_power = "电量低"
    collect_nft = "收集 NFT"
    verify_device = "验证设备"
    update_bootloader = "更新引导加载程序"
    update_resource = "更新资源"
    
    words_num = "单词 #{}"
    download_digital = "下载"
    connect_wallets = "连接硬件钱包"
    start_setup = "开始设置"
    prepare_create = "准备创建"
    prepare_import = "准备导入"
    prepare_check = "准备核对"
    input_words = "输入助记词"
    has_sub = "已提交"
    reatart = "重新开始"
    invalid_words = "助记词无效"
    stop_checking = "终止核对"
    correct_words = "助记词正确"
    mnemonic_not_match = "助记词不匹配"
    wallet_created = "钱包已创建"
    check_words = "核对助记词"
    verified = "已验证"
    wallet_is_ready = "钱包已就绪"

    prepare_backup = "准备备份"
    mnemonic_word = "助记词"
    error_mnemonic_word = "单词错误"
    right_word = "正确"
    wrong_word = "错误"

    pin_not_match = "不匹配"
    has_reset = "设备已重置"
    has_wipe = "设备已抹掉"
    screen_bright = "屏幕亮度"
    download_app = "下载App"
    official_website = "官网"
    scan_ercode = "扫描App上显示的二维码"
    wipe_notice = "在抹除设备之前，请确认已知晓："
    receive_tips = "仅支持接收{}资产"
    sign_fail = "签名失败"
    select_network = "选择网络"
    preview = "预览"
    go_link = "请前往链接："
    connect_again = "请尝试重新连接。"

class Text:
    start_setup = "创建一个新的助记词钱包，或者导入已有的助记词备份来恢复钱包。"
    select_word_count = "请选择助记词的单词个数。"
    input_words = "请按顺序输入单词，确保其编号与您的助记词备份完全一致"
    invalid_words = "您输入的助记词无效，点击单词进行编辑，或重新开始。"
    stop_checking = "终止后所有进度都将丢失，是否确认终止？"
    import_wallet = "输入您已有的助记词备份，恢复钱包。"
    correct_words = "您输入的助记词有效，并且与设备中存储的一致。"
    mnemonic_not_match = "您输入的助记词有效，但与设备中存储的不一致。"
    wallet_created = "新钱包创建成功，请立即备份。"
    mnemonic_word_tips = "请按顺序抄写以下{}个单词。"
    select_words = "请选择正确的单词"
    error_mnemonic_word = "单词不正确，请检查您备份的助记词，确认无误后重试"
    has_reset = "PIN码输入错误次数太多，存储空间已被清空。"
    has_wipe = "设备已成功清除数据，请重启设备。"
    download_digital_tips = "请前往下载 Digital Shield App：https://ds.pro/download"
    sign_fail = "您取消了签名，交易已取消。"
    sign_success = "交易已签名"
    check_words_tips = "请跟随引导，依照您手中的助记词备份，逐一核对单词。"
    backup_verified = "您已完成助记词验证。"
    create_success = "您的助记词已备份，开始体验。"
    tap_to_unlock = "点击屏幕解锁"
    unlocking = "正在解锁设备"

    str_words = "#FFFFFF {}# 个单词"
    backup_manual = "手动写下助记词并存放在安全的地方"
    check_manual = "按顺序依次点击下面的单词"
    backup_invalid = "您输入的助记词不正确，请检查备份的助记词，再次尝试"
    pin_not_match = "两次输入的PIN码不一致，请重试。"
    please_wait = "请稍等"
    wiping_device = "正在清除设备数据..."
    create_wallet = "生成一组新的助记词，建立新钱包"
    restore_wallet = "从您备份的助记词恢复钱包"
    restore_mnemonic_match = "您的助记词匹配，您的助记词备份正确"
    restore_success = "您的助记词已导入，钱包恢复成功。"
    check_recovery_mnemonic = "请检查您的助记词，确认是否完全匹配"
    invalid_recovery_mnemonic = "您输入的助记词无效，请检查您的助记词，再次尝试"
    check_recovery_not_match = "您输入的助记词是有效的，但是与设备中的助记词不匹配"
    shutting_down = "正在关机"
    restarting = "正在重启"
    never = "从不"
    second = "秒"
    seconds = "秒"
    minute = "分钟"
    minutes = "分钟"
    changing_language = "您正在更改语言为{} ，应用此设置将重新启动设备"
    change_pin = "设置一组长度为4~16位的PIN码。"
    wipe_device = "警告：这将从您的设备中抹掉所有数据，并将设备恢复到出厂状态。"
    wipe_device_check = [
        "抹掉后，该设备上存储的助记词将被永久删除。",
        "助记词被删除后将无法恢复。",
        "您的助记词已经备份，并已妥善保管。",
    ]
    wipe_device_success = "设备已成功清除数据\n 请重启设备 ..."
    bluetooth_pair = "请在您的设备上输入配对码"
    bluetooth_pair_failed = "蓝牙配对失败"
    path = "派生路径:"
    chain_id = "Chain ID:"
    send = "发送"
    to = "至"
    amount = "金额"
    from_ = "来自"
    receiver = "接收者"
    fee = "手续费"
    max_fee = "最大手续费"
    max_priority_fee_per_gas = "最大优先级手续费"
    max_fee_per_gas = "单位Gas的交易费上限"
    max_gas_limit = "最大燃料限制:"
    gas_unit_price = "燃料单价:"
    gas_price = "燃料价格"
    total = "总金额"
    do_sign_this_transaction = "确认要签署此 {} 交易吗？"
    transaction_signed = "交易已签名"
    address = '地址:'
    public_key = "公钥:"
    xpub = "XPub:"
    unknown_tx_type = "未知交易类型，请检查输入数据"
    unknown_function = "未知函数:"
    use_app_scan_this_signature = "请使用钱包 APP 扫描签名结果"
    internal_error = "内部错误"
    tap_switch_to_airgap = "点击二维码切换为展示Airgap地址"
    tap_switch_to_receive = "点击二维码切换为展示钱包收款地址"
    incorrect_pin_times_left = "PIN不正确，剩余 {} 次重试机会"
    incorrect_pin_last_time = "PIN不正确，还有最后一次机会"
    wrong_pin = "输入的PIN码不正确"
    seedless = "缺少种子"
    backup_failed = "备份失败！"
    need_backup = "需要备份！"
    pin_not_set = "没有设置PIN！"
    experimental_mode = "实验模式"
    pin_change_success = "PIN码已更改成功"
    pin_enable_success = "PIN码已启用成功"
    pin_disable_success = "PIN码已停用成功"
    # contract = "合約:"
    # new_contract = "新合約?"
    # bytes_ = "{} 位元組"
    # message = "訊息:"
    # no_message = "不包含訊息"
    # contains_x_key = "包含 {} 鍵"
    # array_of_x_type = "陣列類型 {} {}"
    # do_sign_712_typed_data = "是否簽署這筆結構化數據交易？"
    # do_sign_typed_hash = "是否簽署這筆結構化哈希交易？"
    # domain_hash = "Domain 哈希:"
    # message_hash = "訊息 哈希:"
    # switch_to_update_mode = "切換到更新模式"
    # switch_to_boardloader = "Switch to board loader mode"
    # list_credentials = "是否要導出有關存儲在此裝置上的憑證訊息？"
    # coinjoin_at_x = "是否要參加下面的Coinjoin交易:\n{}"
    # signature_is_valid = "簽名有效"
    # signature_is_invalid = "簽名無效"
    # u2f_already_registered = "U2F 已經註冊"
    # u2f_not_registered = "U2F 未註冊"
    # fido2_already_registered_x = "FIDO2 已註冊 {}"
    # fido2_verify_user = "FIDO2 驗證用戶"
    # device_already_registered_x = "裝置已註冊 {}"
    # device_verify_user = "裝置驗證用戶"
    # fee_is_unexpectedly_high = "手續費過高"
    # too_many_change_outputs = "找零輸出太多"
    # change_count = "找零數量"
    # locktime_will_have_no_effect = "鎖定時間將不會有影響"
    # confirm_locktime_for_this_transaction = "確認交易的鎖定時間"
    # block_height = "區塊高度"
    # time = "時間"
    # amount_increased = "金額增加"
    # amount_decreased = "金額減少"
    # fee_unchanged = "手續費未改變"
    # fee_increased = "手續費增加"
    # fee_decreased = "手續費減少"
    # your_spend = "你的花費"
    # change_label_to = "修改標籤為："
    change_label_to_x = "修改设备名称为：{}？"
    enable_passphrase = "你要启用 Passphrase 加密吗？"
    disable_passphrase = "你确定要停用 Passphrase 加密吗？"
    # enable_passphrase_always = "總是在本機輸入 Passphrase 嗎？"
    # revoke_enable_passphrase_always = "要撤銷總是在本機輸入 Passphrase 的設定嗎？"
    # auto_lock_x = "確定要在 {} 之後自動鎖定裝置嗎？"
    # enable_safety_checks = "要執行嚴格的安全檢查嗎？這將提供更全面的安全保護。"
    # disable_safety_checks = "確定要停用安全檢查嗎？繼續操作前，請知悉該行為的潛在安全風險。"
    # enable_experiment_mode = "是否啟用實驗模式？"
    # set_as_homescreen = "確定要更改主屏幕嗎？"
    # replace_homescreen = "確定要替換主屏幕嗎？這將會刪除最早上傳的壁紙。"
    # confirm_replace_wallpaper = "確定要替換主屏幕的壁紙嗎？"
    # get_next_u2f_counter = "確定要獲取下一個U2F計數器嗎？"
    # set_u2f_counter_x = "確定要設定U2F計數器為 {} 嗎？"
    # confirm_entropy = "確定要導出熵嗎？繼續操作之前請明白你在做什麼！"
    # bandwidth = "頻寬"
    # energy = "能量"
    # sender = "傳送者"
    # recipient = "接收者"
    # resource = "資源"
    # frozen_balance = "凍結的金額"
    # unfrozen_balance = "解凍的金額"
    # delegated_balance = "委託的金額"
    # undelegated_balance = "撤銷委託的金額"
    # you_are_freezing = "你正在凍結資產"
    # you_are_unfreezing = "你正在解凍資產"
    # you_are_delegating = "你正在委託資產"
    # you_are_undelegating = "你正在撤銷委託"
    # duration = "持續時間"
    # lock = "鎖定"
    # unlock = "解鎖"
    # all = "全部"
    # source = "來源"
    # tip = "提示"
    # keep_alive = "Keep alive"
    # # invalid_ur = "不支援的二維碼類型，請重試"
    # # sequence_number = "序號"
    # # expiration_time = "過期時間"
    # # argument_x = "參數 #{}"
    low_power_message = "电量剩余 {}%\n请充电"
    collect_nft = "你确定要收集此 NFT 吗？"
    replace_nft = "你想要收集此 NFT 吗？你已达到存储上限，这将移除最早上传的 NFT。"
    verify_device = "你确定要使用 DigitShield 服务器验证你的设备吗？点击确认以检查你的设备是否为原装且未被篡改。"
    update_bootloader = "你想更新引导加载程序吗？"
    update_resource = "你想更新设备资源吗？"
    # need_input_tips = "請輸入完成所有助記詞以後再點擊下一步"
    # need_select_tips = "請按助記詞順序點擊選擇完成以後再點擊下一步"
    # return_check_mnemonic = "查看助記詞"

# class Tip:
#     swipe_down_to_close = "向下滑動以關閉"
class Button:
    done = "完成"
    ok = "好的"
    confirm = "确认"
    reject = "拒绝"
    next = "下一步"
    cancel = "取消"
    redo = "重新生成"
    continue_ = "继续"
    try_again = "重试"
    power_off = "关机"
    hold_to_power_off = "滑动关机"
    restart = "重新启动"
    hold = "按住"
    address = "地址"
    qr_code = "二维码"
    view_detail = "查看详情"
    hold_to_sign = "滑动签名"
    hold_to_wipe = "滑动抹掉"
    receive = "收款地址"
    airgap = "Airgap"
    sign = "签名"
    verify = "验证"
    view_full_array = "查看完整数组"
    view_full_struct = "查看完整结构"
    view_full_message = "查看完整消息"
    view_data = "查看数据"
    view_more = "查看更多"
    update = "更新"
# class WalletSecurity:
#     header = "在一張紙上寫下您的助記詞並將其存放在安全的地方"
#     tips = [
#         {
#             "level": "info",
#             "msgs": [
#                 "#00001F 助記詞需要安全存放#",
#                 "#18794E * 存放在銀行金庫中#",
#                 "#18794E * 存放在保險箱中#",
#                 "#18794E * 存放在多個秘密地點#",
#             ]
#         },
#         {
#             "level": "warning",
#             "msgs": [
#                 "#00001F 一定要注意#",
#                 "#CD2B31 * 謹記保存的助記詞#",
#                 "#CD2B31 * 不要丟失#",
#                 "#CD2B31 * 不要告訴別人#",
#                 "#CD2B31 * 不要存儲在網路上#",
#                 "#CD2B31 * 不要存儲在電腦上#",
#             ]
#         },
#     ]

class MnemonicSecurity:
    header = "助记词用于保管和恢复钱包资产，关乎资产安全和使用权限，备份时需注意："

    tips = [
        "操作时确认环境安全，无他人窥视或摄像设备。",
        "按短语顺序备份助记词，严禁与任何人分享。",
        "选择安全场所离线保存，勿用使用电子形式备份，切勿上传网路。",
    ]

class PinSecurity:
    # 定义类属性header，用于描述PIN码的作用和使用提示
    header = "PIN码是访问设备的授权密码，使用时请遵循以下规范："
    # 定义类属性tips，用于存储PIN码使用的具体提示信息
    tips = [
        "设定或输入时，请确认周围无人窥视或摄影设备监控。",  # 提示1：设置或输入PIN码时请检查环境安全，确保没有旁观者或摄像头
        "设定 4 - 16 位高强度码，切勿使用连续或重复数字（如1234、1111）。",
        "PIN码重试上限为10次，累计错误10次，设备将重置。",
        "请妥善保管PIN码，切勿向任何第三人透露。",
    ]
class DownloadDigital:
    #header = "請下載並安裝DigitShield以進行裝置驗證"
    tips = [
        "1. 点击“连接硬件钱包”",
        "2. 连接设备：",
        "3. 稍等一会，DigitalShield App 将恢复您曾经使用过的账户。",
    ]
# class Solana:
#     ata_reciver = "接收者(關聯代幣帳戶)"
#     ata_sender = "發送者(關聯代幣帳戶)"
#     source_owner = "交易簽署者"
#     fee_payer = "手續費支付者"    