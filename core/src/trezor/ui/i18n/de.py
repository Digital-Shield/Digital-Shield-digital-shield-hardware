class App:
    account = "Konto"
    scan = "Transaktion scannen"
    nft = "NFT-Galerie"
    guide = "Anleitung"
    security = "Sicherheit"
    setting = "Einstellungen"


#### Setting App
class Setting:
    bluetooth = "Bluetooth"
    language = "Sprache"
    vibration = "Vibrationsfeedback"
    brightness = "Bildschirmhelligkeit"
    auto_lock = "Automatische Sperre"
    auto_shutdown = "Automatisches Herunterfahren"
    animation = "Übergangsanimation"
    wallpaper = "Hintergrundbild"
    power_off = "Herunterfahren"
    restart = "Neustart"

#### Security App
class Security:
    change_pin = "PIN ändern"
    backup_mnemonic = "Mnemonic sichern"
    check_mnemonic = "Mnemonic prüfen"
    wipe_device = "Gerät zurücksetzen"

#### guide App
class Guide:
    about = "Über Digital Shield"
    terms_of_use = 'Nutzungsbedingungen'
    device_info = 'Geräteinformationen'
    firmware_update = 'Firmware-Update'
    terms_title_terms_us = 'Digit Shield Nutzungsbedingungen'
    terms_describe_terms_us = 'Die vollständige Version der Nutzungsbedingungen finden Sie unter folgendem Link:\n http://digitshield.com/terms'

    terms_title_product_services = 'Digit Shield Produkte und Dienstleistungen'
    terms_describe_product_services = 'Unsere Hardware-Wallets ermöglichen die sichere Verwaltung von Kryptowährungen'
    terms_title_risks = 'Risiken'
    terms_describe_risks = 'Bitte beachten Sie die mit Kryptowährungen und technischen Schwachstellen verbundenen Risiken.'
    terms_title_disclaimers = 'Haftungsausschluss'
    terms_describe_disclaimers = 'Die bereitgestellten Informationen stellen keine Finanzberatung dar. Bitte holen Sie professionellen Rat ein, bevor Sie Entscheidungen treffen.'
    terms_title_contact_us = 'Kontakt'
    terms_describe_contact_us = 'Bei Fragen oder Anliegen senden Sie uns bitte eine E-Mail an support@digitshield.com'

    accept_tems = 'Nutzungsbedingungen akzeptieren'
    use_range = '1. Anwendungsbereich'
    range_include = 'Diese Bedingungen gelten für alle über die Digital Shield Wallet angebotenen Dienste, einschließlich:'
    range_include_1 = 'Kauf, Aktivierung und After-Sales-Service der Hardware-Wallet; Herunterladen, Installation und Nutzung der mobilen Digital Shield App (Android/iOS/Goolg); Firmware-Updates (einschließlich Sicherheitspatches und Funktionserweiterungen); Verwaltung von Multi-Chain-Digitalvermögen (Unterstützung der Speicherung und Übertragung von über 3000 Token wie BTC, ETH usw.); Technischer Support (Fehlerbehebung bei Geräten, Behandlung von Transaktionssignaturanomalien usw.).'
    user_qualification = '2. Benutzerqualifikation'
    ability_include = 'Sie bestätigen, dass Sie mindestens 18 Jahre alt sind und voll geschäftsfähig sind;'
    ability_include_1 = 'Ihre Gerichtsbarkeit verbietet nicht die Verwendung von Kryptowährungen und verwandten Hardware-Geräten (z.B. müssen Benutzer aus dem chinesischen Festland das Nutzungsrisiko selbst tragen);'
    terms_update_infor = '3. Aktualisierung der Bedingungen und Benachrichtigung'
    update_infor_content = 'Wir behalten uns das Recht vor, die Bedingungen einseitig zu ändern. Die geänderten Inhalte werden über das Ankündigungsbrett der offiziellen Website veröffentlicht, das Datum des Inkrafttretens basiert auf der Ankündigung; Wenn Sie die Dienste weiterhin nutzen, gilt dies als Akzeptanz der geänderten Bedingungen; Wenn Sie nicht einverstanden sind, sollten Sie dies schriftlich mitteilen und die Nutzung vor dem Inkrafttreten beenden.'

    wallet_buy_iterms = 'II. Bedingungen für den Kauf der Hardware-Wallet'
    order_process = '1. Bestellvorgang'
    payment_confirmation = 'Zahlungsbestätigung: Nach erfolgreicher Zahlung der Bestellung (bestätigt durch das Blockchain-Netzwerk oder Bankgutschrift) wird das System den Status innerhalb von 24 Stunden aktualisieren;'
    inventory_shortage = 'Lagerbestand nicht verfügbar: Wenn der Lagerbestand nicht ausreicht, kann der Benutzer wählen:'
    inventory_shortage_1 = 'a. Auf Nachschub warten (maximal 30 Tage, automatische Rückerstattung bei Überschreitung der Frist);'
    inventory_shortage_2 = 'b. Vollständige Rückerstattung über den ursprünglichen Weg (Kryptowährungsbestellungen werden zum Wechselkurs zum Zeitpunkt der Zahlung umgerechnet).'
    return_and_exchange_policy = '2. Rückgabe- und Umtauschrichtlinie'
    return_and_exchange_condi = 'Rückgabebedingungen:'
    return_and_exchange_condi_con = 'a. Nicht aktivierte Geräte müssen das ursprüngliche Versiegeltes Etikett (Nummer stimmt mit der Bestellung überein) und vollständiges Zubehör (USB-Kabel, Bedienungsanleitung, Sicherungswörter-Karte) behalten; b. Rückgabeanträge müssen innerhalb von 7 Tagen nach Erhalt eingereicht werden, danach gilt die Ware als geprüft und akzeptiert; c. Die Rückversandkosten trägt der Benutzer (außer bei Qualitätsproblemen).'
    warranty_scope = 'Garantieumfang:'
    warranty_scope_1 = 'a. Deckt nicht durch den Benutzer verursachte Schäden wie Sicherheitschipfehler, Anzeigeprobleme, Tastenausfall usw. ab;'
    warranty_scope_2 = 'b. Kaufnachweis (Bestellnummer) und Fehlernachweis erforderlich (Video muss die SN-Nummer des Geräts und das abnormale Phänomen klar zeigen);'
    warranty_scope_3 = 'c. Durch den Benutzer verursachte Schäden (z.B. Wasserschaden, Sturz) sind nicht garantiert und können gegen Gebühr repariert werden.'

    disclaimer = 'III. Haftungsausschluss'
    product_risk = '1. Produktrisiken'
    physical_risk = 'Physische Risiken:'
    physical_risk_1 = 'a. Das Gerät kann in Umgebungen mit hohen Temperaturen (>60°C), hoher Luftfeuchtigkeit (>90% RH) und starken Magnetfeldern (>100mT) ausfallen;'
    physical_risk_2 = 'b. Langes Nichtaufladen kann die Batterie beschädigen (empfohlen wird monatliches Aufladen).'
    supply_chain_risk = 'Lieferkettenrisiken:'
    supply_chain_risk_1 = 'a. Die offizielle Website bietet ein Fälschungsschutz-Tool, das durch Scannen des QR-Codes des Geräts die Echtheit überprüft;'
    supply_chain_risk_2 = 'b. Wenn Sie vermuten, dass das Gerät ausgetauscht wurde, kontaktieren Sie sofort den Kundendienst und die Polizei.'
    service_interruption = '2. Dienstunterbrechung'
    service_interruption_1 = 'Geplante Wartung wird 48 Stunden im Voraus über das Ankündigungsbrett der offiziellen Website bekannt gegeben, Notfallwartung kann ohne Vorwarnung den Dienst unterbrechen;'
    service_interruption_2 = 'Wir übernehmen keine Haftung für Datenverluste aufgrund höherer Gewalt.'

    device_label = "Gerätename"
    device_title_firmware_version = 'Firmware-Version'
    device_title_serial_number = 'Seriennummer'
    bluetooth_name = "Bluetooth-Name"
    bluetooth_version = "Bluetooth-Version"
    firmware_title_1 = '1. Stellen Sie sicher, dass der Akkustand über 20% liegt'
    firmware_title_2 = '2. Verbinden Sie das Gerät über ein USB-C-Kabel mit dem Computer'
    firmware_title_3 = '3. Klicken Sie auf "Firmware-Update"'
    firmware_title_caution = 'Warnung'
    firmware_describe_caution = 'Bitte halten Sie die USB-Verbindung während des Updates aufrecht'
    equipment_info = 'Geräteinformationen'
    equipment_name = 'Gerätename'
    equipment_version = 'Geräteversion'

