from model import db, Message


db.connect()
db.drop_tables([Message])
db.create_tables([Message])
