class App:
    account = "Account"
    scan = "Scan Transactions"
    nft = "NFT Gallery"
    guide = "User Guide"
    security = "Security"
    setting = "Settings"

# Setting App
class Setting:
    bluetooth = "Bluetooth"
    language = "Language"
    vibration = "Haptic Feedback"
    brightness = "Brightness"
    auto_lock = "Auto Lock"
    auto_shutdown = "Auto Shutdown"
    animation = "Transition Animation"
    wallpaper = "Wallpaper"
    power_off = "Power Off"
    restart = "Restart"

# Security App
class Security:
    change_pin = "Change PIN"
    backup_mnemonic = "Backup Recovery Phrase"
    check_mnemonic = "Verify Recovery Phrase"
    wipe_device = "Factory Reset"

#### guide App
class Guide:
    about = "About Digit Shield"
    terms_of_use = 'Terms of Service'
    device_info = 'Device Info'
    firmware_update = 'Firmware Update'

    terms_title_terms_us = 'Digit Shield Terms of Service'
    terms_describe_terms_us = 'For complete terms of service, visit:\nhttp://digitshield.com/terms'

    terms_title_product_services = 'Products & Services'
    terms_describe_product_services = 'Our hardware wallet securely manages your crypto assets'

    terms_title_risks = 'Risk Disclosure'
    terms_describe_risks = 'Please be aware of risks associated with crypto and technical vulnerabilities.'

    terms_title_disclaimers = 'Disclaimer'
    terms_describe_disclaimers = 'This information is not financial advice. Seek professional advice before making decisions.'

    terms_title_contact_us = 'Contact Us'
    terms_describe_contact_us = 'For questions or concerns, email us at support@digitshield.com'

    accept_tems = 'I. Acceptance of Terms'
    use_range = '1. Scope of Application'
    range_include = 'These terms apply to all services provided through the Digital Shield Wallet, including:'
    range_include_1 = 'Purchase, activation, and after-sales service of hardware wallets; Download, installation, and use of Digital Shield mobile applications (Android/iOS/Goolg); Firmware upgrade services (including security patches and feature enhancement versions); Multi-chain digital asset management (supporting storage and transfer of over 3000 tokens such as BTC, ETH, etc.); Technical support (device fault troubleshooting, transaction signature anomaly handling, etc.).'
    user_qualification = '2. User Qualification'
    ability_include = 'You confirm that you are at least 18 years old and have full civil capacity;'
    ability_include_1 = 'The jurisdiction where you are located does not prohibit the use of cryptocurrency and related hardware devices (for example, mainland China users need to bear the risk of use themselves);'
    terms_update_infor = '3. Terms Update and Notification'
    update_infor_content = 'We reserve the right to unilaterally modify the terms. The revised content will be published in the official website announcement column, and the effective date will be based on the announcement. If you continue to use the services, it is deemed that you accept the revised terms; If you disagree, you should notify in writing and terminate the use before the effective date.'

    wallet_buy_iterms = 'II. Hardware Wallet Purchase Terms'
    order_process = '1. Order Process'
    payment_confirmation = 'Payment Confirmation: After the order payment is successful (confirmed by the blockchain network or bank account), the system will update the status within 24 hours;'
    inventory_shortage = 'Inventory Shortage: If the inventory is insufficient, users can choose:'
    inventory_shortage_1 = 'a. Wait for restocking (up to 30 days, automatic refund if overdue);'
    inventory_shortage_2 = 'b. Full refund via the original route (cryptocurrency orders are calculated at the exchange rate at the time of payment).'
    return_and_exchange_policy = '2. Return and Exchange Policy'
    return_and_exchange_condi = 'Return Conditions:'
    return_and_exchange_condi_con = 'a. Unactivated devices need to retain the original factory seal label (number consistent with the order) and complete accessories (USB cable, manual, mnemonic card); b. Return applications must be submitted within 7 days after receipt, overdue will be deemed as qualified acceptance; c. Return shipping costs are borne by the user (except for quality issues).'
    warranty_scope = 'Warranty Scope:'
    warranty_scope_1 = 'a. Covers non-human damage such as security chip failure, abnormal screen display, and button malfunction;'
    warranty_scope_2 = 'b. Purchase certificate (order number) and fault proof (videos must clearly show the device SN code and abnormal phenomena) need to be provided;'
    warranty_scope_3 = 'c. Human damage (such as water ingress, falling) is not covered by the warranty, paid maintenance is available.'

    disclaimer = 'III. Disclaimer'
    product_risk = '1. Product Risk'
    physical_risk = 'Physical Risk:'
    physical_risk_1 = 'a. The device may fail in environments with high temperatures (>60℃), high humidity (>90% RH), and strong magnetic fields (>100mT);'
    physical_risk_2 = 'b. Long-term non-charging may cause battery damage (it is recommended to charge once a month).'
    supply_chain_risk = 'Supply Chain Risk:'
    supply_chain_risk_1 = 'a. The official website provides anti-counterfeiting verification tools, scanning the device QR code can verify authenticity;'
    supply_chain_risk_2 = 'b. If you suspect the device has been tampered with, you should immediately contact customer service and report to the police.'
    service_interruption = '2. Service Interruption'
    service_interruption_1 = 'Planned maintenance will be notified through the official website announcement 48 hours in advance, emergency maintenance may suspend services without prior notice;'
    service_interruption_2 = 'We do not assume compensation responsibility for data loss due to force majeure factors.'

    device_label = "Device Name"
    device_title_firmware_version = 'Firmware Version'
    device_title_serial_number = 'Serial Number'
    bluetooth_name = "Bluetooth Name"
    bluetooth_version = "Bluetooth Version"

    firmware_title_1 = '1.Ensure device battery >20%'
    firmware_title_2 = '2.Connect device to computer via USB-C'
    firmware_title_3 = "3.Click 'Firmware Update'"
    firmware_title_caution = 'Warning'
    firmware_describe_caution = 'Maintain USB connection during update'
    equipment_info = 'Equipment information'
    equipment_name = 'Equipment name'
    equipment_version = 'Equipment version'
