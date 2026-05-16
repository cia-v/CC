# 车工计算软件 - Android APK 打包指南

## 📱 应用概述

本应用是基于 Kivy 框架开发的车工计算软件 Android 版本,包含以下功能模块:
- **基础参数计算**: 切削速度、主轴转速、进给量、切削深度
- **螺纹加工计算**: 公制/英制螺纹参数、G92/G76 循环代码生成
- **锥度与圆弧计算**: 圆锥参数、圆弧插补 R/I/K 值计算
- **数据管理**: 材料库(20种)、刀具库(10种)预置数据

## 🔧 打包环境要求

**重要提示**: Buildozer 只能在 **Linux 系统** 上打包 Android APK。macOS 和 Windows 用户需要使用以下方案之一:

### 方案一: 使用 Docker (推荐)

```bash
# 1. 安装 Docker Desktop
# 2. 在项目根目录执行:
docker run -v $(pwd):/app -it kivy/buildozer buildozer android debug

# 生成的 APK 位于: bin/lathecalculator-1.0.0-arm64-v8a_armeabi-v7a-debug.apk
```

### 方案二: 使用 Google Colab (免费云端 Linux)

1. 访问 https://colab.research.google.com/
2. 创建新笔记本,运行以下代码:

```python
!pip install buildozer
!apt-get install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# 上传项目文件到 Colab
from google.colab import files
uploaded = files.upload()

# 执行打包
!buildozer android debug

# 下载生成的 APK
from google.colab import files
files.download('bin/lathecalculator-1.0.0-arm64-v8a_armeabi-v7a-debug.apk')
```

### 方案三: 使用虚拟机

1. 安装 Ubuntu 22.04 LTS 虚拟机
2. 在虚拟机中执行:

```bash
# 安装依赖
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# 安装 Buildozer
pip3 install buildozer cython

# 进入项目目录并打包
cd /path/to/lathe_calculator_android
buildozer init  # 如果还没有 buildozer.spec
buildozer android debug
```

## 📦 打包步骤详解

### 1. 首次打包 (会下载大量依赖,约 1-2 GB)

```bash
cd /Users/clp/磁盘/车工计算/lathe_calculator_android
buildozer android debug
```

首次执行会:
- 下载 Android SDK (~500 MB)
- 下载 Android NDK (~800 MB)
- 编译 Python for Android
- 编译 Kivy 及依赖库
- 生成 APK

**预计耗时**: 30-60 分钟 (取决于网络速度)

### 2. 后续打包 (增量编译)

```bash
buildozer android debug
```

后续打包只需 5-10 分钟。

### 3. 生成发布版 APK (签名版)

```bash
buildozer android release
```

这会生成未签名的 APK,需要使用 jarsigner 或 apksigner 签名后才能安装。

## 📁 项目文件结构

```
lathe_calculator_android/
├── main.py                  # Kivy 应用主程序
├── buildozer.spec           # Buildozer 配置文件
├── lathe_calculator/        # 计算模块 (从桌面版复制)
│   ├── __init__.py
│   ├── basic_calc.py
│   ├── thread_calc.py
│   ├── taper_arc_calc.py
│   ├── data_manager.py
│   ├── constants.py
│   └── utils.py
├── bin/                     # 生成的 APK 存放目录
│   └── lathecalculator-1.0.0-arm64-v8a_armeabi-v7a-debug.apk
└── .buildozer/              # Buildozer 缓存目录 (自动生成)
```

## ⚙️ 配置说明 (buildozer.spec)

| 参数 | 说明 | 当前值 |
|------|------|--------|
| title | 应用名称 | 车工计算软件 |
| package.name | 包名 | lathecalculator |
| package.domain | 域名 | org.lathecalc |
| version | 版本号 | 1.0.0 |
| orientation | 屏幕方向 | portrait (竖屏) |
| android.api | 目标 API 级别 | 33 (Android 13) |
| android.minapi | 最低 API 级别 | 21 (Android 5.0) |
| android.archs | 支持的架构 | arm64-v8a, armeabi-v7a |

## 🐛 常见问题

### 1. 打包失败: "No module named 'lathe_calculator'"

**解决方案**: 确保 `lathe_calculator` 文件夹与 `main.py` 在同一目录下。

### 2. APK 安装后闪退

**原因**: 可能是权限问题或缺少依赖。

**解决方案**:
```bash
# 查看日志
adb logcat | grep python

# 检查权限
adb shell pm grant org.lathecalc.android.permission.WRITE_EXTERNAL_STORAGE
```

### 3. 网络下载超时

**解决方案**: 使用国内镜像源或代理。

```bash
# 设置 pip 镜像
export PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple

# 设置 Gradle 镜像 (编辑 ~/.gradle/init.gradle)
```

### 4. APK 体积过大 (>50 MB)

**优化方案**:
- 移除未使用的 Python 标准库模块
- 使用 `android.presplash_lottie` 替代静态图片
- 启用 ProGuard 压缩 (需要额外配置)

## 📲 安装测试

### 方法一: USB 调试安装

```bash
# 连接手机并开启 USB 调试
adb install bin/lathecalculator-1.0.0-arm64-v8a_armeabi-v7a-debug.apk
```

### 方法二: 扫码安装

将 APK 上传到网盘或服务器,生成二维码供手机扫描下载。

### 方法三: 直接传输

通过微信/QQ/蓝牙将 APK 文件发送到手机,点击安装。

**注意**: Android 8.0+ 需要允许"未知来源应用安装"权限。

## 🎨 界面预览

应用采用标签页设计,包含四个主要功能模块:

1. **基础计算**: 输入直径、转速等参数,实时计算切削速度、进给量等
2. **螺纹加工**: 支持公制/英制螺纹参数计算,生成分层切削表
3. **锥度/圆弧**: 计算圆锥角度、圆弧插补参数,输出 G 代码示例
4. **材料/刀具库**: 浏览预置的 20 种材料和 10 种刀具参数

## 📝 后续优化建议

1. **添加图标和启动画面**:
   ```
   icon.filename = icon.png
   presplash.filename = splash.png
   ```

2. **支持横屏模式**:
   ```
   orientation = all
   ```

3. **添加数据持久化**:
   - 使用 `kivy.storage.jsonstore` 保存计算历史
   - 支持用户自定义材料/刀具数据

4. **国际化支持**:
   - 添加英文界面切换
   - 使用 `kivy.lang` 的多语言支持

## 📞 技术支持

如遇问题,请提供:
- Buildozer 日志文件 (`.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/_python_bundle/_python_bundle.log`)
- 设备型号和 Android 版本
- 具体的错误信息截图

---

**最后更新**: 2026-05-15  
**版本**: 1.0.0  
**开发者**: 车工计算软件团队
