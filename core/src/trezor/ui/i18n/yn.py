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
    auto_lock = "Tự động khóa"
    auto_shutdown = "Tự động tắt nguồn"
    animation = "Hiệu ứng chuyển cảnh"
    wallpaper = "Hình nền"
    power_off = "Tắt máy"
    restart = "Khởi động lại"
    restart_tip = "Khởi động lại thiết bị?"

#### Security App
class Security:
    change_pin = "Thay đổi mã PIN"
    backup_mnemonic = "Sao lưu cụm từ khôi phục"
    check_mnemonic = "Kiểm tra cụm từ khôi phục"
    wipe_device = "Xóa dữ liệu thiết bị"

#### guide App
class Guide:
    about = "Về Digital Shield"
    terms_of_use = 'Điều khoản sử dụng'
    device_info = 'Thông tin thiết bị'
    firmware_update = 'Nâng cấp firmware'
    terms_title_terms_us = 'Điều khoản sử dụng Digit Shield'
    terms_describe_terms_us = 'Để xem toàn bộ điều khoản sử dụng, vui lòng truy cập liên kết sau:\n http://digitshield.com/terms'

    terms_title_product_services = 'Sản phẩm và dịch vụ Digit Shield'
    terms_describe_product_services = 'Ví cứng của chúng tôi giúp quản lý tiền mã hóa một cách an toàn'
    terms_title_risks = 'Rủi ro'
    terms_describe_risks = 'Xin luru y các rüi ro lien quan den tien ma hóa và ló hóng cóng nghê.'
    terms_title_disclaimers = 'Tuyên bố miễn trừ trách nhiệm'

    terms_describe_disclaimers = 'Thông tin cung cấp không phải là lời khuyên tài chính. Vui lòng tham khảo ý kiến chuyên gia trước khi đưa ra quyết định.'
    terms_title_contact_us = 'Liên hệ chúng tôi'
    terms_describe_contact_us = 'Nếu bạn có bất kỳ câu hỏi hoặc thắc mắc nào, vui lòng gửi email cho chúng tôi tại www.ds.pro@gmail.com'

    accept_tems = '1. Chấp nhận các điều khoản'
    use_range = '1. Phạm vi áp dụng'
    range_include = 'Các điều khoản này áp dụng cho tất cả các dịch vụ được cung cấp thông qua ví Digital Shield.'
    range_include_1 = 'Mua, kích hoạt, dịch vụ sau bán hàng của ví cứng; Tải xuống, cài đặt, sử dụng các tính năng của ứng dụng di động Digital Shield (Android/iOS/Goolg); Dịch vụ nâng cấp phần mềm (bao gồm bản vá bảo mật, bản cập nhật cải thiện tính năng); Quản lý tài sản số đa chuỗi (hỗ trợ lưu trữ và chuyển giao hơn 3000 mã token như BTC, ETH, v.v.); Hỗ trợ kỹ thuật (gỡ lỗi thiết bị, xử lý các trường hợp không khớp chữ ký giao dịch, v.v.).'
    user_qualification = '2. Đủ điều kiện sử dụng'
    ability_include = 'Bạn xác nhận rằng bạn đã đủ 18 tuổi và có đầy đủ năng lực hành vi dân sự.'
    ability_include_1 = 'Vùng pháp lý nơi bạn cư trú không cấm sử dụng tiền điện tử và các thiết bị cứng liên quan (ví dụ: người dùng Trung Quốc đại lục phải tự chịu rủi ro khi sử dụng).'
    terms_update_infor = '3. Cập nhật và thông báo các điều khoản'
    update_infor_content = 'Chúng tôi bảo lưu quyền sửa đổi các điều khoản một cách đơn phương. Nội dung sửa đổi sẽ được công bố trên bảng thông báo của trang web chính thức, ngày có hiệu lực sẽ dựa theo thông báo. Nếu bạn tiếp tục sử dụng dịch vụ, điều đó được coi là bạn chấp nhận các điều khoản đã sửa đổi; Nếu bạn không đồng ý, bạn nên thông báo bằng văn bản và ngừng sử dụng trước ngày có hiệu lực.'

    wallet_buy_iterms = '2. Các điều khoản mua ví cứng'
    order_process = '1. Quy trình đặt hàng'
    payment_confirmation = 'Sau khi thanh toán đơn hàng thành công (xác nhận bởi mạng lưới blockchain hoặc tiền vào tài khoản ngân hàng), hệ thống sẽ cập nhật trạng thái trong vòng 24 giờ.'
    inventory_shortage = 'Hết hàng: Nếu hết hàng, người dùng có thể chọn:'
    inventory_shortage_1 = 'a. Chờ hàng về (tối đa 30 ngày, tự động hoàn tiền nếu quá hạn).'
    inventory_shortage_2 = 'b. Hoàn tiền toàn bộ theo phương thức gốc (đơn hàng tiền điện tử sẽ được tính theo tỷ giá lúc thanh toán).'
    return_and_exchange_policy = '2. Chính sách đổi trả'
    return_and_exchange_condi = 'Điều kiện đổi trả:'
    return_and_exchange_condi_con = 'a. Thiết bị chưa kích hoạt phải giữ tem niêm phong gốc (số thứ tự trùng khớp với đơn hàng) và phụ kiện đầy đủ (cáp USB, hướng dẫn sử dụng, thẻ ghi nhớ); b. Phải gửi yêu cầu đổi trả trong vòng 7 ngày sau khi nhận hàng, quá hạn sẽ được coi là chấp nhận kiểm tra chất lượng; c. Phí vận chuyển đổi trả do người dùng chịu (trừ trường hợp lỗi chất lượng).'
    warranty_scope = 'Phạm vi bảo hành:'
    warranty_scope_1 = 'a. Bao gồm các lỗi không phải do con người gây ra như lỗi chip an ninh, màn hình hiển thị bất thường, mất chức năng nút bấm.'
    warranty_scope_2 = 'b. Cần cung cấp chứng từ mua hàng (số thứ tự đơn hàng) và bằng chứng lỗi (video phải hiển thị rõ mã số SN của thiết bị và hiện tượng bất thường).'
    warranty_scope_3 = 'c. Các lỗi do con người gây ra (như ngâm nước, rơi vỡ) không nằm trong phạm vi bảo hành, có thể sửa chữa có phí.'

    disclaimer = '3. Miễn trừ trách nhiệm'
    product_risk = '1. Rủi ro sản phẩm'
    physical_risk = 'Rủi ro vật lý:'
    physical_risk_1 = 'a. Thiết bị có thể không hoạt động trong môi trường nhiệt độ cao (>60℃), độ ẩm cao (>90% RH), trường từ mạnh (>100mT).'
    physical_risk_2 = 'b. Nếu không sạc trong thời gian dài, pin có thể bị hỏng (khuyên sạc một lần mỗi tháng).'
    supply_chain_risk = 'Rủi ro chuỗi cung ứng:'
    supply_chain_risk_1 = 'a. Trang web chính thức cung cấp công cụ xác minh chống giả, quét mã QR của thiết bị để xác minh tính xác thực.'
    supply_chain_risk_2 = 'b. Nếu nghi ngờ thiết bị bị thay thế, hãy liên hệ ngay với bộ phận chăm sóc khách hàng và báo cảnh sát.'
    service_interruption = '2. Dừng dịch vụ'
    service_interruption_1 = 'Bảo trì theo kế hoạch sẽ được thông báo trước 48 giờ thông qua bảng thông báo trên trang web chính thức. Bảo trì khẩn cấp có thể tạm dừng dịch vụ mà không cần thông báo trước.'
    service_interruption_2 = 'Chúng tôi không chịu trách nhiệm bồi thường cho mất mát dữ liệu do các yếu tố bất khả kháng.'
    
    device_label = "Tên thiết bị"
    device_title_firmware_version = 'Phiên bản firmware'
    device_title_serial_number = 'Số serial'
    bluetooth_name = "Tên Bluetooth"
    bluetooth_version = "Phiên bản Bluetooth"
    attention_events = "Lưu ý"
    firmware_title_1 = '1. Đảm bảo thiết bị có pin trên 20%'
    firmware_title_2 = '2. Kết nối thiết bị với máy tính bằng cáp USB-C'
    firmware_title_3 = '3. Nhấp vào "Nâng cấp firmware"'
    firmware_title_caution = 'Cảnh báo'
    firmware_describe_caution = 'Trong quá trình nâng cấp, hãy đảm bảo kết nối USB ổn định'
    equipment_info = 'Thông tin thiết bị'
    equipment_name = 'Tên thiết bị'
    equipment_version = 'Phiên bản thiết bị'

