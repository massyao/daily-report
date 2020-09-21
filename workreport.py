# -*- coding: utf-8 -*-
import datetime
import os
import random
import time
import schedule
# 引入uiautomator库
from pip._vendor import requests
# from uiautomator import device as d
# from uiautomator2 import device as d
import uiautomator2 as u2
from uiautomator2 import Direction


today_work = "完成朴寓商业平台对接的测试开发及其他联调任务，并总结代码经验，完成项目汇报"

tomorrow_plan = "完成朴寓商业平台对接的测试开发及其他联调任务，并总结代码经验，完成项目汇报"

other_word = "完成朴寓商业平台对接的测试开发及其他联调任务，并总结代码经验，完成项目汇报"



# 法定节假日准确日期,不进行打卡
holiday = ['2020-06-25',
           '2020-06-26',
           '2020-06-27',
           '2020-10-01',
           '2020-10-02',
           '2020-10-03',
           '2020-10-04',
           '2020-10-05',
           '2020-10-06',
           '2020-10-07',
           '2020-10-08',
           ]
# 调整工作日准确日期，进行打卡
ajustWorking = ['2020-05-09', '2020-06-28', '2020-09-27', '2020-10-10']
# 调休日期，不进行打卡
compensatoryLeave = ['2020-05-16']

times = 5 # 5

# d = u2.connect('emulator-5554')
# print(d.info)
# d.healthcheck()


def countDown(randomTime = 5):
    a = randomTime * 60 # 60
    while a > 0:
        # if a % 10 == 0 or a < 10:
        #     print("秒数：", a)
        a -= 1
        time.sleep(1)

def timeFormat(date):
    return time.strftime("%Y-%m-%d %H:%M", date)

def dateFormat(date):
    return time.strftime("%Y-%m-%d", date)

def writelog(str):
    f = open("log.txt", "a")
    f.write(str + '\r\n')
    f.close()

def init():
    # os.popen("cls")
    os.popen("d: & cd \"D:\Program Files\leidian\\\" & start dnplayer.exe")
    time.sleep(5 * times)
    # os.popen("adb -s emulator-5554 shell")
    # os.popen("adb devices")
    os.popen("C:")
    res = os.popen("adb devices")
    time.sleep(1 * times)
    # closeApp()

def closeApp():
    try:
        os.popen("TASKKILL /F /IM dnplayer.exe")
        os.popen("TASKKILL /F /IM LdVBoxSVC.exe")
        os.popen("TASKKILL /F /IM LdVBoxHeadless.exe")
        # os.popen("C:")
        # os.popen("adb devices")
        # os.popen("adb kill-server") #conhost.exe
        # os.popen("TASKKILL /F /IM adb.exe")
    finally:
        time.sleep(1 * times)

def openwework():

    init()

    d = u2.connect('emulator-5554')
    print(d.info)
    d.healthcheck()

    msg = u'异常 ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # 先结束再开启
    # os.popen("adb shell am force-stop com.tencent.wework")
    # time.sleep(5)
    os.popen("adb shell am start com.tencent.wework/com.tencent.wework.launch.LaunchSplashActivity")
    time.sleep(3 * times)
    print("启动企业微信成功")
    

    d(text=u"工作台").click()
    time.sleep(1 * times)

    d(text=u"汇报").click()
    time.sleep(3 * times)
    print("打开汇报界面成功")

    d(text=u"日报").click()
    time.sleep(3 * times)
    print("打开日报界面成功")

    print("当前小时：", datetime.datetime.now().hour)

    try:

        if d(className='android.widget.EditText', instance=0):
            # android.widget.EditText
            print(1)
            d(className='android.widget.EditText', instance=0).set_text(today_work)
        if d(className='android.widget.EditText', instance=1):
            # android.widget.EditText
            print(2)
            d(className='android.widget.EditText', instance=1).set_text(tomorrow_plan)
        if d(className='android.widget.EditText', instance=2):
            # android.widget.EditText
            print(3)
            d(className='android.widget.EditText', instance=2).set_text(other_word)

        # d.swipe_ext("up")
        # d.drag(sx, sy, ex, ey, 0.5)
        d.drag(0.5, 0.9, 0.5, 0.3, 0.5)
        time.sleep(1 * times)


        # if d(textContains=u"请选择汇报对象", instance=0):
        if d(text="请选择汇报对象"):
            # android.widget.EditText
            print(4)
            d(text="请选择汇报对象").click()

            time.sleep(1 * times)

            d(resourceId="com.tencent.wework:id/hi7").click()
            time.sleep(0.2 * times)
            d(resourceId="com.tencent.wework:id/g5b").set_text("寿永春")
            time.sleep(0.2 * times)
            d(resourceId="com.tencent.wework:id/dr_").click()
            time.sleep(0.2 * times)

            d(resourceId="com.tencent.wework:id/g5b").set_text("乐萌")
            time.sleep(0.2 * times)
            d(resourceId="com.tencent.wework:id/dr_").click()
            time.sleep(0.2 * times)

            d(resourceId="com.tencent.wework:id/g5b").set_text("陈欢乐")
            time.sleep(0.2 * times)
            d(resourceId="com.tencent.wework:id/dr_").click()
            time.sleep(0.2 * times)

            d(resourceId="com.tencent.wework:id/g8_").click()
            time.sleep(0.2 * times)

            d(text="请选择群聊").click()
            time.sleep(1 * times)

            d(text="幸福社").click()
            time.sleep(0.2 * times)
            d(textContains=u"确定", instance=0).click()
            time.sleep(0.2 * times)
            # d(textContains=u"允许", instance=0)

            d(text="确定").click()
            msg = "汇报成功"

    # except:
    finally:
        return msg

