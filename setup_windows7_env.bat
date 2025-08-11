@echo off

:: 检查是否安装了Python 3.10
python --version 2>nul | findstr /C:"Python 3.10" >nul
if %ERRORLEVEL% NEQ 0 (
    echo 未找到Python 3.10，请先安装Python 3.10版本。
    echo 可以从以下地址下载：https://www.python.org/downloads/release/python-31011/
    pause
    exit /b 1
)

:: 创建虚拟环境
echo 创建虚拟环境...
python -m venv venv_win7
if %ERRORLEVEL% NEQ 0 (
    echo 创建虚拟环境失败。
    pause
    exit /b 1
)

:: 激活虚拟环境
echo 激活虚拟环境...
call venv_win7\Scripts\activate.bat
if %ERRORLEVEL% NEQ 0 (
    echo 激活虚拟环境失败。
    pause
    exit /b 1
)

:: 使用清华镜像安装依赖
echo 使用清华镜像安装依赖...
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements-windows.txt
if %ERRORLEVEL% NEQ 0 (
    echo 安装依赖失败。
    pause
    exit /b 1
)

:: 提示用户环境配置完成
echo.
echo ======================================
echo Windows 7环境配置完成！
echo.
echo 后续操作提示：
echo 1. 运行项目：在激活虚拟环境后，执行 'python KeymouseGo.py'
echo 2. 打包项目：在激活虚拟环境后，执行 'pyinstaller -Fw --icon=Mondrian.ico --add-data "./assets;assets" --win-private-assemblies --target-architecture=32bit KeymouseGo.py'
echo ======================================

pause