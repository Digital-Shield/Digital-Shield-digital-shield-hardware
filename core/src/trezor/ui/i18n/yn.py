class App:
    account = "Tài khoản"
    scan = "Quét giao dịch"
    nft = "Phòng trưng bày NFT"
    guide = "Hướng dẫn sử dụng"
    security = "Bảo mật"
    setting = "Cài đặt"


#### Setting App
class Setting:
    bluetooth = "Bluetooth"
    language = "Ngôn ngữ"
    vibration = "Phản hồi chạm"
    brightness = "Độ sáng màn hình"
    auto_lock = "Khóa tự động"
    auto_shutdown = "Tắt máy tự động"
    animation = "Hoạt hình chuyển đổi"
    wallpaper = "Hình nền"
    power_off = "Tắt máy"
    restart = "Khởi động lại"

#### Security App
class Security:
    change_pin = "Thay đổi mã PIN"
    backup_mnemonic = "Sao lưu cụm từ ghi nhớ"
    check_mnemonic = "Kiểm tra cụm từ ghi nhớ"
    wipe_device = "Xóa sạch thiết bị"

#### guide App
class Guide:
    about = "Giới thiệu về Digit Shield"
    terms_of_use = 'Điều khoản sử dụng'
    device_info = 'Thông tin thiết bị'
    firmware_update = 'Cập nhật phần mềm'
    terms_title_terms_us = 'Điều khoản sử dụng Digit Shield'
    terms_describe_terms_us = 'Để truy cập bản đầy đủ các điều khoản sử dụng, vui lòng truy cập liên kết sau:\n http://digitshield.com/terms'

    terms_title_product_services = 'Sản phẩm và dịch vụ của Digit Shield'
    terms_describe_product_services = 'Ví phần cứng của chúng tôi quản lý tiền mã hóa một cách an toàn'
    terms_title_risks = 'Rủi ro'
    terms_describe_risks = 'Vui lòng lưu ý các rủi ro liên quan đến tiền mã hóa và các lỗ hổng kỹ thuật.'
    terms_title_disclaimers = 'Miễn trừ trách nhiệm'
    terms_describe_disclaimers = 'Thông tin được cung cấp không phải là tư vấn tài chính. Vui lòng tìm kiếm lời khuyên chuyên nghiệp trước khi đưa ra bất kỳ quyết định nào.'
    terms_title_contact_us = 'Liên hệ chúng tôi'
    terms_describe_contact_us = 'Nếu bạn có bất kỳ câu hỏi hoặc mối quan tâm nào, vui lòng gửi email tới support@digitshield.com'
    device_label = "Tên thiết bị"
    device_title_firmware_version = 'Phiên bản phần mềm'
    device_title_serial_number = 'Số sê-ri'
    bluetooth_name = "Tên Bluetooth"
    bluetooth_version = "Phiên bản Bluetooth"
    firmware_title_1 = '1. Vui lòng đảm bảo rằng pin thiết bị trên 20%'
    firmware_title_2 = '2. Kết nối thiết bị với máy tính bằng cáp USB-C'
    firmware_title_3 = '3. Nhấp vào "Cập nhật phần mềm"'
    firmware_title_caution = 'Cảnh báo'
    firmware_describe_caution = 'Trong quá trình cập nhật, vui lòng đảm bảo kết nối USB ổn định'

class Nft:
    nft_item ="{} mục"
    nft_items ="{} mục"
