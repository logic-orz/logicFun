import asyncio

from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

timezone="Asia/Shanghai"

def _fromCron(cron:str):
    values = cron.split(" ")
    if len(values) != 7:
        raise ValueError(
                'Wrong number of fields; got {}, expected 7'.format(len(values)))

    return CronTrigger(second=values[0], minute=values[1], hour=values[2], day=values[3], month=values[4],
                   day_of_week=values[5], year=values[6], timezone=timezone)
  
class backSchedule(object):
    """
    后台同步任务调度
    cron: 0 0 0 * * * *
    """
    executors = {
        'default': ThreadPoolExecutor(20),
        'processpool': ProcessPoolExecutor(10)
    }
    _sched =None
    
    @staticmethod
    def addJob(func, cron:str, id:str=None):
        if not id:
            id = func.__name__
        if not backSchedule._sched:
            backSchedule._sched = BackgroundScheduler(timezone=timezone,
                                         executors=backSchedule.executors)
            backSchedule._sched.start()
        backSchedule._sched.add_job(func, trigger=_fromCron(cron), id=id)
    
    @staticmethod
    def removeJob(id:str):
        backSchedule._sched.remove_job(id)
    
    def __init__(self, cron: str, id=None,isAsync=False):
        self.cron = cron
        self.id = id
        self.isAsync=isAsync

    def __call__(self, __func):  # 接受函数
        if not self.id:
            self.id = __func.__name__
        backSchedule.addJob(__func, 
                            cron=self.cron, 
                            id=self.id)

        def wrapper(*args, **kwargs):
            return __func(*args, **kwargs)
        return wrapper  # 返回函数
    
    
class asyncSchedule(object):
    """
    后台同步任务调度
    cron: 0 0 0 * * * *
    """
    _sched =None
    
    @staticmethod
    def addJob(func, cron:str, id:str=None):
        if not id:
            id = func.__name__
        if not asyncSchedule._sched:
            asyncSchedule._sched = AsyncIOScheduler(timezone=timezone)
            asyncSchedule._sched.start()
        asyncSchedule._sched.add_job(func, trigger=_fromCron(cron), id=id)
    
    @staticmethod
    def removeJob(id:str):
        asyncSchedule._sched.remove_job(id)
    
    def __init__(self, cron: str, id=None,isAsync=False):
        self.cron = cron
        self.id = id
        self.isAsync=isAsync

    def __call__(self, __func):  # 接受函数
        if not self.id:
            self.id = __func.__name__
        asyncSchedule.addJob(__func, 
                            cron=self.cron, 
                            id=self.id)

        def wrapper(*args, **kwargs):
            return __func(*args, **kwargs)
        return wrapper  # 返回函数

import datetime
import time


@asyncSchedule(cron='*/5 * * * * * *')
async def run1():
    
    t1=datetime.datetime.now()
    await asyncio.sleep(3)
    # time.sleep(3)
    print(t1,datetime.datetime.now(),1)
    
asyncio.get_event_loop().run_forever()
    
