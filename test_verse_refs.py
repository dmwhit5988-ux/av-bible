"""verse_refs.parse reads the ref strings the data modules write.

    .venv\\Scripts\\python.exe -m unittest test_verse_refs -v
"""

import unittest

from verse_refs import Ref, parse


class Parse(unittest.TestCase):
    def test_book_carries_on(self):
        self.assertEqual(parse("Gen 11:29, 22:20-23", "1 Chronicles"), [
            Ref("Genesis", 11, 29), Ref("Genesis", 22, 20, None, 23)])

    def test_bare_ref_takes_the_default_book(self):
        self.assertEqual(parse("2:3", "1 Chronicles"),
                         [Ref("1 Chronicles", 2, 3)])
        self.assertEqual(parse("7:19; Num 26:32", "1 Chronicles"), [
            Ref("1 Chronicles", 7, 19), Ref("Numbers", 26, 32)])

    def test_bare_number_after_a_verse_is_a_verse(self):
        self.assertEqual(parse("Ruth 1:2, 20", "1 Chronicles"), [
            Ref("Ruth", 1, 2), Ref("Ruth", 1, 20)])
        self.assertEqual(parse("2 Kgs 8:18, 26, 2 Chr 22:10-12", "x"), [
            Ref("2 Kings", 8, 18), Ref("2 Kings", 8, 26),
            Ref("2 Chronicles", 22, 10, None, 12)])

    def test_chapters_and_chapter_ranges(self):
        self.assertEqual(parse("1 Sam 1-4", "x"), [Ref("1 Samuel", 1, None, 4)])
        self.assertEqual(parse("Judg 9", "x"), [Ref("Judges", 9)])

    def test_range_across_chapters(self):
        self.assertEqual(parse("Gen 29:16-30:21", "x"),
                         [Ref("Genesis", 29, 16, 30, 21)])

    def test_range_across_books_is_read_as_its_ends(self):
        self.assertEqual(parse("1 Kgs 12 - 2 Kgs 17", "x"), [
            Ref("1 Kings", 12), Ref("2 Kings", 17)])

    def test_remark_after_a_dash_is_dropped(self):
        self.assertEqual(
            parse("Matthew 1:13 — past the end of the Old Testament", "x"),
            [Ref("Matthew", 1, 13)])

    def test_verses_web_does_not_have_raise(self):
        with self.assertRaises(ValueError):
            parse("Acts 15:34", "x")         # WEB has no Acts 15:34
        with self.assertRaises(ValueError):
            parse("Gen 51:1", "x")
        with self.assertRaises(ValueError):
            parse("Gen 5:9-3", "x")

    def test_unreadable_text_raises(self):
        with self.assertRaises(ValueError):
            parse("see the note", "x")

    def test_verses_lists_every_verse(self):
        self.assertEqual(Ref("Ruth", 1, 21, 2, 2).verses(), [
            ("Ruth", 1, 21), ("Ruth", 1, 22), ("Ruth", 2, 1), ("Ruth", 2, 2)])
        self.assertEqual(Ref("Ruth", 4, 21, None, 22).first(), (4, 21))


if __name__ == "__main__":
    unittest.main()
