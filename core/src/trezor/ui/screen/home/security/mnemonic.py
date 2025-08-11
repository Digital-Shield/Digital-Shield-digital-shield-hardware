from . import *

class CheckMnemonic(SampleItem):
    def __init__(self, parent):
        super().__init__(parent, i18n.Security.check_mnemonic, "A:/res/check-mnemonic-new.png")

    def action(self):
        super().action()
        from trezor import workflow
        from trezor.ui.screen import manager
        from apps.management.recovery_device import recovery_device
        from trezor.messages import RecoveryDevice
        from trezor.wire import DUMMY_CONTEXT, ProcessError
        async def check_mnemonic():
            try:
                await recovery_device(DUMMY_CONTEXT, RecoveryDevice(dry_run=True))
            finally:
                manager.try_switch_to(SecurityApp)

        workflow.spawn(check_mnemonic())


class BackupMnemonic(SampleItem):
    def __init__(self, parent):
        super().__init__(parent, i18n.Security.backup_mnemonic, "A:/res/backup-mnemonic.png")

    def action(self):
        super().action()
        from trezor import workflow
        from apps.management.backup_device import backup_device
        from trezor.messages import BackupDevice

        from trezor.wire import DUMMY_CONTEXT

        workflow.spawn(backup_device(DUMMY_CONTEXT, BackupDevice()))

