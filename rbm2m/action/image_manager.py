# -*- coding: utf-8 -*-
import logging

from PIL import Image as PilImage

from base_manager import BaseManager
from ..models import Image


logger = logging.getLogger(__name__)


class ImageManager(BaseManager):
    __model__ = Image

    def find_covers_for_records(self, rec_ids):
        """
            Find all images for list of records
        """
        return (
            self.session.query(Image)
            .filter(Image.record_id.in_(rec_ids))
            .filter(Image.is_cover.is_(True))
        )


def make_thumbnail(original_path, thumbnail_path):
    """
        Make image thumbnail
    """
    size = (640, 640)

    try:
        im = PilImage.open(original_path)
        im.thumbnail(size)
        im.save(thumbnail_path, "JPEG")
    except IOError as e:
        logger.error('Thumbnail generation for {} failed: {}'.format(original_path, e))
