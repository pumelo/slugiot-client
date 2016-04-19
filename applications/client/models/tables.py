#########################################################################
## Define your tables below, for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

## These tables are synched "up" from the clients to the server.

from datetime import datetime

############### Procedure Harness Table ###############

db.define_table('procedure',
                Field('proc_id', 'bigint', required=True),  # key
                Field('user_id', 'string', required=True),
                Field('last_update', 'datetime', required=True),
                Field('proc_name', 'string'),  # Name of procedure
                Field('proc_data', 'text', required=True),  # Actual code for procedure - is check IS_LENGTH(65536) ok?
                # Otherwise use string and specifiy larger length
                )

############### Procedure API Tables #################


db.define_table('logs',
                Field('time_stamp', 'datetime', default=datetime.datetime.utcnow()),
                Field('modulename'),
                Field('log_level', 'integer'),  # int, 0 = most important.
                Field('log_message', 'text')
                )

db.define_table('outputs',
                Field('time_stamp', 'datetime', default=datetime.datetime.utcnow()),
                Field('modulename'),
                Field('name'),  # Name of variable
                Field('output_value', 'text'),  # Json, short please
                Field('tag')
                )

db.define_table('module_values',
                Field('time_stamp', 'datetime', default=datetime.datetime.utcnow()),
                Field('modulename'),
                Field('name'),  # Name of variable
                Field('module_value', 'text'),  # Json, short please
                )


