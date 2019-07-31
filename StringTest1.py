
a="""IT_计算机软件_硬件_信息服务<option value="1_1">
    IT_互联网和相关服务<option value="1_2">
    IT_其他<option value="1_3">

    制造业_机械_电子<option value="2_1">
    制造业_重工制造<option value="2_2">
    制造业_汽车<option value="2_3">
    制造业_其他<option value="2_4">

    服装<option value="3_1">
    超市_便利店_百货商店<option value="3_2">
    食品_饮料<option value="3_3">
    家具_家纺<option value="3_4">
    日用品_化妆品<option value="3_5">
    家电_数码<option value="3_6">
    烟酒<option value="3_7">
    文教_工美_体育_娱乐用品<option value="3_8">
    批发<option value="3_9">
    批发_其他<option value="3_10">

    酒店_住宿<option value="4_1">
    餐饮<option value="4_2">
    租赁和商务服务<option value="4_3">
    生活服务_其他<option value="4_4">

    新闻传媒<option value="5_1">
    文化_体育<option value="5_2">
    娱乐_旅游<option value="5_3">
    文化_体育_娱乐业_其他<option value="5_4">

    房地产<option value="6_1">
    建筑业<option value="6_2">
    建材装修<option value="6_3">
    建筑_房地产_其他<option value="6_4">

    学前教育<option value="7_1">
    初中等教育<option value="7_2">
    高等教育<option value="7_3">
    培训机构<option value="7_4">
    教育_其他<option value="7_5">

    道路_铁路运输<option value="8_1">
    航空运输<option value="8_2">
    水上运输<option value="8_3">
    物流_仓储<option value="8_4">
    邮政_快递<option value="8_5">
    运输_物流_仓储_其他<option value="8_6">

    医院_医疗<option value="9_1">
    医药制造<option value="9_2">
    医药流通<option value="9_3">
    医疗器械<option value="9_4">
    医疗_其他<option value="9_5">

    党政机关<option value="10_1">
    国家权力_行政机构<option value="10_2">
    检察院_法院_公安<option value="10_3">
    民政_人社_交通_卫生<option value="10_4">
    发改委_经信委_商务局_统计局<option value="10_5">
    国土_规划<option value="10_6">
    税务_海关_工商_环保_物价_药品<option value="10_7">
    政协_民主党派<option value="10_8">
    政府_其他<option value="10_9">

    保险<option value="11_1">
    银行<option value="11_2">
    证券_投资_基金<option value="11_3">
    金融_其他<option value="11_4">

    钢铁<option value="12_1">
    有色金属<option value="12_2">
    煤炭<option value="12_3">
    石油_天然气<option value="12_4">
    能源_采矿_其他<option value="12_5">

    农林牧渔<option value="13_1">

    科学研究和技术服务业<option value="14_1">
    水利和环境管理<option value="14_2">
    社会组织<option value="14_3">
    电力_热力_燃气_水供应业<option value="14_4">
    国际组织<option value="14_5">
    其他_其他<option value="14_6">"""

newList=[]
industries=a.split("\n")
for industry in industries:
    if(len(industry)<1):
        continue

    index=industry.find("<option")
    zn=industry[0:index]
    oth=industry[index:]

    newInd = oth+zn+"</option>"
    newList.append(newInd)

print(a)