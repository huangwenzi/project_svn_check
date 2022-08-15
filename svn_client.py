import pysvn
import base_client


        
# svn客户端
class SvnClient(base_client.BaseClient):
    client = None
    def __init__(self, *args):
        super(SvnClient, self).__init__(*args)
        # 获取登录信息
        def get_login(realm, _username, may_save):
            retcode = True  # True，如果需要验证；否则用False
            save = False  # True，如果想之后都不用验证；否则用False
            return retcode, self.cfg["username"], self.cfg["password"], save
        # 事件通知
        def callback_notify(event_dict):
            # print(event_dict)
            return
        self.client = pysvn.Client()
        self.client.callback_notify = callback_notify
        self.client.callback_get_login = get_login
        
    # 获取版本号
    def get_revision(self, revision):
        revision_str = str(revision)
        # <Revision kind=number 77>
        num_str = revision_str[len("<Revision kind=number ") : -1]
        return int(num_str)

    # 更新
    def update(self):
        ret = self.client.update(self.cfg["outpath"])
        new_rev = self.get_revision(ret[0])
        return new_rev

