import subprocess
import time
import json
import threading
# from win10toast import ToastNotifier
# toaster = ToastNotifier()
import svn_client
import git_client

print("版本 1")

cfg = {}    # 配置
global_data = {
    "check_status" : False    # 检查线程状态
    , "return_status" : False   # 退出状态
}

# 读取配置
with open("./cfg.json", "r", encoding="utf8") as f:
    cfg = json.load(f)

client = None
if cfg["type"] == "svn":
    client = svn_client.SvnClient(cfg, global_data)
else:
    client = git_client.GitClient(cfg, global_data)

# 检查函数
def check_fun():
    # 读取返回
    res_str = do_cfg_sh(cfg["check_sh"])
    if res_str.find(cfg["check_sh_err_ret"]) > 0:
        print(res_str)
        
        # 是否有二次补救
        if cfg["check_sh_1"] != "":
            res_str = do_cfg_sh(cfg["check_sh_1"])
            if res_str.find(cfg["check_sh_err_ret"]) > 0:
                client.print_win("check", "have err")
                print("\n\n")
                return False
        else:
            return False
    return True

# 执行配置脚本
def do_cfg_sh(sh_str):
    global_data["check_status"] = True
    # res1=subprocess.Popen([sh_str],stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    # res_str = res1.stdout.read().decode(encoding="utf8", errors="ignore")
    res1=subprocess.Popen(sh_str,shell=True,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE,encoding=cfg["out_encoding"], errors="ignore")
    for item in range(cfg["check_sh_input_count"]):
        # str需要转字节码
        # res1.stdin.write(cfg["check_sh_input"].encode("utf-8"))  # send the CR/LF for pause
        res1.stdin.write(cfg["check_sh_input"])
    ret_list = res1.communicate()
    res_str = ""
    for item in ret_list:
        if isinstance(item, str):
            res_str += item
    
    res1.stdin.close()
    global_data["check_status"] = False
    # 读取返回
    return res_str

# 检查函数
def check_rev():
    if not cfg["init_check"]:
        client.now_rev = client.update()
        
    # 开始循环
    while True:
        # 检查更新
        new_rev = client.update()
        if new_rev != client.now_rev:
            time_str = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            print("do_check new_rev:%s, now_rev:%s, time:%s"%(new_rev, client.now_rev, time_str))
            if check_fun():
                client.now_rev = new_rev
                print("check ok\n")
            else:
                time.sleep(cfg["check_sh_err_cool"])
        else:
            time.sleep(cfg["check_cool"])
    


        
# 用线程去跑检查
thread = threading.Thread(target=check_rev)
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
            if global_data["check_status"]:
                time.sleep(1)
            else:
                global_data["return_status"] = True
                break
    else:
        pass
    
    # 是否退出
    if global_data["return_status"]:
        break
        
            

    
