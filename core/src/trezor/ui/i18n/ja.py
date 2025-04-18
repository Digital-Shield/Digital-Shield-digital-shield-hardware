class App:
    account = "アカウント"
    scan = "取引スキャン"
    nft = "NFT 展示室"
    guide = "使用説明"
    security = "セキュリティ"
    setting = "設定"

#### Setting App
class Setting:
    bluetooth = "ブルートゥース"
    language = "言語"
    vibration = "タッチフィードバック"
    brightness = "画面の明るさ"
    auto_lock = "自動ロック"
    auto_shutdown = "自動シャットダウン"
    animation = "トランジションアニメーション"
    wallpaper = "壁紙"
    power_off = "電源オフ"
    restart = "再起動"

#### Security App
class Security:
    change_pin = "PINコードを変更"
    backup_mnemonic = "ニモニックをバックアップ"
    check_mnemonic = "ニモニックを確認"
    wipe_device = "デバイスを消去"

#### guide App
class Guide:
    about = "Digit Shield について"
    terms_of_use = '利用規約'
    device_info = 'デバイス情報'
    firmware_update = 'ファームウェアアップデート'
    terms_title_terms_us = 'Digit Shield 利用規約'
    terms_describe_terms_us = '利用規約の完全版にアクセスするには、以下のリンクを訪問してください:\n http://digitshield.com/terms'

    terms_title_product_services = 'Digit Shield の製品とサービス'
    terms_describe_product_services = '私たちのハードウェアウォレットは、暗号通貨を安全に管理します'
    terms_title_risks = 'リスク'
    terms_describe_risks = '暗号通貨と技術的な脆弱性に関連するリスクに注意してください.'
    terms_title_disclaimers = '免責事項'
    terms_describe_disclaimers = '提供される情報は財務アドバイスではありません。決定を下す前に、専門家のアドバイスを求めてください。'
    terms_title_contact_us = '四、お問い合わせ'
    terms_describe_contact_us = 'ご質問やご不明な点がございましたら、www.ds.pro@gmail.com までメールをお送りください'
    
    accept_tems = '一、条項の承諾'
    use_range = '1. 適用範囲'
    range_include = 'これらの条項は、Digital Shieldウォレットを通じて提供されるすべてのサービスに適用されます。'
    range_include_1 = 'ハードウェアウォレットの購入、アクティベーション、アフターサービス；Digital Shieldモバイルアプリケーション（Android/iOS/Goolg）のダウンロード、インストール、機能の使用；ファームウェアアップグレードサービス（セキュリティパッチ、機能強化バージョンを含む）；マルチチェーンデジタル資産管理（BTC、ETHなど3000以上のトークンの保存と転送をサポート）；技術サポート（デバイスの故障トラブルシューティング、トランザクション署名異常処理など）。'
    user_qualification = '2. ユーザー資格'
    ability_include = 'あなたは、18歳以上であり、完全な民事行為能力を有することを確認します。'
    ability_include_1 = 'お住まいの司法管轄区域では、暗号通貨および関連ハードウェアデバイスの使用が禁止されていません（例：中国本土のユーザーは、使用リスクを自己負担する必要があります）。'
    terms_update_infor = '3. 条項の更新と通知'
    update_infor_content = '私たちは、条項を一方的に変更する権利を留保します。改正内容は、公式ウェブサイトの公告欄で発表され、効力発生日は公告に準じます。サービスを継続して使用する場合、改正後の条項に同意したものとみなされます。同意しない場合、効力発生日までに書面で通知し、使用を中止してください。'

    wallet_buy_iterms = '二、 ハードウェアウォレットの購入条項'
    order_process = '1. 注文プロセス'
    payment_confirmation = '注文の支払いが成功した後（ブロックチェーンネットワークによる確認または銀行口座の入金を基準）、システムは24時間以内に状態を更新します。'
    inventory_shortage = '在庫不足：在庫が不足している場合、ユーザーは選択できます。'
    inventory_shortage_1 = 'a. 在庫補充を待つ（最大30日、期限を過ぎると自動的に返金されます）。'
    inventory_shortage_2 = 'b. 元の方法で完全に返金（暗号通貨注文は、支払い時の為替レートで計算されます）。'
    return_and_exchange_policy = '2. 返品・交換ポリシー'
    return_and_exchange_condi = '返品条件：'
    return_and_exchange_condi_con = 'a. 未アクティベートデバイスは、元の工場シールラベル（注文番号と一致）と完全なアクセサリー（USBケーブル、マニュアル、ニモニックカード）を保持する必要があります。b. 返品申請は、受領後7日以内に提出する必要があり、期限を過ぎると品質検査合格とみなされます。c. 返送送料は、ユーザーが負担します（品質問題を除く）。'
    warranty_scope = '保証範囲：'
    warranty_scope_1 = 'a. 安全チップの故障、ディスプレイの異常、ボタンの故障などの人的でない損傷をカバーします。'
    warranty_scope_2 = 'b. 購入証明（注文番号）と故障証明（動画はデバイスのSNコードと異常現象を明確に表示する必要があります）を提供する必要があります。'
    warranty_scope_3 = 'c. 人的損傷（水没、落下など）は保証範囲外であり、有償修理が可能です。'

    disclaimer = '三、免責事項'
    product_risk = '1. プロダクトリスク'
    physical_risk = '物理的リスク：'
    physical_risk_1 = 'a. デバイスは、高温（>60℃）、高湿度（>90% RH）、強磁場（>100mT）の環境では機能しない可能性があります。'
    physical_risk_2 = 'b. 長期間充電されていない場合、バッテリーが損傷する可能性があります（毎月1回充電することをお勧めします）。'
    supply_chain_risk = 'サプライチェーンリスク：'
    supply_chain_risk_1 = 'a. 公式ウェブサイトでは、偽造防止検証ツールを提供しており、デバイスのQRコードをスキャンして本物かどうかを確認できます。'
    supply_chain_risk_2 = 'b. デバイスが交換されたと疑われる場合、直ちにカスタマーサービスに連絡し、警察に報告してください。'
    service_interruption = '2. サービス中断'
    service_interruption_1 = '計画されたメンテナンスは、公式ウェブサイトの公告で48時間前に通知されます。緊急メンテナンスの場合、予告なしでサービスが一時停止される可能性があります。'
    service_interruption_2 = '不可抗力によるデータ損失については、賠償責任を負いません。'

    
    device_label = "デバイス名"
    device_title_firmware_version = 'ファームウェアバージョン'
    device_title_serial_number = 'シリアル番号'
    bluetooth_name = "ブルートゥース名"
    bluetooth_version = "ブルートゥースバージョン"
    firmware_title_1 = '1. デバイスのバッテリーが20%\n以上であることを確認してください'
    firmware_title_2 = '2. USB-Cケーブルを使用してデバイスをコンピュータに接続してください'
    firmware_title_3 = '3.「ファームウェアアップグレ\nード」をクリックしてください'
    firmware_title_caution = '警告'
    firmware_describe_caution = 'アップデート中は、USB接続が安定していることを確認してください'
    equipment_info = '機器情報'
    equipment_name = '機器名'
    equipment_version = '機器バージョン'