class Nft:
    nft_item ="{} Artikel"
    nft_items ="{} Artikel"
class Title:
    enter_old_pin = "Alten PIN eingeben"
    enter_new_pin = "Neuen PIN eingeben"
    enter_pin = "PIN eingeben"
    enter_pin_again = "PIN erneut eingeben"
    select_language = "Sprache auswählen"
    create_wallet = "Wallet erstellen"
    wallet = "Wallet"
    import_wallet = "Wallet importieren"
    restore_wallet = "Wallet wiederherstellen"
    wallet_is_ready = "Wallet bereit"
    select_word_count = "Wortanzahl wählen"
    wallet_security = "Wallet-Sicherheit"
    pin_security = "PIN-Sicherheitshinweis"
    mnemonic_security = "Mnemonic-Sicherheitshinweis"
    backup_mnemonic = "Mnemonic sichern"
    enter_mnemonic = "Mnemonic eingeben"
    check_mnemonic = "Mnemonic prüfen"
    success = "Erfolgreich"
    operate_success = "Aktion erfolgreich"
    theme_success = "Design erfolgreich geändert"
    warning = "Warnung"
    error = "Fehler"
    verified = "Mnemonic-Sicherung abgeschlossen"
    invalid_mnemonic = "Ungültiger Mnemonic"
    pin_not_match = "PIN stimmt nicht überein"
    check_recovery_mnemonic = "Wiederherstellungs-Mnemonic prüfen"
    mnemonic_not_match = "Mnemonic stimmt nicht überein"
    power_off = "Ausschalten"
    restart = "Neustart"
    change_language = "Sprache ändern"
    wipe_device = "Gerät zurücksetzen"
    bluetooth_pairing = "Bluetooth-Paarung"
    address="{} Adresse"
    public_key = "{} öffentlicher Schlüssel"
    xpub = "{} XPub"
    transaction = "{} Transaktion"
    transaction_detail = "Transaktionsdetails"
    confirm_transaction = "Transaktion bestätigen"
    confirm_message = "Nachricht bestätigen"
    signature = "Signaturergebnis"
    wrong_pin = "Falsche PIN"
    pin_changed = "PIN geändert"
    pin_enabled = "PIN aktiviert"
    pin_disabled = "PIN deaktiviert"
    unknown_token = "Unbekanntes Token"
    view_data = "Daten anzeigen"
    sign_message = "{} Nachricht signieren"
    verify_message = "{} Nachricht verifizieren"
    typed_data = "{} strukturierte Daten"
    typed_hash = "{} strukturierter Hash"
    system_update = "Systemupdate"
    entering_boardloader = "Starte Boardloader"
    remove_credential = "Zugangsdaten entfernen"
    list_credentials = "Zugangsdaten auflisten"
    authorize_coinjoin = "CoinJoin autorisieren"
    multisig_address_m_of_n = "{} Multisig-Adresse\n({} von {})"
    u2f_register = "U2F Registrierung"
    u2f_unregister = "U2F-Registrierung aufheben"
    u2f_authenticate = "U2F Authentifizierung"
    fido2_register = "FIDO2 Registrierung"
    fido2_unregister = "FIDO2-Registrierung aufheben"
    fido2_authenticate = "FIDO2-Authentifizierung"
    finalize_transaction = "Transaktion abschließen"
    meld_transaction = "Zusammenführungs-Transaktion"
    update_transaction = "Transaktionsupdate"
    high_fee = "Hohe Gebühr"
    fee_is_high = "Transaktionsgebühr zu hoch"
    confirm_locktime = "Sperrzeit bestätigen"
    view_transaction = "Transaktion anzeigen"
    x_confirm_payment = "{} Zahlung bestätigen"
    confirm_replacement = "Ersatztransaktion bestätigen"
    x_transaction = "{} Transaktion"
    x_joint_transaction = "{} gemeinsame Transaktion"
    change_label = "Gerätename ändern"
    enable_passphrase = "Passphrase aktivieren"
    disable_passphrase = "Passphrase deaktivieren"
    passphrase_source = "Passphrase-Eingabeeinstellung"
    enable_safety_checks ="Sicherheitsprüfungen aktivieren"
    disable_safety_checks ="Sicherheitsprüfungen deaktivieren"
    experiment_mode = "Experimentiermodus"
    set_as_homescreen = "Als Startbildschirm festlegen"
    get_next_u2f_counter = "Nächsten U2F-Zähler abrufen"
    set_u2f_counter = "U2F-Zähler setzen"
    encrypt_value = "Daten verschlüsseln"
    decrypt_value = "Daten entschlüsseln"
    confirm_entropy = "Entropie exportieren"
    memo = "Notiz"
    import_credential = "Zugangsdaten importieren"
    export_credential = "Zugangsdaten exportieren"
    asset = "Asset"
    unimplemented = "Nicht implementiert"
    invalid_data="Ungültiges Datenformat"
    low_power = "Akku schwach"
    collect_nft = "NFT sammeln"
    verify_device = "Gerät verifizieren"
    update_bootloader = "Bootloader aktualisieren"
    update_resource = "Ressourcen aktualisieren"

