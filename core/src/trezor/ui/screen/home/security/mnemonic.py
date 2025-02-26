from . import *

class CheckMnemonic(SampleItem):
    def __init__(self, parent):
        super().__init__(parent, i18n.Security.check_mnemonic, "A:/res/check-mnemonic.png")

    def action(self):
        super().action()
        from trezor import workflow
        from apps.management.recovery_device import recovery_device
        from trezor.messages import RecoveryDevice
        from trezor.wire import DUMMY_CONTEXT

        workflow.spawn(recovery_device(DUMMY_CONTEXT, RecoveryDevice(dry_run=True)))


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