#### nft App
class Nft:
    nft_item ="{} item"
    nft_items ="{} items"
class Button:
    done = "Done"
    ok = "OK"
    confirm = "Confirm"
    reject = "Reject"
    next = "Next"
    redo = "Regenerate"
    continue_ = "Continue"
    cancel = "Cancel"
    try_again = "Try again"
    power_off = "Power Off"
    restart = "Restart"
    hold = "Keep\nhold"
    address = "Address"
    qr_code = "QR Code"
    view_detail = "View Details"
    hold_to_sign = "Hold to\nsign"
    hold_to_wipe = "Hold to\nwipe"
    receive = "Receive Address"
    airgap = "Airgap"
    sign = "Sign"
    verify = "Verify"
    view_full_array = "View Full Array"
    view_full_struct = "View Full Structure"
    view_full_message = "View Full Message"
    view_data = "View Data"
    view_more = "View More"

class Title:
    enter_old_pin = "Enter Current PIN"
    enter_new_pin = "Enter New PIN"
    enter_pin = "Enter PIN"
    enter_pin_again = "Re-enter PIN"
    select_language = "Language"
    create_wallet = "Create Wallet"
    wallet = "Wallet"
    import_wallet = "Import Wallet"
    restore_wallet = "Restore Wallet"
    wallet_is_ready = "Wallet Ready"
    select_word_count = "Select Recovery Phrase Length"
    wallet_security = "Wallet Security"
    pin_security = "PIN Security Hint"
    mnemonic_security = "Recovery Phrase Security Hint"
    backup_mnemonic = "Backup Recovery Phrase"
    check_mnemonic = "Verify Recovery Phrase"
    enter_mnemonic = "Enter Recovery Phrase"
    success = "Success"
    operate_success = "Operation Successful"
    theme_success = "Theme Switched Successfully"
    warning = "Warning"
    error = "Error"
    verified = "Backup Complete"
    invalid_mnemonic = "Invalid Recovery Phrase"
    pin_not_match = "PIN Mismatch"
    check_recovery_mnemonic = "Verify Recovery Phrase"
    mnemonic_not_match = "Recovery Phrase Mismatch"
    power_off = "Power Off"
    restart = "Restart"
    change_language = "Change Language"
    wipe_device = "Factory Reset"
    bluetooth_pairing = "Bluetooth Pairing"
    address = "{} Address"
    public_key = "{} Public Key"
    xpub = "{} XPub"
    transaction = "{} Transaction"
    transaction_detail = "Transaction Details"
    confirm_transaction = "Confirm Transaction"
    confirm_message = "Confirm Message"
    signature = "Signature Details"
    wrong_pin = "Incorrect PIN"
    pin_changed = "PIN Changed"
    pin_enabled = "PIN Enabled"
    pin_disabled = "PIN Disabled"
    unknown_token = "Unknown Token"
    view_data = "View Data"
    sign_message = "{} Message Signing"
    verify_message = "{} Message Verification"
    typed_data = "{} Structured Data"
    typed_hash = "{} Structured Hash"
    system_update = "System Update"
    entering_boardloader = "Entering Boardloader"
    remove_credential = "Remove Credential"
    list_credentials = "List Credentials"
    authorize_coinjoin = "Authorize CoinJoin"
    multisig_address_m_of_n = "{} Multisig Address\n({} of {})"
    u2f_register = "U2F Registration"
    u2f_unregister = "U2F Deregistration"
    u2f_authenticate = "U2F Authentication"
    fido2_register = "FIDO2 Registration"
    fido2_unregister = "FIDO2 Deregistration"
    fido2_authenticate = "FIDO2 Authentication"
    finalize_transaction = "Finalize Transaction"
    meld_transaction = "Merge Transaction"
    update_transaction = "Update Transaction"
    high_fee = "High Fee"
    fee_is_high = "The handling fee is too high" 
    confirm_locktime = "Confirm Locktime"
    view_transaction = "View Transaction"
    x_confirm_payment = "{} Confirm Payment"
    confirm_replacement = "Confirm Replacement Tx"
    x_transaction = "{} Transaction"
    x_joint_transaction = "{} Joint Transaction"
    change_label = "Edit Device Name"
    enable_passphrase = "Enable Passphrase"
    disable_passphrase = "Disable Passphrase"
    passphrase_source = "Passphrase Input Settings"
    enable_safety_checks = "Enable Safety Checks"
    disable_safety_checks = "Disable Safety Checks"
    experimental_mode =  "Experimental Mode",
    set_as_homescreen = "Set as Homescreen"
    get_next_u2f_counter = "Get U2F Counter"
    set_u2f_counter = "Set U2F Counter"
    encrypt_value = "Encrypt Data"
    decrypt_value = "Decrypt Data"
    confirm_entropy = "Export Entropy"
    memo = "Memo"
    import_credential = "Import Credential"
    export_credential = "Export Credential"
    asset = "Asset"
    unimplemented = "Not Implemented"
    invalid_data = "Invalid Data Format"
    low_power = "Low Battery"
    collect_nft = "Collect NFT"

