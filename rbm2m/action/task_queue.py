# -*- coding: utf-8 -*-
import rq


JOB_TIMEOUT=300


class TaskQueue(object):
    """
        Abstracts task queue
    """
    def __init__(self, redis=None):
        self.q = rq.Queue(redis_conn=redis)

    def enqueue(self, task_name, *args, **kwargs):
        """
            Add task with specified name and arguments to task queue
        """
        timeout = kwargs.pop('timeout', JOB_TIMEOUT)
        at_front = kwargs.pop('at_front', False)
        job = self.q.enqueue('worker.run_task', task_name,
                             timeout=timeout, at_front=at_front,
                             *args, **kwargs)
        return job
