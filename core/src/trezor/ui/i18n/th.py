class App:
    account = "계정"
    scan = "거래 스캔"
    nft = "NFT 전시실"
    guide = "사용 가이드"
    security = "보안"
    setting = "설정"

#### Setting App
class Setting:
    bluetooth = "블루투스"
    language = "언어"
    vibration = "터치 피드백"
    brightness = "화면 밝기"
    auto_lock = "자동 잠금"
    auto_shutdown = "자동 종료"
    animation = "전환 애니메이션"
    wallpaper = "배경화면"
    power_off = "전원 끄기"
    restart = "재시작"

#### Security App
class Security:
    change_pin = "PIN 코드 변경"
    backup_mnemonic = "니모닉 백업"
    check_mnemonic = "니모닉 확인"
    wipe_device = "장치 지우기"

#### guide App
class Guide:
    about = "Digit Shield 정보"
    terms_of_use = '이용 약관'
    device_info = '장치 정보'
    firmware_update = '펌웨어 업데이트'
    terms_title_terms_us = 'Digit Shield 이용 약관'
    terms_describe_terms_us = '전체 버전의 이용 약관에 액세스하려면 다음 링크를 방문하십시오:\n http://digitshield.com/terms'

    terms_title_product_services = 'Digit Shield 제품 및 서비스'
    terms_describe_product_services = '우리의 하드웨어 지갑은 암호화폐를 안전하게 관리합니다'
    terms_title_risks = '위험'
    terms_describe_risks = '암호화폐와 기술적 취약점과 관련된 위험에 주의하십시오.'
    terms_title_disclaimers = '면책 조항'
    terms_describe_disclaimers = '제공된 정보는 금융 조언이 아닙니다. 결정을 내리기 전에 전문가의 조언을 구하십시오.'
    terms_title_contact_us = '문의하기'
    terms_describe_contact_us = '질문이나 우려 사항이 있으면 support@digitshield.com으로 이메일을 보내주십시오'
    device_label = "장치 이름"
    device_title_firmware_version = '펌웨어 버전'
    device_title_serial_number = '시리얼 번호'
    bluetooth_name = "블루투스 이름"
    bluetooth_version = "블루투스 버전"
    firmware_title_1 = '1. 장치의 배터리가 20% 이상인지 확인하십시오'
    firmware_title_2 = '2. USB-C 케이블로 장치를 컴퓨터에 연결하십시오'
    firmware_title_3 = '3. "펌웨어 업데이트"를 클릭하십시오'
    firmware_title_caution = '경고'
    firmware_describe_caution = '업그레이드 중에는 USB 연결이 안정되어 있는지 확인하십시오'

class Nft:
    nft_item ="{} 항목"
    nft_items ="{} 항목"
class Title:
    enter_old_pin = "이전 PIN 코드를 입력하십시오"
    enter_new_pin = "새 PIN 코드를 입력하십시오"
    enter_pin = "PIN 코드를 입력하십시오"
    enter_pin_again = "다시 PIN 코드를 입력하십시오"
    select_language = "언어 선택"
    create_wallet = "지갑 생성"
    wallet = "지갑"
    import_wallet = "지갑 가져오기"
    restore_wallet = "지갑 복원"
    wallet_is_ready = "지갑이 준비되었습니다"
    select_word_count = "단어 수 선택"
    wallet_security = "지갑 보안"
    pin_security = "PIN 보안 힌트"
    mnemonic_security = "니모닉 보안 힌트"
    backup_mnemonic = "니모닉 백업"
    enter_mnemonic = "니모닉을 입력하십시오"
    check_mnemonic = "니모닉 확인"
    success = "성공"
    warning = "경고"
    error = "오류"
    verified = "니모닉 백업 완료"
    invalid_mnemonic = "잘못된 니모닉"
    pin_not_match = "PIN 코드가 일치하지 않습니다"
    check_recovery_mnemonic = "복원 니모닉 확인"
    mnemonic_not_match = "니모닉이 일치하지 않습니다"
    power_off = "전원 끄기"
    restart = "재시작"
    change_language = "언어 변경"
    wipe_device = "장치 지우기"
    bluetooth_pairing = "블루투스 페어링"
    address="{} 주소"
    public_key = "{} 공개키"
    xpub = "{} XPub"
    transaction = "{} 거래"
    transaction_detail = "거래 상세"
    confirm_transaction = "거래 확인"
    confirm_message = "메시지 확인"
    signature = "서명 결과"
    wrong_pin = "잘못된 PIN 코드"
    pin_changed = "PIN 코드가 변경되었습니다"
    pin_enabled = "PIN 코드가 활성화되었습니다"
    pin_disabled = "PIN 코드가 비활성화되었습니다"
    unknown_token = "알려지지 않은 토큰"
    view_data = "데이터 보기"
    sign_message = "{} 메시지 서명"
    verify_message = "{} 메시지 검증"
    typed_data = "{} 구조화된 데이터"
    typed_hash = "{} 구조화된 해시"
    system_update = "시스템 업데이트"
    entering_boardloader = "보드로더 진입"
    remove_credential = "凭据 삭제"
    list_credentials = "凭据 목록"
    authorize_coinjoin = "CoinJoin 승인"
    multisig_address_m_of_n = "{} 다중서명 주소\n({} of {})"
    u2f_register = "U2F 등록"
    u2f_unregister = "U2F 등록 해제"
    u2f_authenticate = "U2F 인증"
    fido2_register = "FIDO2 등록"
    fido2_unregister = "FIDO2 등록 해제"
    fido2_authenticate = "FIDO2 인증"
    fee_is_high = "수수료가 높습니다"
    confirm_locktime = "잠금 시간 확인"
    view_transaction = "거래 보기"
    x_confirm_payment = "{} 결제 확인"
    confirm_replacement = "교체 거래 확인"
    x_transaction = "{} 거래"
    x_joint_transaction = "{} 공동 거래"
    change_label = "장치 이름 변경"
    enable_passphrase = "Passphrase 활성화"
    disable_passphrase = "Passphrase 비활성화"
    passphrase_source = "Passphrase 입력 설정"
    enable_safety_checks ="안전 확인 활성화"
    disable_safety_checks ="안전 확인 비활성화"
    experiment_mode = "실험 모드"
    set_as_homescreen = "홈 화면으로 설정"
    get_next_u2f_counter = "다음 U2F 카운터 가져오기"
    set_u2f_counter = "U2F 카운터 설정"
    encrypt_value = "데이터 암호화"
    decrypt_value = "데이터 복호화"
    confirm_entropy = "엔트로피 내보내기"
    memo = "메모"
    import_credential = "凭据 가져오기"
    export_credential = "凭据 내보내기"
    asset = "자산"
    unimplemented = "구현되지 않음"

