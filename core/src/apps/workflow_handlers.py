from typing import TYPE_CHECKING

from trezor import utils
from trezor.enums import MessageType

if TYPE_CHECKING:
    from trezor.wire import Handler, Msg
    from trezorio import WireInterface


workflow_handlers: dict[int, Handler] = {}


def register(wire_type: int, handler: Handler[Msg]) -> None:
    """Register `handler` to get scheduled after `wire_type` message is received."""
    workflow_handlers[wire_type] = handler


def find_message_handler_module(msg_type: int) -> str:
    """Statically find the appropriate workflow handler.

    For now, new messages must be registered by hand in the if-elif manner below.
    The reason for this is memory fragmentation optimization:
    - using a dict would mean that the whole thing stays in RAM, whereas an if-elif
      sequence is run from flash
    - collecting everything as strings instead of importing directly means that we don't
      need to load any of the modules into memory until we actually need them
    """
    # debug
    if __debug__ and msg_type == MessageType.LoadDevice:
        return "apps.debug.load_device"

    # management
    if msg_type == MessageType.ResetDevice:
        return "apps.management.reset_device"
    if msg_type == MessageType.BackupDevice:
        return "apps.management.backup_device"
    if msg_type == MessageType.WipeDevice:
        return "apps.management.wipe_device"
    if msg_type == MessageType.RecoveryDevice:
        return "apps.management.recovery_device"
    if msg_type == MessageType.ApplySettings:
        return "apps.management.apply_settings"
    if msg_type == MessageType.ApplyFlags:
        return "apps.management.apply_flags"
    if msg_type == MessageType.ChangePin:
        return "apps.management.change_pin"
    if msg_type == MessageType.ChangeWipeCode:
        return "apps.management.change_wipe_code"
    elif msg_type == MessageType.GetNonce:
        return "apps.management.get_nonce"
    elif msg_type == MessageType.SESignMessage:
        return "apps.management.se_sign_message"
    elif msg_type == MessageType.RebootToBootloader:
        return "apps.management.reboot_to_bootloader"
    elif msg_type == MessageType.DeviceBackToBoot:
        return "apps.management.reboot_to_bootloader"
    elif msg_type == MessageType.RebootToBoardloader:
        return "apps.management.reboot_to_boardloader"
    elif msg_type == MessageType.ReadSEPublicCert:
        return "apps.management.se_read_cert"

    if utils.MODEL in ("T",) and msg_type == MessageType.SdProtect:
        return "apps.management.sd_protect"
    if utils.MODEL == "T" and msg_type == MessageType.ResourceUpload:
        if utils.EMULATOR:
            raise ValueError
        return "apps.management.upload_res"
    if utils.MODEL == "T" and msg_type == MessageType.ResourceUpdate:
        if utils.EMULATOR:
            raise ValueError
        return "apps.management.update_res"
    if utils.MODEL == "T" and msg_type == MessageType.ListResDir:
        if utils.EMULATOR:
            raise ValueError
        return "apps.management.list_dir"

    # bitcoin
    if msg_type == MessageType.AuthorizeCoinJoin:
        return "apps.bitcoin.authorize_coinjoin"
    if msg_type == MessageType.GetPublicKey:
        return "apps.bitcoin.get_public_key"
    if msg_type == MessageType.GetAddress:
        return "apps.bitcoin.get_address"
    if msg_type == MessageType.GetOwnershipId:
        return "apps.bitcoin.get_ownership_id"
    if msg_type == MessageType.GetOwnershipProof:
        return "apps.bitcoin.get_ownership_proof"
    if msg_type == MessageType.SignTx:
        return "apps.bitcoin.sign_tx"
    if msg_type == MessageType.SignMessage:
        return "apps.bitcoin.sign_message"
    if msg_type == MessageType.VerifyMessage:
        return "apps.bitcoin.verify_message"

    # misc
    if msg_type == MessageType.GetEntropy:
        return "apps.misc.get_entropy"
    if msg_type == MessageType.SignIdentity:
        return "apps.misc.sign_identity"
    if msg_type == MessageType.GetECDHSessionKey:
        return "apps.misc.get_ecdh_session_key"
    if msg_type == MessageType.CipherKeyValue:
        return "apps.misc.cipher_key_value"
    if msg_type == MessageType.GetFirmwareHash:
        return "apps.misc.get_firmware_hash"
    if msg_type == MessageType.BatchGetPublickeys:
        return "apps.misc.batch_get_pubkeys"

    if not utils.BITCOIN_ONLY:
        if msg_type == MessageType.SetU2FCounter:
            return "apps.management.set_u2f_counter"
        if msg_type == MessageType.GetNextU2FCounter:
            return "apps.management.get_next_u2f_counter"

        # webauthn
        if msg_type == MessageType.WebAuthnListResidentCredentials:
            return "apps.webauthn.list_resident_credentials"
        if msg_type == MessageType.WebAuthnAddResidentCredential:
            return "apps.webauthn.add_resident_credential"
        if msg_type == MessageType.WebAuthnRemoveResidentCredential:
            return "apps.webauthn.remove_resident_credential"

        # ethereum
        if msg_type == MessageType.EthereumGetAddress:
            return "apps.ethereum.get_address"
        if msg_type == MessageType.EthereumGetPublicKey:
            return "apps.ethereum.get_public_key"
        if msg_type == MessageType.EthereumSignTx:
            return "apps.ethereum.sign_tx"
        if msg_type == MessageType.EthereumSignTxEIP1559:
            return "apps.ethereum.sign_tx_eip1559"
        if msg_type == MessageType.EthereumSignMessage:
            return "apps.ethereum.sign_message"
        if msg_type == MessageType.EthereumVerifyMessage:
            return "apps.ethereum.verify_message"
        if msg_type == MessageType.EthereumSignTypedData:
            return "apps.ethereum.sign_typed_data"
        if msg_type == MessageType.EthereumSignTypedHash:
            return "apps.ethereum.sign_typed_data_hash"

        # ethereum Digitalshield
        if msg_type == MessageType.EthereumGetAddressDigitalshield:
            return "apps.ethereum.digitalshield.get_address"
        if msg_type == MessageType.EthereumGetPublicKeyDigitalshield:
            return "apps.ethereum.digitalshield.get_public_key"
        if msg_type == MessageType.EthereumSignTxDigitalshield:
            return "apps.ethereum.digitalshield.sign_tx"
        if msg_type == MessageType.EthereumSignTxEIP1559Digitalshield:
            return "apps.ethereum.digitalshield.sign_tx_eip1559"
        if msg_type == MessageType.EthereumSignMessageDigitalshield:
            return "apps.ethereum.digitalshield.sign_message"
        if msg_type == MessageType.EthereumVerifyMessageDigitalshield:
            return "apps.ethereum.digitalshield.verify_message"
        if msg_type == MessageType.EthereumSignTypedDataDigitalshield:
            return "apps.ethereum.digitalshield.sign_typed_data"
        if msg_type == MessageType.EthereumSignTypedHashDigitalshield:
            return "apps.ethereum.digitalshield.sign_typed_data_hash"

        # eos
        if msg_type == MessageType.EosGetPublicKey:
            return "apps.eos.get_public_key"
        if msg_type == MessageType.EosSignTx:
            return "apps.eos.sign_tx"

        # polkadot
        if msg_type == MessageType.PolkadotGetAddress:
            return "apps.polkadot.get_address"
        if msg_type == MessageType.PolkadotSignTx:
            return "apps.polkadot.sign_tx"

        # ton
        if msg_type == MessageType.TonGetAddress:
            return "apps.ton.get_address"
        if msg_type == MessageType.TonSignMessage:
            return "apps.ton.sign_message"
        if msg_type == MessageType.TonSignProof:
            return "apps.ton.sign_proof"
        
        # tron
        if msg_type == MessageType.TronGetAddress:
            return "apps.tron.get_address"
        if msg_type == MessageType.TronSignTx:
            return "apps.tron.sign_tx"
        if msg_type == MessageType.TronSignMessage:
            return "apps.tron.sign_message"

        # solana
        if msg_type == MessageType.SolanaGetAddress:
            return "apps.solana.get_address"
        if msg_type == MessageType.SolanaSignTx:
            return "apps.solana.sign_tx"

        # sui
        if msg_type == MessageType.SuiGetAddress:
            return "apps.sui.get_address"
        if msg_type == MessageType.SuiSignTx:
            return "apps.sui.sign_tx"
        if msg_type == MessageType.SuiSignMessage:
            return "apps.sui.sign_message"

        # aptos
        if msg_type == MessageType.AptosGetAddress:
            return "apps.aptos.get_address"
        if msg_type == MessageType.AptosSignTx:
            return "apps.aptos.sign_tx"
        if msg_type == MessageType.AptosSignMessage:
            return "apps.aptos.sign_message"

    raise ValueError


def find_registered_handler(iface: WireInterface, msg_type: int) -> Handler | None:
    if msg_type in workflow_handlers:
        # Message has a handler available, return it directly.
        return workflow_handlers[msg_type]

    try:
        modname = find_message_handler_module(msg_type)
        handler_name = modname[modname.rfind(".") + 1 :]
        module = __import__(modname, None, None, (handler_name,), 0)
        return getattr(module, handler_name)
    except ValueError:
        return None
