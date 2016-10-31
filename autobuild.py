#!/usr/bin/env python
import logging
import commands
import os
import time

def git_pull():
    print (os.chdir("/opt/push/jpush-docs/jpush-docs/"))
<<<<<<< HEAD
    logging.info(commands.getstatusoutput("git pull origin master"))
    print ("git pull origin master")
=======
    logging.info(commands.getstatusoutput("git pull origin renew"))
    print ("git pull origin renew")
>>>>>>> e8ebb19e891ee41f300ee8854a1e907b07df85b2


def build():
    print (os.chdir("/opt/push/jpush-docs/jpush-docs/zh/JPush/"))
    print ("JPush/")
    logging.info (commands.getstatusoutput("/opt/push/jpush-docs/venv/bin/mkdocs build"))
    time.sleep(1)
    print time.asctime(time.localtime(time.time()))
    logging.info (os.chdir("/opt/push/jpush-docs/jpush-docs/zh/JMessage/"))
    print ("JMessage/")
    logging.info (commands.getstatusoutput("/opt/push/jpush-docs/venv/bin/mkdocs build"))
    time.sleep(1)
    print time.asctime(time.localtime(time.time()))
    logging.info (os.chdir("/opt/push/jpush-docs/jpush-docs/zh/JSMS/"))
    print ("JSMS/")
    logging.info (commands.getstatusoutput("/opt/push/jpush-docs/venv/bin/mkdocs build"))
    time.sleep(1)
    print time.asctime(time.localtime(time.time()))
    logging.info (os.chdir("/opt/push/jpush-docs/jpush-docs/zh/Index/"))
    print ("Index/")
    logging.info (commands.getstatusoutput("/opt/push/jpush-docs/venv/bin/mkdocs build"))
    time.sleep(1)
    print time.asctime(time.localtime(time.time()))


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='/opt/push/jpush-docs/autobuild.log',
                    filemode='a+')

git_pull()
build()
<<<<<<< HEAD
print time.asctime(time.localtime(time.time()))
=======
print time.asctime(time.localtime(time.time()))








>>>>>>> e8ebb19e891ee41f300ee8854a1e907b07df85b2
