# -*- coding: utf-8 -*-
import os

from image_manager import ImageManager
from record_manager import RecordManager
import scraper


class ImageImporter(object):
    """
        Imports images for records
    """
    def __init__(self, config, session):
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
            Import images for records, identified by rec_ids
        """
        rec_image_urls = scraper.get_image_urls(rec_ids)

        dl_list = self.make_dl_list(rec_image_urls)

        saved = scraper.download_and_save_images(dl_list)

        for img_id, length in saved:
            img = self.image_manager.get(img_id)
            img.length = length

    def make_dl_list(self, rec_image_urls):
        """
            Accepts dict {rec_id_1: ['img_url_1', 'img_url_2', ..], ...}
            Generate list of tuples (image_id, image_url, filename)
        """
        for rec_id, urls in rec_image_urls.items():
            if not urls:
                self.mark_record(rec_id, 'missing_images')
                print "*** Missing images for #%d".format(rec_id)
                continue

            img_ids = self.save_image_rows(rec_id, urls)

            for img_id, url in zip(img_ids, urls):
                yield img_id, url, make_filename(img_id, self.config.MEDIA_DIR)

    def save_image_rows(self, rec_id, urls):
        """
            Insert images for record and yield inserted row ids
        """
        for url in urls:
            img = self.image_manager.from_dict({'record_id': rec_id, 'url': url})
            yield img.id

    def mark_record(self, rec_id, flag):
        """
            Mark record, identified by rec_id, with flag
        """
        recman = RecordManager(self.session)
        rec = recman.get(rec_id)
        rec.flags.append(flag)


def make_filename(img_id, basedir='', suffix='.jpg'):
    """
        Generate filename from id and base dir, with optional suffix
    """
    strid = str(img_id).zfill(6)
    frags = [strid[i:i+2] for i in range(0, len(strid), 2)]
    frags.append("{}{}".format(img_id, suffix))
    frags.insert(0, basedir)
    return os.path.join(*frags)
