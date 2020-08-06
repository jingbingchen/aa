from BeautifulReport import BeautifulReport


class MyBeautifulReport(BeautifulReport):

    def __init__(self, suites):
        super(MyBeautifulReport, self).__init__(suites)
        self.suites = suites

    # 启动
    def run_result_report(self):
        self.suites.run(result=self)
        self.stopTestRun(self.title)
