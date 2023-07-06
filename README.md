# replace-docx

<!-- Yeah, names are hard, shush. -->

This is a simple package that replaces `<<text>>` with `your own text` in docx
files. For now, this is literally all it does. If you want something more
feature-rich to work with docx files, you can look at the (unmaintained, untyped
and cumbersome) `python-docx` package on PyPI.

This project is still in early stages, and there may (will) be lots of feature
creep.

## Installation

```sh
pip install -U git+ssh://git@github.com:krtrimaiq-cognitive-solutions/replace-docx-pdf.git  # optional: @<branch|revision|tag>
```

## Usage

```py
from docx import Document

doc = Document.open('template.docx')
doc.render(abc='def')  # replaces <<abc>> with def
doc.save('final.docx')
```

## Drawbacks

A lot. Call them as they come...