class Nft:
    nft_item ="{} mục"
    nft_items ="{} mục"
class Title:
    enter_old_pin = "Nhập mã PIN cũ"
    enter_new_pin = "Nhập mã PIN mới"
    enter_pin = "Nhập mã PIN"
    enter_pin_again = "Nhập lại mã PIN"
    select_language = "Ngôn ngữ"
    create_wallet = "Tạo ví"
    wallet = "Ví"
    import_wallet = "Nhập ví"
    restore_wallet = "Khôi phục ví"
    select_word_count = "Chọn số lượng từ"
    wallet_security = "Bảo mật ví"
    pin_security = "Bật bảo vệ bằng mã PIN"
    mnemonic_security = "Lưu ý bảo mật cụm từ khôi phục"
    backup_mnemonic = "Sao lưu cụm từ khôi phục"
    enter_mnemonic = "Nhập cụm từ khôi phục"
    check_mnemonic = "Kiểm tra cụm từ khôi phục"
    success = "Thành công"
    operate_success = "Thao tác thành công"
    theme_success = "Đổi chủ đề thành công"
    warning = "Cảnh báo"
    error = "Lỗi"
    invalid_mnemonic = "Cụm từ khôi phục không hợp lệ"
    pin_not_match = "PIN không khớp"
    check_recovery_mnemonic = "Kiểm tra cụm từ khôi phục"
    power_off = "Tắt nguồn"
    restart = "Khởi động lại"
    change_language = "Thay đổi ngôn ngữ"
    wipe_device = "Xóa thiết bị"
    bluetooth_pairing = "Ghép nối Bluetooth"
    address="Địa chỉ {}"
    public_key = "Khóa công khai {}"
    xpub = "XPub {}"
    transaction = "Giao dịch {}"
    transaction_detail = "Chi tiết giao dịch"
    confirm_transaction = "Xác nhận giao dịch"
    confirm_message = "Xác nhận thông điệp"
    signature = "Kết quả chữ ký"
    wrong_pin = "Sai PIN"
    pin_changed = "Đã thay đổi PIN"
    pin_enabled = "Đã bật PIN"
    pin_disabled = "Đã tắt PIN"
    unknown_token = "Token không xác định"
    view_data = "Xem dữ liệu"
    sign_message = "Ký thông điệp {}"
    verify_message = "Xác minh thông điệp {}"
    typed_data = "Dữ liệu có cấu trúc {}"
    typed_hash = "Hash có cấu trúc {}"
    system_update = "Nâng cấp hệ thống"
    entering_boardloader = "Đang vào Boardloader"
    remove_credential = "Xóa chứng chỉ"
    list_credentials = "Liệt kê chứng chỉ"
    authorize_coinjoin = "Ủy quyền CoinJoin"
    multisig_address_m_of_n = "Địa chỉ đa chữ ký {}\n({} trên {})"
    u2f_register = "Đăng ký U2F"
    u2f_unregister = "Hủy đăng ký U2F"
    u2f_authenticate = "Xác thực U2F"
    fido2_register = "Đăng ký FIDO2"
    fido2_unregister = "Hủy đăng ký FIDO2"
    fido2_authenticate = "Xác thực FIDO2"
    finalize_transaction = "Hoàn tất giao dịch"
    meld_transaction = "Giao dịch Meld"
    update_transaction = "Cập nhật giao dịch"
    high_fee = "Phí cao"
    fee_is_high = "Phí giao dịch quá cao"
    confirm_locktime = "Xác nhận thời gian khóa"
    view_transaction = "Xem giao dịch"
    x_confirm_payment = "Xác nhận thanh toán {}"
    confirm_replacement = "Xác nhận thay thế giao dịch"
    x_transaction = "Giao dịch {}"
    x_joint_transaction = "Giao dịch liên hợp {}"
    change_label = "Thay đổi tên thiết bị"
    enable_passphrase = "Bật Passphrase"
    disable_passphrase = "Tắt Passphrase"
    passphrase_source = "Cài đặt nhập Passphrase"
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
    import_credential = "Nhập chứng chỉ"
    export_credential = "Xuất chứng chỉ"
    asset = "Tài sản"
    unimplemented = "Chưa triển khai"
    invalid_data="Định dạng dữ liệu không hợp lệ"
    low_power = "Pin yếu"
    collect_nft = "Thu thập NFT"
    verify_device = "Xác minh thiết bị"
    update_bootloader = "Cập nhật trình引导 (bootloader)"
    update_resource = "Cập nhật tài nguyên"

    words_num = "Từ #{}"
    download_digital = "Tải xuống"
    connect_wallets = "Kết nối ví"
    start_setup = "Bắt đầu thiết lập"
    prepare_create = "Chuẩn bị tạo"
    prepare_import = "Chuẩn bị nhập"
    prepare_check = "Chuẩn bị kiểm tra"
    input_words = "Nhập cụm từ khôi phục"
    has_sub = "Đã gửi"
    reatart = "Khởi động lại"
    invalid_words = "Cụm từ khôi phục không hợp lệ"
    stop_checking = "Dừng kiểm tra"
    correct_words = "Cụm từ khôi phục chính xác"
    mnemonic_not_match = "Cụm từ khôi phục không khớp"
    wallet_created = "Ví đã được tạo"
    check_words = "Kiểm tra cụm từ khôi phục"
    verified = "Đã xác minh"
    wallet_is_ready = "Ví đã sẵn sàng"

    prepare_backup = "Chuẩn bị sao lưu"
    mnemonic_word = "Cụm từ khôi phục"
    error_mnemonic_word = "Từ không chính xác"
    right_word = "Đúng"
    wrong_word = "Sai"

    pin_not_match = "Không khớp"
    has_reset = "Thiết bị đã được đặt lại"
    has_wipe = "Thiết bị đã bị xóa"
    screen_bright = "Độ sáng màn hình"
    download_app = "Tải ứng dụng"
    official_website = "Trang web chính thức"
    scan_ercode = "Quét mã QR hiển thị trên ứng dụng"
    wipe_notice = "Trước khi xóa thiết bị, hãy đảm bảo bạn đã hiểu:"
    receive_tips = "Chỉ hỗ trợ nhận tài sản {}"
    sign_fail = "Ký thất bại"
    select_network = "Chọn mạng"
    preview = "Xem trước"
    go_link = "Vui lòng truy cập liên kết:"
    connect_again = "Vui lòng thử lại kết nối."

