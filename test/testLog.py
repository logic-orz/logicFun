from cttqFuncs.common import SimpleLog,log


SimpleLog.init(logFileName="tmp1",useSizeRoute=True)
SimpleLog.addSizeRoute(logFileName="tmp2",filter=lambda record:record['level'].name=='DEBUG')


log.info("test1")
log.debug("test2")