class Text:
    tap_to_unlock = "Zum Entsperren tippen"
    unlocking = "Gerät wird entsperrt..."
    str_words = "#FFFFFF {}# Wörter"
    backup_manual = "Mnemonic manuell aufschreiben und sicher aufbewahren"
    check_manual = "Wörter in der richtigen Reihenfolge auswählen"
    backup_verified = "Mnemonic erfolgreich gesichert. Bewahren Sie ihn sicher auf und teilen Sie ihn mit niemandem"
    backup_invalid = "Ungültiger Mnemonic. Bitte überprüfen und erneut versuchen"
    pin_not_match = "Falsche PIN. Bitte erneut versuchen"
    please_wait = "Bitte warten..."
    wiping_device = "Gerätedaten werden gelöscht..."
    create_wallet = "Neuen Mnemonic generieren und Wallet erstellen"
    restore_wallet = "Wallet aus gesichertem Mnemonic wiederherstellen"
    restore_mnemonic_match = "Mnemonic stimmt überein - Ihre Sicherung ist korrekt"
    restore_success = "Wallet erfolgreich wiederhergestellt"
    create_success = "Mnemonic erfolgreich gesichert und Wallet erstellt"
    check_recovery_mnemonic = "Bitte überprüfen Sie Ihren Mnemonic auf Übereinstimmung"
    invalid_recovery_mnemonic = "Ungültiger Mnemonic. Bitte überprüfen und erneut versuchen"
    check_recovery_not_match = "Mnemonic ist gültig, stimmt aber nicht mit dem Gerät überein"
    shutting_down = "Wird heruntergefahren..."
    restarting = "Wird neu gestartet..."
    never = "Nie"
    second = "Sekunde"
    seconds = "Sekunden"
    minute = "Minute"
    minutes = "Minuten"
    changing_language = "Sie ändern die Sprache\nDiese Änderung erfordert einen Neustart des Geräts"
    change_pin = "Legen Sie einen 4-16-stelligen PIN-Code fest, um Ihr Gerät zu schützen"
    wipe_device = "Setzt das Gerät auf Werkseinstellungen zurück.\nWarnung: Alle Daten werden unwiderruflich gelöscht."
    wipe_device_check = [
        "Zurücksetzen löscht alle Daten",
        "Daten können nicht wiederhergestellt werden",
        "Mnemonic wurde gesichert",
    ]
    wipe_device_success = "Gerät erfolgreich zurückgesetzt\nStartet neu..."
    bluetooth_pair = "Bitte geben Sie den Pairing-Code auf Ihrem Gerät ein"
    bluetooth_pair_failed = "Bluetooth-Pairing fehlgeschlagen"
    path = "Ableitungspfad:"
    chain_id = "Chain-ID:"
    send = "Senden"
    to = "An"
    amount = "Betrag"
    from_ = "Von"
    receiver = "Empfänger"
    fee = "Gebühr"
    max_fee = "Maximale Gebühr"
    max_priority_fee_per_gas = "Maximale Prioritätsgebühr pro Gas"
    max_fee_per_gas = "Maximale Gebühr pro Gas"
    gas_price = "Gas-Preis"
    total = "Gesamtbetrag"
    do_sign_this_transaction = "Diese {} Transaktion signieren?"
    transaction_signed = "Transaktion signiert"
    address = 'Adresse:'
    public_key = "Öffentlicher Schlüssel:"
    xpub = "XPub:"
    unknown_tx_type = "Unbekannter Transaktionstyp, bitte Eingabedaten prüfen"
    unknown_function = "Unbekannte Funktion:"
    use_app_scan_this_signature = "Bitte Wallet-App zum Scannen des Signaturergebnisses verwenden"
    internal_error = "Interner Fehler"
    tap_switch_to_airgap = "Zum Wechseln zur Airgap-Adresse QR-Code antippen"
    tap_switch_to_receive = "Zum Wechseln zur Empfangsadresse QR-Code antippen"
    incorrect_pin_times_left = "Falsche PIN, noch {} Versuche übrig"
    incorrect_pin_last_time = "Falsche PIN, letzter Versuch"
    wrong_pin = "Falsche PIN eingegeben"
    seedless = "Seed fehlt"
    backup_failed = "Sicherung fehlgeschlagen!"
    need_backup = "Sicherung benötigt!"
    pin_not_set = "PIN nicht gesetzt!"
    experimental_mode = "Experimenteller Modus"
    pin_change_success = "PIN erfolgreich geändert"
    pin_enable_success = "PIN erfolgreich aktiviert"
    pin_disable_success = "PIN erfolgreich deaktiviert"
    contract = "Vertrag:"
    new_contract = "Neuer Vertrag?"
    bytes_ = "{} Bytes"
    message = "Nachricht:"
    no_message = "Keine Nachricht enthalten"
    contains_x_key = "Enthält {} Schlüssel"
    array_of_x_type = "Array vom Typ {} {}"
    do_sign_712_typed_data = "Strukturierte Daten-Transaktion signieren?"
    do_sign_typed_hash = "Strukturierte Hash-Transaktion signieren?"
    domain_hash = "Domain-Hash:"
    message_hash = "Nachrichten-Hash:"
    switch_to_update_mode = "Zum Update-Modus wechseln"
    switch_to_boardloader = "In Boardloader-Modus wechseln"
    list_credentials = "Gespeicherte Zugangsdaten exportieren?"
    coinjoin_at_x = "An folgender Coinjoin-Transaktion teilnehmen:\n{}"
    signature_is_valid = "Signatur ist gültig"
    signature_is_invalid = "Signatur ist ungültig"
    u2f_already_registered = "U2F bereits registriert"
    u2f_not_registered = "U2F nicht registriert"
    fido2_already_registered_x = "FIDO2 bereits registriert {}"
    fido2_verify_user = "FIDO2 Benutzerverifizierung"
    device_already_registered_x = "Gerät bereits registriert {}"
    device_verify_user = "Geräte-Benutzerverifizierung"
    fee_is_unexpectedly_high = "Transaktionsgebühr unerwartet hoch"
    too_many_change_outputs = "Zu viele Wechselgeld-Ausgaben"
    change_count = "Wechselgeld-Anzahl"
    locktime_will_have_no_effect = "Sperrzeit wird keine Wirkung haben"
    confirm_locktime_for_this_transaction = "Sperrzeit für diese Transaktion bestätigen"
    block_height = "Blockhöhe"
    time = "Zeit"
    amount_increased = "Betrag erhöht"
    amount_decreased = "Betrag verringert"
    fee_unchanged = "Gebühr unverändert"
    fee_increased = "Gebühr erhöht"
    fee_decreased = "Gebühr verringert"
    your_spend = "Ihre Ausgabe"
    change_label_to_x = "Beschriftung ändern zu {}"
    enable_passphrase = "Passphrase-Verschlüsselung aktivieren?"
    disable_passphrase = "Passphrase-Verschlüsselung deaktivieren?"
    enable_passphrase_always = "Passphrase immer lokal eingeben?"
    revoke_enable_passphrase_always = "Einstellung 'Passphrase immer lokal eingeben' widerrufen?"
    auto_lock_x = "Gerät nach {} automatisch sperren?"
    enable_safety_checks = "Strenge Sicherheitsprüfungen aktivieren? Dies bietet umfassenderen Schutz."
    disable_safety_checks = "Sicherheitsprüfungen deaktivieren? Bitte beachten Sie die potenziellen Risiken."
    enable_experiment_mode = "Experimentellen Modus aktivieren?"
    set_as_homescreen = "Als Startbildschirm festlegen?"
    replace_homescreen = "Startbildschirm ersetzen? Dies löscht das zuerst hochgeladene Hintergrundbild."
    confirm_replace_wallpaper = "Sind Sie sicher, dass Sie das Startbildschirm-Hintergrundbild ändern möchten?"
    get_next_u2f_counter = "Nächsten U2F-Zähler abrufen?"
    set_u2f_counter_x = "U2F-Zähler auf {} setzen?"
    confirm_entropy = "Entropie exportieren? Bitte verstehen Sie was Sie tun!"
    bandwidth = "Bandbreite"
    energy = "Energie"
    sender = "Absender"
    recipient = "Empfänger"
    resource = "Ressource"
    frozen_balance = "Eingefrorener Betrag"
    unfrozen_balance = "Aufgetauter Betrag"
    delegated_balance = "Delegierter Betrag"
    undelegated_balance = "Nicht delegierter Betrag"
    you_are_freezing = "Sie frieren Assets ein"
    you_are_unfreezing = "Sie tauen Assets auf"
    you_are_delegating = "Sie delegieren Assets"
    you_are_undelegating = "Sie beenden Asset-Delegierung"
    duration = "Dauer"
    lock = "Sperren"
    unlock = "Entsperren"
    all = "Alle"
    source = "Quelle"
    tip = "Hinweis"
    keep_alive = "Keep alive"
    invalid_ur = "Nicht unterstützter QR-Code-Typ, bitte erneut versuchen"
    sequence_number = "Sequenznummer"
    expiration_time = "Ablaufzeit"
    argument_x = "Argument #{}"
    low_power_message = "Akku: {}% verbleibend\nBitte aufladen"
    collect_nft = "Sind Sie sicher, dass Sie dieses NFT sammeln möchten?"
    replace_nft = "Möchten Sie dieses NFT sammeln? Sie haben das Speicherlimit erreicht, dies wird das älteste hochgeladene NFT entfernen."
    verify_device = "Sind Sie sicher, dass Sie Ihr Gerät mit dem DigitShield-Server authentifizieren möchten? Tippen Sie auf Bestätigen, um zu prüfen, ob Ihr Gerät original und nicht manipuliert ist."
    update_bootloader = "Möchten Sie den Bootloader aktualisieren?"
    update_resource = "Möchten Sie die Geräteressourcen aktualisieren?"
