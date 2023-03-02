from datetime import datetime
from cttqFuncs.common.logFunc import SimpleLog
import os
import traceback
if __name__ =='__main__':
    
    log=SimpleLog.get()
    
    log.info('hahah info ')
    log.warning('hahah warning ')
    log.error('hahah error ')
    log.debug('hahah debug ')