# -*- coding: utf-8 -*-
import rq


JOB_TIMEOUT = 900   # seconds


class TaskQueue(object):

    """
        Abstracts task queue
    """

    def __init__(self, redis=None):
        self.q = rq.Queue(connection=redis, default_timeout=JOB_TIMEOUT)

    def enqueue(self, task_name, *args, **kwargs):
        """
            Add task with specified name and arguments to task queue
        """
        job = self.q.enqueue('rbm2m.worker.run_task', task_name, *args, **kwargs)
        return job
