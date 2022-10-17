from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

SCHEDULES = list()

_sched = BackgroundScheduler()
_sched.start()


class schedule(object):
    """
    * 后置函数，操作对象为被装饰函数的返回结果
    """

    def __init__(self, cron: str):
        self.cron = cron

    def __call__(self, __func):  # 接受函数
        def wrapper(*args, **kwargs):
            _sched.add_job(__func, 'cron',
                           andTri=CronTrigger.from_crontab(self.cron))
            return __func(*args, **kwargs)
        return wrapper  # 返回函数
