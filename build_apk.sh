#!/bin/bash
# 车工计算软件 - Android APK 打包脚本
# 仅在 Linux 环境下运行

set -e  # 遇到错误立即退出

echo "=========================================="
echo "车工计算软件 - Android APK 打包工具"
echo "=========================================="
echo ""

# 检查是否在 Linux 环境
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "❌ 错误: 此脚本只能在 Linux 系统上运行"
    echo ""
    echo "当前系统: $OSTYPE"
    echo ""
    echo "请使用以下方案之一:"
    echo "1. Docker: docker run -v \$(pwd):/app -it kivy/buildozer buildozer android debug"
    echo "2. Google Colab: 上传项目到云端执行"
    echo "3. Ubuntu 虚拟机: 安装 Ubuntu 22.04 后运行此脚本"
    exit 1
fi

# 检查 Buildozer 是否安装
if ! command -v buildozer &> /dev/null; then
    echo "⚠️  Buildozer 未安装,正在安装..."
    pip3 install buildozer cython
fi

# 检查依赖
echo "📦 检查系统依赖..."
sudo apt-get update -qq
sudo apt-get install -y -qq git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev > /dev/null 2>&1
echo "✅ 依赖检查完成"
echo ""

# 清理旧构建
if [ -d ".buildozer" ]; then
    read -p "⚠️  检测到旧的构建缓存,是否清理? (y/n): " clean_choice
    if [ "$clean_choice" = "y" ] || [ "$clean_choice" = "Y" ]; then
        echo "🗑️  清理旧构建..."
        rm -rf .buildozer bin
        echo "✅ 清理完成"
    fi
fi

# 开始打包
echo ""
echo "🚀 开始打包 APK..."
echo "   首次打包需要下载约 1-2 GB 依赖,预计耗时 30-60 分钟"
echo "   后续打包仅需 5-10 分钟"
echo ""

buildozer android debug

# 检查是否成功
if [ -f "bin/lathecalculator-1.0.0-arm64-v8a_armeabi-v7a-debug.apk" ]; then
    echo ""
    echo "=========================================="
    echo "✅ 打包成功!"
    echo "=========================================="
    echo ""
    echo "APK 文件位置: bin/lathecalculator-1.0.0-arm64-v8a_armeabi-v7a-debug.apk"
    echo ""
    echo "文件大小:"
    ls -lh bin/lathecalculator-1.0.0-arm64-v8a_armeabi-v7a-debug.apk
    echo ""
    echo "安装方法:"
    echo "1. USB 调试: adb install bin/lathecalculator-1.0.0-arm64-v8a_armeabi-v7a-debug.apk"
    echo "2. 扫码安装: 将 APK 上传到网盘生成二维码"
    echo "3. 直接传输: 通过微信/QQ/蓝牙发送到手机"
    echo ""
else
    echo ""
    echo "=========================================="
    echo "❌ 打包失败"
    echo "=========================================="
    echo ""
    echo "请查看日志文件获取详细信息:"
    echo ".buildozer/android/platform/build-arm64-v8a_armeabi-v7a/_python_bundle/_python_bundle.log"
    echo ""
    exit 1
fi
