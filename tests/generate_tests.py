import os

from tests.tests_runner import get_merger


def generate_tests():
    directory = os.path.dirname(os.path.realpath(__file__))
    for test in os.listdir(directory):
        if os.path.samefile(test, __file__) or os.path.isfile(test) or test == '__pycache__' or (
                os.path.isfile(os.path.join(directory, test, "result_full.xml")) and
                os.path.isfile(os.path.join(directory, test, "result_incremental.xml"))
        ):
            continue
        print("Generating tests for: {}".format(test))
        with open(os.path.join(directory, test, "result_full.xml"), "wb+") as f:
            f.write(get_merger(os.path.join(directory, test)).get_full_result())
        with open(os.path.join(directory, test, "result_incremental.xml"), "wb+") as f:
            f.write(get_merger(os.path.join(directory, test)).get_incremental_result())


def main():
    generate_tests()


if __name__ == '__main__':
    main()
