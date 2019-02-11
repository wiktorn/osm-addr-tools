import multiprocessing
import typing
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor


def parallel_execution(*args):
    """run in parallel all functions passed as args"""
    max_workers = multiprocessing.cpu_count()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        return tuple(
            map(lambda x: x.result(),
                [executor.submit(x) for x in args]))


def parallel_map(func, lst, max_workers=multiprocessing.cpu_count()):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        return tuple(executor.map(func, lst))


K = typing.TypeVar('K')
V = typing.TypeVar('V')
E = typing.TypeVar('E')


def groupby(lst: typing.Iterable[E],
            keyfunc: typing.Callable[[E], K] = lambda x: x,
            valuefunc: typing.Callable[[E], V] = lambda x: x
            ) -> typing.DefaultDict[K, V]:
    ret = defaultdict(list)
    for i in lst:
        ret[keyfunc(i)].append(valuefunc(i))
    return ret


def main():
    from time import sleep, time
    print(time())

    def f(x):
        sleep(1)
        return str(x)
    print(parallel_map(f, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]))
    print(time())


if __name__ == '__main__':
    main()
