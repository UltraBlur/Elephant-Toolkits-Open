# 🐘 Elephant Toolkits Open

专为视频后期制作工作流程设计的专业 VFX 流程工具集。

[English](README.md) | 简体中文

## 工具列表

### 时间码计算器（Timecode Calculator）

专为 VFX 和后期制作工作流程设计的专业时间码计算器，基于 PyQt5 构建，由 `dftt-timecode` 库驱动。

![Timecode Calculator](https://img.shields.io/badge/PyQt5-Powered-blue)
![Python](https://img.shields.io/badge/Python-3.12+-green)

#### 功能特性

- **时间码运算**：支持时间码的加法和减法运算
- **多帧率支持**：支持行业标准帧率
  - 23.976 fps（电影）
  - 24 fps（影院）
  - 25 fps（PAL 制式）
  - 29.97 fps（NTSC 丢帧）
  - 30 fps（NTSC）
  - 50 fps（PAL 高帧率）
  - 59.94 fps（NTSC 高帧率）
  - 60 fps（高帧率）

- **多种时间码格式**：
  - **SMPTE** (HH:MM:SS:FF) - 行业标准
  - **SRT** (HH:MM:SS,mmm) - 字幕格式
  - **DLP** (HH:MM:SS:sss) - 数字电影格式
  - **FFmpeg** (HH:MM:SS.xx) - FFmpeg 格式
  - **FCPX** (fraction/s) - Final Cut Pro X 格式
  - **Frame** (count) - 帧编号
  - **Time** (seconds) - 十进制秒数

- **自动格式化输入**：输入时自动格式化时间码
- **计算历史记录**：保存最近 10 次计算记录
- **深色主题界面**：符合 VFX 流程美学的专业深色界面
- **格式转换**：在不同格式之间即时转换时间码

#### 使用方法

```bash
# 运行时间码计算器
python scripts_ui/TC_Calculator.py
```

#### 界面特性

计算器包含以下特性：
- 简洁直观的深色主题界面
- 实时输入格式化
- 可视化操作选择（加/减）
- 即时格式切换和自动转换
- 持久化计算历史记录

#### 应用场景

- **剪辑**：计算剪辑时长和偏移量
- **特效**：计算帧范围和时间码偏移
- **套底**：在不同格式之间转换时间码
- **调色**：计算不同帧率下的时间线位置
- **字幕**：处理 SRT 格式时间码

## 安装

### 环境要求

- Python 3.12 或更高版本
- pip 或 uv 包管理器

### 使用 uv 安装（推荐）

```bash
# 克隆仓库
git clone https://github.com/yourusername/Elephant-Toolkits-Open.git
cd Elephant-Toolkits-Open

# 使用 uv 安装依赖
uv sync
```

### 使用 pip 安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/Elephant-Toolkits-Open.git
cd Elephant-Toolkits-Open

# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Windows 系统: .venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

## 依赖项

- **dftt-timecode** (>=0.0.14) - 专业时间码库
- **PyQt5** (>=5.15.11) - GUI 框架
- **numpy** (>=2.3.3) - 数值计算
- **pybmd** (>=2025.2.4) - Blackmagic Design 支持

## 开发

这是 Elephant Toolkits 的开源版本，包含从主 VFX 流程工具包中精选的工具。

### 贡献

欢迎贡献！请随时提交问题或拉取请求。

### 许可证

详见 [LICENSE](LICENSE) 文件。

## 关于

Elephant Toolkits Open 旨在为视频后期制作工作流程提供专业级工具。每个工具都经过精心设计，符合行业标准，注重实用性。

---

用 ❤️ 为 VFX 和后期制作社区打造
