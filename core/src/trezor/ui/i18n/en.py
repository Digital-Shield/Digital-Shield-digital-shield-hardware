class App:
    account = "Account"
    scan = "Scan"
    nft = "NFT Gallery"
    guide = "Guide"
    security = "Security"
    setting = "Setting"

# Setting App
class Setting:
    bluetooth = "Bluetooth"
    language = "Language"
    vibration = "Vibration"
    brightness = "Brightness"
    auto_lock = "Auto Lock"
    auto_shutdown = "Auto Shutdown"
    animation = "Animation"
    wallpaper = "Wallpaper"
    power_off = "Power Off"
    restart = "Restart"

# Security App
class Security:
    change_pin = "Change PIN"
    backup_mnemonic = "Backup Mnemonic"
    check_mnemonic = "Check Mnemonic"
    wipe_device = "Wipe Device"

#### guide App
class Guide:
    about = "About Digit Shield"
    terms_of_use = 'Terms of Use'
    device_info = 'Device Info'
    firmware_update = 'Firmware Update'

    terms_title_terms_us = 'Digit Shield Terms of Use'
    terms_describe_terms_us = 'To access the full version of the TERMS OF USE ,please visit the following link:\n http://digitshield.com/terms'

    terms_title_product_services = 'Digit Shield Product & Services'
    terms_describe_product_services = 'Our harware wallet securely manages cryptocurrencies'

    terms_title_risks = 'Risks'
    terms_describe_risks = 'Be aware of the risks associated with  cryptocurrencies and technology vulnerabilities'

    terms_title_disclaimers = 'DISCLAIMERS'
    terms_describe_disclaimers = 'The information provided is not financial advice. Seek professional advice before making any decisions.'

    terms_title_contact_us = 'Contact Us'
    terms_describe_contact_us = 'If you have any questions or concerns, please email us at support@digitshield.com'

    device_label = "Label"
    device_title_firmware_version = 'Firmware Version'
    device_title_serial_number = 'Serial Number'
    bluetooth_name = "Bluetooth Name"
    bluetooth_version = "Bluetooth Version"

    firmware_title_1 = '1.Ensure that you Device has at least 20% battery life remaining.'
    firmware_title_2 = '2.Connect you Device to you computer using a USB-C cable'
    firmware_title_3 = '3.Click the Install Update button'
    firmware_title_caution = 'Caution'
    firmware_describe_caution = 'Do not unplug the USB cable while the installation process is underway.'
#### nft App
class Nft:
    nft_item ="{} 个展品"
    nft_items ="{} 个展品"
class Button:
    done = "Done"
    ok = "Ok"
    confirm = "Confirm"
    reject = "Reject"
    next = "Next"
    redo = "Re-generate"
    continue_ = "Continue"
    cancel = "Cancel"
    try_again = "Try Again"
    power_off = "Power Off"
    restart = "Restart"
    hold = "Keep\nhold"
    address = "Address"
    qr_code = "QR Code"
    view_detail = "View detail"
    hold_to_sign = "Hold to\nsign"
    hold_to_wipe = "Hold to\nwipe"
    receive = "Receive"
    airgap = "Airgap"
    sign = "Sign"
    verify = "Verify"
    view_full_array = "View full array"
    view_full_struct = "View full struct"
    view_full_message = "View full message"
    view_data = "View data"
    view_more = "View more"

