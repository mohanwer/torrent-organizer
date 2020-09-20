import unittest
from app.tvfile import TvFile


class TvFileTestMethods(unittest.TestCase):

    def test_tv_show_file(self):
        test_show_path = '\\home\\some.show.S01E02.avi'
        test_show = TvFile(test_show_path)
        formatted_tv_name = test_show.get_show_name()
        self.assertTrue(test_show.is_tv_show)
        self.assertEqual(formatted_tv_name, 'SOME.SHOW')
        self.assertEqual(test_show.episode, '02')
        self.assertEqual(test_show.season, '01')
        self.assertEqual(test_show.extension, '.avi')

    def test_non_tv_show_file(self):
        non_tv_show_file = '\\home\random_file.txt'
        test_tv_file = TvFile(non_tv_show_file)
        self.assertFalse(test_tv_file.is_tv_show)