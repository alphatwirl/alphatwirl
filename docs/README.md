
##### How to update the docs

In the top directory of AlphaTwirl (one directory up from this directory):

    rm docs/alphatwirl*.rst
    sphinx-apidoc -F -o docs/ alphatwirl/
    cd docs

Edit `conf.py` if need, e.g., increment the version number

Make

    make html

The entry page will be at `_build/html/index.html`.