class Title:
    enter_old_pin = "Vui lòng nhập mã PIN cũ"
    enter_new_pin = "Vui lòng nhập mã PIN mới"
    enter_pin = "Vui lòng nhập mã PIN"
    enter_pin_again = "Vui lòng nhập lại mã PIN"
    select_language = "Chọn ngôn ngữ"
    create_wallet = "Tạo ví"
    wallet = "Ví tiền"
    import_wallet = "Ví nhập khẩu"
    restore_wallet = "Phục hồi ví"
    wallet_is_ready = "Ví đã sẵn sàng"
    select_word_count = "Chọn số lượng từ"
    wallet_security = "Bảo mật ví"
    pin_security = "Mẹo bảo mật mã PIN"
    mnemonic_security = "Mẹo bảo mật cụm từ ghi nhớ"
    backup_mnemonic = "Sao lưu cụm từ ghi nhớ"
    enter_mnemonic = "Vui lòng nhập cụm từ ghi nhớ"
    check_mnemonic = "Kiểm tra cụm từ ghi nhớ"
    success = "Thành công"
    warning = "Cảnh báo"
    error = "Lỗi"
    verified = "Đã sao lưu cụm từ ghi nhớ"
    invalid_mnemonic = "Cụm từ ghi nhớ không hợp lệ"
    pin_not_match = "Mã PIN không khớp"
    check_recovery_mnemonic = "Kiểm tra cụm từ ghi nhớ phục hồi"
    mnemonic_not_match = "Cụm từ ghi nhớ không khớp"
    power_off = "Tắt máy"
    restart = "Khởi động lại"
    change_language = "Thay đổi ngôn ngữ"
    wipe_device = "Xóa sạch thiết bị"
    bluetooth_pairing = "Kết nối Bluetooth"
    address="{} Địa chỉ"
    public_key = "{} Khóa công khai"
    xpub = "{} XPub"
    transaction = "{} Giao dịch"
    transaction_detail = "Chi tiết giao dịch"
    confirm_transaction = "Xác nhận giao dịch"
    confirm_message = "Xác nhận tin nhắn"
    signature = "Kết quả ký"
    wrong_pin = "Mã PIN sai"
    pin_changed = "Mã PIN đã thay đổi"
    pin_enabled = "Mã PIN đã bật"
    pin_disabled = "Mã PIN đã tắt"
    unknown_token = "Mã thông báo không xác định"
    view_data = "Xem dữ liệu"
    sign_message = "{} Ký tin nhắn"
    verify_message = "{} Xác minh tin nhắn"
    typed_data = "{} Dữ liệu có cấu trúc"
    typed_hash = "{} Hash có cấu trúc"
    system_update = "Cập nhật hệ thống"
    entering_boardloader = "Vào Boardloader"
    remove_credential = "Xóa thông tin xác thực"
    list_credentials = "Liệt kê thông tin xác thực"
    authorize_coinjoin = "Ủy quyền CoinJoin"
    multisig_address_m_of_n = "{} Địa chỉ đa chữ ký\n({} of {})"
    u2f_register = "Đăng ký U2F"
    u2f_unregister = "Hủy đăng ký U2F"
    u2f_authenticate = "Xác thực U2F"
    fido2_register = "Đăng ký FIDO2"
    fido2_unregister = "Hủy đăng ký FIDO2"
    fido2_authenticate = "Xác thực FIDO2"
    fee_is_high = "Phí quá cao"
    confirm_locktime = "Xác nhận thời gian khóa"
    view_transaction = "Xem giao dịch"
    x_confirm_payment = "{} Xác nhận thanh toán"
    confirm_replacement = "Xác nhận thay thế giao dịch"
    x_transaction = "{} Giao dịch"
    x_joint_transaction = "{} Giao dịch chung"
    change_label = "Thay đổi tên thiết bị"
    enable_passphrase = "Bật mật khẩu"
    disable_passphrase = "Tắt mật khẩu"
    passphrase_source = "Cài đặt nhập mật khẩu"
    enable_safety_checks ="Bật kiểm tra an toàn"
    disable_safety_checks ="Tắt kiểm tra an toàn"
    experiment_mode = "Chế độ thử nghiệm"
    set_as_homescreen = "Đặt làm màn hình chính"
    get_next_u2f_counter = "Lấy bộ đếm U2F tiếp theo"
    set_u2f_counter = "Đặt bộ đếm U2F"
    encrypt_value = "Mã hóa dữ liệu"
    decrypt_value = "Giải mã dữ liệu"
    confirm_entropy = "Xuất entropy"
    memo = "Ghi chú"
    import_credential = "Nhập thông tin xác thực"
    export_credential = "Xuất thông tin xác thực"
    asset = "Tài sản"
    unimplemented = "Chưa thực hiện"
    invalid_data="Định dạng dữ liệu không hợp lệ"
    low_power = "Pin thấp"