class Tip:
    swipe_down_to_close = "Swipe Down to Close"
class Text:
    tap_to_unlock = "Tap to Unlock"
    unlocking = "Unlocking device..."
    str_words = "#FFFFFF {}# words"
    backup_manual = "Manually write down recovery phrase and store securely"
    check_manual = "Tap words below in correct order"
    backup_verified = "Recovery phrase backup complete. Store securely and never share"
    backup_invalid = "Invalid recovery phrase. Please verify and try again"
    pin_not_match = "Incorrect PIN. Please try again"
    please_wait = "Please wait"
    wiping_device = "Wiping device data..."
    create_wallet = "Generate a new recovery phrase to create wallet"
    restore_wallet = "Restore wallet from your backup phrase"
    restore_mnemonic_match = "Recovery phrase matches. Backup is valid"
    restore_success = "Wallet Restored Successfully"
    create_success = "Recovery phrase backed up successfully. Wallet created"
    check_recovery_mnemonic = "Verify your recovery phrase matches exactly"
    invalid_recovery_mnemonic = "Invalid recovery phrase. Please verify and try again"
    check_recovery_not_match = "Valid recovery phrase but doesn't match device"
    shutting_down = "Shutting down..."
    restarting = "Restarting..."
    never = "Never"
    second = "Second"
    seconds = "Seconds"
    minute = "Minute"
    minutes = "Minutes"
    changing_language = "Changing language\nDevice will restart"
    change_pin = "Set a 4-16 digit PIN to secure your device"
    wipe_device = "Reset device to factory settings.\nWARNING: This erases ALL data."
    wipe_device_check = [
        "Factory reset erases all data",
        "Data cannot be recovered",
        "Recovery phrase is backed up",
    ]
    wipe_device_success = "Device wiped successfully\nRestarting..."
    bluetooth_pair = "Enter pairing code on your device"
    bluetooth_pair_failed = "Bluetooth Pairing Failed"
    path = "Derivation Path:"
    chain_id = "Chain ID:"
    send = "Send"
    to = "To"
    amount = "Amount"
    from_ = "From"
    receiver = "Recipient"
    fee = "Fee"
    max_fee = "Max Fee"
    max_priority_fee_per_gas = "Max Priority Fee"
    max_fee_per_gas = "Max Fee per Gas"
    max_gas_limit = "Max gas limit:"
    gas_unit_price= "Gas unit price:"
    gas_price = "Gas Price"
    total = "Total"
    do_sign_this_transaction = "Sign this{}transaction?"
    transaction_signed = "Transaction signed"
    address = 'Address:'
    public_key = 'Public Key:'
    xpub = "XPub:"
    unknown_tx_type = "Unknown transaction type. Check input data"
    unknown_function = "Unknown function:"
    use_app_scan_this_signature = "Scan signature with Digital Shield app"
    internal_error = "Internal Error"
    tap_switch_to_airgap = "Tap QR code to show Airgap address"
    tap_switch_to_receive = "Tap QR code to show receive address"
    incorrect_pin_times_left = "Incorrect PIN. {} attempts remaining"
    incorrect_pin_last_time = "Incorrect PIN.Last attempt"
    wrong_pin = "Incorrect PIN"
    seedless = "No seed phrase detected"
    backup_failed = "Backup Failed!"
    need_backup = "Backup Required!"
    pin_not_set = "No PIN Set!"
    experimental_mode = "Experimental Mode"
    pin_change_success = "PIN Changed Successfully"
    pin_enable_success = "PIN Enabled Successfully"
    pin_disable_success = "PIN Disabled Successfully"
    contract = "Contract:"
    new_contract = "New contract?"
    bytes_ = "{} bytes"
    message = "Message:"
    no_message = "No message included"
    contains_x_key = "Contains {} key(s)"
    array_of_x_type = "Array type {} {}"
    do_sign_712_typed_data = "Sign this structured data transaction？"
    do_sign_typed_hash = "Sign this structured hash transaction?"
    domain_hash = "Domain Hash:"
    message_hash = "Message  Hash:"
    switch_to_update_mode = "Switch to Update Mode"
    switch_to_boardloader = "Switch to Boardloader Mode"
    list_credentials = "Export credentials stored on this device？"
    coinjoin_at_x = "participate in the following CoinJoin transaction:\n{}?"
    signature_is_valid = "Valid Signature"
    signature_is_invalid = "Signature Invalid"
    u2f_already_registered = "U2F Already Registered"
    u2f_not_registered = "U2F Not Registered"
    fido2_already_registered_x = "FIDO2 Registered {}"
    fido2_verify_user = "FIDO2 Verify User"
    device_already_registered_x = "Device Registered {}"
    device_verify_user = "Device-Verified User"
    fee_is_unexpectedly_high = "Unexpectedly High Transaction Fee"
    too_many_change_outputs= "There are too many change outputs"
    change_count = "Change Output Count"
    locktime_will_have_no_effect = "Locktime Will Have No Effect"
    confirm_locktime_for_this_transaction = "Confirm Transaction Locktime"
    block_height = "Block Height"
    time = "Time"
    amount_increased = "Amount Increased"
    amount_decreased = "Amount Decreased"
    fee_unchanged = "Fee Unchanged"
    fee_increased = "Fee Increased"
    fee_decreased = "Fee Decreased"
    your_spend = "Your Spend"
    change_label_to_x = "Change Label to {}"
    enable_passphrase = "Enable Passphrase Encryption?"
    disable_passphrase = "Disable Passphrase Encryption?"
    enable_passphrase_always = "Always Enter Passphrase On Device?"
    revoke_enable_passphrase_always = "Revoke On-Device Passphrase Entry?"
    auto_lock_x = "Auto-Lock Device After {}?"
    enable_safety_checks = "Enable strict safety checks for enhanced security?"
    disable_safety_checks = "Disable safety checks? Understand security risks."
    experimental_mode = "Experimental Mode"
    set_as_homescreen = "Set as Homescreen?"
    replace_homescreen = "Replace Homescreen? Previous wallpaper will be deleted."
    confirm_replace_wallpaper = "Are you sure you want to replace the wallpaper of the home screen?"
    get_next_u2f_counter = "Get Next U2F Counter?"
    set_u2f_counter_x = "Set U2F Counter to ?"
    confirm_entropy = "Export Entropy? Understand the risks before proceeding."
    bandwidth = "Bandwidth"
    energy = "Energy"
    sender = "Sender"
    recipient = "Recipient"
    resource = "Resource"
    frozen_balance = "Frozen Balance"
    unfrozen_balance = "Unfrozen Balance"
    delegated_balance = "Delegated Balance"
    undelegated_balance = "Undelegated Balance"
    you_are_freezing = "Freezing Assets"
    you_are_unfreezing = "Unfreezing Assets"
    you_are_delegating = "Delegating Assets"
    you_are_undelegating = "Undelegating Assets"
    duration = "Duration"
    lock = "Lock"
    unlock = "Unlock"
    all = "All"
    source = "Source"
    tip = "Tip"
    keep_alive = "Keep Alive"
    invalid_ur = "Unsupported QR Type. Please Retry."
    sequence_number = "Serial Number"
    expiration_time = "Expiration Time"
    argument_x = "Argument #{}"
    low_power_message = "Battery at {}%\nPlease charge"
    collect_nft = "Are you sure collect the NFT?"
    replace_nft = "Do you want to collect this NFT? You have reach the storage limit, this will remove the oldest uploaded NFT."

