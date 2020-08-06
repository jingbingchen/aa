from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED


class DmPool(object):

    all_task = []
    wait_task = []

    def __init__(self):
        """
        初始化
        """
        self.pool = ThreadPoolExecutor(max_workers=200)

    def add_task(self, fn, *args):
        task = self.pool.submit(fn, *args)
        self.all_task.append(task)

    def add_task_map(self, fn, urls):
        self.pool.map(fn, urls)

    def add_task_wait(self, fn, *args):
        task = self.pool.submit(fn, *args)
        self.all_task.append(task)
        self.wait_task.append(task)

    def task_wait(self, timeout=None, return_when=ALL_COMPLETED):
        wait(self.wait_task, timeout, return_when)


dmPool = DmPool()