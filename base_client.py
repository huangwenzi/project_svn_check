from plyer import notification
import win32api,win32con



# 客户端基础
class BaseClient(object):
    cfg = {}    # 配置
    global_data = {}    # 全局数据
    now_rev = 0
    def __init__(self, cfg, global_data):
        self.cfg = cfg
        self.global_data = global_data
    
    # 输出win弹窗
    def print_win(self, title, notic):
        # notification.notify(title=title,
        #                 message=notic,
        #                 timeout=self.cfg["check_sh_show_time"])
        win32api.MessageBox(None, notic, "提醒：", win32con.MB_TOPMOST)