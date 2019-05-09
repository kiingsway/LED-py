d={}
for x in range(1,10):
        d["string{0}".format(x)]="Hello"

print (d['string5'])

if d['string5'].endswith('o'):
	print('hmmmmmmmmmmm')