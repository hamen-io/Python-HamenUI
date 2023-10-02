import inspect
import datetime

class Console:
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.debug_prefix = lambda : "Line " + str(inspect.currentframe().f_back.f_back.f_lineno) + " @ " + datetime.datetime.today().strftime("%H:%M:%S") + ": "
        self._stdout = lambda *values,end,separator : print(*([self.debug_prefix() if self.debug else ""] + list(*values)), end = end, sep = separator)

    def log(self, *values, end: str = "\n", separator: str = ""):
        self._stdout(*values, end=end, separator=separator)