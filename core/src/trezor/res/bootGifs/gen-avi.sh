#!/usr/bin/env sh

# 检查 ffmpeg 是否存在
if ! command -v ffmpeg &> /dev/null; then
  # 打印红色错误信息并退出
  echo -e "\033[31mffmpeg not found, please install ffmpeg\033[0m"
  exit 1
fi

# 如果 ffmpeg 存在，执行指定命令
ffmpeg -framerate 11 -i qingmiao_%02d.png -c:v mjpeg -q:v 2.3 -pix_fmt yuv420p ../booting.avi
