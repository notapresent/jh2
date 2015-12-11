# -*- coding: utf-8 -*-
import datetime

from base_manager import BaseManager
from ..models import Export


class ExportManager(BaseManager):
    __model__ = Export

    def last_exports(self):
        return (
            self.session.query(Export)
            .order_by(Export.started_at.desc())
            .limit(50)
            .all()
        )

    def clean_up_old_exports(self):
        """
            Delete all exports older than 30 days from now
        """
        threshold = datetime.datetime.utcnow() - datetime.timedelta(days=30)
        self.session.query(Export).filter(Export.started_at < threshold).delete()
