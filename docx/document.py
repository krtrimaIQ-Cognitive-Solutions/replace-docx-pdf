"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from __future__ import annotations

import os
import re
import zipfile
from collections import defaultdict
from typing import TYPE_CHECKING, DefaultDict, List, Union

from lxml import etree


if TYPE_CHECKING:
    from typing_extensions import Self


class Document:
    # If you want to use a different template syntax, change this regex.
    # BUT: it should have exactly one capturing group, the key.
    # The key should be a valid Python identifier.
    # The key should not contain any whitespace.
    # The key should not contain any characters that are special in XML.
    # The key should not contain any characters that are special in regex.
    TEMPLATE_RE = re.compile(r'<<(\w+)>>')
    NSMAP = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    # A hack. You can override this too.
    __template_fmt = None

    def __init__(self, __zf: zipfile.ZipFile, __tree: etree._Element) -> None:
        self.__files: dict[str, bytes] = {name: __zf.read(name) for name in __zf.namelist()}
        self.__tree = __tree
        self.__mapping: DefaultDict[str, List[etree._Element]] = defaultdict(list)

    @classmethod
    @property
    def _TEMPLATE_FMT(cls) -> str:
        if cls.__template_fmt is not None:
            return cls.__template_fmt
        cls.__template_fmt = cls.TEMPLATE_RE.pattern.replace(r'(\w+)', '{key}')
        return cls.__template_fmt

    @_TEMPLATE_FMT.setter
    def _TEMPLATE_FMT(cls, value: str) -> None:
        cls.__TEMPLATE_FMT = value

    @classmethod
    def open(cls, fname: Union[str, os.PathLike[str]]) -> Self:
        with zipfile.ZipFile(fname) as zf:
            tree = etree.fromstring(zf.read('word/document.xml'))
            self = cls(zf, tree)

        runs = tree.xpath('.//w:p/w:r/w:t', namespaces=cls.NSMAP)

        for run in runs:
            for match in cls.TEMPLATE_RE.finditer(run.text):
                self.__mapping[match.group(1)].append(run)
        return self

    def render(self, **kwargs: str) -> None:
        for key, value in kwargs.items():
            elems = self.__mapping[key]
            if not elems:
                raise KeyError(f'No such key: {key}')
            for elem in elems:
                assert elem.text is not None
                elem.text = elem.text.replace(self._TEMPLATE_FMT.format(key=key), value)

    def write(self, fname: str) -> None:
        with zipfile.ZipFile(fname, 'w') as zf:
            for k, v in self.__files.items():
                if k != 'word/document.xml':
                    zf.writestr(k, v)
                else:
                    zf.writestr(k, etree.tostring(self.__tree))

    @property
    def keys(self) -> List[str]:
        return list(self.__mapping.keys())

    @property
    def text_runs(self) -> list[str]:
        return [t.text for t in self.__tree.xpath('.//w:r/w:t')]

    def xml(self, *, pretty_print: bool = True) -> str:
        return etree.tostring(self.__tree, encoding='unicode', pretty_print=pretty_print)
