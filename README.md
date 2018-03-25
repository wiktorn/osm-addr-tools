== Installation ==

On Ubuntu (17.10):

```commandline
$ apt-get install libspatialindex4v5 libspatialindex-c4v5
$ python3 -m venv venv
$ venv/bin/pip install -r requirements.txt
$ git submodule init
$ git submodule update
```

Now you can run:
```commandline
$ venv/bin/python merger.py --gugik --terc 0601032
```

To update:
```commandline
$ git pull
$ git submodule update --remote
```

