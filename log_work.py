# -*- coding: utf-8 -*-
import datetime
import os
import random
import time
import schedule
# 引入uiautomator库
from pip._vendor import requests
# from uiautomator import device as d
import uiautomator2 as u2
from uiautomator2 import Direction

# python -m weditor

# 法定节假日准确日期,不进行打卡
holiday = [
    '2021-01-01',
    '2021-01-02',
    '2021-01-03',
    '2021-02-11',
    '2021-02-12',
    '2021-02-13',
    '2021-02-14',
    '2021-02-15',
    '2021-02-16',
    '2021-02-17',
    '2021-04-03',
    '2021-04-04',
    '2021-04-05',
    '2021-05-01',
    '2021-05-02',
    '2021-05-03',
    '2021-06-12',
    '2021-06-13',
    '2021-06-14',
    '2021-09-21',
    '2021-10-01',
    '2021-10-02',
    '2021-10-03',
    '2021-10-04',
    '2021-10-05',
    '2021-10-06',
    '2021-10-07',
    '2020-10-08',
    '2020-10-09',
    '2020-10-10'
]
# 调整工作日准确日期，进行打卡
ajustWorking = ['2021-02-07', '2021-02-20', '2021-09-26', '2021-10-09']
# 调休日期，不进行打卡
compensatoryLeave = ['2020-05-16']

times = 5 # 5

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
    """
    企业微信打卡
    clock in out 上班 下班
    :return:
    """


    try:
        msg = u'启动失败 ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        init()

        d = u2.connect('emulator-5554')
        print(d.info)
        d.healthcheck()
    
    
        msg = u'连接失败 ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # 先结束再开启
        # os.popen("adb shell am force-stop com.tencent.wework")
        # time.sleep(5)
        os.popen("adb shell am start com.tencent.wework/com.tencent.wework.launch.LaunchSplashActivity")
        time.sleep(3 * times)
        print("启动企业微信成功")
        

        d(text=u"工作台").click()
        time.sleep(1 * times)
        d(text=u"移动签到").click()
        print("打开打卡界面成功")
        time.sleep(3 * times)

        print("当前小时：", datetime.datetime.now().hour)
    
        if datetime.datetime.now().hour < 11:
            if d(text=u"允许").info['text'] == u"允许":
                print("定位授权")
                d(text=u"允许").click()
                time.sleep(3 * times)
                

            # 早晨卡
            if d(text=u"已在范围内").info['text'] == u"已在范围内":
                print("现在是上午")
                d(textContains=u"上班打卡").click()
                time.sleep(2 * times)

                    
                # if d(text=u"正常").info['text'] == "正常":
                if d(textContains=u"正常", instance=0):
                    # in_time = d(className="android.widget.TextView", resourceId="com.tencent.wework:id/mp").info['text']
                    print("打卡时间：",  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                    msg = "上班打卡成功: 时间：" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                else:
                    msg = "打卡失败:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        else:
            if d(text=u"允许").info['text'] == u"允许":
                print("定位授权")
                d(text=u"允许").click()
                time.sleep(3 * times)

            # 下班卡
            if d(text=u"已在范围内").info['text'] == u"已在范围内":
                print("现在是下午")
                d(textContains=u"下班打卡").click()
                time.sleep(2 * times)
                    
                # if d(text=u"正常").info['text'] == "正常":
                if d(textContains=u"正常", instance=1):
                    # in_time = d(className="android.widget.TextView", resourceId="com.tencent.wework:id/mp").info['text']
                    print("打卡时间：",  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                    msg = "下班打卡成功: 时间：" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                else:
                    msg = "打卡失败:" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    # except:
    finally:
        return msg

def pushmsg(msg):
    """
    推送消息给微信
    :return:
    """
    try:
        url = 'http://wxpusher.zjiecode.com/api/send/message/?appToken=AT_rj717GNzJEovwYQXeIIQZTGx9sDn2n3U&content=' + msg + '&uid=UID_qOkRBipsTZbq4UF7qLYsLWpgFuvw'
        res = requests.get(url)
    except Exception:
        print("推送消息异常")

def logTime(tryTimes = 1):
    try:
        # 获取当前时间，2020-05-05 07:45
        nowtime = datetime.datetime.now()
        writelog("当前时间：" + nowtime.strftime("%Y-%m-%d %H:%M:%S"))
        # 加上随机数(0-3分钟)，2020-05-05 07:46
        randomTime = random.randint(1, 3)
        # print(randomTime + "分钟后打卡")
        # print( "执行任务时间：" + timeFormat(nowtime + datetime.timedelta(randomTime)) )
        # countDown(randomTime)
        writelog('logTime start')
        writelog(" --------------------------------- ")
        msg = openwework()
        # pushmsg(msg)
    except ConnectionRefusedError as e:
        writelog(e)
        # closeApp()
        os.popen("C:")
        os.popen("adb devices")
        os.popen("adb kill-server")
        os.popen("adb start-server")
        msg = openwework()
        # pushmsg(msg)
    except BaseException as e:
        writelog(e)
        closeApp()
        msg = openwework()
        # pushmsg(msg)
    finally:
        closeApp()
        writelog(msg)
        wechatStatus = msg.find('打卡') == -1
        if tryTimes < 6 and wechatStatus:
            writelog('try again')
            logTime(tryTimes + 1)
        else:
            pushmsg(msg)
            writelog('logTime end')
            writelog(' ----------------------------------------- ')

def dispatchTask():

    # if time.strftime("%Y-%m-%d", time.localtime()) in holiday:
    # if time.strftime("%Y-%m-%d", time.localtime()) in compensatoryLeave:
    # if time.strftime("%Y-%m-%d", time.localtime()) in ajustWorking:   
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
        logTime()
        return True

    # weekindex 0~6
    # 判断是否为周一到周五 
    weekIndex = datetime.datetime.now().weekday()
    if weekIndex != 6 and weekIndex != 5:
        print("周一至周五")
        logTime()

def test():

    openwework()
    
    # os.popen("adb kill-server")
    # os.popen("adb start-server")
        
    # os.popen("C:")
    # res = os.popen("adb devices")
    # time.sleep(1 * times)
    # os.popen("adb shell am start com.tencent.wework/com.tencent.wework.launch.LaunchSplashActivity")

    # d.watcher('agree').when(text=u'允许').click(text=u'允许')
    # print(type(d(text=u"允许"))) # <class 'uiautomator.AutomatorDeviceObject'>
    # if d(text=u"授权使用").info['text'] == "授权使用":
    # print(d(text=u"授权使用"))
    # print(d(textContains=u"授权").info['text'])
    # d(textContains=u"授权", instance=1).click()
    # d(text=u"授权使用", instance=0).click()

# 企业微信自动打卡
if __name__ == "__main__":
    '''
    # 主函数
    # linux 后台运行
    nohup python3 -u main.py > main.log 2>&1 &

    # Windows 
    start /b python3 main.py
    '''
    # msg = openwework()
    # print(msg)
    # test()
    # logTime()
    # schedule.every().day.at('11:06').do(dispatchTask)
    dispatchTask()
    
    # 每天执行打卡
    # # 第一个卡
    # schedule.every().day.at('08:45').do(dispatchTask)

    # # 第二个卡
    # schedule.every().day.at('18:11').do(dispatchTask)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(29)