class Text:
    # tap_to_unlock = "Tap to unlock"
    tap_to_unlock = "Nhấn để mở khóa"
    unlocking = "Đang mở khóa thiết bị..."
    # str_words = "#18794E {}# từ"
    str_words = "#FFFFFF {}# từ"
    backup_manual = "Viết cụm từ ghi nhớ ra giấy và lưu ở nơi an toàn"
    check_manual = "Nhấn vào các từ dưới đây theo thứ tự"
    backup_verified = "Bạn đã sao lưu cụm từ ghi nhớ, vui lòng lưu giữ cẩn thận, đừng chia sẻ với bất kỳ ai"
    backup_invalid = "Cụm từ ghi nhớ bạn nhập không chính xác, vui lòng kiểm tra cụm từ ghi nhớ đã sao lưu và thử lại"
    pin_not_match = "Mã PIN bạn nhập không chính xác, vui lòng thử lại"
    please_wait = "Vui lòng đợi"
    wiping_device = "Đang xóa sạch dữ liệu thiết bị..."
    create_wallet = "Tạo một ví mới bằng cách sinh một cụm từ ghi nhớ mới"
    restore_wallet = "Phục hồi ví từ cụm từ ghi nhớ đã sao lưu"
    restore_mnemonic_match = "Cụm từ ghi nhớ khớp, bản sao lưu cụm từ ghi nhớ chính xác"
    restore_success = "Phục hồi ví thành công"
    create_success = "Cụm từ ghi nhớ đã được sao lưu thành công, ví đã được tạo"
    check_recovery_mnemonic = "Vui lòng kiểm tra cụm từ ghi nhớ, xác nhận xem chúng có khớp hoàn toàn không"
    invalid_recovery_mnemonic = "Cụm từ ghi nhớ bạn nhập không hợp lệ, vui lòng kiểm tra cụm từ ghi nhớ và thử lại"
    check_recovery_not_match = "Cụm từ ghi nhớ bạn nhập là hợp lệ, nhưng không khớp với cụm từ ghi nhớ trong thiết bị"
    shutting_down = "Đang tắt máy..."
    restarting = "Đang khởi động lại..."
    never = "Không bao giờ"
    second = "giây"
    seconds = "giây"
    minute = "phút"
    minutes = "phút"
    changing_language = "Bạn đang thay đổi ngôn ngữ\nÁp dụng cài đặt này sẽ khởi động lại thiết bị"
    change_pin = "Đặt mã PIN dài từ 4~16 chữ số để bảo vệ thiết bị của bạn"
    wipe_device = "Khôi phục thiết bị về trạng thái gốc.\nCảnh báo: Điều này sẽ xóa tất cả dữ liệu trên thiết bị của bạn."
    wipe_device_check = [
        "Xóa sạch thiết bị sẽ xóa tất cả dữ liệu",
        "Không thể khôi phục dữ liệu",
        "Bạn đã sao lưu cụm từ ghi nhớ",
    ]
    wipe_device_success = "Dữ liệu thiết bị đã được xóa sạch thành công\n Đang khởi động lại thiết bị ..."
    bluetooth_pair = "Vui lòng nhập mã ghép nối trên thiết bị của bạn"
    bluetooth_pair_failed = "Ghép nối Bluetooth thất bại"
    path = "Đường dẫn phân cấp:"
    chain_id = "Chain ID:"
    send = "Gửi"
    to = "Tới"
    amount = "Số tiền"
    from_ = "Người gửi"
    receiver = "Người nhận"
    fee = "Phí"
    max_fee = "Phí tối đa"
    max_priority_fee_per_gas = "Phí ưu tiên tối đa mỗi gas"
    max_fee_per_gas = "Phí giao dịch tối đa mỗi gas"
    gas_price = "Giá gas"
    total = "Tổng cộng"
    do_sign_this_transaction = "Bạn có muốn ký giao dịch này {} không?"
    transaction_signed = "Giao dịch đã được ký"
    address = 'Địa chỉ:'
    public_key = "Khóa công khai:"
    xpub = "XPub:"
    unknown_tx_type = "Loại giao dịch không xác định, vui lòng kiểm tra dữ liệu nhập"
    use_app_scan_this_signature = "Vui lòng sử dụng ứng dụng ví để quét kết quả ký"
    internal_error = "Lỗi nội bộ"
    tap_switch_to_airgap = "Nhấn vào mã QR để chuyển sang hiển thị địa chỉ Airgap"
    tap_switch_to_receive = "Nhấn vào mã QR để chuyển sang hiển thị địa chỉ nhận tiền ví"
    incorrect_pin_times_left = "Mã PIN không chính xác, số lần thử còn lại {}"
    incorrect_pin_last_time = "Mã PIN không chính xác, đây là lần thử cuối cùng"
    wrong_pin = "Mã PIN bạn nhập không chính xác"
    seedless = "Thiếu hạt giống"
    backup_failed = "Sao lưu thất bại!"
    need_backup = "Cần sao lưu!"
    pin_not_set = "Chưa đặt mã PIN!"
    experimental_mode = "Chế độ thử nghiệm"
    pin_change_success = "Mã PIN đã thay đổi thành công"
    pin_enable_success = "Mã PIN đã bật thành công"
    pin_disable_success = "Mã PIN đã tắt thành công"
    contract = "Hợp đồng:"
    new_contract = "Hợp đồng mới?"
    bytes_ = "{} byte"
    message = "Tin nhắn:"
    no_message = "Không bao gồm tin nhắn"
    contains_x_key = "Bao gồm phím {}"
    array_of_x_type = "Kiểu mảng {} {}"
    do_sign_712_typed_data = "Bạn có muốn ký giao dịch dữ liệu có cấu trúc này không?"
    do_sign_typed_hash = "Bạn có muốn ký giao dịch hash có cấu trúc này không?"
    domain_hash = "Domain hash:"
    message_hash = "Message hash:"
    switch_to_update_mode = "Chuyển sang chế độ cập nhật"
    switch_to_boardloader = "Chuyển sang chế độ Boardloader"
    list_credentials = "Bạn có muốn xuất thông tin xác thực được lưu trữ trên thiết bị này không?"
    coinjoin_at_x = "Bạn có muốn tham gia giao dịch Coinjoin sau đây không?:\n{}"
    signature_is_valid = "Chữ ký hợp lệ"
    signature_is_invalid = "Chữ ký không hợp lệ"
    u2f_already_registered = "U2F đã đăng ký"
    u2f_not_registered = "U2F chưa đăng ký"
    fido2_already_registered_x = "FIDO2 đã đăng ký {}"
    fido2_verify_user = "Xác minh người dùng FIDO2"
    device_already_registered_x = "Thiết bị đã đăng ký {}"
    device_verify_user = "Xác minh người dùng trên thiết bị"
    finalize_transaction = "Hoàn tất giao dịch"
    meld_transaction = "Hợp nhất giao dịch"
    update_transaction = "Cập nhật giao dịch"
    fee_is_unexpectedly_high = "Phí bất ngờ cao"
    change_count = "Số lượng thay đổi"
    locktime_will_have_no_effect = "Thời gian khóa sẽ không có tác dụng"
    confirm_locktime_for_this_transaction = "Xác nhận thời gian khóa cho giao dịch này"
    block_height = "Chiều cao khối"
    time = "Thời gian"
    amount_increased = "Số tiền tăng"
    amount_decreased = "Số tiền giảm"
    fee_unchanged = "Phí không thay đổi"
    fee_increased = "Phí tăng"
    fee_decreased = "Phí giảm"
    your_spend = "Bạn đã chi"
    change_label_to_x = "Thay đổi nhãn thành {}"
    enable_passphrase = "Bạn có muốn bật mật khẩu không?"
    disable_passphrase = "Bạn có muốn tắt mật khẩu không?"
    enable_passphrase_always = "Bạn có muốn luôn nhập mật khẩu trên thiết bị này không?"
    revoke_enable_passphrase_always = "Bạn có muốn thu hồi cài đặt luôn nhập mật khẩu trên thiết bị này không?"
    auto_lock_x = "Bạn có muốn tự động khóa thiết bị sau {} không?"
    enable_safety_checks = "Bạn có muốn thực hiện kiểm tra an toàn nghiêm ngặt không? Điều này sẽ cung cấp bảo vệ an toàn toàn diện hơn."
    disable_safety_checks = "Bạn có muốn tắt kiểm tra an toàn không? Trước khi tiếp tục, vui lòng biết rủi ro tiềm ẩn liên quan đến hành vi này."
    enable_experiment_mode = "Bạn có muốn bật chế độ thử nghiệm không?"
    set_as_homescreen = "Bạn có muốn thay đổi màn hình chính không?"
    replace_homescreen = "Bạn có muốn thay thế màn hình chính không? Điều này sẽ xóa hình nền được tải lên đầu tiên."
    get_next_u2f_counter = "Bạn có muốn lấy bộ đếm U2F tiếp theo không?"
    set_u2f_counter_x = "Bạn có muốn đặt bộ đếm U2F thành {} không?"
    confirm_entropy = "Bạn có muốn xuất entropy không? Trước khi tiếp tục, vui lòng biết bạn đang làm gì!"
    bandwidth = "Băng thông"
    energy = "Năng lượng"
    sender = "Người gửi"
    recipient = "Người nhận"
    resource = "Tài nguyên"
    frozen_balance = "Số dư bị đóng băng"
    unfrozen_balance = "Số dư không bị đóng băng"
    delegated_balance = "Số dư được ủy quyền"
    undelegated_balance = "Số dư không được ủy quyền"
    you_are_freezing = "Bạn đang đóng băng tài sản"
    you_are_unfreezing = "Bạn đang bỏ đóng băng tài sản"
    you_are_delegating = "Bạn đang ủy quyền tài sản"
    you_are_undelegating = "Bạn đang bỏ ủy quyền tài sản"
    duration = "Thời lượng"
    lock = "Khóa"
    unlock = "Mở khóa"
    all = "Tất cả"
    source = "Nguồn"
    tip = "Gợi ý"
    keep_alive = "Giữ hoạt động"
    invalid_ur = "Loại mã QR không được hỗ trợ, vui lòng thử lại"
    sequence_number = "Số thứ tự"
    expiration_time = "Thời gian hết hạn"
    argument_x = "Tham số #{}"
    low_power_message = "Pin còn {}%\nVui lòng sạc"

