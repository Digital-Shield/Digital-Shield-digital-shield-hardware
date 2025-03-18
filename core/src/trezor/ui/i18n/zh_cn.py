class App:
    account = "账户"
    scan = "扫描交易"
    nft = "NFT 陈列室"
    guide = "使用说明"
    security = "安全"
    setting = "设置"


#### Setting App
class Setting:
    bluetooth = "蓝牙"
    language = "语言"
    vibration = "触摸反馈"
    brightness = "屏幕亮度"
    auto_lock = "自动锁定"
    auto_shutdown = "自动关机"
    animation = "过场动画"
    wallpaper = "壁纸"
    power_off = "关机"
    restart = "重新启动"

#### Security App
class Security:
    change_pin = "更改PIN码"
    backup_mnemonic = "备份助记词"
    check_mnemonic = "检查助记词"
    wipe_device = "抹掉设备"

#### guide App
class Guide:
    about = "关于Digit Shield"
    terms_of_use = '使用条款'
    device_info = '设备信息'
    firmware_update = '固件升级'
    terms_title_terms_us = 'Digit Shield使用条款'
    terms_describe_terms_us = '要访问使用条款的完整版本，请访问以下具体链接:\n http://digitshield.com/terms'

    terms_title_product_services = 'Digit Shield产品和服务'
    terms_describe_product_services = '我们的硬件钱包安全的管理加密货币'
    terms_title_risks = '风险'
    terms_describe_risks = '请注意与加密货币和技术漏洞相关的风险.'
    terms_title_disclaimers = '免责声明'
    terms_describe_disclaimers = '提供的信息不是财务建议。在做出任何决定前，请寻求专业建议。'
    terms_title_contact_us = '联系我们'
    terms_describe_contact_us = '如果您有任何疑问或疑虑，请给我们发送电子邮件至support@digitshield.com'
    device_label = "设备名称"
    device_title_firmware_version = '固件版本'
    device_title_serial_number = '序列号'
    bluetooth_name = "蓝牙名称"
    bluetooth_version = "蓝牙版本"
    firmware_title_1 = '1.请确保设备电量高于20%'
    firmware_title_2 = '2.使用USB-C线将设备链接至计算机'
    firmware_title_3 = '3.单击“固件升级”'
    firmware_title_caution = '警告'
    firmware_describe_caution = '升级中，请确保USB链接'

class Nft:
    nft_item ="{} item"
    nft_items ="{} items"
class Title:
    enter_old_pin = "请输入旧PIN码"
    enter_new_pin = "请输入新PIN码"
    enter_pin = "请输入PIN码"
    enter_pin_again = "请再次输入PIN码"
    select_language = "语言"
    create_wallet = "创建钱包"
    restore_wallet = "恢复钱包"
    wallet_is_ready = "钱包准备就绪"
    select_word_count = "选择单词数量"
    wallet_security = "钱包安全"
    pin_security = "PIN 安全提示"
    mnemonic_security = "助记词安全提示"
    backup_mnemonic = "备份助记词"
    enter_mnemonic = "请输入助记词"
    check_mnemonic = "检查助记词"
    success = "成功"
    warning = "警告"
    error = "错误"
    verified = "助记词备份完成"
    invalid_mnemonic = "无效的助记词"
    pin_not_match = "PIN 不匹配"
    check_recovery_mnemonic = "检查恢复助记词"
    mnemonic_not_match = "助记词不匹配"
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
    pin_changed = "PIN已修改"
    pin_enabled = "PIN已启用"
    pin_disabled = "PIN已禁用"
    unknown_token = "未知代币"
    view_data = "查看数据"
    sign_message = "{} 消息签名"
    verify_message = "{} 消息验签"
    typed_data = "{} 结构化数据"
    typed_hash = "{} 结构化哈希"
    system_update = "系统升级"
    entering_boardloader = "Entering Boardloader"
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
    fee_is_high = "手续费过高"
    confirm_locktime = "确认锁定时间"
    view_transaction = "查看交易"
    x_confirm_payment = "{} 确认付款"
    confirm_replacement = "确认替换交易"
    x_transaction = "{} 交易"
    x_joint_transaction = "{} 联合交易"
    change_label = "修改设备名称"
    enable_passphrase = "启用 Passphrase"
    disable_passphrase = "禁用 Passphrase"
    passphrase_source = "Passphrase 输入设置"
    enable_safety_checks ="启用安全检查"
    disable_safety_checks ="禁用安全检查"
    experiment_mode = "实验模式"
    set_as_homescreen = "设置为主屏幕"
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
    invalid_data="无效的数据格式"

