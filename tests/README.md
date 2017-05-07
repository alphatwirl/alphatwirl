
##### How to run the unit tests.

###### Run all tests

The arguments depend on where you are.

from this direcotry:
```
python -m unittest discover -s ./unit/ -t ../
```

from the top directory of AlphaTwirl (one directory up from this directory):
```
python -m unittest discover -s ./tests/unit/ 
```

from further up:
```
python -m unittest discover -s ./AlphaTwirl/tests/unit -t ./AlphaTwirl/
```

###### Run a particular test

from the top directory of AlphaTwirl (one directory up from this directory):
```
python -m unittest tests.unit.examples.test_test_example.TestExample1.test_example
```
