import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
class plot:

    def plot(self,xd,yd,filename):
        xData = xd
        yData1 = yd
        #yData2 = np.arange(15,61,5)
        plt.figure(num=1, figsize=(8,6))
        plt.title('Plot 1', size=14)
        plt.xlabel('x-axis', size=14)
        plt.ylabel('y-axis', size=14)
        plt.plot(xData, yData1, color='b', linestyle='--', marker='o', label='y1 data')
        #plt.plot(xData, yData2, color='r', linestyle='-', label='y2 data')
        plt.legend(loc='upper left')
        plt.savefig(filename, format='png')

    def plot3d(self,xd,yd,zd,filename):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_trisurf(xd,yd,zd)
        plt.savefig(filename,format='png')