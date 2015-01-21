import sys
from TableMgr import TableMgr
reload(sys)
sys.setdefaultencoding('utf-8')

my_mgr = TableMgr()
my_mgr.init()
my_mgr.check_all_tables()