class WalletSecurity:
    header = "Write recovery phrase on paper and store securely"
    tips = [
        {
            "level": "info",
            "msgs": [
                "#00001F Securely store your recovery phrase#",
                "#18794E * Store in a bank safety deposit box#",
                "#18794E * Store it in a home safe#",
                "#18794E * Store in multiple secret locations#",
            ]
        },
        {
            "level": "warning",
            "msgs": [
                "#00001F Critical Warnings#",
                "#CD2B31 * Memorize recovery phrase#",
                "#CD2B31 * Never lose it#",
                "#CD2B31 * Never share it#",
                "#CD2B31 * Never store it online#",
                "#CD2B31 * Never store it on your computer#",
            ]
        },
    ]

class MnemonicSecurity:
    header = "Recovery phrase restores wallet assets. Whoever possesses it controls your assets. Store securely."

    tips = [
        "1. Ensure private environment without observers/cameras",
        "2. Backup words in correct order. Never share your phrase",
        "3. Store offline securely. Never backup digitally or upload online",
    ]

class PinSecurity:
    header = "PIN authorizes device access. Follow these security practices:"
    tips = [
        "1.Ensure your environment is safe when setting or entering your PIN — avoid bystanders or surveillance."
        "2.Choose a strong PIN (4–16 digits). Avoid patterns like repeated or sequential numbers.",
        "3.You have up to 10 attempts. The device will reset after 10 incorrect entries.",
        "4.Keep your PIN confidential. Never share it with anyone.",
    ]

class Solana:
    ata_reciver = "Receiver (Associated Token Account)"
    ata_sender = "Sender (Associated Token Account)"
    source_owner = "Transaction Signer"
    fee_payer = "Fee Payer"