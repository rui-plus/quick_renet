import ctypes
import sys
import subprocess
import psutil
import time


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def input_num(networks):
    falg = True
    while falg:
        try:
            key = int(input("Input id:"))
            if 0 < key and key <= len(networks):
                falg = False
                return key
        except:
            print("请输入编号-例如1")
            pass


if __name__ == '__main__':

    if is_admin():
        # 这里写入需要管理员权限执行的操作
        file = open(".Selected", "a+", encoding="utf8")
        file.seek(0)
        line = file.readline()
        if line is not None and line != "":
            network = line
        else:
            networks = []
            index = 0
            for k in psutil.net_if_addrs():
                networks.append(k)

                index += 1
                print(index, k)
            key = input_num(networks)
            network = networks[key - 1]
            file.write(network)

        disabled = f'netsh interface set interface "{network}" disabled'
        enabled = f'netsh interface set interface "{network}" enabled'

        if psutil.net_if_stats()[network].isup:  # 如果网卡是开启的，就先关闭它
            subprocess.run(disabled, shell=True, stdout=subprocess.PIPE)
        subprocess.run(enabled, shell=True, stdout=subprocess.PIPE)
    else:
        if sys.version_info[0] == 3:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)

    input("please input any key to exit!")