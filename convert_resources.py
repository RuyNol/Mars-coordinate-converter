#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将图片资源转换为Python代码，以便打包进单个exe
"""

import base64
import os
from pathlib import Path


def pic2py(picture_names: list, py_name):
    """将图片转换为Python代码"""
    write_data = []

    print(f"正在转换图片到 {py_name}.py...")

    for picture_name in picture_names:
        if not os.path.exists(picture_name):
            print(f"警告: 图片文件不存在: {picture_name}")
            continue

        # 生成变量名（将.替换为_）
        filename = os.path.basename(picture_name)
        var_name = filename.replace('.', '_')

        print(f"  转换: {picture_name} -> {var_name}")

        with open(picture_name, 'rb') as r:
            b64str = base64.b64encode(r.read())

        # 注意：b64str 一定要加上.decode()
        write_data.append('%s = "%s"\n' % (var_name, b64str.decode()))

    if write_data:
        with open(f'{py_name}.py', 'w+', encoding='utf-8') as w:
            # 添加文件头注释
            w.write('# -*- coding: utf-8 -*-\n')
            w.write('# 本文件由 convert_resources.py 自动生成\n')
            w.write('# 包含打包到exe中的图片资源\n\n')

            for data in write_data:
                w.write(data)

        print(f"✓ 已生成 {py_name}.py")
        return True
    else:
        print("✗ 没有生成任何图片数据")
        return False


def convert_logo_to_base64():
    """转换logo.ico到base64"""
    logo_files = ['logo.ico', 'logo.png', 'logo.jpg']

    for logo_file in logo_files:
        if os.path.exists(logo_file):
            return pic2py([logo_file], 'logo_resources')

    print("未找到logo文件，将使用默认图标")
    return False


def convert_qrcode_to_base64():
    """转换二维码图片到base64"""
    qrcode_files = ['qrcode.jpg', 'qrcode.png', 'wechat_qrcode.jpg']

    for qrcode_file in qrcode_files:
        if os.path.exists(qrcode_file):
            return pic2py([qrcode_file], 'qrcode_resources')

    print("未找到二维码文件")
    return False


def convert_all_resources():
    """转换所有资源文件"""
    print("=" * 60)
    print("资源文件转换工具")
    print("=" * 60)

    # 转换logo
    logo_converted = convert_logo_to_base64()

    # 转换二维码
    qrcode_converted = convert_qrcode_to_base64()

    print("\n" + "=" * 60)
    print("转换完成！")

    if logo_converted or qrcode_converted:
        print("生成的Python文件:")
        if logo_converted:
            print("  - logo_resources.py")
        if qrcode_converted:
            print("  - qrcode_resources.py")

        print("\n现在可以修改主程序，从这些文件中导入图片数据")
    else:
        print("没有找到任何图片文件，将不使用自定义图标和二维码")

    print("=" * 60)
    return logo_converted or qrcode_converted


def create_temp_image_from_base64(base64_str, temp_filename):
    """从base64字符串创建临时图片文件"""
    import tempfile

    # 解码base64
    image_data = base64.b64decode(base64_str)

    # 创建临时文件
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, temp_filename)

    with open(temp_path, 'wb') as f:
        f.write(image_data)

    return temp_path


if __name__ == "__main__":
    convert_all_resources()
    input("\n按Enter键退出...")