import ctypes
import subprocess
import sys

import psutil
from PyQt5.QtWidgets import QApplication,QMainWindow

from quick_renet import Ui_Dialog


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def show_ui():
    app = QApplication(sys.argv)
    mainWindows = QMainWindow()
    ui = Ui_Dialog()
    ui.setupUi(mainWindows)
    mainWindows.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    print("Quick_Renet --v1.0 by Rui")
    print("需要重新配置请删除.Selected文件")

    try:
        f = open(".Selected","r+",encoding='utf-8')
        line = f.readline()
        if line is not None and line != "":
        #     restart networks
            print("restart network")
            print(line,type(line))
            network = line
            if is_admin():
                disabled = f'netsh interface set interface "{network}" disabled'
                enabled = f'netsh interface set interface "{network}" enabled'

                if psutil.net_if_stats()[network].isup:  # 如果网卡是开启的，就先关闭它
                    subprocess.run(disabled, shell=True, stdout=subprocess.PIPE)
                subprocess.run(enabled, shell=True, stdout=subprocess.PIPE)
            else:
                if sys.version_info[0] == 3:
                    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        else:
        #     show UI
            show_ui()
    except FileNotFoundError:
        print("未找到配置文件,进行初始配置.")
        show_ui()
    except Exception as e:
        print(type(e))
        print(str(e))
