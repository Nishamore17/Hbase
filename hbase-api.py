import happybase
connection = happybase.Connection('10.1.1.204',9090,table_prefix='myproject12')


connection.create_table(
    'mycustomer',
    {'cf1': dict(max_versions=10),
     'cf2': dict(max_versions=1, block_cache_enabled=False),
     'cf3': dict(),  # use defaults
    }
)

print(connection.tables())
table = connection.table('mycustomer')

for i in range(20):
	table.put(b'Cust-%d'%(i), {b'cf1:name': b'ABC%d'%(i),b'cf1:orderid': b'%d'%(i)})



Retrieving rows with row-key
----------------------------
row = table.row(b'Cust-15')
print(row)
print(row[b'cf1:name'])



Retreiving with only column family
----------------------------------

row = table.row(b'Cust-15', columns=[b'cf1'])
print(row)

Selecting specific columns
--------------------------
row = table.row(b'Cust-15', columns=[b'cf1:name', b'cf1:orderid'])
print(row[b'cf1:name'])
print(row[b'cf1:orderid'])

Retrieving cell data with time stamp
------------------------------------

row = table.row(b'Cust-15', columns=[b'cf1:name'], include_timestamp=True)
value, timestamp = row[b'cf1:name']


Scanning the rows
------------------

for key, data in table.scan():
  print(key, data)

for key, data in table.scan(row_start=b'Cust-2'):
    print(key, data)

for key, data in table.scan(row_stop=b'Cust-15'):
    print(key, data)

for key, data in table.scan(row_start=b'Cust-1', row_stop=b'Cust-15'):
    print(key, data)

for key, data in table.scan(row_prefix=b'Cust-'):
    print(key, data)

Deleting data
-------------

table.delete(b'cust-4')

table.delete(b'Cust-13', columns=[b'cf1:name', b'cf1:orderid'])


Performing Batch operations
---------------------------

b = table.batch()
b.put(b'Cust-11', {b'cf1:name': b'Changed', b'cf1:col2': b'newval'})
b.put(b'Cust-22', {b'cf1:orderdate': b'12/12/2023', b'cf1:status': b'returned'})
b.put(b'Cust-23', {b'cf1:name': b'Ravi23', b'cf1:orderid': b'23'})
b.delete(b'Cust-4')
b.send()