class Title:
    enter_old_pin = "Enter Old PIN"
    enter_new_pin = "Enter New PIN"
    enter_pin = "Enter PIN"
    enter_pin_again = "Enter PIN again"
    select_language = "Language"
    create_wallet = "Create Wallet"
    restore_wallet = "Restore Wallet"
    wallet_is_ready = "Wallet is ready"
    select_word_count = "Select Word Count"
    wallet_security = "Wallet security"
    pin_security = "PIN security"
    mnemonic_security = "Confirm backup"
    backup_mnemonic = "Backup Mnemonic"
    check_mnemonic = "Check Mnemonic"
    enter_mnemonic = "Enter Mnemonic"
    success = "Success"
    warning = "Warning"
    error = "Error"
    verified = "Verified"
    invalid_mnemonic = "Invalid Mnemonic"
    pin_not_match = "PIN Not Match"
    check_recovery_mnemonic = "Check Recovery Mnemonic"
    mnemonic_not_match = "Mnemonic Not Match"
    power_off = "Power Off"
    restart = "Restart"
    change_language = "Change Language"
    wipe_device = "Wipe Device"
    bluetooth_pairing = "Bluetooth Pairing"
    address = "{} address"
    public_key = "{} public key"
    xpub = "{} xpub"
    transaction = "{} Transaction"
    transaction_detail = "Detail"
    confirm_transaction = "Confirm Transaction"
    confirm_message = "Confirm Message"
    signature = "Signature"
    wrong_pin = "Wrong PIN"
    pin_changed = "PIN Changed"
    pin_enabled = "PIN Enabled"
    pin_disabled = "PIN Disabled"
    unknown_token = "Unknown Token"
    view_data = "View Data"
    sign_message = "{} sign message"
    verify_message = "{} verify message"
    typed_data = "{} typed data"
    typed_hash = "{} typed hash"
    system_update = "System Update"
    entering_boardloader = "Entering Boardloader"
    remove_credential = "Remove Credential"
    list_credentials = "List Credentials"
    authorize_coinjoin = "Authorize CoinJoin"
    multisig_address_m_of_n = "{} Multisig Address\n({} of {})"
    u2f_register = "U2F Register"
    u2f_unregister = "U2F Unregister"
    u2f_authenticate = "U2F Authenticate"
    fido2_register = "FIDO2 Register"
    fido2_unregister = "FIDO2 Unregister"
    fido2_authenticate = "FIDO2 Authenticate"
    finalize_transaction = "Finalize Transaction"
    meld_transaction = "Meld Transaction"
    update_transaction = "Update Transaction"
    high_fee = "High Fee"
    confirm_locktime = "Confirm locktime"
    view_transaction = "View Transaction"
    x_confirm_payment = "{} confirm payment"
    confirm_replacement = "Confirm replacement"
    x_transaction = "{} transaction"
    x_joint_transaction = "{} joint transaction"
    change_label = "Change Label"
    enable_passphrase = "Enable Passphrase"
    disable_passphrase = "Disable Passphrase"
    passphrase_source = "Passphrase Source"
    enable_safety_checks = "Enable Safety Checks"
    disable_safety_checks = "Disable Safety Checks"
    experimental_mode =  "Experimental mode",
    set_as_homescreen = "Set as homescreen"
    get_next_u2f_counter = "Get next U2F counter"
    set_u2f_counter = "Set U2F counter"
    encrypt_value = "Encrypt Value"
    decrypt_value = "Decrypt Value"
    confirm_entropy = "Confirm entropy"
    memo = "Memo"
    import_credential = "Import Credential"
    export_credential = "Export Credential"
    asset = "Asset"
    unimplemented = "Unimplemented"


class Tip:
    swipe_down_to_close = "Swipe down to close"
