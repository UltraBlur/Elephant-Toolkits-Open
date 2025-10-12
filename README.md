# = Elephant Toolkits Open

A collection of professional VFX pipeline tools for video post-production workflows.

English | [简体中文](README_zh.md)

## Tools

### Timecode Calculator

A professional timecode calculator designed for VFX and post-production workflows, built with PyQt5 and powered by the `dftt-timecode` library.

![Timecode Calculator](https://img.shields.io/badge/PyQt5-Powered-blue)
![Python](https://img.shields.io/badge/Python-3.12+-green)

#### Features

- **Timecode Arithmetic**: Perform addition and subtraction operations on timecodes
- **Multiple Frame Rates**: Support for industry-standard frame rates
  - 23.976 fps (Film)
  - 24 fps (Cinema)
  - 25 fps (PAL)
  - 29.97 fps (NTSC Drop-frame)
  - 30 fps (NTSC)
  - 50 fps (PAL High Frame Rate)
  - 59.94 fps (NTSC High Frame Rate)
  - 60 fps (High Frame Rate)

- **Multiple Timecode Formats**:
  - **SMPTE** (HH:MM:SS:FF) - Industry standard
  - **SRT** (HH:MM:SS,mmm) - Subtitle format
  - **DLP** (HH:MM:SS:sss) - Digital cinema format
  - **FFmpeg** (HH:MM:SS.xx) - FFmpeg format
  - **FCPX** (fraction/s) - Final Cut Pro X format
  - **Frame** (count) - Frame number
  - **Time** (seconds) - Decimal seconds

- **Auto-formatting Input**: Automatically formats timecode as you type
- **Calculation History**: Keeps track of your last 10 calculations
- **Dark Theme UI**: Professional dark interface matching VFX pipeline aesthetics
- **Format Conversion**: Instantly convert timecodes between different formats

#### Usage

```bash
# Run the Timecode Calculator
python scripts_ui/TC_Calculator.py
```

#### Screenshots

The calculator features:
- Clean, intuitive interface with dark theme
- Real-time input formatting
- Visual operation selection (+/-)
- Instant format switching with automatic conversion
- Persistent calculation history

#### Use Cases

- **Editorial**: Calculate edit durations and offsets
- **VFX**: Compute frame ranges and timecode offsets
- **Conform**: Convert timecodes between different formats
- **Grading**: Calculate timeline positions across different frame rates
- **Subtitling**: Work with SRT format timecodes

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
