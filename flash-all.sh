.venv/bin/trezorctl device reboot-to-bootloader

.venv/bin/trezorctl device emmc-dir-make -p 0:boot
.venv/bin/trezorctl device emmc-file-write -l ./files/bootloader.bin -r 0:boot/bootloader.bin -f -cs 16384
.venv/bin/trezorctl device emmc-dir-make -p 0:updates
.venv/bin/trezorctl device emmc-file-write -l ./files/firmware.bin -r 0:updates/firmware.bin -f -cs 16384
.venv/bin/trezorctl device firmware-update-emmc -p 0:updates/firmware.bin
.venv/bin/trezorctl device bl-reboot

.venv/bin/trezorctl device reboot-to-bootloader

.venv/bin/trezorctl device emmc-file-write -l ./files/app_settings_six.png -r 0:res/app_settings_six.png -f -cs 16384
.venv/bin/trezorctl device emmc-file-write -l ./files/booting.avi -r 0:res/booting.avi -f -cs 16384
.venv/bin/trezorctl device emmc-file-write -l ./files/0.png -r 0:res/wallpapers/0.png -f -cs 16384
.venv/bin/trezorctl device emmc-file-write -l ./files/3.png -r 0:res/wallpapers/3.png -f -cs 16384
.venv/bin/trezorctl device emmc-file-write -l ./files/thumbnail/0.png -r 0:res/wallpapers/thumbnail/0.png -f -cs 16384
.venv/bin/trezorctl device emmc-file-write -l ./files/thumbnail/3.png -r 0:res/wallpapers/thumbnail/3.png -f -cs 16384
.venv/bin/trezorctl device bl-reboo


# .venv/bin/trezorctl device reboot-to-bootloader

# .venv/bin/trezorctl device emmc-dir-make -p 0:boot
# .venv/bin/trezorctl device emmc-file-write -l ./core/embed/bootloader.bin -r 0:boot/bootloader.bin -f -cs 16384
# .venv/bin/trezorctl device emmc-dir-make -p 0:updates
# .venv/bin/trezorctl device emmc-file-write -l ./core/embed/firmware.bin -r 0:updates/firmware.bin -f -cs 16384
# .venv/bin/trezorctl device firmware-update-emmc -p 0:updates/firmware.bin
# .venv/bin/trezorctl device bl-reboot



#更新se
.venv/bin/trezorctl device reboot-to-bootloader
.venv/bin/trezorctl device emmc-dir-make -p 0:updates
.venv/bin/trezorctl device emmc-file-write -l ./files/se-debug-v1.1.0.bin -r 0:updates/se-debug-v1.1.0.bin -f -cs 16384
.venv/bin/trezorctl device firmware-update-emmc -p 0:updates/se-debug-v1.1.0.bin
.venv/bin/trezorctl device bl-reboot