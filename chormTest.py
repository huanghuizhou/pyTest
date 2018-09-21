# coding=utf-8
import datetime
import logging
import os
import random
import time
import traceback

import pymysql
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 打开数据库链接
# db = pymysql.connect(host="121.201.69.46",#192.168.100.254
#                      user="gtdata",
#                      passwd="Admin@123",
#                      db="Spide_800jit_logistics",
#                      port=23306,#3306
#                      use_unicode=True,
#                      charset="utf8")

# db = pymysql.connect(host="192.168.2.203",  # 192.168.100.254
#                      user="gt_user",
#                      passwd="greatTao1314!@#$",
#                      db="gt_spider",
#                      port=3306,  # 3306
#                      use_unicode=True,
#                      charset="utf8")


db = pymysql.connect(host="localhost",  # 192.168.100.254
                     user="root",
                     passwd="12345678",
                     db="gt_spider",
                     port=3306,  # 3306
                     use_unicode=True,
                     charset="utf8")


# 日志
def get_logger(name):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    # Standard output handler
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(logging.Formatter('%(levelname)s - %(name)s:%(lineno)s: %(message)s'))
    log.addHandler(sh)
    return log


logger = get_logger(__file__)


# 测试用例执行函数
def work(browser):
    cursor = db.cursor()
    url = "https://exmail.qq.com/cgi-bin/loginpage"
    browser.get(url)
    time.sleep(2)
    #browser.switch_to_frame('loginEntry1')  # Frame/Iframe定位
    try:
        # 输入账号和密码
        browser.find_element_by_name("inputuin").send_keys('huanghuizhou@egtcp.com')
        browser.find_element_by_id("pp").send_keys('Hhz0508')
        time.sleep(2)
        # 点击按钮提交登录表单
        browser.find_element_by_name("btlogin").click()
        # browser.send_keys(Keys.RETURN)
        time.sleep(5)

        # 验证登录成功的url
        currUrl = browser.current_url
        if currUrl.startswith("https://exmail.qq.com/cgi-bin/frame_html"):
            print(111)
        if currUrl == "http://saas.800jit.com/modelhome/applogin":
            print("success")
        else:
            print("failure1")
            print(browser.page_source)
            return
            # writeLog()

    except:
        print("failure2")
        print(traceback.format_exc())
        # writeLog()
    # 需要完成Java
    # browser.switch_to_frame('content')
    # browser.find_element_by_id("asp_modelhome$$$business$$$tr_business_seaexport0").click()#海运出口
    time.sleep(random.random() * 1)

    # for page in range(2):
    page = 0  # 0是第一页
    # browser.get("http://saas.800jit.com/modelhome/applogin?handler=context&option=getPage&modelid=business&casenumber=securityc0b56fcaebce2e03aeaf46af15da51add947d81e1c5737f8&page=pg_seaexport_search0&pagekey=business@ModelCtx@business@pg_seaexport_search0&portlet=qp_seaexport0&paging="+str(page))
    browser.get(
        "http://saas.800jit.com/modelhome/applogin?handler=context&option=getPage&modelid=business&casenumber=securityc0b56fcaebce2e03aeaf46af15da51add947d81e1c5737f8&page=pg_seaexport_search0")

    # browser.switch_to.frame('iframe')
    # js = "$('input[id=qybu_datestart]').attr('readonly','');$('input[id=qybu_dateend]').attr('readonly','')"  # 4.jQuery，设置为空（同3）
    # browser.execute_script(js)
    # browser.find_element_by_name("qybu_datestart").send_keys('2015-07-01')
    # browser.find_element_by_name("qybu_dateend").send_keys('2015-07-02')
    # browser.find_element_by_name("bt_query").click()
    # time.sleep(60)
    # browser.get("http://saas.800jit.com/modelhome/applogin?handler=context&option=getPage&modelid=business&casenumber=securityc0b56fcaebce2e03aeaf46af15da51add947d81e1c5737f8&page=pg_seaexport_search0&pagekey=business@ModelCtx@business@pg_seaexport_search0&portlet=qp_seaexport0&paging="+str(page))
    # time.sleep(60)

    html1 = browser.execute_script("return document.documentElement.outerHTML")
    soup = BeautifulSoup(html1, "lxml")

    for link in soup.findAll("td", {"class": "vrws-row-value", "elementname": "qp_seaexport0:businessno"}):
        businessno = link.find("a").string.replace("\n", "").strip()
        businessno_urllink = link.find("a").get("href")
        businessno_urllink = businessno_urllink[businessno_urllink.find('security'):businessno_urllink.find('&page')]
        if businessno_urllink == 'security6e8612fb35474cf42c402e01':
            continue
        # for page in range(2)
        geturl1 = "http://saas.800jit.com/modelhome/applogin?handler=context&option=getPage&modelid=business&casenumber=" + businessno_urllink + "&page=pg_seaexport0"

        time.sleep(random.random() * 1)
        browser.get(geturl1)
        html2 = browser.execute_script("return document.documentElement.outerHTML")
        soupdetail = BeautifulSoup(html2, "lxml")
        # 列表页页面解析
        companyname = "宁波钧海供应链管理有限公司"  # 服务商名称
        if soupdetail.find("input", {"id": "bn_mains_mblno"}):
            continue
        mblno = soupdetail.find("span", {"elementname": "bn_mains_mblno"}).find("span",
                                                                                {"class": "value"}).string.replace("\n",
                                                                                                                   "")  # 主单号
        bookingno = soupdetail.find("span", {"elementname": "bn_mains_bookingno"}).find("span", {
            "class": "value"
        }).string.replace("\n", "")  # 内部委托编号
        seaconsigntype = soupdetail.find("span", {"elementname": "bn_mains_seaconsigntype"}).find("span", {
            "class": "value"
        }).string.replace("\n", "")  # 托运类型
        customername = soupdetail.find("span", {"elementname": "bn_mains_customername"}).find("span", {
            "class": "content_value"
        }).string.replace("\n", "")  # 委托单位
        receiptname = soupdetail.find("span", {"elementname": "bn_mains_receiptname"}).find("span", {
            "class": "content_value"
        }).string.replace("\n", "")  # 结算单位
        bookingagency = soupdetail.find("span", {"elementname": "bn_mains_bookingagency"}).find("span", {
            "class": "content_value"
        }).string.replace("\n", "")  # 订舱代理
        plancarrier = soupdetail.find("span", {"elementname": "bn_assistants_plancarrier"}).find("span", {
            "class": "content_value"
        }).string.replace("\n", "")  # 预配船司
        carrier = soupdetail.find("span", {"elementname": "bn_mains_carrier"}).find("span", {
            "class": "content_value"
        }).string.replace("\n", "")  # 船公司
        vesselname = soupdetail.find("span", {"elementname": "bn_mains_vesselname"}).find("span", {
            "class": "content_value"
        }).string.replace("\n", "")  # 船名
        vesselname_cn = soupdetail.find("span", {"elementname": "bn_assistants_vesselname_cn"}).find("span", {
            "class": "content_value"
        }).string.replace("\n", "")  # 中文船名
        voyno = soupdetail.find("span", {"elementname": "bn_mains_voyno"}).find("span", {
            "class": "content_value"
        }).string.replace("\n", "")  # 航次
        recplacecode = soupdetail.find("span", {"elementname": "bn_assistants_recplacecode"}).find("span", {
            "class": "content_value portCode_value"
        }).string.replace("\n", "")  # 收货地点code
        recplace = soupdetail.find("span", {"elementname": "bn_mains_recplace"}).find("span", {
            "class": "content_value"
        }).string.replace("\n", "")  # 收货地点
        loadportcode = soupdetail.find("span", {"elementname": "bn_assistants_loadportcode"}).find("span", {
            "class": "content_value portCode_value"
        }).string.replace("\n", "")  # 起运港code
        loadport = soupdetail.find("span", {"elementname": "bn_mains_loadport"}).find("span", {
            "class": "content_value"
        }).string.replace("\n", "")  # 起运港
        dischargeportcode = soupdetail.find("span", {"elementname": "bn_assistants_dischargeportcode"}).find("span", {
            "class": "content_value portCode_value"
        }).string.replace("\n", "")  # 目的港code
        dischargeport = soupdetail.find("span", {"elementname": "bn_mains_dischargeport"}).find("span", {
            "class": "content_value"
        }).string.replace("\n", "")  # 目的港
        finalplacecode = soupdetail.find("span", {"elementname": "bn_assistants_finalplacecode"}).find("span", {
            "class": "content_value portCode_value"
        }).string.replace("\n", "")  # 目的地code
        finalplace = soupdetail.find("span", {"elementname": "bn_mains_finalplace"}).find("span", {
            "class": "content_value"
        }).string.replace("\n", "")  # 目的地
        delplacecode = soupdetail.find("span", {"elementname": "bn_assistants_delplacecode"}).find("span", {
            "class": "content_value portCode_value"
        }).string.replace("\n", "")  # 交货地址code
        delplace = soupdetail.find("span", {"elementname": "bn_mains_delplace"}).find("span", {
            "class": "content_value"
        }).string.replace("\n", "")  # 交货地址
        transferportcode = soupdetail.find("span", {"elementname": "bn_assistants_transferportcode"}).find("span", {
            "class": "content_value portCode_value"
        }).string.replace("\n", "")  # 中转港code
        transferport = soupdetail.find("span", {"elementname": "bn_mains_transferport"}).find("span", {
            "class": "content_value"
        }).string.replace("\n", "")  # 中转港
        searoute = soupdetail.find("span", {"elementname": "bn_assistants_searoute"}).find("span", {
            "class": "content_value"
        }).string.replace("\n", "")  # 航线
        freightclause = soupdetail.find("span", {"elementname": "bn_mains_freightclause"}).find("span", {
            "class": "content_value"
        }).string.replace("\n", "")  # 付款方式
        paymentplace = soupdetail.find("span", {"elementname": "bn_mains_paymentplace"}).find("span", {
            "class": "content_value"
        }).string.replace("\n", "")  # 付款地点
        transclause = soupdetail.find("span", {"elementname": "bn_mains_transclause"}).find("span", {
            "class": "content_value"
        }).string.replace("\n", "")  # 运输条款
        bookingnumber = soupdetail.find("span", {"elementname": "bn_assistants_bookingnumber"}).find("span", {
            "class": "content_value"
        }).string.replace("\n", "")  # 订舱编号
        billtype = soupdetail.find("span", {"elementname": "bn_assistants_billtype"}).find("span", {
            "class": "content_value"
        }).string.replace("\n", "")  # 提单方式
        sendtype = soupdetail.find("span", {"elementname": "bn_mains_sendtype"}).find("span", {
            "class": "content_value"
        }).string.replace("\n", "")  # 出单方式
        contractno = soupdetail.find("span", {"elementname": "bn_assistant2s_contractno"}).find("span", {
            "class": "content_value"
        }).string.replace("\n", "")  # 合约号
        hblno = soupdetail.find("span", {"elementname": "bn_mains_hblno"}).find("span", {
            "class": "content_value"
        }).string.replace("\n", "")  # 分单号
        compactno = soupdetail.find("span", {"elementname": "bn_assistants_compactno"}).find("span", {
            "class": "content_value"
        }).string.replace("\n", "")  # 合同号
        count = soupdetail.find("span", {"elementname": "bn_mains_count"}).find("span", {
            "class": "content_value"
        }).string.replace("\n", "").replace(",", "")  # 件数
        goodsname = soupdetail.find("span", {"elementname": "bn_mains_goodsname"}).find("span", {
            "class": "content_value"
        }).string.replace("\n", "")  # 货物名称
        goodstype = soupdetail.find("span", {"elementname": "bn_assistants_goodstype"}).find("span", {
            "class": "content_value"
        }).string.replace("\n", "")  # 货物类型
        weight = soupdetail.find("span", {"elementname": "bn_mains_weight"}).find("span", {
            "class": "short_value"
        }).string.replace("\n", "").replace(",", "")  # 毛重
        volume = soupdetail.find("span", {"elementname": "bn_mains_volume"}).find("span", {
            "class": "content_value short_value"
        }).string.replace("\n", "").replace(",", "")  # 体积
        vgm_weight = soupdetail.find("span", {"elementname": "bn_mains_vgm_weight"}).find("span", {
            "class": "content_value"
        }).string.replace("\n", "").replace(",", "")  # VGM
        calweight = soupdetail.find("span", {"elementname": "bn_mains_calweight"}).find("span", {
            "class": "content_value short_value"
        }).string.replace("\n", "").replace(",", "")  # 计重
        planetd = soupdetail.find("span", {"elementname": "bn_assistants_planetd"}).find("span", {
            "class": "content_value"
        }).string.replace("\n", "")  # 预配船期
        acceptdate = soupdetail.find("span", {"elementname": "bn_mains_acceptdate"}).find("span", {
            "class": "content_value"
        }).string.replace("\n", "")  # 接单日期
        bookingdate = soupdetail.find("span", {"elementname": "bn_mains_bookingdate"}).find("span", {
            "class": "content_value"
        }).string.replace("\n", "")  # 订舱日期
        putcabindate = soupdetail.find("span", {"elementname": "bn_mains_putcabindate"}).find("span", {
            "class": "content_value"
        }).string.replace("\n", "")  # 放舱日期
        etc = soupdetail.find("span", {"elementname": "bn_mains_etc"}).find("span",
                                                                            {"class": "content_value"}).string.replace(
            "\n", "")  # 截关日期
        cutoffbilldate = soupdetail.find("span", {"elementname": "bn_assistants_cutoffbilldate"}).find("span", {
            "class": "content_value"
        }).string.replace("\n", "")  # 截单日期
        etd = soupdetail.find("span", {"elementname": "bn_mains_etd"}).find("span",
                                                                            {"class": "content_value"}).string.replace(
            "\n", "")  # 离港日期
        eta = soupdetail.find("span", {"elementname": "bn_mains_eta"}).find("span",
                                                                            {"class": "content_value"}).string.replace(
            "\n", "")  # 抵港日期
        completedate = soupdetail.find("span", {"elementname": "bn_mains_completedate"}).find("span", {
            "class": "content_value"
        }).string.replace("\n", "")  # 完结日期
        bookingservice = soupdetail.find("span", {"elementname": "bn_mains_bookingservice"}).find("span", {
            "class": "content_value"
        }).string.replace("\n", "")  # 订舱服务
        sendgoodsservice = soupdetail.find("span", {"elementname": "bn_assistants_sendgoodsservice"}).find("span", {
            "class": "content_value"
        }).string.replace("\n", "")  # 内装(进仓)
        landservice = soupdetail.find("span", {"elementname": "bn_mains_landservice"}).find("span", {
            "class": "content_value"
        }).string.replace("\n", "")  # 陆运服务
        customerservice = soupdetail.find("span", {"elementname": "bn_mains_customerservice"}).find("span", {
            "class": "content_value"
        }).string.replace("\n", "")  # 报关服务
        inspectservice = soupdetail.find("span", {"elementname": "bn_mains_inspectservice"}).find("span", {
            "class": "content_value"
        }).string.replace("\n", "")  # 报检服务
        pawnservice = soupdetail.find("span", {"elementname": "bn_assistants_pawnservice"}).find("span", {
            "class": "content_value"
        }).string.replace("\n", "")  # 押箱服务

        if soupdetail.find("textarea", {"name": "bn_mains_mshipper"}).string:
            mshipper = soupdetail.find("textarea", {"name": "bn_mains_mshipper"}).string.replace("\n", "").replace("\r",
                                                                                                                   "").strip()  # 发货人
        else:
            mshipper = soupdetail.find("textarea", {"name": "bn_mains_mshipper"}).string

        if soupdetail.find("textarea", {"name": "bn_mains_mconsignee"}).string:
            mconsignee = soupdetail.find("textarea", {"name": "bn_mains_mconsignee"}).string.replace("\n", "").replace(
                "\r", "").strip()  # 收货人
        else:
            mconsignee = soupdetail.find("textarea", {"name": "bn_mains_mconsignee"}).string

        if soupdetail.find("textarea", {"name": "bn_mains_mnotify"}).string:
            mnotify = soupdetail.find("textarea", {"name": "bn_mains_mnotify"}).string.replace("\n", "").replace("\r",
                                                                                                                 "").strip()  # 通知人
        else:
            mnotify = soupdetail.find("textarea", {"name": "bn_mains_mnotify"}).string

        if soupdetail.find("textarea", {"name": "bn_mains_mark"}).string:
            marks = soupdetail.find("textarea", {"name": "bn_mains_mark"}).string.replace("\n", "").replace("\r",
                                                                                                            "").strip()  # 唛头
        else:
            marks = soupdetail.find("textarea", {"name": "bn_mains_mark"}).string

        uptime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        sql_save1 = """INSERT INTO wuliudetail\
                                          (servername,  businessno,   mblno,	bookingno,	seaconsigntype,	customername,	receiptname,	bookingagency,	plancarrier,	carrier,	vesselname,	vesselname_cn,	voyno,	recplacecode,	recplace,	loadportcode,	loadport,	dischargeportcode,	dischargeport,	finalplacecode,	finalplace,	delplacecode,	delplace,	transferportcode,	transferport,	searoute,	freightclause,	paymentplace,	transclause,	bookingnumber,	billtype,	sendtype,	contractno,	hblno,	compactno,	count,	goodsname,	goodstype,	weight,	volume,	vgm_weight,	calweight,	planetd,	acceptdate,	bookingdate,	putcabindate,	etc,	cutoffbilldate,	etd,	eta,	completedate,	bookingservice,	sendgoodsservice,	landservice,	customerservice,	inspectservice,	pawnservice,	mshipper,	mconsignee,	mnotify,uptime,marks) value\
                                          (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

        try:
            cursor.execute(sql_save1, (
                companyname, businessno, mblno, bookingno, seaconsigntype, customername, receiptname, bookingagency,
                plancarrier, carrier,
                vesselname, vesselname_cn, voyno, recplacecode, recplace, loadportcode, loadport, dischargeportcode,
                dischargeport, finalplacecode, finalplace, delplacecode, delplace, transferportcode, transferport,
                searoute, freightclause, paymentplace, transclause, bookingnumber, billtype, sendtype, contractno,
                hblno,
                compactno, count, goodsname, goodstype, weight, volume, vgm_weight, calweight, planetd, acceptdate,
                bookingdate, putcabindate, etc, cutoffbilldate, etd, eta, completedate, bookingservice,
                sendgoodsservice,
                landservice, customerservice, inspectservice, pawnservice, mshipper, mconsignee, mnotify,
                uptime, marks))

            db.commit()
        except Exception as e:
            logger.warning('Failed to insert into wuliudetail sql is %s' % sql_save1, e)
            print('Failed to insert into wuliudetail sql is %s' % sql_save1, e)
            time.sleep(5)

        # 转跳分箱
        geturl2 = "http://saas.800jit.com/modelhome/applogin?handler=context&option=getPage&modelid=business&casenumber=" + businessno_urllink + "&page=pg_setruck0&pagekey=business"
        time.sleep(random.random() * 1)
        browser.get(geturl2)
        html3 = browser.execute_script("return document.documentElement.outerHTML")
        soupdetail2 = BeautifulSoup(html3, "lxml")

        # 分箱页面
        box1 = soupdetail2.find("span", {"elementname": "bn_mains_ctntype1"}).find("span",
                                                                                   {"class": "value_1"}).string.replace(
            "\n", "")  # 箱型1
        boxcount1 = soupdetail2.find("span", {"elementname": "bn_mains_ctncount1"}).find("span", {
            "class": "value countValue"
        }).string.replace("\n", "")  # 箱型1数量
        box2 = soupdetail2.find("span", {"elementname": "bn_mains_ctntype2"}).find("span",
                                                                                   {"class": "value_1"}).string.replace(
            "\n", "")  # 箱型2
        boxcount2 = soupdetail2.find("span", {"elementname": "bn_mains_ctncount2"}).find("span", {
            "class": "value countValue"
        }).string.replace("\n", "")  # 箱型2数量
        box3 = soupdetail2.find("span", {"elementname": "bn_mains_ctntype3"}).find("span",
                                                                                   {"class": "value_1"}).string.replace(
            "\n", "")  # 箱型3
        boxcount3 = soupdetail2.find("span", {"elementname": "bn_mains_ctncount3"}).find("span", {
            "class": "value countValue"
        }).string.replace("\n", "")  # 箱型3数量
        box4 = soupdetail2.find("span", {"elementname": "bn_mains_ctntype4"}).find("span",
                                                                                   {"class": "value_1"}).string.replace(
            "\n", "")  # 箱型4
        boxcount4 = soupdetail2.find("span", {"elementname": "bn_mains_ctncount4"}).find("span", {
            "class": "value countValue"
        }).string.replace("\n", "")  # 箱型4数量
        fleet = soupdetail2.find("span", {"elementname": "bn_mains_fleet"}).find("span",
                                                                                 {"class": "value"}).string.replace(
            "\n", "")  # 承运车队
        fleetlinkman = soupdetail2.find("span", {"elementname": "bn_mains_fleetlinkman"}).find("span", {
            "class": "value"
        }).string.replace("\n", "")  # 车队联系人
        fleetmobile = soupdetail2.find("span", {"elementname": "bn_mains_fleetmobile"}).find("span", {
            "class": "value"
        }).string.replace("\n", "")  # 车队手机
        getcy = soupdetail2.find("span", {"elementname": "bn_mains_getcy"}).find("span",
                                                                                 {"class": "value"}).string.replace(
            "\n", "")  # 提箱地点

        sql_save2 = """INSERT INTO luyunfeixiang\
                                  (businessno, box1, boxcount1, box2, boxcount2, box3, boxcount3, box4, boxcount4, fleet,fleetlinkman,fleetmobile,getcy,uptime) value\
                                  (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

        try:
            cursor.execute(sql_save2, (
                businessno, box1, boxcount1, box2, boxcount2, box3, boxcount3, box4, boxcount4, fleet, fleetlinkman,
                fleetmobile, getcy, uptime))
            db.commit()
        except Exception as e:
            logger.warning('Failed to insert into luyunfeixiang sql is %s' % sql_save2, e)
            print('Failed to insert into luyunfeixiang sql is %s' % sql_save2, e)
            time.sleep(5)

        boxtype = soupdetail2.findAll("td", {
            "class": "vrws-row-value", "elementname": "sp_seacontainers:bn_containers_ctntype"
        })  # 箱型
        containersno = soupdetail2.findAll("td", {
            "class": "vrws-row-value", "elementname": "sp_seacontainers:bn_containers_ctnno"
        })  # 箱号
        sealno = soupdetail2.findAll("td", {
            "class": "vrws-row-value", "elementname": "sp_seacontainers:bn_containers_sealno"
        })  # 封箱号
        containerssize = soupdetail2.findAll("td", {
            "class": "vrws-row-value", "elementname": "sp_seacontainers:bn_containers_ctnsize"
        })  # 箱型尺寸

        for i in range(len(boxtype)):
            if containersno[i].find("a").string:  # 装箱号为空，默认为没有确认，不抓取
                boxtype_ctn = boxtype[i].find("select").find("option", {"selected": True}).string.replace("\n",
                                                                                                          "").strip()

                containersno_ctn = containersno[i].find("a").string.replace("\n", "").strip()

                if sealno[i].string:
                    sealno_ctn = sealno[i].string.replace("\n", "").strip()
                else:
                    sealno_ctn = ''

                containerssize_ctn = containerssize[i].find("select").find("option", {"selected": True}).string.replace(
                    "\n", "").strip()

                # todo INSERT => REPLACE

                sql_save2_2 = """INSERT INTO luyunfeixiangdetail\
                                          (businessno, boxtype_ctn, containersno_ctn, sealno_ctn, containerssize_ctn,uptime) value\
                                          (%s,%s,%s,%s,%s,%s)"""

                try:
                    cursor.execute(sql_save2_2,
                                   (businessno, boxtype_ctn, containersno_ctn, sealno_ctn, containerssize_ctn,
                                    uptime))
                    db.commit()
                except Exception as e:
                    logger.warning('Failed to insert into luyunfeixiangdetail sql is %s' % sql_save2_2, e)
                    print('Failed to insert into luyunfeixiangdetail sql is %s' % sql_save2_2, e)
                    time.sleep(5)
                    continue

        # 转费用列表
        geturl3 = "http://saas.800jit.com/modelhome/applogin?handler=context&option=getPage&modelid=business&casenumber=" + businessno_urllink + "&page=pg_fee_apply&pagekey=business"
        time.sleep(random.random() * 1)
        browser.get(geturl3)

        html4 = browser.execute_script("return document.documentElement.outerHTML")
        soupdetail3 = BeautifulSoup(html4, "lxml")
        # 收入费用页面解析
        # businessno = soupdetail3.find("tr", {"elementName": "bn_mains_businessno"}).find("td", {"class": "value"}).string  # 业务编号

        feeitem = soupdetail3.findAll("td", {
            "class": "vrws-row-value", "elementname": "sp_receipt_apply:bn_receipts_feeitem"
        })  # 费用项目
        price = soupdetail3.findAll("td", {
            "class": "vrws-row-value", "elementname": "sp_receipt_apply:bn_receipts_price"
        })  # 单价
        count = soupdetail3.findAll("td", {
            "class": "vrws-row-value", "elementname": "sp_receipt_apply:bn_receipts_count"
        })  # 数量
        amount = soupdetail3.findAll("td", {
            "class": "vrws-row-value", "elementname": "sp_receipt_apply:bn_receipts_amount"
        })  # 金额
        currency = soupdetail3.findAll("td", {
            "class": "vrws-row-value", "elementname": "sp_receipt_apply:bn_receipts_currency"
        })  # 币种
        rate = soupdetail3.findAll("td", {
            "class": "vrws-row-value", "elementname": "sp_receipt_apply:bn_receipts_rate"
        })  # 汇率
        customername = soupdetail3.findAll("td", {
            "class": "vrws-row-value", "elementname": "sp_receipt_apply:bn_receipts_customername"
        })  # 结算公司
        fullname = soupdetail3.findAll("td", {
            "class": "vrws-row-value", "elementname": "sp_receipt_apply:bn_receipts_fullname"
        })  # 发票抬头
        realamount = soupdetail3.findAll("td", {
            "class": "vrws-row-value", "elementname": "sp_receipt_apply:bn_receipts_realamount"
        })  # 实收
        confirmor = soupdetail3.findAll("td", {
            "class": "vrws-row-value", "elementname": "sp_receipt_apply:bn_receipts_confirmor"
        })  # 费用确认人

        for i in range(len(feeitem)):
            # feeitem_get = feeitem[i].string.replace("\n", "").strip()
            # price_get = price[i].string.replace("\n", "").strip()
            # count_get = count[i].string.replace("\n", "").strip()
            # amount_get = amount[i].string.replace("\n", "").strip()
            # currency_get = currency[i].string.replace("\n", "").strip()
            # rate_get = rate[i].string.replace("\n", "").strip()
            # customername_get = customername[i].string.replace("\n", "").strip()
            # fullname_get = fullname[i].string.replace("\n", "").strip()
            # realamount_get = realamount[i].string.replace("\n", "").strip()
            # confirmor_get = confirmor[i].string.replace("\n", "").strip()

            if confirmor[i].string.replace("\n", "").strip() == "":
                continue
            feeitem_get = feeitem[i].string.replace("\n", "").strip()
            price_get = price[i].string.replace("\n", "").replace(",", "").strip()
            count_get = count[i].string.replace("\n", "").strip()
            amount_get = amount[i].string.replace("\n", "").replace(",", "").strip()
            currency_get = currency[i].string.replace("\n", "").strip()
            rate_get = rate[i].string.replace("\n", "").strip()
            customername_get = customername[i].string.replace("\n", "").strip()
            fullname_get = fullname[i].string.replace("\n", "").strip()
            realamount_get = realamount[i].string.replace("\n", "").strip()
            confirmor_get = confirmor[i].string.replace("\n", "").strip()

            # 插入数据库
            sql_save3 = """INSERT INTO feiyongshouru\
                          (businessno, feeitem, price, counta, amount, currency, rate, customername, fullname, realamount,confirmor,uptime) value\
                          (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        """

            try:
                cursor.execute(sql_save3, (
                    businessno, feeitem_get, price_get, count_get, amount_get, currency_get, rate_get, customername_get,
                    fullname_get, realamount_get,
                    confirmor_get, uptime))

                db.commit()
            except Exception as e:
                logger.warning('Failed to insert into feiyongshouru sql is %s' % sql_save3, e)
                print('Failed to insert into feiyongshouru sql is %s' % sql_save3, e)
                time.sleep(5)

    db.commit()
    db.close()

    # 支出费用页面解析


#        feeitem_pay = soupdetail.findAll("td",{"class": "vrws-row-value", "elementname": "sp_pay_apply:bn_pays_feeitem"})  #　费用项目
#        type_pay = soupdetail.findAll("td", {"class": "vrws-row-value", "elementname": "sp_pay_apply:bn_pays_type"}) #　类型
#        price_pay = soupdetail3.findAll("td",{"class": "vrws-row-value", "elementname": "sp_pay_apply:bn_pays_saleprice"})  # 单价
#        count_pay = soupdetail3.findAll("td",{"class": "vrws-row-value", "elementname": "sp_pay_apply:bn_pays_count"})  # 币种
#        amount_pay = soupdetail3.findAll("td", {"class": "vrws-row-value","elementname": "sp_pay_apply:bn_pays_saleamount"})  # 金额
#        rate_pay = soupdetail3.findAll("td", {"class": "vrws-row-value", "elementname": "sp_pay_apply:bn_pays_additionalrate"})  # 汇率
#        currency_pay = soupdetail3.findAll("td", {"class": "vrws-row-value","elementname": "sp_pay_apply:bn_pays_currency"})  # 币种
#        fullname_pay = soupdetail3.findAll("td", {"class": "vrws-row-value","elementname": "sp_pay_apply:bn_pays_customername"})  # 付款单位
#        realamount_pay = soupdetail3.findAll("td", {"class": "vrws-row-value","elementname": "sp_pay_apply:bn_pays_realamount"})  # 实收
#        confirmor_pay = soupdetail3.findAll("td", {"class": "vrws-row-value","elementname": "sp_pay_apply:bn_pays_payauditman"})  # 费用确认人

#       for i in range(len(feeitem_pay)):
#           feeitem_to = feeitem_pay[i].find("input").get("value").replace("\n", "").strip()
#           type_to = type_pay[i].find("option", {"selected": True}).string.replace("\n", "").strip()
#           price_to = price_pay[i].string.replace("\n", "").strip()
#           count_to = count_pay[i].string.replace("\n", "").strip()
#           amount_to = amount_pay[i].string.replace("\n", "").strip()
#           currency_to = currency_pay[i].string.replace("\n", "").strip()
#           rate_to = rate_pay[i].string.replace("\n", "").strip()
#           fullname_to = fullname_pay[i].string.replace("\n", "").strip()
#           realamount_to = realamount_pay[i].string.replace("\n", "").strip()
#           confirmor_to = confirmor_pay[i].string.replace("\n", "").strip()

# 插入数据库
#           sql_save4 = """INSERT INTO feiyongzhichu\
#                                     (businessno, feeitem, type_pay, price, counta, amount, currency, rate, customername, fullname, realamount,confirmor) value\
#                                     (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

#            cursor.execute(sql_save4, (businessno, feeitem_to, type_to, price_to, count_to, amount_to, currency_to, rate_to, fullname_to, realamount_to,
#            confirmor_to))
#            db.commit()


# 写错误日志并截图
def writeLog():
    # 组合日志文件名（当前文件名+当前时间）.比如：case_login_success_20150817192533
    basename = os.path.splitext(os.path.basename(__file__))[0]
    logFile = basename + "-" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".log"
    logging.basicConfig(filename=logFile)
    s = traceback.format_exc()
    logging.error(s)
    browser.get_screenshot_as_file("./" + logFile + "-screenshot_error.png")


if __name__ == "__main__":
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    browser = webdriver.Chrome(chrome_options=chrome_options)  # Chrome界面
    # browser = webdriver.PhantomJS()  # 无界面
    work(browser)

    browser.quit()