class Nft:
    nft_item ="{} アイテム"
    nft_items ="{} アイテム"
class Title:
    enter_old_pin = "古いPINコードを入力してください"
    enter_new_pin = "新しいPINコードを入力してください"
    enter_pin = "PINコードを入力してください"
    enter_pin_again = "もう一度PINコードを入力してください"
    select_language = "言語を選択"
    create_wallet = "ウォレットを作成"
    wallet = "ウォレットを作成"
    import_wallet = "지갑 가져오기"
    restore_wallet = "ウォレットを復元"
    wallet_is_ready = "ウォレットの準備ができました"
    select_word_count = "単語数を選択"
    wallet_security = "ウォレットのセキュリティ"
    pin_security = "PINのセキュリティヒント"
    mnemonic_security = "ニモニックのセキュリティヒント"
    backup_mnemonic = "ニモニックをバックアップ"
    enter_mnemonic = "ニモニックを入力してください"
    check_mnemonic = "ニモニックを確認"
    success = "成功"
    operate_success = "操作が成功しました"
    theme_success = "テーマが正常に切り替わりました"
    warning = "警告"
    error = "エラー"
    verified = "ニモニックのバックアップが完了しました"
    invalid_mnemonic = "無効なニモニック"
    pin_not_match = "PINコードが一致しません"
    check_recovery_mnemonic = "回復ニモニックを確認"
    mnemonic_not_match = "ニモニックが一致しません"
    power_off = "電源オフ"
    restart = "再起動"
    change_language = "言語を変更"
    wipe_device = "デバイスを消去"
    bluetooth_pairing = "ブルートゥースペアリング"
    address="{} アドレス"
    public_key = "{} 公開鍵"
    xpub = "{} XPub"
    transaction = "{} 取引"
    transaction_detail = "取引の詳細"
    confirm_transaction = "取引を確認"
    confirm_message = "メッセージを確認"
    signature = "署名結果"
    wrong_pin = "PINコードが間違っています"
    pin_changed = "PINコードが変更されました"
    pin_enabled = "PINコードが有効化されました"
    pin_disabled = "PINコードが無効化されました"
    unknown_token = "不明なトークン"
    view_data = "データを表示"
    sign_message = "{} メッセージの署名"
    verify_message = "{} メッセージの検証"
    typed_data = "{} 構造化データ"
    typed_hash = "{} 構造化ハッシュ"
    system_update = "システムアップデート"
    entering_boardloader = "ボードローダーに入る"
    remove_credential = "資格情報を削除"
    list_credentials = "資格情報を一覧表示"
    authorize_coinjoin = "CoinJoinを許可"
    multisig_address_m_of_n = "{} 多重署名アドレス\n({} of {})"
    u2f_register = "U2F 登録"
    u2f_unregister = "U2F 登録解除"
    u2f_authenticate = "U2F 認証"
    fido2_register = "FIDO2 登録"
    fido2_unregister = "FIDO2 登録解除"
    fido2_authenticate = "FIDO2 認証"
    finalize_transaction = "取引を完了"
    meld_transaction = "取引を統合"
    update_transaction = "取引を更新"
    high_fee = "高い料金"
    fee_is_high = "手数料が高すぎます"
    confirm_locktime = "ロックタイムを確認"
    view_transaction = "取引を表示"
    x_confirm_payment = "{} 支払いを確認"
    confirm_replacement = "取引の置き換えを確認"
    x_transaction = "{} 取引"
    x_joint_transaction = "{} 共同取引"
    change_label = "デバイス名を変更"
    enable_passphrase = "Passphraseを有効化"
    disable_passphrase = "Passphraseを無効化"
    passphrase_source = "Passphrase 入力設定"
    enable_safety_checks ="セキュリティチェックを有効化"
    disable_safety_checks ="セキュリティチェックを無効化"
    experiment_mode = "実験モード"
    set_as_homescreen = "ホーム画面として設定"
    get_next_u2f_counter = "次のU2Fカウンターを取得"
    set_u2f_counter = "U2Fカウンターを設定"
    encrypt_value = "データを暗号化"
    decrypt_value = "データを復号化"
    confirm_entropy = "エントロピーをエクスポート"
    memo = "メモ"
    import_credential = "資格情報をインポート"
    export_credential = "資格情報をエクスポート"
    asset = "資産"
    unimplemented = "未実装"
    invalid_data="無効なデータ形式"
    low_power = "電池が低い"
    collect_nft = "NFT を収集する"

