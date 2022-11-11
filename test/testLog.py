from cttqFuncs.common.logFunc import Log



Log.logFileName='testLog'

Log.useTimeRoute=True
log=Log.get()
for i in range(0,1000):
    log.info('test---info')
    log.debug('test--debug')
    log.warning('test--warning')
    log.error('test--error')