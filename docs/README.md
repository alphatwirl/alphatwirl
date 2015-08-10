
##### How to update the docs

In the top directory of AlphaTwirl (one directory up from this directory):

    rm docs/AlphaTwirl.*.rst
    sphinx-apidoc -F -A "Tai Sakuma" -V "0.7" -R "0.7.x" -o docs/ AlphaTwirl/

Edit conf.py to increment the version number

Make

    $ make html

The entry page will be at

 * open _build/html/index.html
