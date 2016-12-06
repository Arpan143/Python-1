f = open('E:\\1.exe', 'rb')
f.seek(0, 0)
f.close()
pe_str = {'e_magic': 2, 'e_cblp': 2, 'e_cp': 2}
for i in pe_str:
    byte = f.read(pe_str.get(i))
    hex_str = "%s" % byte.encode('hex')
    pe_str[i] = hex_str
print pe_str