class Text:
    tap_to_unlock = "터치하여 잠금 해제"
    unlocking = "장치를 해제하는 중..."
    str_words = "#18794E {}# 개의 단어"
    backup_manual = "니모닉을 종이에 적어 안전한 곳에 보관하십시오"
    check_manual = "아래 단어를 순서대로 클릭하십시오"
    backup_verified = "니모닉 백업이 완료되었습니다. 다른 사람과 공유하지 마십시오"
    backup_invalid = "입력한 니모닉이 올바르지 않습니다. 백업한 니모닉을 확인하고 다시 시도하십시오"
    pin_not_match = "입력한 PIN 코드가 올바르지 않습니다. 다시 시도하십시오"
    please_wait = "잠시 기다리십시오"
    wiping_device = "장치 데이터를 지우는 중..."
    create_wallet = "새로운 니모닉을 생성하여 지갑을 만듭니다"
    restore_wallet = "백업한 니모닉에서 지갑을 복원합니다"
    restore_mnemonic_match = "니모닉이 일치합니다. 백업이 올바릅니다"
    restore_success = "지갑 복원 성공"
    create_success = "니모닉이 성공적으로 백업되었으며 지갑이 생성되었습니다"
    check_recovery_mnemonic = "니모닉이 완전히 일치하는지 확인하십시오"
    invalid_recovery_mnemonic = "입력한 니모닉이 유효하지 않습니다. 니모닉을 확인하고 다시 시도하십시오"
    check_recovery_not_match = "입력한 니모닉은 유효하지만 장치의 니모닉과 일치하지 않습니다"
    shutting_down = "전원을 끄는 중..."
    restarting = "재시작하는 중..."
    never = "안 함"
    second = "초"
    seconds = "초"
    minute = "분"
    minutes = "분"
    changing_language = "언어를 변경하고 있습니다\n이 설정을 적용하면 장치가 다시 시작됩니다"
    change_pin = "장치를 보호하기 위해 4~16자리의 PIN 코드를 설정하십시오"
    wipe_device = "장치를 공장 출고 상태로 복원합니다.\n경고: 이 작업은 장치의 모든 데이터를 지웁니다."
    wipe_device_check = [
        "장치를 지우면 모든 데이터가清除됩니다",
        "데이터를 복구할 수 없습니다",
        "니모닉을 백업했습니다",
    ]
    wipe_device_success = "장치 데이터가 성공적으로 지워졌습니다\n 장치를 재시작하는 중 ..."
    bluetooth_pair = "장치에서 페어링 코드를 입력하십시오"
    bluetooth_pair_failed = "블루투스 페어링 실패"
    path = "파생 경로:"
    chain_id = "체인 ID:"
    send = "보내기"
    to = "받는 사람"
    amount = "금액"
    from_ = "보내는 사람"
    receiver = "받는 사람"
    fee = "수수료"
    max_fee = "최대 수수료"
    max_priority_fee_per_gas = "가스당 최대 우선 순위 수수료"
    max_fee_per_gas = "가스당 거래 수수료 상한"
    gas_price = "가스 가격"
    total = "총액"
    do_sign_this_transaction = "이 {} 거래에 서명하시겠습니까?"
    transaction_signed = "거래가 서명되었습니다"
    address = '주소:'
    public_key = "공개키:"
    xpub = "XPub:"
    unknown_tx_type = "알려지지 않은 거래 유형, 입력 데이터를 확인하십시오"
    use_app_scan_this_signature = "지갑 앱으로 서명 결과를 스캔하십시오"
    internal_error = "내부 오류"
    tap_switch_to_airgap = "에어갭 주소를 표시하려면二维码를 터치하십시오"
    tap_switch_to_receive = "지갑收款 주소를 표시하려면二维码를 터치하십시오"
    incorrect_pin_times_left = "PIN 코드가 잘못되었습니다. 남은 시도 횟수: {}"
    incorrect_pin_last_time = "PIN 코드가 잘못되었습니다. 마지막 기회입니다"
    wrong_pin = "잘못된 PIN 코드를 입력했습니다"
    seedless = "시드가 없습니다"
    backup_failed = "백업 실패!"
    need_backup = "백업이 필요합니다!"
    pin_not_set = "PIN 코드가 설정되지 않았습니다!"
    experimental_mode = "실험 모드"
    pin_change_success = "PIN 코드가 성공적으로 변경되었습니다"
    pin_enable_success = "PIN 코드가 성공적으로 활성화되었습니다"
    pin_disable_success = "PIN 코드가 성공적으로 비활성화되었습니다"
    contract = "계약:"
    new_contract = "새 계약?"
    bytes_ = "{} 바이트"
    message = "메시지:"
    no_message = "메시지를 포함하지 않음"
    contains_x_key = "{} 키 포함"
    array_of_x_type = "타입 {}의 배열 {}"
    do_sign_712_typed_data = "이 구조화된 데이터 거래에 서명하시겠습니까?"
    do_sign_typed_hash = "이 구조화된 해시 거래에 서명하시겠습니까?"
    domain_hash = "도메인 해시:"
    message_hash = "메시지 해시:"
    switch_to_update_mode = "업데이트 모드로 전환"
    switch_to_boardloader = "보드로더 모드로 전환"
    list_credentials = "이 장치에 저장된凭据 정보를 내보내시겠습니까?"
    coinjoin_at_x = "다음 Coinjoin 거래에 참여하시겠습니까?:\n{}"
    signature_is_valid = "서명이 유효합니다"
    signature_is_invalid = "서명이 유효하지 않습니다"
    u2f_already_registered = "U2F 이미 등록됨"
    u2f_not_registered = "U2F 등록되지 않음"
    fido2_already_registered_x = "FIDO2 이미 등록됨 {}"
    fido2_verify_user = "FIDO2 사용자 인증"
    device_already_registered_x = "장치 이미 등록됨 {}"
    device_verify_user = "장치 사용자 인증"
    finalize_transaction = "거래 완료"
    meld_transaction = "거래 통합"
    update_transaction = "거래 업데이트"
    fee_is_unexpectedly_high = "수수료가 예상보다 높습니다"
    change_count = "잔돈 수량"
    locktime_will_have_no_effect = "잠금 시간은 영향을 미치지 않습니다"
    confirm_locktime_for_this_transaction = "이 거래의 잠금 시간을 확인하십시오"
    block_height = "블록 높이"
    time = "시간"
    amount_increased = "금액 증가"
    amount_decreased = "금액 감소"
    fee_unchanged = "수수료 변경 없음"
    fee_increased = "수수료 증가"
    fee_decreased = "수수료 감소"
    your_spend = "지출 금액"
    change_label_to_x = "라벨을 {}로 변경"
    enable_passphrase = "Passphrase 암호화를 활성화하시겠습니까?"
    disable_passphrase = "Passphrase 암호화를 비활성화하시겠습니까?"
    enable_passphrase_always = "항상 기기에서 Passphrase를 입력하시겠습니까?"
    revoke_enable_passphrase_always = "항상 기기에서 Passphrase를 입력하는 설정을 취소하시겠습니까?"
    auto_lock_x = "{} 후 자동 잠금하시겠습니까?"
    enable_safety_checks = "엄격한 안전 확인을 실행하시겠습니까? 이는 더 포괄적인 보안 보호를 제공합니다."
    disable_safety_checks = "안전 확인을 비활성화하시겠습니까? 계속하기 전에 이 작업의 잠재적인 보안 위험을 이해하십시오."
    enable_experiment_mode = "실험 모드를 활성화하시겠습니까?"
    set_as_homescreen = "홈 화면으로 설정하시겠습니까?"
    replace_homescreen = "홈 화면을 교체하시겠습니까? 이 작업은 가장 먼저 업로드한 배경화면을 삭제합니다."
    get_next_u2f_counter = "다음 U2F 카운터를 가져오시겠습니까?"
    set_u2f_counter_x = "U2F 카운터를 {}로 설정하시겠습니까?"
    confirm_entropy = "엔트로피를 내보내시겠습니까? 무엇을 하는지 확실하게 이해한 후에 계속하십시오!"
    bandwidth = "대역폭"
    energy = "에너지"
    sender = "보내는 사람"
    recipient = "받는 사람"
    resource = "자원"
    frozen_balance = "동결된 잔액"
    unfrozen_balance = "해동된 잔액"
    delegated_balance = "위임된 잔액"
    undelegated_balance = "위임 해지된 잔액"
    you_are_freezing = "자산을 동결하고 있습니다"
    you_are_unfreezing = "자산을 해동하고 있습니다"
    you_are_delegating = "자산을 위임하고 있습니다"
    you_are_undelegating = "자산의 위임을 해지하고 있습니다"
    duration = "지속 시간"
    lock = "잠금"
    unlock = "잠금 해제"