class Text:
    tap_to_unlock = "クリックしてロックを解除"
    unlocking = "デバイスのロックを解除しています..."
    str_words = "#FFFFFF {}# 個の単語"
    backup_manual = "ニモニックを手動で記録し、安全な場所に保管してください"
    check_manual = "以下の単語を順番にクリックしてください"
    backup_verified = "ニモニックのバックアップが完了しました。他の人と共有しないでください"
    backup_invalid = "入力されたニモニックが正しくありません。バックアップしたニモニックを確認して再度試してください"
    pin_not_match = "入力されたPINコードが正しくありません。再度試してください"
    please_wait = "お待ちください"
    wiping_device = "デバイスのデータを消去しています..."
    create_wallet = "新しいニモニックを生成し、ウォレットを作成します"
    restore_wallet = "バックアップしたニモニックからウォレットを復元します"
    restore_mnemonic_match = "ニモニックが一致します。バックアップは正しいです"
    restore_success = "ウォレットの復元に成功しました"
    create_success = "ニモニックが正常にバックアップされ、ウォレットが作成されました"
    check_recovery_mnemonic = "ニモニックが完全に一致しているか確認してください"
    invalid_recovery_mnemonic = "入力されたニモニックは無効です。ニモニックを確認して再度試してください"
    check_recovery_not_match = "入力されたニモニックは有効ですが、デバイスのニモニックと一致しません"
    shutting_down = "シャットダウンしています..."
    restarting = "再起動しています..."
    never = "しない"
    second = "秒"
    seconds = "秒"
    minute = "分"
    minutes = "分"
    changing_language = "言語を変更しています\nこの設定を適用すると、デバイスが再起動します"
    change_pin = "デバイスを保護するために4~16桁のPINコードを設定してください"
    wipe_device = "デバイスを工場出荷状態に復元します。\n警告： これにより、デバイスのすべてのデータが消去されます。"
    wipe_device_check = [
        "デバイスを消去すると、すべてのデータが削除されます",
        "データを復元することはできません",
        "ニモニックをバックアップしました",
    ]
    wipe_device_success = "デバイスのデータが正常に消去されました \n デバイスを再起動してください..."
    bluetooth_pair = "デバイスでペアリングコードを入力してください"
    bluetooth_pair_failed = "ブルートゥースのペアリングに失敗しました"
    path = "派生パス:"
    chain_id = "チェーンID:"
    send = "送信"
    to = "宛先"
    amount = "金額"
    from_ = "送信者"
    receiver = "受信者"
    fee = "手数料"
    max_fee = "最大手数料"
    max_priority_fee_per_gas = "最大優先手数料"
    max_fee_per_gas = "ガス当たりの取引手数料上限"
    max_gas_limit = "最大ガス制限:"
    gas_unit_price = "ガス単価:"
    gas_price = "ガス価格"
    total = "合計金額"
    do_sign_this_transaction = "この{}取引に署名しますか？"
    transaction_signed = "取引が署名されました"
    address = 'アドレス:'
    public_key = "公開鍵:"
    xpub = "XPub:"
    unknown_tx_type = "不明な取引タイプ、入力データを確認してください"
    unknown_function = "未知の関数:"
    use_app_scan_this_signature = "ウォレットアプリで署名結果をスキャンしてください"
    internal_error = "内部エラー"
    tap_switch_to_airgap = "QRコードをタップしてAirgapアドレスを表示"
    tap_switch_to_receive = "QRコードをタップしてウォレットの受信アドレスを表示"
    incorrect_pin_times_left = "PINが正しくありません。残りの試行回数: {}"
    incorrect_pin_last_time = "PINが正しくありません。最後のチャンスです"
    wrong_pin = "入力されたPINコードが正しくありません"
    seedless = "シードがありません"
    backup_failed = "バックアップに失敗しました！"
    need_backup = "バックアップが必要です！"
    pin_not_set = "PINコードが設定されていません！"
    experimental_mode = "実験モード"
    pin_change_success = "PINコードが正常に変更されました"
    pin_enable_success = "PINコードが正常に有効化されました"
    pin_disable_success = "PINコードが正常に無効化されました"
    contract = "契約:"
    new_contract = "新規契約?"
    bytes_ = "{} バイト"
    message = "メッセージ:"
    no_message = "メッセージを含みません"
    contains_x_key = "{} キーを含む"
    array_of_x_type = "タイプ {} の配列 {}"
    do_sign_712_typed_data = "この構造化データ取引に署名しますか？"
    do_sign_typed_hash = "この構造化ハッシュ取引に署名しますか？"
    domain_hash = "ドメインハッシュ:"
    message_hash = "メッセージハッシュ:"
    switch_to_update_mode = "更新モードに切り替え"
    switch_to_boardloader = "ボードローダーモードに切り替え"
    list_credentials = "このデバイスに保存された資格情報をエクスポートしますか？"
    coinjoin_at_x = "以下のCoinjoin取引に参加しますか？:\n{}"
    signature_is_valid = "署名は有効です"
    signature_is_invalid = "署名は無効です"
    u2f_already_registered = "U2F はすでに登録されています"
    u2f_not_registered = "U2F は登録されていません"
    fido2_already_registered_x = "FIDO2 はすでに登録されています {}"
    fido2_verify_user = "FIDO2 ユーザー認証"
    device_already_registered_x = "デバイスはすでに登録されています {}"
    device_verify_user = "デバイスユーザー認証"
    fee_is_unexpectedly_high = "手数料が予想外に高すぎます"
    too_many_change_outputs = "釣り銭の出力が多すぎます"
    change_count = "おつり数量"
    locktime_will_have_no_effect = "ロックタイムは影響しません"
    confirm_locktime_for_this_transaction = "この取引のロックタイムを確認してください"
    block_height = "ブロック高さ"
    time = "時間"
    amount_increased = "金額が増加しました"
    amount_decreased = "金額が減少しました"
    fee_unchanged = "手数料は変わりませんでした"
    fee_increased = "手数料が増加しました"
    fee_decreased = "手数料が減少しました"
    your_spend = "あなたの支出"
    change_label_to_x = "ラベルを {} に変更"
    enable_passphrase = "Passphrase 暗号化を有効にしますか？"
    disable_passphrase = "Passphrase 暗号化を無効にしますか？"
    enable_passphrase_always = "常にデバイスでPassphraseを入力しますか？"
    revoke_enable_passphrase_always = "常にデバイスでPassphraseを入力する設定を取り消しますか？"
    auto_lock_x = "{} 後にデバイスを自動的にロックしますか？"
    enable_safety_checks = "厳格なセキュリティチェックを実行しますか？これにより、より包括的なセキュリティ保護が提供されます。"
    disable_safety_checks = "セキュリティチェックを無効にしますか？操作を続行する前に、この行為の潜在的なセキュリティリスクを理解してください。"
    enable_experiment_mode = "実験モードを有効にしますか？"
    set_as_homescreen = "ホーム画面を変更しますか？"
    replace_homescreen = "ホーム画面を置き換えますか？これにより、最も早くアップロードされた壁紙が削除されます。"
    confirm_replace_wallpaper = "ホーム画面の壁紙を置き換えますか？"
    get_next_u2f_counter = "次のU2Fカウンターを取得しますか？"
    set_u2f_counter_x = "U2Fカウンターを {} に設定しますか？"
    confirm_entropy = "エントロピーをエクスポートしますか？操作を続行する前に、何をしているかを十分に理解してください！"
    bandwidth = "帯域幅"
    energy = "エネルギー"
    sender = "送信者"
    recipient = "受信者"
    resource = "リソース"
    frozen_balance = "凍結された残高"
    unfrozen_balance = "解凍された残高"
    delegated_balance = "委任された残高"
    undelegated_balance = "委任解除された残高"
    you_are_freezing = "資産を凍結しています"
    you_are_unfreezing = "資産を解凍しています"
    you_are_delegating = "資産を委任しています"
    you_are_undelegating = "資産の委任を解除しています"
    duration = "持続時間"
    lock = "ロック"
    unlock = "ロック解除"
    all = "すべて"
    source = "ソース"
    tip = "ヒント"
    keep_alive = "継続的に実行"
    invalid_ur = "サポートされていないQRコードタイプです。再試行してください"
    sequence_number = "シーケンス番号"
    expiration_time = "有効期限"
    argument_x = "引数 #{}"
    low_power_message = "電池が {}% 残っています。\n充電してください"
    collect_nft = "この NFT を収集することを確認しますか？"
    replace_nft = "この NFT を収集しますか？ストレージの上限に達しており、最も古いアップロードされた NFT が削除されます。"

