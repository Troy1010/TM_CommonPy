import TM_CommonPy as TM

class LoggingHeaderDecorator:
    """Decorator to add a header"""
    bFirstCall = True
    sLastFnName = ""
    def __init__(self, method):
        self.method = method
    def __call__(self, *args, **kwargs):
        if __class__.sLastFnName != TM.FnName(1):
            __class__.sLastFnName = TM.FnName(1)
            if __class__.bFirstCall:
                __class__.bFirstCall = False
                self.method("-------"+__class__.sLastFnName)
            else:
                self.method("\n\n-------"+__class__.sLastFnName)
        self.method(*args, **kwargs)
