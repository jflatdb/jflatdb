from jflatdb.cli import CLI #New
from jflatdb.database import Database

db = Database("db.json", password="1234")

cli = CLI(db)
cli.run()