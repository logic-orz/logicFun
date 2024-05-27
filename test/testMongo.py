from cttqFuncs.conn.mongoFunc import MongoDB
from cttqFuncs.conn import DbConfig


mongo = MongoDB(DbConfig(host='rpa-data.cttq.com', port=27017, db='test'))

print(mongo.tables())
print(mongo.query("coll1", {}))
