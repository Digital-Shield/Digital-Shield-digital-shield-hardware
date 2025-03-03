# 环境搭建

1.安装 arm-none-eabi-gcc  
2.安装 stm32cubeide 与 stm32cubeprogrammer  
3.复制 core/tools/GD25Qxx-DunAn-8MB.stldr 到 stm32cubeprogrammer 安装目录的 ExternalLoader 文件夹中  
4.在项目根目录创建.env.sh 内容为

```
STM32PROG_DIR=/path/to/your/stm32cubeprogrmmer
```
5.安装git-lfs  
mac系统  
```
brew install git-lfs
```
ubuntu系统
```
sudo apt install git-lfs
```

# 代码编译

```
git submodule update --init --recursivecd
git lfs install
git lfs pull
nix-shell
poetry install
poetry shell
sh ./build-local.sh
```

# 代码烧录

```
sh ./flash.sh
```

# 拷贝资源文件
- 第一次烧录后，硬件上电进入 boardloader，会在电脑系统上挂载两个 U 盘，把 core/src/trezor/res 文件夹下除 res/nfts 文件拷贝到 SYSTEM 盘符下。
- 后续测试时，在 poetry shell 环境下使用如下指令回到 boardloader，同样会在系统上挂载两个 U 盘，把相应的资源拷贝到相应位置,res文件夹为隐藏属性，打开文件浏览器的查看隐藏功能。
```
trezorctl device reboot-to-boardloader
```

- 真正上线时，禁止回boardloader指令，使用update-res指令进行升级资源

# 固件升级指令
```
trezorctl device reboot-to-bootloader
trezorctl device emmc-dir-make -p 0:updates
trezorctl device emmc-file-write -l ./core/build/firmware/firmware.bin -r 0:updates/firmware.bin -f -cs 16384
trezorctl device firmware-update-emmc -p 0:updates/firmware.bin
trezorctl device reboot-to-boardloader
```

# ⚠️ 注意Nix 版本
Nix-shell需要安装2.23版本，可以使用如下指令安装
```
sh <(curl -L https://releases.nixos.org/nix/nix-2.23.3/install) --daemon
```
如果Mac系统报3001 User无法使用，可以使用如下指令安装
```
NIX_FIRST_BUILD_UID=30001 sh <(curl -L https://releases.nixos.org/nix/nix-2.23.3/install) --daemon
```
如果已经安装其他版本的Nix，先按照官方手册进行卸载  
https://nix.dev/manual/nix/2.21/installation/uninstall


# ⚠️ 注意Poetry 版本
如果使用nix-shell中的poetry或者2.0以下版本，注释掉pyproject.toml中这句
```
#package-mode = false
```

