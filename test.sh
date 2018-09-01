pip freeze
nosetests --with-coverage --cover-package youtube2mp3 --cover-package tests tests  docs/source youtube2mp3 && flake8 . --exclude=.moban.d,docs --builtins=unicode,xrange,long