class Text:
    start_setup = "Tạo ví mới với cụm từ khôi phục hoặc nhập cụm từ khôi phục đã có để khôi phục ví."
    select_word_count = "Vui lòng chọn số lượng từ của cụm từ khôi phục."
    input_words = "Vui lòng nhập các từ của cụm từ khôi phục theo đúng thứ tự, đảm bảo số thứ tự khớp với bản sao lưu của bạn."
    invalid_words = "Cụm từ khôi phục bạn nhập không hợp lệ, hãy nhấp vào từ để chỉnh sửa hoặc bắt đầu lại."
    stop_checking = "Nếu dừng lại, tất cả tiến trình sẽ bị mất. Bạn có chắc chắn muốn dừng không?"
    import_wallet = "Nhập cụm từ khôi phục đã có của bạn để khôi phục ví."
    correct_words = "Cụm từ khôi phục bạn nhập hợp lệ và trùng khớp với thiết bị."
    mnemonic_not_match = "Cụm từ khôi phục bạn nhập hợp lệ nhưng không khớp với thiết bị."
    wallet_created = "Ví mới đã được tạo thành công, vui lòng sao lưu ngay."
    mnemonic_word_tips = "Vui lòng ghi lại {} từ sau theo đúng thứ tự."
    select_words = "Vui lòng chọn đúng các từ"
    error_mnemonic_word = "Từ không chính xác, vui lòng kiểm tra lại cụm từ khôi phục và thử lại."
    pin_not_match = "Mã PIN bạn nhập không khớp, vui lòng thử lại."
    has_reset = "Nhập sai mã PIN quá nhiều lần, bộ nhớ đã bị xóa."
    restart_countdown = "Thiết bị sẽ khởi động lại sau {} giây"
    has_wipe = "Thiết bị đã được xóa dữ liệu thành công, vui lòng khởi động lại thiết bị."
    download_digital_tips = "Vui lòng tải ứng dụng Digital Shield tại: \n{}"
    sign_fail = "Bạn đã hủy ký, giao dịch đã bị hủy."
    sign_success = "Giao dịch đã được ký"
    check_words_tips = "Vui lòng kiểm tra từng từ theo hướng dẫn, đối chiếu với bản sao lưu cụm từ khôi phục của bạn."
    backup_verified = "Bạn đã hoàn thành xác minh cụm từ khôi phục."
    create_success = "Bạn đã sao lưu cụm từ khôi phục thành công. Ví đã được tạo"
    tap_to_unlock = "Chạm để mở khóa"
    unlocking = "Đang mở khóa thiết bị..."

    str_words = "#FFFFFF {}# từ"
    backup_manual = "Ghi lại cụm từ khôi phục thủ công và lưu trữ ở nơi an toàn"
    check_manual = "Nhấn vào các từ theo đúng thứ tự"
    backup_invalid = "Cụm từ khôi phục bạn nhập không chính xác. Vui lòng kiểm tra và thử lại"
    pin_not_match = "Mã PIN bạn nhập không chính xác. Vui lòng thử lại"
    please_wait = "Vui lòng chờ"
    wiping_device = "Đang xóa dữ liệu thiết bị..."
    create_wallet = "Tạo cụm từ khôi phục mới để thiết lập ví"
    restore_wallet = "Khôi phục ví từ cụm từ khôi phục đã sao lưu"
    restore_mnemonic_match = "Cụm từ khôi phục của bạn khớp. Bạn đã sao lưu chính xác"
    restore_success = "Cụm từ khôi phục của bạn đã được nhập, ví đã khôi phục thành công."
    check_recovery_mnemonic = "Vui lòng kiểm tra cụm từ khôi phục để xác nhận khớp hoàn toàn"
    invalid_recovery_mnemonic = "Cụm từ khôi phục bạn nhập không hợp lệ. Vui lòng kiểm tra và thử lại"
    check_recovery_not_match = "Cụm từ khôi phục bạn nhập hợp lệ nhưng không khớp với thiết bị",
    shutting_down = "Đang tắt nguồn..."
    restarting = "Đang khởi động lại..."
    never = "Không bao giờ"
    second = "giây"
    seconds = "giây"
    minute = "phút"
    minutes = "phút"
    changing_language = "Bạn đang thay đổi ngôn ngữ thành {}. Áp dụng cài đặt này sẽ khởi động lại thiết bị."
    change_pin = "Vui lòng đặt mã PIN có độ dài từ 4 đến 16 ký tự."
    wipe_device = "Khôi phục thiết bị về trạng thái ban đầu.\nCảnh báo: Thao tác này sẽ xóa mọi dữ liệu trên thiết bị của bạn"
    wipe_device_check = [
        "Xóa thiết bị sẽ xóa tất cả dữ liệu",
        "Dữ liệu không thể khôi phục",
        "Đã sao lưu cụm từ khôi phục"
    ]
    wipe_device_success = "Thiết bị đã xóa dữ liệu thành công\nĐang khởi động lại thiết bị..."
    bluetooth_pair = "Vui lòng nhập mã ghép nối trên thiết bị của bạn"
    bluetooth_pair_failed = "Ghép nối Bluetooth thất bại"
    path = "Đường dẫn:"
    chain_id = "Chain ID:"
    send = "Gửi"
    to = "đến"
    amount = "Số lượng"
    from_ = "Từ"
    receiver = "Người nhận"
    fee = "Phí"
    max_fee = "Phí tối đa"
    max_priority_fee_per_gas = "Phí ưu tiên tối đa trên mỗi Gas"
    max_fee_per_gas = "Giới hạn phí giao dịch trên mỗi Gas"
    gas_price = "Giá Gas"
    total = "Tổng cộng"
    do_sign_this_transaction = "Bạn có chắc chắn muốn ký giao dịch {} này không?"
    transaction_signed = "Giao dịch đã được ký"
    address = 'Địa chỉ:'
    public_key = "Khóa công khai:"
    xpub = "XPub:"
    unknown_tx_type = "Loại giao dịch không xác định, vui lòng kiểm tra dữ liệu nhập"
    unknown_function = "Hàm không xác định:"
    use_app_scan_this_signature = "Vui lòng dùng ứng dụng ví quét kết quả chữ ký"
    internal_error = "Lỗi nội bộ"
    tap_switch_to_airgap = "Chạm để chuyển sang hiển thị địa chỉ Airgap"
    tap_switch_to_receive = "Chạm để chuyển sang hiển thị địa chỉ nhận tiền"
    incorrect_pin_times_left = "Sai PIN, còn lại {} lần thử"
    incorrect_pin_last_time = "Sai PIN, còn 1 lần thử cuối"
    wrong_pin = "Mã PIN không chính xác"
    seedless = "Không có seed"
    backup_failed = "Sao lưu thất bại!"
    need_backup = "Cần sao lưu!"
    pin_not_set = "Chưa đặt PIN!"
    experimental_mode = "Chế độ thử nghiệm"
    pin_change_success = "Đã thay đổi PIN thành công"
    pin_enable_success = "Đã bật PIN thành công"
    pin_disable_success = "Đã tắt PIN thành công"
    contract = "Hợp đồng:"
    new_contract = "Hợp đồng mới?"
    bytes_ = "{} bytes"
    message = "Thông điệp:"
    no_message = "Không chứa thông điệp"
    contains_x_key = "Chứa {} khóa"
    array_of_x_type = "Mảng kiểu {} {}"
    do_sign_712_typed_data = "Xác nhận ký giao dịch dữ liệu có cấu trúc này?"
    do_sign_typed_hash = "Xác nhận ký giao dịch hash có cấu trúc này?"
    domain_hash = "Hash domain:"
    message_hash = "Hash thông điệp:"
    switch_to_update_mode = "Chuyển sang chế độ cập nhật"
    switch_to_boardloader = "Chuyển sang chế độ board loader"
    list_credentials = "Xuất thông tin chứng chỉ lưu trữ trên thiết bị?"
    coinjoin_at_x = "Tham gia giao dịch Coinjoin sau:\n{}"
    signature_is_valid = "Chữ ký hợp lệ"
    signature_is_invalid = "Chữ ký không hợp lệ"
    u2f_already_registered = "U2F đã đăng ký"
    u2f_not_registered = "U2F chưa đăng ký"
    fido2_already_registered_x = "FIDO2 đã đăng ký {}"
    fido2_verify_user = "FIDO2 xác thực người dùng"
    device_already_registered_x = "Thiết bị đã đăng ký {}"
    device_verify_user = "Thiết bị xác thực người dùng"
    fee_is_unexpectedly_high = "Phí giao dịch quá cao"
    too_many_change_outputs = "Quá nhiều đầu ra tiền thối"
    change_count = "Số lượng tiền thừa"
    locktime_will_have_no_effect = "Thời gian khóa sẽ không có hiệu lực"
    confirm_locktime_for_this_transaction = "Xác nhận thời gian khóa cho giao dịch này"
    block_height = "Độ cao khối"
    time = "Thời gian"
    amount_increased = "Số tiền tăng"
    amount_decreased = "Số tiền giảm"
    fee_unchanged = "Phí không thay đổi"
    fee_increased = "Phí tăng"
    fee_decreased = "Phí giảm"
    your_spend = "Khoản chi của bạn"
    change_label_to_x = "Đổi nhãn thành {}"
    enable_passphrase = "Bật mã hóa Passphrase?"
    disable_passphrase = "Tắt mã hóa Passphrase?"
    enable_passphrase_always = "Luôn nhập Passphrase trên thiết bị?"
    revoke_enable_passphrase_always = "Hủy bỏ cài đặt luôn nhập Passphrase trên thiết bị?"
    auto_lock_x = "Tự động khóa thiết bị sau {}?"
    enable_safety_checks = "Bật kiểm tra an toàn nghiêm ngặt? Tính năng này cung cấp bảo vệ an toàn toàn diện hơn."
    disable_safety_checks = "Tắt kiểm tra an toàn? Vui lòng hiểu rõ các rủi ro bảo mật tiềm ẩn trước khi tiếp tục."
    enable_experiment_mode = "Bật chế độ thử nghiệm?"
    set_as_homescreen = "Đặt làm màn hình chính?"
    replace_homescreen = "Thay thế màn hình chính? Hành động này sẽ xóa hình nền được tải lên đầu tiên."
    confirm_replace_wallpaper = "Bạn có chắc chắn muốn thay đổi hình nền màn hình chính không?"
    get_next_u2f_counter = "Lấy bộ đếm U2F tiếp theo?"
    set_u2f_counter_x = "Đặt bộ đếm U2F thành {}?"
    confirm_entropy = "Xuất entropy? Hãy chắc chắn bạn hiểu mình đang làm gì trước khi tiếp tục!"
    bandwidth = "Băng thông"
    energy = "Năng lượng"
    sender = "Người gửi"
    recipient = "Người nhận"
    resource = "Tài nguyên"
    frozen_balance = "Số dư bị đóng băng"
    unfrozen_balance = "Số dư được mở khóa"
    delegated_balance = "Số dư ủy quyền"
    undelegated_balance = "Số dư hủy ủy quyền"
    you_are_freezing = "Bạn đang đóng băng tài sản"
    you_are_unfreezing = "Bạn đang mở khóa tài sản"
    you_are_delegating = "Bạn đang ủy quyền tài sản"
    you_are_undelegating = "Bạn đang hủy ủy quyền"
    duration = "Thời lượng"
    lock = "Khóa"
    unlock = "Mở khóa"
    all = "Tất cả"
    source = "Nguồn"
    tip = "Mẹo"
    keep_alive = "Giữ kết nối"
    invalid_ur = "Loại QR code không được hỗ trợ, vui lòng thử lại"
    sequence_number = "Số thứ tự"
    expiration_time = "Thời gian hết hạn"
    argument_x = "Tham số #{}"
    low_power_message = "Pin còn {}%\nVui lòng sạc pin"
    collect_nft = "Bạn có chắc chắn muốn thu thập NFT này không?"
    replace_nft = "Bạn có muốn thu thập NFT này không? Bạn đã đạt giới hạn lưu trữ, việc này sẽ xóa NFT được tải lên lâu nhất."
    verify_device = "Bạn có chắc chắn muốn xác thực thiết bị của mình với máy chủ DigitShield không? Nhấn xác nhận để kiểm tra xem thiết bị của bạn có phải là chính hãng và không bị篡改 không."
    update_bootloader = "Bạn có muốn cập nhật trình引导 (bootloader) không?"
    update_resource = "Bạn có muốn cập nhật tài nguyên thiết bị không?"

