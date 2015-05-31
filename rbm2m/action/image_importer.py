# -*- coding: utf-8 -*-
from image_manager import ImageManager


class ImageImporter(object):
    """
        Imports images
    """
    def __init__(self, config, session):
        super(ImageImporter, self).__init__()
        self.config = config
        self.session = session
        self._image_manager = None

    @property
    def image_manager(self):
        if self._image_manager is None:
            self._image_manager = ImageManager(self.session)

        return self._image_manager

    def run(self, rec_ids):
        """

        """
        # multi-download image lists for each record
        # multi-download images for each record
        # TODO
        pass