class Text:
    # tap_to_unlock = "Tap to unlock"
    tap_to_unlock = "点击以解锁"
    unlocking = "正在解锁设备..."
    str_words = "#18794E {}# 个单词"
    backup_manual = "手动写下助记词并存放在安全的地方"
    check_manual = "按顺序依次点击下面的单词"
    backup_verified = "您已完成助记词的备份，请妥善保存,不要与任何人分享"
    backup_invalid = "您输入的助记词不正确,请检查备份的助记词，再次尝试"
    pin_not_match = "您输入的PIN码不正确，请再次尝试"
    please_wait = "请稍等"
    wiping_device = "正在清除设备数据..."
    create_wallet = "生成一组新的助记词，创建新钱包"
    restore_wallet = "从您备份的助记词恢复钱包"
    restore_mnemonic_match = "您的助记词匹配，您的助记词备份正确"
    restore_success = "恢复钱包成功"
    create_success = "您的助记词已成功备份，钱包已创建"
    check_recovery_mnemonic = "请检查您的助记词，确认是否完全匹配"
    invalid_recovery_mnemonic = "您输入的助记词无效，请检查您的助记词，再次尝试"
    check_recovery_not_match = "您输入的助记词是有效的，但是和设备中的助记词不匹配"
    shutting_down = "正在关机..."
    restarting = "正在重新启动..."
    never = "从不"
    second = "秒"
    seconds = "秒"
    minute = "分钟"
    minutes = "分钟"
    changing_language = "您正在更改语言\n应用此设置将重新启动设备"
    change_pin = "设置一个长度为4~16位的PIN码，保护您的设备"
    wipe_device = "将设备恢复到出厂状态。\n警告： 这将从您的设备中抹掉所有数据。"
    wipe_device_check = [
        "抹掉设备会清除所有数据",
        "数据将无法恢复",
        "已经备份了助记词",
    ]
    wipe_device_success = "设备已成功清除数据\n 正在重启设备 ..."
    bluetooth_pair = "请在您的设备上输入配对码"
    bluetooth_pair_failed = "蓝牙配对失败"
    path = "派生路经:"
    chain_id = "Chain ID:"
    send = "发送"
    to = "至"
    amount = "金额"
    from_ = "发送者"
    receiver = "接收者"
    fee = "手续费"
    max_fee = "最大手续费"
    max_priority_fee_per_gas = "最大优先级手续费"
    max_fee_per_gas = "单位Gas的交易费上限"
    max_gas_limit = "最大Gas上限"
    gas_unit_price= "单位Gas价格"
    gas_price = "燃料价格"
    total = "总金额"
    do_sign_this_transaction = "是否签名这笔{}交易"
    transaction_signed = "交易已签名"
    address = '地址:'
    public_key = "公钥:"
    xpub = "XPub:"
    unknown_tx_type = "未知交易类型, 请检查输入数据"
    unknown_function = "未知的函数"
    use_app_scan_this_signature = "请使用钱包 APP 扫描签名结果"
    internal_error = "内部错误"
    tap_switch_to_airgap = "点击二维码切换为展示Airgap地址"
    tap_switch_to_receive = "点击二维码切换为展示钱包收款地址"
    incorrect_pin_times_left = "PIN不正确, 剩余 {} 次重试机会"
    incorrect_pin_last_time = "PIN不正确, 还有最后一次机会"
    wrong_pin = "输入的PIN码不正确"
    seedless = "缺少种子"
    backup_failed = "备份失败！"
    need_backup = "需要备份！"
    pin_not_set = "没有设置PIN！"
    experimental_mode = "实验模式"
    pin_change_success = "PIN码已成功更改"
    pin_enable_success = "PIN码已成功启用"
    pin_disable_success = "PIN码已成功禁用"
    contract = "合约:"
    new_contract = "新合约?"
    bytes_ = "{} 字节"
    message = "消息:"
    no_message = "不包含消息"
    contains_x_key = "包含 {} 键"
    array_of_x_type = "数组类型 {} {}"
    do_sign_712_typed_data = "是否签署这笔结构化数据交易？"
    do_sign_typed_hash = "是否签署这笔结构化哈希交易？"
    domain_hash = "Domain 哈希:"
    message_hash = "消息 哈希:"
    switch_to_update_mode = "切换到更新模式"
    switch_to_boardloader = "Switch to board loader mode"
    list_credentials = "是否要导出有关存储在此设备上的凭证信息？"
    coinjoin_at_x = "是否要参加下面的Coinjoin交易:\n{}"
    signature_is_valid = "签名有效"
    signature_is_invalid = "签名无效"
    u2f_already_registered = "U2F 已经注册"
    u2f_not_registered = "U2F 未注册"
    fido2_already_registered_x = "FIDO2 已注册 {}"
    fido2_verify_user = "FIDO2 验证用户"
    device_already_registered_x = "设备已注册 {}"
    device_verify_user = "设备验证用户"
    finalize_transaction = "完成交易"
    meld_transaction = "融合交易"
    update_transaction = "更新交易"
    fee_is_unexpectedly_high = "手续费过高"
    change_count = "找零数量"
    locktime_will_have_no_effect = "锁定时间将不会有影响"
    confirm_locktime_for_this_transaction = "确认交易的锁定时间"
    block_height = "区块高度"
    time = "时间"
    amount_increased = "金额增加"
    amount_decreased = "金额减少"
    fee_unchanged = "手续费未改变"
    fee_increased = "手续费增加"
    fee_decreased = "手续费减少"
    your_spend = "你的花费"
    change_label_to_x = "修改标签为 {}"
    enable_passphrase = "要启用 Passphrase 加密吗？"
    disable_passphrase = "要禁用 Passphrase 加密吗？"
    enable_passphrase_always = "总是在本机输入 Passphrase 吗？"
    revoke_enable_passphrase_always = "要撤销总是在本机输入 Passphrase 的设置吗？"
    auto_lock_x = "确定要在 {} 之后自动锁定设备吗？"
    enable_safety_checks = "要执行严格的安全检查吗？这将提供更全面的安全保护。"
    disable_safety_checks = "确定要禁用安全检查吗？继续操作前，请知悉该行为的潜在安全风险。"
    enable_experiment_mode = "是否启用实验模式？"
    set_as_homescreen = "确定要更改主屏幕吗？"
    replace_homescreen = "确定要替换主屏幕吗？这将会删除最早上传的壁纸。"
    get_next_u2f_counter = "确定要获取下一个U2F计数器吗？"
    set_u2f_counter_x = "确定要设置U2F计数器为 {} 吗？"
    confirm_entropy = "确定要导出熵吗？继续操作之前请明白你在做什么！"
    bandwidth = "带宽"
    energy = "能量"
    sender = "发送者"
    recipient = "接收者"
    resource = "资源"
    frozen_balance = "冻结的金额"
    unfrozen_balance = "解冻的金额"
    delegated_balance = "委托的金额"
    undelegated_balance = "撤销委托的金额"
    you_are_freezing = "你正在冻结资产"
    you_are_unfreezing = "你正在解冻资产"
    you_are_delegating = "你正在委托资产"
    you_are_undelegating = "你正在撤销委托"
    duration = "持续时间"
    lock = "锁定"
    unlock = "解锁"
    all = "全部"
    source = "来源"
    tip = "提示"
    keep_alive = "Keep alive"
    invalid_ur = "不支持的二维码类型，请重试"
    sequence_number = "序列号"
    expiration_time = "过期时间"
    argument_x = "参数 #{}"

