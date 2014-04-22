[![Build Status](https://travis-ci.org/Matvey-Kuk/network.png?branch=master)](https://travis-ci.org/Matvey-Kuk/network)

К чему мы стремимся:
------------
Распределенное децентрализованное хранилише файлов для малых рабочих групп с версионированием.
Позволяет пользователю зарегистрироваться в децентрализованной базе данных,
организовать в рабочую группу из нескольких пользователей и вести совместную работу над приватными файлами в git-подобном стиле.

Запуск:
------------

python3 Main.py -h

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

