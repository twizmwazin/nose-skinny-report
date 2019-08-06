import re
import sys
from unittest.util import strclass

from nose2 import events, result, util

__unittest = True

class ResultReporter(events.Plugin):

    """Result plugin that implements standard unittest console reporting"""
    alwaysOn = True

    def __init__(self):
        self.stream = util._WritelnDecorator(sys.stdout)
        self.reportCategories = {}
        self.tests = []

    def startTest(self, event):
        try:
            test = '.'.join([
                str(sys.modules[event.test._testFunc.__module__].__name__),
                str(event.test._testFunc.__qualname__),
            ])
        except:
            test = event.test._name
        if test not in self.tests:
            self.tests.append(test)
        event.handled = True

    def afterTestRun(self, event):
        evt = events.ReportSummaryEvent(
            event, self.stream, self.reportCategories)
        for t in self.tests:
            evt.stream.write('{}\n'.format(t))
            evt.stream.flush()
