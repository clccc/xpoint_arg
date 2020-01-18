#coding:utf-8
#---------------------------
#code by Chenlin 2016-03-26
#uses pickle to save struct data to a file or load stract data from a file
#---------------------------


import pickle

class ObjDataAndBinFile:
    def objdata2file(self,objData,filename):
        output = open(filename,'wb')
        # Pickle dictionary using protocol 0.
        #pickle.dump(objData, output)

        # Pickle the list using the highest protocol available.
        pickle.dump(objData, output, -1)
        output.close()

        #使用pickle模块从文件中重构python对象
    def binfile2objdata(self, filename):
        pkl_file = open(filename, 'rb')
        objData = pickle.load(pkl_file)
        pkl_file.close()
        return objData
