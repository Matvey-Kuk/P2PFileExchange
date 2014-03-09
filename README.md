Дамы и господа, это наш священый курсач!

Когда-то мы даже напишем автоматизированные тесты... [![Build Status](https://travis-ci.org/Matvey-Kuk/network.png?branch=master)](https://travis-ci.org/Matvey-Kuk/network)

Запуск:
------------
Уже что-то можно запустить, но толку с этого мало:

1-я копия: python3 Main.py -port 1235

2-я копия: python3 Main.py -peer localhost:1235

Есть даже help: python3 Main.py -h

Материалы:
------------

Книжка на русском (В нашем случае можно читать до 3-й главы включительно): http://git-scm.com/book/ru

Игра по ветвлению, обязательна к прохождению: http://pcottle.github.io/learnGitBranching/

Список используемых нами команд:
------------

Инициализировать репозиторий: git init

Установить свой ник: git config --global user.name "Billy Everyteen"

Установить свою почту (она должна совпадать с указанной здесь, чтобы гитхаб вас опознал: https://github.com/settings/emails): git config --global user.email "me@here.com"

Добавить удаленный репозиторий: git remote add origin git@github.com:Matvey-Kuk/network.git

Забрать из удаленного мастера: git pull origin master

Узнать, какие файлы будут закоммичены: git add --all (вместо --all можно указать конкретные файлы)

Узнать, какие файлы будут закоммичены: git status

Закоммитить изменения: git commit -am "I've made something really strange"

Посмотреть последние коммиты: git log

Залить на удаленный мастер: git push origin master

Узнать, в какой мы ветке: git branch

Создать новую ветку: git branch newBranchName

Переключиться на другую ветку: git checkout someBranchName

Слить с текущей веткой, ветку someBranch: git merge someBranch

Python:
------------

Поставить интерпритатор, обязательно версии 3.3, или новее: http://www.python.org/downloads/

Поставить кошерный редактор (Обязательно Community Edition): http://www.jetbrains.com/pycharm/download/

RSA-библиотека:
-------------
Необходимо добавить библиотеку "rsa" в питон(папка rsa-3.1.4): python setup.py install 

Домашняя страница: https://pypi.python.org/pypi/rsa