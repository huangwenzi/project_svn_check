import os
import subprocess
import pysvn
import time
import json
import threading
# from win10toast import ToastNotifier
# toaster = ToastNotifier()
from plyer import notification

cfg = {}    # 配置
check_status = False    # 检查线程状态
return_status = False   # 退出状态
# 读取配置
with open("./cfg.json", "r", encoding="utf8") as f:
    cfg = json.load(f)

# 输出win弹窗
def print_win(title, notic):
    notification.notify(title=title,
                    message=notic,
                    timeout=cfg["check_sh_show_time"])
        
# 获取登录信息
def get_login(realm, _username, may_save):
    retcode = True  # True，如果需要验证；否则用False
    save = False  # True，如果想之后都不用验证；否则用False
    return retcode, cfg["username"], cfg["password"], save

# 事件通知
def callback_notify(event_dict):
    # print(event_dict)
    return

# 获取版本号
def revision_to_num(revision):
    revision_str = str(revision)
    # <Revision kind=number 77>
    num_str = revision_str[len("<Revision kind=number ") : -1]
    return int(num_str)

# 检查函数
def check_fun():
    global check_status
    check_status = True
    # print("check doing")
    # out = os.popen(".\\test.bat")
    # print(out.read())
    res1=subprocess.Popen(cfg["check_sh"],shell=True,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    for item in range(cfg["check_sh_input_count"]):
        # str需要转字节码
        res1.stdin.write(cfg["check_sh_input"].encode("utf-8"))  # send the CR/LF for pause
    res1.stdin.close()
    # 读取返回
    res_str = res1.stdout.read().decode(encoding="utf8", errors="ignore")
    check_status = False
    if res_str.find(cfg["check_sh_err_ret"]) > 0:
        print(res_str)
        print_win("check", "have err")
        print("\n\n")
        return False
    return True

# 检查函数
def check_svn():
    # 定义变量
    now_rev = 0 # 当前版本
    client = pysvn.Client() # svn客户端
    # 设置svn回调
    client.callback_notify = callback_notify
    client.callback_get_login = get_login
    ret = client.update(cfg["outpath"])
    if not cfg["init_check"]:
        now_rev = revision_to_num(ret[0])
        
    # 开始循环
    while True:
        # 检查svn更新
        ret = client.update(cfg["outpath"])
        new_rev = revision_to_num(ret[0])
        if new_rev != now_rev:
            print("do_check new_rev:%s, now_rev:%s"%(new_rev, now_rev))
            if check_fun():
                now_rev = new_rev
                print("check ok\n")
            else:
                time.sleep(cfg["check_sh_err_cool"])
        time.sleep(cfg["check_cool"])
    


        
# 用线程去跑检查
thread = threading.Thread(target=check_svn)
thread.setDaemon(True)  # 设为thread的守护线程
thread.start()

# 监听退出
while True:
    putin_str = input("输入指令 或help查看\n")
    if putin_str == "help":
        print("""
exit 退出
              """)
    elif putin_str == "exit":
        while True:
            if check_status:
                time.sleep(1)
            else:
                return_status = True
                break
    else:
        pass
    
    # 是否退出
    if return_status:
        break
        
            

    