class Tip:
    swipe_down_to_close = "Zum Schließen nach unten wischen"

class Button:
    done = "Fertig"
    ok = "OK"
    confirm = "Bestätigen"
    reject = "Ablehnen"
    next = "Weiter"
    cancel = "Abbrechen"
    redo = "Neu generieren"
    continue_ = "Fortsetzen"
    try_again = "Erneut versuchen"
    power_off = "Ausschalten"
    restart = "Neu starten"
    hold = "Gedrückt halten"
    address = "Adresse"
    qr_code = "QR-Code"
    view_detail = "Details anzeigen"
    hold_to_sign = "Zum Signieren gedrückt halten"
    hold_to_wipe = "Zum Zurücksetzen gedrückt halten"
    receive = "Empfangsadresse"
    airgap = "Airgap"
    sign = "Signieren"
    verify = "Verifizieren"
    view_full_array = "Vollständiges Array anzeigen"
    view_full_struct = "Vollständige Struktur anzeigen"
    view_full_message = "Vollständige Nachricht anzeigen"
    view_data = "Daten anzeigen"
    view_more = "Mehr anzeigen"

class WalletSecurity:
    header = "Schreiben Sie Ihren Mnemonic auf Papier und bewahren Sie ihn sicher auf"
    tips = [
        {
            "level": "info",
            "msgs": [
                "#00001F Mnemonic muss sicher aufbewahrt werden#",
                "#18794E * In einem Bankschließfach#",
                "#18794E * In einem Tresor#",
                "#18794E * An mehreren geheimen Orten#",
            ]
        },
        {
            "level": "warning",
            "msgs": [
                "#00001F Wichtige Hinweise#",
                "#CD2B31 * Merken Sie sich Ihren Mnemonic#",
                "#CD2B31 * Gehen Sie nicht verloren#",
                "#CD2B31 * Teilen Sie ihn niemandem mit#",
                "#CD2B31 * Nicht online speichern#",
                "#CD2B31 * Nicht auf dem Computer speichern#",
            ]
        },
    ]

