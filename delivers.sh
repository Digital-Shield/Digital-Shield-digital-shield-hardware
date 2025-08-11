.venv/bin/trezorctl device reboot-to-bootloader

venv/bin/trezorctl device emmc-file-write -l ./files/res/app_account_six.png -r 0:res/app_account_six.png -f -cs 16384

for file in ./files/res/*; do
    filename=$(basename "$file")
    .venv/bin/trezorctl device emmc-file-write -l "$file" -r "0:res/$filename" -f -cs 16384
done
for file in ./files/res/wallpapers/*; do
    filename=$(basename "$file")
    .venv/bin/trezorctl device emmc-file-write -l "$file" -r "0:res/wallpapers/$filename" -f -cs 16384
done
for file in ./files/res/wallpapers/thumbnail/*; do
    filename=$(basename "$file")
    .venv/bin/trezorctl device emmc-file-write -l "$file" -r "0:res/wallpapers/thumbnail/$filename" -f -cs 16384
done
# # .venv/bin/trezorctl device bl-reboot

# # .venv/bin/trezorctl device reboot-to-bootloader

.venv/bin/trezorctl device emmc-dir-make -p 0:boot
.venv/bin/trezorctl device emmc-file-write -l ./files/bootloader.bin -r 0:boot/bootloader.bin -f -cs 16384
.venv/bin/trezorctl device emmc-dir-make -p 0:updates
.venv/bin/trezorctl device emmc-file-write -l ./files/firmware.bin -r 0:updates/firmware.bin -f -cs 16384
.venv/bin/trezorctl device firmware-update-emmc -p 0:updates/firmware.bin
.venv/bin/trezorctl device bl-reboot

# .venv/bin/trezorctl device reboot-to-bootloader
# # .venv/bin/trezorctl device emmc-dir-make -p 0:boot
# # .venv/bin/trezorctl device emmc-file-write -l ./files/bootloader.bin -r 0:boot/bootloader.bin -f -cs 16384
# .venv/bin/trezorctl device emmc-dir-make -p 0:updates
# #  .venv/bin/trezorctl device emmc-file-write -l ./files/firmware.bin -r 0:updates/firmware.bin -f -cs 16384
# .venv/bin/trezorctl device emmc-file-write -l ./files/firmware.bin -r 0:updates/firmware.bin -f -cs 16384
# .venv/bin/trezorctl device firmware-update-emmc -p 0:updates/firmware.bin
# .venv/bin/trezorctl device bl-reboot

