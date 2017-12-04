import os
import pathlib

from tests.tests_runner import get_merger


def generate_tests():
    directory = pathlib.Path(__file__).parent.parent / "testdata"
    for test in directory.iterdir():
        if test.is_dir() and not ((test / "result_full.xml").is_file() and (test / "result_incremental.xml").is_file()):
            print("Generating tests for: {}".format(test))
            with open(os.path.join(directory, test, "result_full.xml"), "wb+") as f:
                f.write(get_merger(test).get_full_result())
            with open(os.path.join(directory, test, "result_incremental.xml"), "wb+") as f:
                f.write(get_merger(test).get_incremental_result())


def main():
    generate_tests()


if __name__ == '__main__':
    main()
