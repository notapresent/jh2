# -*- coding: utf-8 -*-
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