class Tip:
    swipe_down_to_close = "Vuốt xuống để đóng"

class Button:
    done = "Xong"
    ok = "Đồng ý"
    confirm = "Xác nhận"
    reject = "Từ chối"
    next = "Tiếp theo"
    cancel = "Hủy"
    redo = "Tạo lại"
    continue_ = "Tiếp tục"
    try_again = "Thử lại"
    power_off = "Tắt nguồn"
    hold_to_power_off = "Nhấn giữ để tắt máy"
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
    update = "Cập nhật"

class WalletSecurity:
    header = "Ghi lại cụm từ khôi phục của bạn trên giấy và lưu trữ ở nơi an toàn"
    tips = [
        {
            "level": "info",
            "msgs": [
                "#00001F Cụm từ khôi phục cần được lưu trữ an toàn#",
                "#18794E * Trong két an toàn ngân hàng#",
                "#18794E * Trong hộp khóa an toàn#",
                "#18794E * Tại nhiều địa điểm bí mật#",
            ]
        },
        {
            "level": "warning",
            "msgs": [
                "#00001F CẢNH BÁO QUAN TRỌNG#",
                "#CD2B31 * Ghi nhớ cụm từ khôi phục#",
                "#CD2B31 * Không được làm mất#",
                "#CD2B31 * Không tiết lộ cho bất kỳ ai#",
                "#CD2B31 * Không lưu trữ trực tuyến#",
                "#CD2B31 * Không lưu trên máy tính#",
            ]
        },
    ]

