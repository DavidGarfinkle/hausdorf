

Running
-------

Install docker and docker-compose, and configure your user to have permissions to them.
Then,

```
docker-compose up
```

If this worked then http://localhost:80 should return some [SWAGGER]() metadata.
And you can access the DB like this:

```
PGHOST=localhost PGUSER=postgres psql 
```

To fill the database:

```
# this will take quite a while; but it can run in parallel with other work
# it's also not necessary to run this to completion to have a useful dataset
find testdata/palestrina_masses/mid -type f | while read piece; do
  PGHOST=localhost PGUSER=postgres testdata/insert_hausdorf.sh "$piece";
done
```

To boot the front-end:

Install python's virtualenv, python3, and node and npm, then

```
(cd webclient; npm install; npx webpack-cli --bundle --mode=development)
virtualenv .venv
. .venv/bin/activate
pip install -r requirements.txt
FLASK_APP=smrpy/app.py PGHOST=localhost PGUSER=postgres flask run
```

