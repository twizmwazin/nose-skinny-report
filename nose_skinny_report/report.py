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

    # Nothing about this monstronsity is beutiful or elegant. It desperatly
    # needs some attention. But... it works, I think
    def startTest(self, event):
        if isinstance(event.test, Exception):
            event.handled = true
            return
        try:
            test = '.'.join([
                str(sys.modules[event.test._testFunc.__module__].__name__),
                str(event.test._testFunc.__qualname__),
            ])
        except:
            try:
                test = event.test._name
            except:
                test = '.'.join([
                    type(event.test).__module__,
                    type(event.test).__qualname__,
                ])
        if test not in self.tests:
            self.tests.append(test)
        event.handled = True

    def afterTestRun(self, event):
        evt = events.ReportSummaryEvent(
            event, self.stream, self.reportCategories)
        for t in self.tests:
            evt.stream.write('{}\n'.format(t))
            evt.stream.flush()