class MnemonicSecurity:
    header = "Cụm từ khôi phục là tập hợp các từ ngắn dùng để khôi phục tài sản trong ví. Ai có cụm từ này có thể sử dụng tài sản của bạn, vui lòng bảo quản cẩn thận"

    tips = [
        "1. Kiểm tra môi trường xung quanh, đảm bảo không có người xem hoặc camera",
        "2. Sao lưu cụm từ khôi phục theo đúng thứ tự, tuyệt đối không chia sẻ với bất kỳ ai",
        "3. Lưu trữ cụm từ khôi phục ngoại tuyến tại nơi an toàn, không sử dụng phương thức điện tử để sao lưu và không tải lên mạng",
    ]

class PinSecurity:
    header = "Mã PIN là mật khẩu truy cập thiết bị, dùng để ủy quyền truy cập thiết bị hiện tại. Vui lòng sử dụng mã PIN đúng cách theo hướng dẫn sau"
    tips = [
        "1. Kiểm tra môi trường an toàn khi đặt hoặc nhập mã PIN, đảm bảo không có người xem hoặc camera",
        "2. Đặt mã PIN mạnh từ 4-16 ký tự, tránh dùng các số liên tiếp hoặc lặp lại",
        "3. Số lần nhập sai mã PIN tối đa là 10 lần, sau đó thiết bị sẽ tự động thiết lập lại",
        "4. Bảo quản mã PIN cẩn thận, không chia sẻ với bất kỳ ai",
    ]
class DownloadDigital:
    #header = "Vui lòng tải xuống và cài đặt DigitShield để xác thực thiết bị"
    tips = [
        "1. Nhấp vào 'Kết nối ví'",
        "2. Kết nối thiết bị:",
        "3. Chờ một chút, ứng dụng DigitalShield sẽ khôi phục các tài khoản bạn đã từng sử dụng.",
    ]
class Solana:
    ata_reciver = "Người nhận (Tài khoản token liên kết)"
    ata_sender = "Người gửi (Tài khoản token liên kết)"
    source_owner = "Người ký giao dịch"
    fee_payer = "Người trả phí"