def pushmsg(msg):
    """
    推送消息给微信
    :return:
    """
    try:
        url = 'http://wxpusher.zjiecode.com/api/send/message/?appToken=${你的app token}&content=' + msg + '&uid=${推送用户id}' # 在wxpusher.zjiecode.com 申请
        res = requests.get(url)
    except Exception:
        print("推送消息异常")

def gotoreport(tryTimes = 1):
    try:
        # 获取当前时间，2020-05-05 07:45
        nowtime = datetime.datetime.now()
        writelog("当前时间：" + nowtime.strftime("%Y-%m-%d %H:%M:%S"))
        # 加上随机数(0-3分钟)，2020-05-05 07:46
        randomTime = random.randint(1, 3)
        # print(randomTime + "分钟后打卡")
        # print( "执行任务时间：" + timeFormat(nowtime + datetime.timedelta(randomTime)) )
        countDown(randomTime)
        writelog('gotoreport start')
        writelog(" --------------------------------- ")
        msg = openwework()
        pushmsg(msg)
    except ConnectionRefusedError as e:
        print(e)
        # closeApp()
        os.popen("adb kill-server")
        os.popen("adb start-server")
        msg = openwework()
        pushmsg(msg)
    except BaseException as e:
        print(e)
        closeApp()
        msg = openwework()
        pushmsg(msg)
    finally:
        closeApp()
        writelog(msg)
        wechatStatus = msg.find('成功') == -1
        if tryTimes < 6 and wechatStatus:
            writelog('try again')
            gotoreport(tryTimes + 1)
        else:
            writelog('gotoreport end')
            writelog(' ----------------------------------------- ')

def dispatchTask():
 
    now = time.localtime()
    #if dateFormat(now) in holiday:
    if time.strftime("%Y-%m-%d", time.localtime()) in holiday:
        print("今天是法定假日")
        return True
    #if dateFormat(now) in compensatoryLeave:
    if time.strftime("%Y-%m-%d", time.localtime()) in compensatoryLeave:
        print("今天是调休日期，不进行打卡~~")
        return True
    #if dateFormat(now) in ajustWorking:
    if time.strftime("%Y-%m-%d", time.localtime()) in ajustWorking:   
        print("今天是调整工作日，需要进行打卡")
        gotoreport()
        return True

    # weekindex 0~6
    # 判断是否为周一到周五 
    weekIndex = datetime.datetime.now().weekday()
    if weekIndex != 6 and weekIndex != 5:
        print("周一至周五")
        gotoreport()

def report():
    d = u2.connect('emulator-5554')
    print(d.info)
    d.healthcheck()

    if d(className='android.widget.EditText', instance=0):
        d(className='android.widget.EditText', instance=0).set_text(today_work)
    if d(className='android.widget.EditText', instance=1):
        d(className='android.widget.EditText', instance=1).set_text(tomorrow_plan)
    if d(className='android.widget.EditText', instance=2):
        d(className='android.widget.EditText', instance=2).set_text(other_word)

    # d.swipe_ext("up")
    # d.drag(sx, sy, ex, ey, 0.5)
    d.drag(0.5, 0.9, 0.5, 0.3, 0.5)
    time.sleep(1 * times)


    # if d(textContains=u"请选择汇报对象", instance=0):
    if d(text="请选择汇报对象"):
        # android.widget.EditText
        print(4)
        d(text="请选择汇报对象").click()

        time.sleep(1 * times)

        d(resourceId="com.tencent.wework:id/hi7").click()
        time.sleep(0.2 * times)
        d(resourceId="com.tencent.wework:id/g5b").set_text("寿永春")
        time.sleep(0.2 * times)
        d(resourceId="com.tencent.wework:id/dr_").click()
        time.sleep(0.2 * times)

        d(resourceId="com.tencent.wework:id/g5b").set_text("乐萌")
        time.sleep(0.2 * times)
        d(resourceId="com.tencent.wework:id/dr_").click()
        time.sleep(0.2 * times)

        d(resourceId="com.tencent.wework:id/g5b").set_text("陈欢乐")
        time.sleep(0.2 * times)
        d(resourceId="com.tencent.wework:id/dr_").click()
        time.sleep(0.2 * times)

        d(resourceId="com.tencent.wework:id/g8_").click()
        time.sleep(0.2 * times)

        d(text="请选择群聊").click()
        time.sleep(1 * times)

        d(text="幸福社").click()
        time.sleep(0.2 * times)
        d(textContains=u"确定", instance=0).click()
        time.sleep(0.2 * times)
        # d(textContains=u"允许", instance=0)

        # d(text="确定").click()
        return "汇报成功"


# 企业微信自动打卡
if __name__ == "__main__":
    '''
    # 主函数
    # linux 后台运行
    nohup python3 -u main.py > main.log 2>&1 &

    # Windows 
    start /b python3 main.py
    '''
    # openwework()
    dispatchTask()
    
    # 每天汇报
    # schedule.every().day.at('18:11').do(dispatchTask)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(29)