class Tip:
    swipe_down_to_close = "아래로 스와이프하여 닫기"

class Button:
    done = "완료"
    ok = "확인"
    confirm = "확인"
    reject = "거부"
    next = "다음"
    cancel = "취소"
    redo = "재생성"
    continue_ = "계속"
    try_again = "재시도"
    power_off = "전원 끄기"
    restart = "재시작"
    hold = "길게 누르기"
    address = "주소"
    qr_code = "QR 코드"
    view_detail = "상세 정보 보기"
    hold_to_sign = "길게 누르고 서명"
    hold_to_wipe = "길게 누르고 지우기"
    receive = "받기 주소"
    airgap = "에어갭"
    sign = "서명"
    verify = "검증"
    view_full_array = "전체 배열 보기"
    view_full_struct = "전체 구조 보기"
    view_full_message = "전체 메시지 보기"
    view_data = "데이터 보기"
    view_more = "更多 보기"

class WalletSecurity:
    header = "니모닉을 종이에 적어 안전한 곳에 보관하십시오"
    tips = [
        {
            "level": "info",
            "msgs": [
                "#00001F 니모닉은 안전하게 보관해야 합니다#",
                "#18794E * 은행 금고에 보관#",
                "#18794E * 보험箱에 보관#",
                "#18794E * 여러 비밀 장소에 보관#",
            ]
        },
        {
            "level": "warning",
            "msgs": [
                "#00001F 주의해야 합니다#",
                "#CD2B31 * 니모닉을 기억하세요#",
                "#CD2B31 *丧失하지 마십시오#",
                "#CD2B31 * 다른 사람에게 알리지 마십시오#",
                "#CD2B31 * 온라인에 저장하지 마십시오#",
                "#CD2B31 * 컴퓨터에 저장하지 마십시오#",
            ]
        },
    ]