class Tip:
    swipe_down_to_close = "Vuốt xuống để đóng"

class Button:
    done = "Xong"
    ok = "OK"
    confirm = "Xác nhận"
    reject = "Từ chối"
    next = "Tiếp"
    cancel = "Hủy"
    redo = "Làm lại"
    continue_ = "Tiếp tục"
    try_again = "Thử lại"
    power_off = "Tắt máy"
    restart = "Khởi động lại"
    hold = "Giữ"
    address = "Địa chỉ"
    qr_code = "Mã QR"
    view_detail = "Xem chi tiết"
    hold_to_sign = "Giữ để ký"
    hold_to_wipe = "Giữ để xóa"
    receive = "Địa chỉ nhận"
    airgap = "Airgap"
    sign = "Ký"
    verify = "Xác minh"
    view_full_array = "Xem mảng đầy đủ"
    view_full_struct = "Xem cấu trúc đầy đủ"
    view_full_message = "Xem tin nhắn đầy đủ"
    view_data = "Xem dữ liệu"
    view_more = "Xem thêm"

class WalletSecurity:
    header = "Viết cụm từ ghi nhớ ra giấy và lưu ở nơi an toàn"
    tips = [
        {
            "level": "info",
            "msgs": [
                "#00001F Cụm từ ghi nhớ cần được lưu trữ an toàn#",
                "#18794E * Lưu trong két an toàn ngân hàng#",
                "#18794E * Lưu trong tủ#",
                "#18794E * Lưu ở nhiều nơi bí mật#",
            ]
        },
        {
            "level": "warning",
            "msgs": [
                "#00001F Cần phải chú ý#",
                "#CD2B31 * Nhớ cụm từ ghi nhớ#",
                "#CD2B31 * Không để mất#",
                "#CD2B31 * Không chia sẻ với người khác#",
                "#CD2B31 * Không lưu trữ trực tuyến#",
                "#CD2B31 * Không lưu trữ trên máy tính#",
            ]
        },
    ]