class Tip:
    swipe_down_to_close = "スワイプダウンで閉じる"

class Button:
    done = "完了"
    ok = "OK"
    confirm = "確認"
    reject = "拒否"
    next = "次へ"
    cancel = "キャンセル"
    redo = "再実行"
    continue_ = "続行"
    try_again = "再試行"
    power_off = "電源オフ"
    restart = "再起動"
    hold = "長押し"
    address = "アドレス"
    qr_code = "QRコード"
    view_detail = "詳細を表示"
    hold_to_sign = "長押しで署名"
    hold_to_wipe = "長押しで消去"
    receive = "受信アドレス"
    airgap = "エアギャップ"
    sign = "署名"
    verify = "検証"
    view_full_array = "完全な配列を表示"
    view_full_struct = "完全な構造を表示"
    view_full_message = "完全なメッセージを表示"
    view_data = "データを表示"
    view_more = "もっと表示"

class WalletSecurity:
    header = "ニモニックを紙に記録し、安全な場所に保管してください"
    tips = [
        {
            "level": "info",
            "msgs": [
                "#00001F ニモニックは安全に保管する必要があります#",
                "#18794E * 銀行の金庫に保管#",
                "#18794E * 保险庫に保管#",
                "#18794E * 複数の秘密の場所に保管#",
            ]
        },
        {
            "level": "warning",
            "msgs": [
                "#00001F 注意してください#",
                "#CD2B31 * ニモニックを覚えておいてください#",
                "#CD2B31 * 丧失しないでください#",
                "#CD2B31 * 他の人に教えないでください#",
                "#CD2B31 * オンラインに保存しないでください#",
                "#CD2B31 * コンピュータに保存しないでください#",
            ]
        },
    ]

