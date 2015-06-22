# -*- coding: utf-8 -*-
from record_manager import RecordManager
from scan_manager import ScanManager
import scraper


class RecordImporter(object):

    def __init__(self, session, scan):
        self.session = session
        self.scan = scan
        self._record_manager = None
        self._scan_manager = None
        self._next_page = None
        self._has_images = []

    @property
    def record_manager(self):
        if self._record_manager is None:
            self._record_manager = RecordManager(self.session)

        return self._record_manager

    @property
    def scan_manager(self):
        if self._scan_manager is None:
            self._scan_manager = ScanManager(self.session)

        return self._scan_manager

    @property
    def has_images(self):
        """
            List of ids of records with images
        """
        return self._has_images

    @property
    def next_page(self):
        """
            Number of next page in scan or none if no more pages
        """
        return self._next_page

    def run(self, scan, page_no):
        """
            Run scrape and process results
        """
        scrape = scraper.Scrape()
        try:
            scrape.run(scan.genre.title, page_no)
        except scraper.ScrapeError as e:
            raise RecordImportError(str(e))

        self.update_record_count(page_no, scrape.rec_count)
        self._next_page = scrape.next_page
        self.process_records(scrape.records)

    def process_records(self, records):
        """
            Add existing records to scan and process new ones
        """
        record_ids = [rec['id'] for rec in records]
        record_ids = self.scan_manager.records_not_in_scan(self.scan.id, record_ids)
        old_records = self.record_manager.find_existing(record_ids)
        old_ids = [rec.id for rec in old_records]
        self.scan.records.extend(old_records)

        for rec_dict in records:
            if rec_dict['id'] not in old_ids:
                rec_dict['genre_id'] = self.scan.genre_id
                rec = self.new_record(rec_dict)
                self.scan.records.append(rec)

    def new_record(self, rec_dict):
        """
            Create new record and add images to self._has_images
        """
        has_images = rec_dict.pop('has_images')
        if has_images:
            self._has_images.append(rec_dict['id'])

        record = self.record_manager.from_dict(rec_dict)
        record.genre_id = self.scan.genre_id
        return record

    def update_record_count(self, page_no, rec_count):
        """
            Update estimated records count every 10 pages
        """
        if page_no is None or page_no % 10 == 0:
            self.scan.est_num_records = rec_count


class RecordImportError(Exception):

    """
        Unrecoverable record import error
    """
    pass
