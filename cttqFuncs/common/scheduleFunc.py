from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

_sched = BackgroundScheduler()
_sched.start()


class MyCronTrigger(CronTrigger):

    @classmethod
    def my_from_crontab(cls, expr, timezone=None):
        values = expr.split(" ")
        if len(values) != 7:
            raise ValueError(
                'Wrong number of fields; got {}, expected 7'.format(len(values)))

        return cls(second=values[0], minute=values[1], hour=values[2], day=values[3], month=values[4],
                   day_of_week=values[5], year=values[6], timezone=timezone)


def addJob(func, cron, id=None):
    if not id:
        id = func.__name__
    _sched.add_job(func, trigger=MyCronTrigger.my_from_crontab(cron), id=id)


def removeJob(id:str):
    _sched.remove_job(id)
    
class backSchedule(object):
    """
    * 后置函数，操作对象为被装饰函数的返回结果
    """

    def __init__(self, cron: str, id=None):
        self.cron = cron
        self.id = id

    def __call__(self, __func):  # 接受函数
        if not self.id:
            self.id = __func.__name__
        _sched.add_job(__func, trigger=MyCronTrigger.my_from_crontab(
            self.cron), id=self.id)

        def wrapper(*args, **kwargs):
            return __func(*args, **kwargs)
        return wrapper  # 返回函数