class MnemonicSecurity:
    header = "ニモニックはウォレット資産を復元するためのフレーズです。ニモニックを持っているということは、あなたの資産を使用できるということです。適切に保管してください"

    tips = [
        "1. 環境の安全を確認し、見張りやカメラがないことを確認してください",
        "2. フレーズの正しい順序でニモニックをバックアップし、他の人と共有しないでください",
        "3. 安全な場所でオフラインでニモニックを保管してください。電子的な方法でバックアップしないでください。ネットワークにアップロードしないでください",
    ]

class PinSecurity:
    header = "PINコードは現在のデバイスにアクセスするためのパスワードです。以下のヒントに従って正しくPINコードを使用してください"
    tips = [
        "1. PINコードを設定または入力する際には、環境の安全を確認し、見張りやカメラがないことを確認してください",
        "2. 4~16桁の強力なPINコードを設定してください。連続または繰り返しの数字を使用しないでください",
        "3. PINコードの最大試行回数は10回で、10回連続で間違えるとデバイスがリセットされます",
        "4. PINコードを適切に保管してください。他の人に教えないでください",
    ]

class Solana:
    ata_reciver = "受信者(関連するトークンアカウント)"
    ata_sender = "送信者(関連するトークンアカウント)"
    source_owner = "取引の署名者"
    fee_payer = "手数料支払者"



