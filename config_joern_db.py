# 作者：cl
# 时间：2019-12-11
# 功能：以.joernIndex_xxx作为参数，修改jeorn，neo4j配置文件中的数据库位置，
# 实现自动更换源代码库。
import sys
filename = sys.argv[1]
joern_config_file = "/home/ccc/program/joern-0.3.1/joern.conf"
neo4j_config_file = "/home/ccc/program/neo4j-community-2.1.5/conf/neo4j-server.properties"
f = open(joern_config_file,'r+')
flines = f.readlines()
f.close()
for i in range(0,len(flines)):
    if "index = " in flines[i]:
        flines[i] = "index = %s\n"%filename
        break
f = open(joern_config_file,'w+')
f.writelines(flines)
f.close()

f = open(neo4j_config_file,'r+')
flines = f.readlines()
f.close()
for i in range(0,len(flines)):
    if "org.neo4j.server.database.location=/home/ccc/program/joern-0.3.1/" in flines[i]:
        flines[i] = "org.neo4j.server.database.location=/home/ccc/program/joern-0.3.1/%s\n"%filename
        break
f = open(neo4j_config_file,'w+')
f.writelines(flines)
f.close()