class MnemonicSecurity:
    header = "Cụm từ ghi nhớ là một loạt các từ dùng để phục hồi tài sản ví, sở hữu cụm từ ghi nhớ có nghĩa là bạn có thể sử dụng tài sản của mình, vui lòng lưu giữ cẩn thận"

    tips = [
        "1. Vui lòng kiểm tra an toàn môi trường, đảm bảo không có người quan sát hoặc máy quay",
        "2. Vui lòng sao lưu cụm từ ghi nhớ theo thứ tự chính xác, đừng chia sẻ cụm từ ghi nhớ của bạn với bất kỳ ai",
        "3. Vui lòng lưu trữ cụm từ ghi nhớ ở nơi an toàn ngoại tuyến, đừng sao lưu cụm từ ghi nhớ bằng phương thức điện tử, đừng tải lên mạng",
    ]

class PinSecurity:
    header = "Mã PIN là mật khẩu để truy cập thiết bị, dùng để ủy quyền truy cập thiết bị hiện tại. Vui lòng sử dụng mã PIN một cách chính xác theo các mẹo sau"
    tips = [
        "1. Vui lòng kiểm tra an toàn môi trường khi đặt hoặc nhập mã PIN, đảm bảo không có người quan sát hoặc máy quay",
        "2. Vui lòng đặt mã PIN dài từ 4~16 chữ số mạnh, tránh sử dụng các chữ số liên tiếp hoặc lặp lại",
        "3. Số lần thử tối đa của mã PIN là 10 lần, khi sai 10 lần liên tiếp thiết bị sẽ được đặt lại",
        "4. Vui lòng lưu giữ mã PIN cẩn thận, đừng chia sẻ mã PIN của bạn với bất kỳ ai",
    ]

class Solana:
    ata_reciver = "Người nhận (tài khoản tiền tệ liên kết)"
    ata_sender = "Người gửi (tài khoản tiền tệ liên kết)"
    source_owner = "Người ký giao dịch"
    fee_payer = "Người trả phí"
