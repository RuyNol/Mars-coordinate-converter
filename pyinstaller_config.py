"""
pyinstaller打包配置
"""

import os
import sys
from pathlib import Path


def get_pyinstaller_options():
    """返回pyinstaller打包选项"""

    # 获取当前目录
    current_dir = Path(__file__).parent.absolute()

    # 图标文件路径
    icon_file = current_dir / "logo.ico"


    options = {
        # 主程序文件
        'script': 'main.py',

        # 输出选项
        'name': 'GIS坐标转换工具',
        'onefile': True,  # 打包为单个exe文件
        'console': False,  # 不显示控制台窗口
        'icon': str(icon_file) if icon_file.exists() else None,

        # 清理选项
        'clean': True,
        'noconfirm': True,

        # 优化选项
        'optimize': 2,  # 优化级别
        'strip': True,  # 剥离二进制文件

        # 隐藏导入（确保包含需要的模块）
        'hidden-imports': [
            'PIL',
            'PIL._tkinter_finder',
            'osgeo',
            'osgeo.gdal',
            'osgeo.ogr',
            'osgeo.osr',
            'json',
            'csv',
            'math',
            'datetime',
            'base64',
            'tkinter',
            'tkinter.ttk',
            'tkinter.filedialog',
            'tkinter.messagebox',
            'tkinter.scrolledtext',
            'warnings',
        ],

        # 排除不需要的模块（减小体积）
        'exclude-modules': [
            'matplotlib',
            'numpy',  # 除非你的程序需要numpy
            'scipy',
            'pandas',
            'test',
            'unittest',
            'pydoc',
            'doctest',
            'pdb',
        ],

        # 添加数据文件
        'datas': [
            # (源文件, 目标目录)
            ('logo.ico', '.'),
            ('qrcode.jpg', '.'),
        ] if (current_dir / "logo.ico").exists() else [],

        # 运行时钩子
        'runtime-hooks': [],

        # 其他选项
        'uac-admin': False,  # 不需要管理员权限
        'disable-windowed-traceback': True,
        'bootloader-ignore-signals': True,
    }

    return options


if __name__ == "__main__":
    options = get_pyinstaller_options()
    print("打包配置:")
    for key, value in options.items():
        print(f"  {key}: {value}")