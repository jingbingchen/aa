from multiprocessing import Pool

from base_logging import log


class RunPool(object):
    count_num = 1

    def run(self, params, fn, run_number):
        """
        执行次数
        :param params: 运行参数
        :param fn: 运行函数
        :param run_number: 运行次数
        :return:
        """
        with Pool(len(params)) as pool:
            # while True:
            for i in range(run_number):
                log.info("-----------------------------运行[{}]次-----------------------------", self.count_num)
                result = pool.map_async(fn, params)
                result.get()
                self.count_num = self.count_num + 1

    def run_result(self, params, fn):
        """
        执行次数
        :param params: 运行参数
        :param fn: 运行函数
        :param run_number: 运行次数
        :return:
        """
        with Pool(len(params)) as pool:
            # while True:
            # for i in range(run_number):
            log.info("-----------------------------运行[{}]次-----------------------------", self.count_num)
            result = pool.map_async(fn, params)
            result.get()
            self.count_num = self.count_num + 1

    def run_true(self, params, fn):
        """
        阻塞运行（不推荐）
        :param params: 运行参数
        :param fn: 运行函数
        :return:
        """
        with Pool(len(params)) as pool:
            while True:
                log.info("-----------------------------运行[{}]次-----------------------------", self.count_num)
                result = pool.map_async(fn, params)
                result.get()
                self.count_num = self.count_num + 1