class MnemonicSecurity:
    header = "Der Mnemonic ist eine Wortgruppe zur Wiederherstellung Ihrer Wallet-Assets. Wer den Mnemonic besitzt, hat Zugriff auf Ihre Assets - bewahren Sie ihn daher sorgfältig auf"

    tips = [
        "1. Überprüfen Sie die Umgebung auf Sicherheit (keine Beobachter oder Kameras)",
        "2. Sichern Sie den Mnemonic in der korrekten Reihenfolge und teilen Sie ihn NIEMANDEM mit",
        "3. Bewahren Sie den Mnemonic offline an einem sicheren Ort auf. Nutzen Sie KEINE digitalen Speichermethoden und laden Sie ihn NIEMALS ins Internet hoch",
    ]

class PinSecurity:
    header = "Der PIN-Code ist das Passwort für den Gerätezugriff und autorisiert die Nutzung dieses Geräts. Bitte beachten Sie folgende Hinweise zur korrekten PIN-Verwendung"
    tips = [
        "1. Überprüfen Sie die Umgebungssicherheit, bevor Sie einen PIN festlegen oder eingeben (keine Beobachter oder Kameras).",
        "2. Wählen Sie einen starken 4-16-stelligen PIN-Code und vermeiden Sie aufeinanderfolgende oder wiederholte Zahlen.",
        "3. Maximale Fehlversuche: 10. Nach dem 10. Fehlversuch wird das Gerät zurückgesetzt.",
        "4. Bewahren Sie Ihren PIN sicher auf und teilen Sie ihn NIEMANDEM mit.",
    ]

class Solana:
    ata_reciver = "Empfänger (Assoziiertes Token-Konto)"
    ata_sender = "Sender (Assoziiertes Token-Konto)"
    source_owner = "Transaktionssignierer"
    fee_payer = "Gebührenzahler"