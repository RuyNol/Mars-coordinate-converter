"""
打包脚本 - 执行此脚本进行打包
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
#from pyinstaller_config import get_pyinstaller_options

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

def run_pyinstaller():
    """运行pyinstaller打包"""

    # 导入配置
    #from pyinstaller_config import get_pyinstaller_options

    options = get_pyinstaller_options()

    # 构建pyinstaller命令
    cmd = ['pyinstaller']

    # 添加选项
    if options.get('onefile'):
        cmd.append('--onefile')

    if not options.get('console'):
        cmd.append('--windowed')

    if options.get('icon'):
        cmd.extend(['--icon', options['icon']])

    if options.get('name'):
        cmd.extend(['--name', options['name']])

    # 添加隐藏导入
    for hidden_import in options.get('hidden-imports', []):
        cmd.extend(['--hidden-import', hidden_import])

    # 添加排除模块
    for exclude_module in options.get('exclude-modules', []):
        cmd.extend(['--exclude-module', exclude_module])

    # 添加数据文件
    for data_src, data_dst in options.get('datas', []):
        cmd.extend(['--add-data', f'{data_src}{os.pathsep}{data_dst}'])

    # 添加其他选项
    if options.get('clean'):
        cmd.append('--clean')

    if options.get('noconfirm'):
        cmd.append('--noconfirm')

    # 优化选项 - 修正-O参数的使用方式
    if options.get('optimize'):
        # PyInstaller 6.x 版本中，-O 参数的使用方式已变更
        # 可以使用 --optimize 或 -O 但需要正确格式
        level = str(options['optimize'])
        cmd.append(f'--optimize={level}')  # 使用 --optimize=2 格式

    if options.get('strip'):
        cmd.append('--strip')

    # 添加运行时钩子
    for hook in options.get('runtime-hooks', []):
        cmd.extend(['--runtime-hook', hook])

    # UAC选项
    if options.get('uac-admin'):
        cmd.append('--uac-admin')

    # 添加禁用窗口回溯选项
    cmd.append('--disable-windowed-traceback')

    # 添加引导加载器忽略信号选项
    cmd.append('--bootloader-ignore-signals')

    # 最终添加主脚本
    cmd.append(options['script'])

    # 打印命令
    print("执行命令:")
    print(' '.join(cmd))
    print("\n" + "="*50 + "\n")

    # 执行打包
    try:
        result = subprocess.run(cmd, check=True, text=True, capture_output=True)
        print("打包输出:")
        print(result.stdout)

        if result.stderr:
            print("错误信息:")
            print(result.stderr)

        return True

    except subprocess.CalledProcessError as e:
        print(f"打包失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False

def cleanup_build_files():
    """清理构建过程中产生的临时文件"""
    files_to_remove = [
        'build',
        f'{get_pyinstaller_options().get("name", "GIS坐标转换工具")}.spec',
    ]

    for file in files_to_remove:
        if os.path.exists(file):
            if os.path.isdir(file):
                shutil.rmtree(file)
            else:
                os.remove(file)
            print(f"已删除: {file}")

def create_dist_folder():
    """创建发布文件夹"""
    dist_dir = Path("dist")
    if not dist_dir.exists():
        dist_dir.mkdir()

    # 复制必要的文件到dist目录
    files_to_copy = [
        'README.md',
        'logo.ico',
        'qrcode.jpg',
    ]

    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, dist_dir / file)
            print(f"已复制: {file}")

def main():
    """主函数"""
    print("="*50)
    print("开始打包GIS坐标转换工具")
    print("="*50)

    # 检查pyinstaller是否安装
    try:
        import PyInstaller
        print(f"PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("错误: 未安装PyInstaller")
        print("请运行: pip install pyinstaller")
        return

    # 执行打包
    success = run_pyinstaller()

    if success:
        print("\n" + "="*50)
        print("打包成功!")

        # 清理临时文件
        cleanup_build_files()

        # 创建发布文件夹
        create_dist_folder()

        # 显示结果
        exe_name = get_pyinstaller_options().get('name', 'GIS坐标转换工具')
        exe_path = Path("dist") / f"{exe_name}.exe"

        if exe_path.exists():
            print(f"\n生成的可执行文件:")
            print(f"  {exe_path}")
            print(f"  文件大小: {exe_path.stat().st_size / 1024 / 1024:.2f} MB")

            print("\n使用方法:")
            print("  1. 将dist文件夹中的文件复制到任意位置")
            print("  2. 双击运行 'GIS坐标转换工具.exe'")
            print("  3. 不需要安装Python或其他依赖")
        else:
            print(f"\n警告: 未找到生成的可执行文件 {exe_path}")

    else:
        print("\n打包失败，请检查错误信息")

if __name__ == "__main__":
    main()