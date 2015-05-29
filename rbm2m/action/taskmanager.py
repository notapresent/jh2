# -*- coding: utf-8 -*-

class TaskManager(object):
    """
        Manages page task creation and execution
    """
    def __init__(self, config, session, redis):
        self.config = config
        self.session = session
        self.redis = redis

    def run_task(self):
        pass