class Tip:
    swipe_down_to_close = "向下滑动以关闭"
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
    restart = "重新启动"
    hold = "按住"
    address = "地址"
    qr_code = "二维码"
    view_detail = "查看详情"
    hold_to_sign = "长按签名"
    hold_to_wipe = "长按抹掉"
    receive = "收款地址"
    airgap = "Airgap"
    sign = "签名"
    verify = "验证"
    view_full_array = "查看完整数组"
    view_full_struct = "查看完整结构"
    view_full_message = "查看完整消息"
    view_data = "查看数据"
    view_more = "查看更多"
class WalletSecurity:
    header = "在一张纸上写下您的助记词并将其存放在安全的地方"
    tips = [
        {
            "level": "info",
            "msgs": [
                "#00001F 助记词需要安全存放#",
                "#18794E * 存放在银行金库中#",
                "#18794E * 存放在保险箱中#",
                "#18794E * 存放在多个秘密地点#",
            ]
        },
        {
            "level": "warning",
            "msgs": [
                "#00001F 一定要注意#",
                "#CD2B31 * 谨记保存的助记词#",
                "#CD2B31 * 不要丢失#",
                "#CD2B31 * 不要告诉别人#",
                "#CD2B31 * 不要存储在网络上#",
                "#CD2B31 * 不要存储在计算机上#",
            ]
        },
    ]

class MnemonicSecurity:
    header = "助记词是一组用来恢复钱包资产的短语，拥有助记词就意味着可以使用您的资产，请妥善保管"

    tips = [
        "1. 请检查环境安全，确保没有旁观者或摄像头",
        "2. 请按短语的正确顺序备份助记词，切勿与任何人分享您的助记词",
        "3. 请在安全的地方离线保存助记词，切勿使用电子方式备份助记词，切勿上传网络",
    ]

class PinSecurity:
    header = "PIN码是设备访问的密码,用于授权访问当前设备。请按照以下提示正确使用PIN码"
    tips = [
        "1. 设置或录入PIN时请检查环境安全，确保没有旁观者或摄像头",
        "2. 请设置长度为4-16位的高强度的IN码，避免使用连续或重复的数字",
        "3. PIN码的最大重试次数为10次，当错误10次后设备将会被重置",
        "4. 请妥善保管PIN码，不要和任何人分享您的PIN码",
    ]

class Solana:
    ata_reciver = "接收者(关联代币账户)"
    ata_sender = "发送者(关联代币账户)"
    source_owner = "交易签名者"
    fee_payer = "手续费支付者"