class Text:
    tap_to_unlock = "Tap to unlock"
    unlocking = "Unlocking device ..."
    str_words = "#18794E {}# words"
    backup_manual = "write down mnemonic and store it safely"
    check_manual = "click mnemonic in the correct order"
    backup_verified = "Your mnemonic has been backed up. Please store it offline in a safe place and never share it with anyone."
    backup_invalid = "The mnemonic you entered is invalid. Please check your mnemonic, and try again."
    pin_not_match = "The PIN you entered does not match. Please try again."
    please_wait = "Please wait"
    wiping_device = "Wiping device ..."
    create_wallet = "Create wallet a new wallet from generated mnemonic"
    restore_wallet = "Import your stored recovery phrase to restore existing wallet"
    restore_mnemonic_match = "The recovery mnemonic you entered is matched, your backup is correct."
    restore_success = "You have successfully recovered your wallet."
    create_success = "You have backup mnemonic successfully. The wallet has been created."
    check_recovery_mnemonic = "Check your backup, make sure it is exactly matched the recovery mnemonic stored on device."
    invalid_recovery_mnemonic = "The recovery phrase you entered is invalid. Check your backup and try again."
    check_recovery_not_match = "The entered recovery phrase is valid but does not match the one in the device."
    shutting_down = "Shutting down ..."
    restarting = "Restarting ..."
    never = "Never"
    second = "second"
    seconds = "seconds"
    minute = "minute"
    minutes = "minutes"
    changing_language = "You are changing language\n Applying this setting will restart the device"
    change_pin = "Please set a length of 4-16 characters strong PIN code, protect the device"
    wipe_device = "To remove all data from your device, you can reset your device to factory settings."
    wipe_device_check = [
        "wipe device will erase all data",
        "Data can't be recovered",
        "Have backup mnemonic",
    ]
    wipe_device_success = "Device wiped successfully\n Restarting the device ..."
    bluetooth_pair = "Please input the code at your pairing device"
    bluetooth_pair_failed = "Bluetooth pairing failed"
    path = "Path:"
    chain_id = "Chain ID:"
    send = "Send"
    to = "To:"
    amount = "Amount:"
    from_ = "From:"
    receiver = "Receiver:"
    fee = "Fee: "
    max_fee = "Max fee:"
    max_priority_fee_per_gas = "Max priority fee per gas:"
    max_fee_per_gas = "Max fee per gas:"
    gas_price = "Price:"
    total = "Total:"
    do_sign_this_transaction = "Do you want to sign this {} transaction?"
    transaction_signed = "Transaction signed successfully"
    address = 'Address:'
    public_key = 'Public key:'
    xpub = "XPub:"
    unknown_tx_type = "Unknown transaction type, please check input data"
    use_app_scan_this_signature = "Please use your wallet scan the signature"
    internal_error = "Internal error"
    tap_switch_to_airgap = "Tap QRCode to show airgaped address"
    tap_switch_to_receive = "Tap QRCode to show receive address"
    incorrect_pin_times_left = "Incorrect PIN, {} attempts left"
    incorrect_pin_last_time = "Incorrect PIN, this is your last attempt"
    wrong_pin = "The PIN you entered is incorrect."
    seedless = "Seedless"
    backup_failed = "Backup failed!"
    need_backup = "Need backup!"
    pin_not_set = "PIN not set!"
    experimental_mode = "Experimental Mode"
    pin_change_success = "You have successfully changed your PIN"
    pin_enable_success = "You have successfully enabled your PIN"
    pin_disable_success = "You have successfully disabled your PIN"
    contract = "Contract:"
    new_contract = "New Contract?"
    bytes_ = "{} bytes"
    message = "Message:"
    no_message = "No message field"
    contains_x_key = "Contains {} key"
    array_of_x_type = "Array of {} {}"
    do_sign_712_typed_data = "Do you want to sign this typed data?"
    do_sign_typed_hash = "Do you want to sign this typed hash?"
    domain_hash = "Domain Hash:"
    message_hash = "Message Hash:"
    switch_to_update_mode = "Switch to update mode"
    switch_to_boardloader = "Switch to board loader mode"
    list_credentials = "Do you want to export information about the resident credentials stored on this device?"
    coinjoin_at_x = "Do you really want to take part in a CoinJoin transaction at:\n{}"
    signature_is_valid = "The signature is valid"
    signature_is_invalid = "The signature is invalid"
    u2f_already_registered = "U2F already registered"
    u2f_not_registered = "U2F not registered"
    fido2_already_registered_x = "FIDO2 already registered with {}"
    fido2_verify_user = "FIDO2 verify user"
    device_already_registered_x = "Device already registered with {}"
    device_verify_user = "Device verify user"
    fee_is_unexpectedly_high = "Fee is unexpectedly high"
    too_many_change_outputs= "There are too many change outputs"
    change_count = "Change Count:"
    locktime_will_have_no_effect = "Locktime will have no effect"
    confirm_locktime_for_this_transaction = "Confirm locktime for this transaction"
    block_height = "Block Height:"
    time = "Time:"
    amount_increased = "Amount increased by:"
    amount_decreased = "Amount decreased by:"
    fee_unchanged = "Fee unchanged:"
    fee_increased = "Fee increased by:"
    fee_decreased = "Fee decreased by:"
    your_spend = "Your spend:"
    change_label_to_x = "Change label to {}"
    enable_passphrase = "Do you want to enable passphrase encryption?"
    disable_passphrase = "Do you want to disable passphrase encryption?"
    enable_passphrase_always = "Do you want to enter Passphrase always on this device?"
    revoke_enable_passphrase_always = "Do you want to revoke the setting of always enter Passphrase on the device?"
    auto_lock_x = "Do you really want to auto-lock your device after {}?"
    enable_safety_checks = "Do you want to enforce strict safety checks? It will provide full security protection."
    disable_safety_checks = "Are you sure to disable safety checks? Continue only if you know what you are doing!"
    enable_experimental_features = "Enable experimental features?",
    set_as_homescreen = "Do you want to change the homescreen?"
    replace_homescreen = "Do you want to change the homescreen? This will delete the oldest uploaded wallpaper."
    get_next_u2f_counter = "Do you want to get the next U2F counter?"
    set_u2f_counter_x = "Do you want to set the U2F counter to {}?"
    confirm_entropy = "Do you want to export entropy? Continue only if you know what you are doing!"
    bandwidth = "Bandwidth:"
    energy = "Energy:"
    sender = "Sender:"
    recipient = "Recipient:"
    resource = "Resource:"
    frozen_balance = "Frozen Balance:"
    unfrozen_balance = "Unfrozen Balance:"
    delegated_balance = "Delegate Balance:"
    undelegated_balance = "UnDelegate Balance:"
    you_are_freezing = "You are freezing asset"
    you_are_unfreezing = "You are unfreezing asset"
    you_are_delegating = "You are delegating asset"
    you_are_undelegating = "You are undelegating asset"
    duration = "Duration:"
    lock = "Lock"
    unlock = "Unlock"

