# 环境搭建

1.安装 arm-none-eabi-gcc  
2.安装 stm32cubeide 与 stm32cubeprogrammer  
3.复制 core/tools/GD25Qxx-DunAn-8MB.stldr 到 stm32cubeprogrammer 安装目录的 ExternalLoader 文件夹中  
4.在项目根目录创建.env.sh 内容为

```
STM32PROG_DIR=/path/to/your/stm32cubeprogrmmer
```

# 代码编译

```
git submodule update --init --recursivecd
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
第一次烧录后，硬件上电进行bootloader，会在电脑系统上挂载两个U盘，把core/src/trezor/res 文件夹下除res/nfts文件拷贝到SYSTEM盘符下
