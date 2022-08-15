from git import Git
import base_client


        
# svn客户端
class GitClient(base_client.BaseClient):
    client = None
    def __init__(self, *args):
        super(GitClient, self).__init__(*args)
        #获取repo对象。本地仓库地址
        self.clent = Git(self.cfg["outpath"])
        
    # 获取版本号
    def get_revision(self, revision:str):
        # commit b50c28082871bdcff22f4508745ad4fa66fd1f24 (HEAD -> master, origin/master, origin/HEAD)
        begin_idx = revision.find("commit ") + len("commit ")
        end_idx = revision.find("\n", begin_idx)
        revision_1 = revision[begin_idx:end_idx]
        return revision_1

    # 更新
    def update(self):
        ret = self.clent.execute('git log -1')
        new_rev = self.get_revision(ret)
        return new_rev

