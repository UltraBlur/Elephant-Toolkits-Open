#!/usr/bin/env python3
"""
WAV文件时间码批量偏移脚本
========================================

功能说明:
    批量修改WAV文件的BWF时间码(TimeReference)，支持按帧数进行精确偏移。
    适用于音频后期制作中需要统一调整时间码的场景。

主要特性:
    - 批量处理整个文件夹的WAV文件
    - 支持正向/负向帧数偏移
    - 自动读取WAV文件的采样率和当前时间码
    - 支持多种帧率(23.976, 24, 25, 29.97, 30, 50, 59.94, 60等)
    - 显示SMPTE格式的时间码(HH:MM:SS:FF)
    - 处理结果统计和错误提示

依赖工具:
    - bwfmetaedit: 用于读写WAV文件的BWF元数据
      安装: macOS: brew install bwfmetaedit
           Linux: apt-get install bwfmetaedit
    - dftt-timecode: Python时间码处理库
      安装: pip install dftt-timecode

使用方法:
    1. 修改下方"配置区域"中的参数:
       - INPUT_FOLDER: 输入文件夹路径
       - OFFSET_FRAMES: 偏移帧数(正数向后，负数向前)
       - FRAME_RATE: 项目帧率
    2. 运行脚本: python wav_tc_offset.py

作者: Claude Code
版本: 1.0
"""

import os
import subprocess
import csv
from io import StringIO
from pathlib import Path
from dftt_timecode import DfttTimecode

# ============ 配置区域 - 在这里修改参数 ============
INPUT_FOLDER = "/Users/gaohuyuchen/Downloads/DAY004_Offset/"  # 输入文件夹路径
OFFSET_FRAMES = 146  # 偏移帧数（正数向后偏移，负数向前偏移）
FRAME_RATE = 24  # 帧率 (23.976, 24, 25, 29.97, 30, 50, 59.94, 60 等)
# =================================================

def get_wav_timecode(wav_path):
    """读取WAV文件的时间码"""
    try:
        result = subprocess.run(
            ['bwfmetaedit', '--out-core', wav_path],
            capture_output=True,
            text=True,
            check=True
        )

        # 使用csv模块正确解析CSV输出（处理引号和换行符）
        csv_reader = csv.DictReader(StringIO(result.stdout))

        # 读取第一行数据
        try:
            row = next(csv_reader)

            # 获取TimeReference值
            if 'TimeReference' in row:
                time_ref_value = row['TimeReference'].strip()
                if time_ref_value:
                    samples = int(time_ref_value)
                    return samples
                else:
                    print(f"  警告: TimeReference为空")
                    return None
            else:
                print(f"  错误: 未找到TimeReference列")
                return None

        except StopIteration:
            print(f"  错误: CSV无数据行")
            return None
        except ValueError as e:
            print(f"  错误: TimeReference值无法转换为整数: {row.get('TimeReference', 'N/A')}")
            return None

    except subprocess.CalledProcessError as e:
        print(f"  错误: 无法读取 {wav_path} 的时间码")
        return None
    except FileNotFoundError:
        print("  错误: 未找到 bwfmetaedit 工具，请先安装")
        print("  macOS: brew install bwfmetaedit")
        print("  Linux: apt-get install bwfmetaedit 或从源码编译")
        return None

def get_sample_rate(wav_path):
    """读取WAV文件的采样率"""
    try:
        result = subprocess.run(
            ['bwfmetaedit', '--out-core', wav_path],
            capture_output=True,
            text=True,
            check=True
        )
        
        for line in result.stdout.split('\n'):
            if 'SampleRate' in line:
                sample_rate = int(line.split(':')[-1].strip())
                return sample_rate
        return 48000  # 默认值
    except:
        return 48000

def set_wav_timecode(wav_path, samples):
    """设置WAV文件的时间码"""
    try:
        subprocess.run(
            ['bwfmetaedit', f'--Timereference={samples}', wav_path],
            check=True,
            capture_output=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"  错误: 无法写入 {wav_path} 的时间码")
        if e.stderr:
            print(f"  详情: {e.stderr.decode() if isinstance(e.stderr, bytes) else e.stderr}")
        return False

def samples_to_timecode(samples, sample_rate, frame_rate):
    """将样本数转换为时间码"""
    seconds = samples / sample_rate
    # 使用float类型创建时间码，timecode_type='time'表示输入是秒数
    return DfttTimecode(seconds, timecode_type='time', fps=frame_rate)

def timecode_to_samples(timecode, sample_rate):
    """将时间码转换为样本数"""
    # 使用timestamp属性获取秒数
    seconds = timecode.timestamp
    return int(seconds * sample_rate)

def offset_timecode(timecode, offset_frames, frame_rate):
    """偏移时间码指定帧数"""
    # 使用framecount属性获取总帧数
    total_frames = timecode.framecount

    # 应用偏移
    new_frames = total_frames + offset_frames

    # 确保不为负数
    if new_frames < 0:
        print(f"警告: 偏移后时间码为负数，将设置为 00:00:00:00")
        new_frames = 0

    # 使用int类型创建时间码，timecode_type='frame'表示输入是帧数
    return DfttTimecode(new_frames, timecode_type='frame', fps=frame_rate)

def process_wav_files(folder_path, offset_frames, frame_rate):
    """批量处理文件夹中的所有WAV文件"""
    folder = Path(folder_path)
    
    if not folder.exists():
        print(f"错误: 文件夹不存在: {folder_path}")
        return
    
    # 获取所有WAV文件
    wav_files = list(folder.glob("*.wav")) + list(folder.glob("*.WAV"))
    
    if not wav_files:
        print(f"未在 {folder_path} 中找到WAV文件")
        return
    
    print(f"找到 {len(wav_files)} 个WAV文件")
    print(f"偏移参数: {offset_frames} 帧 @ {frame_rate} fps")
    print("-" * 60)
    
    success_count = 0
    
    for wav_file in wav_files:
        print(f"\n处理: {wav_file.name}")
        
        # 读取当前时间码
        current_samples = get_wav_timecode(str(wav_file))
        if current_samples is None:
            continue
        
        # 读取采样率
        sample_rate = get_sample_rate(str(wav_file))
        
        # 转换为时间码
        current_tc = samples_to_timecode(current_samples, sample_rate, frame_rate)
        print(f"  当前时间码: {current_tc.timecode_output('smpte')}")

        # 应用偏移
        new_tc = offset_timecode(current_tc, offset_frames, frame_rate)
        print(f"  新时间码:   {new_tc.timecode_output('smpte')}")
        
        # 转换回样本数
        new_samples = timecode_to_samples(new_tc, sample_rate)
        
        # 写入新时间码
        if set_wav_timecode(str(wav_file), new_samples):
            print(f"  ✓ 成功")
            success_count += 1
        else:
            print(f"  ✗ 失败")
    
    print("\n" + "=" * 60)
    print(f"完成! 成功处理 {success_count}/{len(wav_files)} 个文件")

if __name__ == "__main__":
    print("=" * 60)
    print("WAV 时间码批量偏移工具")
    print("=" * 60)
    
    # 执行处理
    process_wav_files(INPUT_FOLDER, OFFSET_FRAMES, FRAME_RATE)