# = Elephant Toolkits Open

A collection of professional VFX pipeline tools for video post-production workflows.

English | [简体中文](README_zh.md)

## Tools

### Timecode Toolbox

A professional timecode toolbox combining converter and calculator for VFX and post-production workflows, built with PyQt5 and powered by the `dftt-timecode` library.

![Timecode Toolbox](https://img.shields.io/badge/PyQt5-Powered-blue)
![Python](https://img.shields.io/badge/Python-3.12+-green)

#### Features

**Timecode Converter:**
- **Multi-Format Conversion**: Convert between 7 different timecode formats
  - **SMPTE** (HH:MM:SS:FF) - Industry standard
  - **SRT** (HH:MM:SS,mmm) - Subtitle format
  - **DLP** (HH:MM:SS:sss) - Digital cinema format
  - **FFmpeg** (HH:MM:SS.xx) - FFmpeg format
  - **FCPX** (fraction/s) - Final Cut Pro X format
  - **Frame** (count) - Frame number
  - **Time** (seconds) - Decimal seconds

**Timecode Calculator:**
- **Timecode Arithmetic**: Perform addition and subtraction operations on timecodes
- **Calculation History**: Keeps track of your last 10 calculations
- **Real-time Results**: Instant calculation with format conversion

**Common Features:**
- **Multiple Frame Rates**: Support for industry-standard frame rates
  - 23.976 fps (Film)
  - 24 fps (Cinema)
  - 25 fps (PAL)
  - 29.97 fps (NTSC Drop-frame)
  - 30 fps (NTSC)
  - 50 fps (PAL High Frame Rate)
  - 59.94 fps (NTSC High Frame Rate)
  - 60 fps (High Frame Rate)

- **Auto-formatting Input**: Automatically formats timecode as you type
- **Dark Theme UI**: Professional dark interface matching VFX pipeline aesthetics
- **Drop Frame Support**: Handle drop-frame timecode for 29.97 and 59.94 fps
- **Strict Mode**: Optional strict mode for 24-hour timecode validation

#### Usage

```bash
# Run the Timecode Toolbox
python scripts_ui/TC_Toolbox.py
```

#### Use Cases

- **Editorial**: Calculate edit durations and offsets
- **VFX**: Compute frame ranges and timecode offsets
- **Conform**: Convert timecodes between different formats
- **Grading**: Calculate timeline positions across different frame rates
- **Subtitling**: Work with SRT format timecodes
- **Audio Post**: Convert timecodes for audio sync workflows

---

### WAV Timecode Batch Offset Tool

A command-line tool for batch modifying BWF timecode (TimeReference) in WAV files with frame-accurate offsets. Designed for audio post-production workflows requiring synchronized timecode adjustments.

![CLI Tool](https://img.shields.io/badge/CLI-Tool-orange)
![Python](https://img.shields.io/badge/Python-3.8+-green)

#### Features

- **Batch Processing**: Process entire folders of WAV files automatically
- **Frame Offset**: Offset timecode by specified number of frames (positive or negative)
- **Auto Detection**: Automatically read sample rate and current timecode from files
- **Multiple Frame Rates**: 23.976, 24, 25, 29.97, 30, 50, 59.94, 60 fps
- **SMPTE Display**: Show timecode in standard HH:MM:SS:FF format
- **Progress Reporting**: Real-time display of processing status and statistics
- **BWF Metadata**: Direct manipulation of Broadcast Wave Format metadata
- **Non-Destructive**: Only modifies metadata, audio data remains untouched

#### Requirements

- **bwfmetaedit**: Command-line tool for BWF metadata editing
  ```bash
  # macOS
  brew install bwfmetaedit

  # Linux
  apt-get install bwfmetaedit
  ```

#### Usage

1. Edit configuration in `AKLD/wav_tc_offset.py`:
   ```python
   INPUT_FOLDER = "/path/to/wav/files/"
   OFFSET_FRAMES = -934  # Negative for backward, positive for forward
   FRAME_RATE = 24
   ```

2. Run the script:
   ```bash
   python AKLD/wav_tc_offset.py
   ```

#### Example Output

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

============================================================
完成! 成功处理 56/56 个文件
```

#### Use Cases

- **Audio Sync**: Adjust timecode to match video edits
- **Conform**: Offset audio timecode after video conform
- **Multi-cam**: Synchronize timecode across multiple audio recordings
- **Archive**: Correct timecode errors in archived recordings

## Installation

### Prerequisites

- Python 3.12 or higher
- pip or uv package manager

### Install with uv (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/Elephant-Toolkits-Open.git
cd Elephant-Toolkits-Open

# Install dependencies with uv
uv sync
```

### Install with pip

```bash
# Clone the repository
git clone https://github.com/yourusername/Elephant-Toolkits-Open.git
cd Elephant-Toolkits-Open

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Dependencies

- **dftt-timecode** (>=0.0.14) - Professional timecode library
- **PyQt5** (>=5.15.11) - GUI framework
- **numpy** (>=2.3.3) - Numerical computing
- **pybmd** (>=2025.2.4) - Blackmagic Design support

## Development

This is the open-source version of Elephant Toolkits, containing selected tools from the main VFX pipeline toolkit.

### Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

### License

See [LICENSE](LICENSE) file for details.

## About

Elephant Toolkits Open is designed to provide professional-grade tools for video post-production workflows. Each tool is crafted with attention to industry standards and practical usability.

---

Made with d for the VFX and post-production community
