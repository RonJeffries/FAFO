import os
from os.path import expanduser

import pytest


class TestDatabase:
    def test_listdir(self):
        all_filenames = self.get_all_filenames()
        assert len(all_filenames) == 1000

    def get_all_filenames(self):
        database = expanduser("~/programming/database")
        all_files = os.listdir(database)
        return all_files

    def test_find_hill_math(self):
        all_names = self.get_all_filenames()
        hill = [name for name in all_names if "_author-geepaw_" in name]
        math_hill = [name for name in hill if "_topic-math_" in name]
        hector = [name for name in math_hill if "_student-hector_" in name]
        assert len(hill) == 100
        assert len(math_hill) == 10
        assert len(hector) == 1

    # @pytest.mark.skip("timing skip")
    # def test_selections_per_second(self):
    #     start = datetime.now()
    #     for i in range(1500):
    #         all_names = self.get_all_filenames()
    #     hill = [name for name in all_names if "_author-geepaw_" in name]
    #     math_hill = [name for name in hill if "_topic-math_" in name]
    #     hector = [name for name in math_hill if "_student-hector_" in name]
    #     elapsed = datetime.now() - start
    #     print(elapsed, elapsed.seconds, elapsed.microseconds)
    #     seconds = elapsed.seconds + elapsed.microseconds/1000000.0
    #     assert seconds < 1.0