class MnemonicSecurity:
    header = "니모닉은 지갑 자산을 복원하는 일련의 문구입니다. 니모닉을 소유하면 자산을 사용할 수 있습니다. 잘 관리하십시오"

    tips = [
        "1. 환경의 안전을 확인하고 관찰자나 카메라가 없는지 확인하십시오",
        "2. 문구의 올바른 순서대로 니모닉을 백업하고 다른 사람과 공유하지 마십시오",
        "3. 안전한 곳에서 오프라인으로 니모닉을 보관하십시오. 전자 방식으로 백업하지 마십시오. 인터넷에 올리지 마십시오",
    ]

class PinSecurity:
    header = "PIN 코드는 현재 장치에 액세스하기 위한 비밀번호입니다. 다음 지침에 따라 PIN 코드를 올바르게 사용하십시오"
    tips = [
        "1. PIN 코드를 설정하거나 입력할 때 환경의 안전을 확인하고 관찰자나 카메라가 없는지 확인하십시오",
        "2. 4-16자리의 강력한 PIN 코드를 설정하십시오. 연속 또는 반복되는 숫자를 사용하지 마십시오",
        "3. PIN 코드의 최대 재시도 횟수는 10회이며, 10회 연속으로 잘못 입력하면 장치가 재설정됩니다",
        "4. PIN 코드를 안전하게 보관하십시오. 다른 사람에게 알리지 마십시오",
    ]

class Solana:
    ata_reciver = "받는 사람(연결된 토큰 계정)"
    ata_sender = "보내는 사람(연결된 토큰 계정)"
    source_owner = "거래 서명자"
    fee_payer = "수수료 지불자"
   