class WalletSecurity:
    header = "Write down mnemonic on a piece of paper and store it in a safe place."
    tips = [
        {
            "level": "info",
            "msgs": [
                "#00001F Mnemonic need to be stored in a safe place#",
                "#18794E * In a bank vault#",
                "#18794E * In a safe deposit box#",
                "#18794E * In multiple secret locations#",
            ]
        },
        {
            "level": "warning",
            "msgs": [
                "#00001F Be careful#",
                "#CD2B31 * Never share mnemonic with anyone#",
                "#CD2B31 * Never store mnemonic in a public place#",
                "#CD2B31 * Never store mnemonic in an unencrypted device#",
                "#CD2B31 * Never store mnemonic on a computer#",
                "#CD2B31 * Never store mnemonic on the internet#",
            ]
        },
    ]

class PinSecurity:
    header = "PIN is a password used to access your device. Please keep it safe."
    tips = [
        "1. Please check that the environment is safe and there are no bystanders or cameras.",
        "2. Please set a length of 4-16 characters strong PIN code.",
        "3. The maximum number of PIN attempts is 10. If you enter the wrong PIN 10 times, the device will be reset.",
        "4. Please keep your PIN code safe and never share it with anyone."
    ]

class MnemonicSecurity:
    header = "A mnemonic is a set of words used to recover a wallet. Having the mnemonic allows access to your assets. Please keep it safe."

    tips = [
        "1. Please check that the environment is safe and there are no bystanders or cameras.",
        "2. Please backup your mnemonic in the correct order and never share your mnemonic with anyone.",
        "3. Please save the mnemonic offline in a safe place, never back up the mnemonic electronically, and never upload it online.",
    ]

class Solana:
    ata_reciver = "Reciver(ATA)"
    ata_sender = "Sender(ATA)"
    source_owner = "Source Owner"
    fee_payer = "Fee Payer"
