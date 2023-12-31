import subprocess
import sys
import os


def create_venv():
    print(sys.executable)
    # 创建虚拟环境
    subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)


def install_requirements():
    # 激活虚拟环境
    activate_script = "venv\\Scripts\\activate" if os.name == "nt" else "source venv/bin/activate"
    subprocess.run(activate_script, shell=True, check=True)

    # 安装依赖
    subprocess.run(["venv\\Scripts\\pip.exe", "install", "-r", "requirements.txt"], check=True, shell=True)


def run_script():
    # 运行脚本
    subprocess.run(["venv\\Scripts\\python.exe", "init.py"], check=True, shell=True)


def main():
    # 创建虚拟环境
    create_venv()

    # 安装依赖
    install_requirements()

    # 运行脚本
    run_script()


if __name__ == "__main__":
    main()
