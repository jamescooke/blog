Getting up and running
----------------------

Pull down the repo and build the virtualenv.

    $ git clone git@github.com:jamescooke/blog
    $ virtualenv --python /home/james/active/py/bin/bin/python env
    $ source env/bin/activate
    $ pip install -r requirements.txt


Writing and testing
-------------------

While **still in the virtualenv**, build the HTML and run dev server.

    $ mkdir output
    $ make html
    $ make devserver


Publishing
----------

Commit content and images as required, push to master. Then...

    $ make publish
    $ make github

All good in the hood.
