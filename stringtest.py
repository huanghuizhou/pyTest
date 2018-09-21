import time

import datetime

a="javascript:navigateUrl('http://saas.800jit.com/modelhome/applogin?handler=context&option=editRow&modelid=business&casenumber=" \
  "securitycd3fa0b43945577bc2abf471&page=spg_receipt&pagekey=business%403844519%40pg_fee_apply&element=bn_receipts&rowkey=bn_receipts$$TableRowKey_260235&c_lockstatus=none&c_id=16005644&is_load=true', '', '', 'true', 'false', '收入费用', {height:520,width:800});"
tou=a.find("http")
mo=a.find("',")
print(tou)
print(mo)
print(a[0:-1])

a=time.localtime(time.time())
b=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
print(b)