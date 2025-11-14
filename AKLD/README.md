# WAV Timecode Batch Offset Tool
# WAV时间码批量偏移工具

A command-line tool for batch modifying BWF timecode (TimeReference) in WAV files with frame-accurate offsets.

命令行工具，用于批量修改WAV文件的BWF时间码(TimeReference)，支持按帧数进行精确偏移。

## Features | 功能特性

- **Batch Processing** | **批量处理**: Process entire folders of WAV files automatically
- **Frame Offset** | **帧数偏移**: Offset timecode by specified number of frames (positive or negative)
- **Auto Detection** | **自动检测**: Automatically read sample rate and current timecode from files
- **Multiple Frame Rates** | **多帧率支持**: 23.976, 24, 25, 29.97, 30, 50, 59.94, 60 fps
- **SMPTE Display** | **SMPTE显示**: Show timecode in standard HH:MM:SS:FF format
- **Progress Reporting** | **进度报告**: Real-time display of processing status and statistics

## 系统要求

- Python 3.8+
- macOS / Linux
- bwfmetaedit 工具

## 安装

### 1. 安装 bwfmetaedit

**macOS:**
```bash
brew install bwfmetaedit
```

**Linux:**
```bash
apt-get install bwfmetaedit
```

或从源码编译: https://mediaarea.net/BWFMetaEdit

### 2. 安装 Python 依赖

推荐使用 `uv` 进行 Python 包管理：

**安装 uv:**
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# 或使用 pip
pip install uv
```

**创建虚拟环境并安装依赖:**
```bash
# 创建虚拟环境
uv venv

# 激活虚拟环境
source .venv/bin/activate  # macOS/Linux
# 或 Windows: .venv\Scripts\activate

# 安装依赖
uv pip install dftt-timecode
```

## 使用方法

### 1. 配置参数

编辑 `wav_tc_offset.py` 文件中的配置区域：

```python
# ============ 配置区域 - 在这里修改参数 ============
INPUT_FOLDER = "/path/to/your/wav/files/"  # 输入文件夹路径
OFFSET_FRAMES = -934  # 偏移帧数（正数向后偏移，负数向前偏移）
FRAME_RATE = 24  # 帧率 (23.976, 24, 25, 29.97, 30, 50, 59.94, 60 等)
# =================================================
```

**参数说明:**
- `INPUT_FOLDER`: WAV文件所在的文件夹路径
- `OFFSET_FRAMES`: 偏移的帧数
  - 正数: 向后偏移（时间码增加）
  - 负数: 向前偏移（时间码减少）
- `FRAME_RATE`: 项目帧率，需与视频帧率一致

### 2. 运行脚本

```bash
# 确保虚拟环境已激活
source .venv/bin/activate

# 运行脚本
python wav_tc_offset.py
```

### 3. 查看结果

脚本会显示每个文件的处理过程：

```
============================================================
WAV 时间码批量偏移工具
============================================================
找到 56 个WAV文件
偏移参数: -934 帧 @ 24 fps
------------------------------------------------------------

处理: 171112_T41_1_2_3_4.WAV
  当前时间码: 06:03:19:00
  新时间码:   06:02:40:02
  ✓ 成功

处理: 171112_T31_1_2_3_4.WAV
  当前时间码: 05:32:51:00
  新时间码:   05:32:12:02
  ✓ 成功

...

============================================================
完成! 成功处理 56/56 个文件
```

## 工作原理

1. **读取时间码**: 使用 `bwfmetaedit` 读取WAV文件的BWF元数据中的 TimeReference 值（样本数）
2. **转换计算**:
   - 将样本数转换为时间码（基于采样率和帧率）
   - 应用帧数偏移
   - 将新时间码转换回样本数
3. **写入时间码**: 使用 `bwfmetaedit` 将新的 TimeReference 值写入WAV文件

## 常见问题

### Q: 为什么选择 uv 而不是 pip？

A: `uv` 是一个极快的 Python 包管理器，比 pip 快 10-100 倍，并且提供更好的依赖解析和虚拟环境管理。

### Q: 脚本会修改原始文件吗？

A: 是的，脚本会直接修改WAV文件的元数据。建议在运行前备份重要文件。

### Q: 支持哪些WAV文件格式？

A: 支持包含BWF (Broadcast Wave Format) 元数据的WAV文件。这是专业音频录制设备的标准格式。

### Q: 时间码为负数怎么办？

A: 如果偏移后时间码为负数，脚本会自动将其设置为 `00:00:00:00` 并显示警告。

### Q: 可以处理子文件夹吗？

A: 当前版本只处理指定文件夹中的WAV文件，不递归处理子文件夹。

## 技术细节

### 依赖库

- **dftt-timecode**: 专业的时间码处理库，支持多种时间码格式转换
  - SMPTE (HH:MM:SS:FF)
  - Frame count
  - Seconds
  - SRT, DLP, FFmpeg, FCPX 等格式

- **bwfmetaedit**: MediaArea 开发的 BWF 元数据编辑工具
  - 读写 BWF 元数据
  - 支持批量处理
  - 命令行界面

### 时间码计算

```
样本数 = 时间码(秒) × 采样率
时间码(秒) = 帧数 / 帧率
```

例如，在 48kHz 采样率、24fps 的情况下：
- 1帧 = 1/24秒 = 2000样本
- 偏移 -934帧 = -934/24秒 = -1,868,000样本

## 许可证

MIT License

## 作者

Claude Code

## 更新日志

### v1.0 (2025-01-14)
- 初始版本
- 支持批量WAV时间码偏移
- 支持多种帧率
- SMPTE时间码显示
