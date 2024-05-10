# code by David Salvisberg on python discussion boards
# https://discuss.python.org/t/make-mypy-happy-across-python-versions/40350/2
from __future__ import annotations
from itertools import * # i know this is bad practice in general, I'm only doing this so I can have a version
                        # of itertools with batched() in it, and having to use itertools312.iterators.batched()
                        # would defeat the purpose
import sys

if sys.version_info >= (3, 12):
    from itertools import batched
else:
    from typing import Iterable, Iterator, TypeVar

    T = TypeVar("T")

    def batched(iterable: Iterable[T], n: int) -> Iterator[tuple[T, ...]]:
        if n < 1:
            raise ValueError("n must be at least one")
        it = iter(iterable)
        while batch := tuple(islice(it, n)):
            yield batch