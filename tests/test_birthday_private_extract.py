"""Synthetic XLSX fixtures only. Never loads the Owner's workbook or credentials."""
from datetime import datetime
import importlib.util
import json
from pathlib import Path
import stat
import tempfile
import unittest

from openpyxl import Workbook

spec = importlib.util.spec_from_file_location('extractor', Path(__file__).resolve().parents[1] / 'scripts/airo_birthday_private_extract.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class ExtractionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = self.root / 'synthetic.xlsx'

    def tearDown(self):
        self.temp.cleanup()

    def workbook(self, rows, duplicate_tab=False):
        book = Workbook(); book.active.title = 'Operations'
        book.active.append(['NAMA', 'Operational data'])
        sheet = book.create_sheet('Birthday synthetic')
        sheet.append(['Synthetic test only']); sheet.append([]); sheet.append(list(m.HEADERS))
        for row in rows:
            sheet.append(row)
        if duplicate_tab:
            book.copy_worksheet(sheet)
        book.save(self.source); book.close()

    def extract(self):
        return m.extract(self.source, 'synthetic-file-id', 'synthetic-modified-time')

    def test_exact_tab_and_provenance(self):
        self.workbook([['SYNTHETIC DEALER', ' SYNTHETIC PERSON ', datetime(2000, 2, 29), datetime(2024, 2, 29)]])
        manifest, valid, review, records = self.extract()
        self.assertEqual(manifest['BIRTHDAY_TAB'], 'Birthday synthetic')
        self.assertEqual(valid[0]['output']['NAMA'], ' SYNTHETIC PERSON ')
        self.assertEqual(valid[0]['output']['SOURCE_ROW'], 4)
        self.assertEqual(valid[0]['output']['SOURCE_CELLS'], 'A4,B4,C4,D4')
        self.assertEqual(valid[0]['output']['BIRTH_YEAR'], 2000)
        self.assertFalse(review)

    def test_ambiguous_tabs_fail_closed(self):
        self.workbook([], duplicate_tab=True)
        with self.assertRaises(ValueError):
            self.extract()

    def test_unknown_year_and_normalized_only(self):
        self.workbook([['SYNTHETIC', 'A', datetime(2024, 5, 7), datetime(2024, 5, 7)],
                       ['SYNTHETIC', 'B', None, datetime(2024, 6, 8)]])
        manifest, valid, review, _ = self.extract()
        self.assertEqual(manifest['UNKNOWN_BIRTH_YEAR_ROWS'], 2)
        self.assertEqual(manifest['NORMALIZED_ONLY_ROWS'], 1)
        self.assertEqual(len(valid), 2)
        self.assertTrue(all(x['output']['BIRTH_YEAR'] == '' for x in valid))
        self.assertFalse(review)

    def test_column_conflict_is_preserved_and_quarantined(self):
        self.workbook([['SYNTHETIC', 'A', datetime(1964, 4, 4), datetime(2024, 3, 4)]])
        manifest, valid, review, _ = self.extract()
        self.assertFalse(valid)
        self.assertEqual(manifest['CONFLICT_ROWS'], 1)
        self.assertIn('DATE_COLUMN_CONFLICT', review[0]['flags'])
        self.assertNotEqual(review[0]['original_cells']['TANGGAL LAHIR'], review[0]['original_cells']['TANPA TAHUN'])

    def test_possible_duplicates_are_not_deleted(self):
        row = ['SYNTHETIC', 'A', datetime(2000, 1, 2), datetime(2024, 1, 2)]
        self.workbook([row, row])
        manifest, valid, review, _ = self.extract()
        self.assertEqual(len(valid), 2)
        self.assertEqual(manifest['POSSIBLE_DUPLICATE_ROWS'], 2)
        self.assertEqual(valid[0]['output']['DUPLICATE_GROUP'], valid[1]['output']['DUPLICATE_GROUP'])
        self.assertFalse(review)

    def test_same_name_different_dealers_preserved(self):
        self.workbook([['SYNTHETIC A', 'A', datetime(2000, 1, 2), None],
                       ['SYNTHETIC B', 'A', datetime(2000, 4, 5), None]])
        manifest, valid, review, _ = self.extract()
        self.assertEqual(len(valid), 2)
        self.assertEqual(manifest['CONFLICT_ROWS'], 0)

    def test_same_identity_conflicting_dates_are_all_quarantined(self):
        self.workbook([['SYNTHETIC', 'A', datetime(2000, 1, 2), None],
                       ['SYNTHETIC', 'A', datetime(2000, 4, 5), None]])
        manifest, valid, review, _ = self.extract()
        self.assertFalse(valid)
        self.assertEqual(manifest['CONFLICT_ROWS'], 2)

    def test_incomplete_and_invalid_records_excluded(self):
        self.workbook([['SYNTHETIC', '-', datetime(2000, 1, 2), None],
                       ['SYNTHETIC', 'A', None, None], ['SYNTHETIC', 'B', 'invalid', datetime(2024, 1, 2)]])
        manifest, valid, review, _ = self.extract()
        self.assertFalse(valid)
        self.assertEqual(manifest['MISSING_NAME_ROWS'], 1)
        self.assertEqual(manifest['INVALID_DATE_ROWS'], 1)
        self.assertEqual(len(review), 3)

    def test_private_publication_reproducible_and_source_unchanged(self):
        self.workbook([['SYNTHETIC', 'A', datetime(2000, 1, 2), None]])
        before = self.source.read_bytes()
        a = m.publish(self.source, self.root / 'private', 'synthetic', 'synthetic')
        b = m.publish(self.source, self.root / 'private', 'synthetic', 'synthetic')
        self.assertEqual(a, b)
        folder = Path(a['PRIVATE_DATASET_DIR'])
        self.assertEqual(stat.S_IMODE(folder.stat().st_mode), 0o700)
        self.assertTrue(all(stat.S_IMODE(p.stat().st_mode) == 0o600 for p in folder.iterdir()))
        self.assertEqual(before, self.source.read_bytes())
        self.assertFalse(a['ACTIVATED'])

    def test_symlink_output_rejected(self):
        self.workbook([])
        (self.root / 'actual').mkdir(); (self.root / 'link').symlink_to(self.root / 'actual', target_is_directory=True)
        with self.assertRaises(ValueError):
            m.publish(self.source, self.root / 'link', 'synthetic', 'synthetic')

    def test_leap_day_and_invalid_date(self):
        self.assertEqual(m.parse('29/02', datetime(1899, 12, 30)).day, 29)
        self.assertIsNone(m.parse('31/02/2000', datetime(1899, 12, 30)))


if __name__ == '__main__':
    unittest.main()
