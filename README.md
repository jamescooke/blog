Getting up and running
----------------------

Pull down the repo and build the virtualenv.

    $ git clone git@github.com:jamescooke/blog
    $ virtualenv env
    $ source env/bin/activate
    $ pip install -r requirements.txt


Writing and testing
-------------------

While **still in the virtualenv**, build the HTML and run dev server.

    $ mkdir output
    $ make html
    $ make devserver

Hit localhost - http://localhost:8000/


Publishing
----------

Commit content and images as required, push to master. Then...

    $ make publish
    $ make github

All good in the hood.


License
-------

Content in this repository is covered by the same license as the content when
published in the blog at [jamescooke.info](http://jamescooke.info/).

Licensed under [Creative Commons Attribution-ShareAlike 3.0 Unported
License](http://creativecommons.org/licenses/by-sa/3.0/deed.en_GB).
