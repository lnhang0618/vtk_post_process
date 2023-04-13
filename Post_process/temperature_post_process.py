'''
Created on April 11th 2023

@author:LeonRho
'''
# Temperature_post_process.py
import logging
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from matplotlib import cm
from .post_process_base import PostProcessBase

logging.basicConfig(filename='post_process.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


class Temperature_Post_Process(PostProcessBase):
    def __init__(self, vtk_file, x_range, y_range, cmap='cividis',grids='off',normalization='off'):
        super().__init__(vtk_file)
        self.x_range = x_range
        self.y_range = y_range
        self.cmap = cmap
        self.grids=grids
        self.normalization = normalization
        
        #statistics:
        logging.info("Input parameters:")
        logging.info("VTK file: %s", self.vtk_file)
        logging.info("x_range: %s", self.x_range)
        logging.info("y_range: %s", self.y_range)
        logging.info("cmap: %s", self.cmap)
        logging.info("grids: %s", self.grids)
        logging.info("normalization: %s", self.normalization)
        
                # 提取温度数据
        T = self.get_field("T")

        # 获取网格的点坐标
        points = self.get_points()
        
        # 提取x, y坐标和温度数据
        x = points[:, 0]
        y = points[:, 2]
        T = T
        
        #statistics:
        logging.info("\nTemperature data statistics:")
        logging.info("Min temperature: %s", np.min(T))
        logging.info("Max temperature: %s", np.max(T))
        logging.info("Mean temperature: %s", np.mean(T))

        #归一化输入坐标
        if self.normalization =='on':
            self.x_max,self.x_min=np.max(x),np.min(x)
            self.y_max,self.y_min=np.max(y),np.min(y)
            # 将x和y归一化
            x = (x - self.x_min) / (self.x_max - self.x_min)
            y = (y - self.y_min) / (self.y_max - self.y_min)
            
            #statistics
            logging.info("\nNormalized coordinates range:")
            logging.info("Min normalized x: %s", np.min(x))
            logging.info("Max normalized x: %s", np.max(x))
            logging.info("Min normalized y: %s", np.min(y))
            logging.info("Max normalized y: %s", np.max(y))
        
        # 筛选需要展示的区域
        indices = np.where((self.x_range[0] < x) & (x < self.x_range[1]) 
                           & (self.y_range[0] < y) & (y < self.y_range[1]))

        # 提取对应的点坐标和温度数据
        filtered_points = points[indices]
        self.filtered_T = T[indices]
        
        #statistics
        logging.info("\nFiltered data points:")
        logging.info("Number of filtered points: %s", len(filtered_points))
        
        # 提取x, y坐标
        self.filtered_x = filtered_points[:, 0]
        self.filtered_y = filtered_points[:, 2]
        
                #归一化作图坐标
        if self.normalization == "on":

            self.filtered_x = (self.filtered_x - self.x_min) / (self.x_max - self.x_min)
            self.filtered_y = (self.filtered_y - self.y_min) / (self.y_max - self.y_min)

    def plot_temperature_contour(self):
        
        # 创建一个新的图形
        plt.figure()

        # 使用三角剖分方法绘制填充的等高线图
        contour = plt.tricontourf(self.filtered_x, self.filtered_y, self.filtered_T, cmap=self.cmap,levels=12)
        
            # 绘制网格线
        if self.grids == 'on':
            for x_grid in self.filtered_x:
                plt.axvline(x=x_grid, color="black", linewidth=0.5, linestyle='-', alpha=0.3)
            for y_grid in self.filtered_y:
                plt.axhline(y=y_grid, color="black", linewidth=0.5, linestyle='-', alpha=0.3)
        
        
        # 为x和y轴添加标签
        plt.xlabel('x')
        plt.ylabel('y')

        # 添加图标题
        plt.title('Temperature T in the region where {0} < x < {1} and {2} < y < {3}'.format(*self.x_range, *self.y_range), fontsize=10)

        # 添加颜色条
        plt.colorbar(label='T', fraction=0.05, pad=0.1)

        # 显示网格线
        plt.grid()

        # 显示图形
        plt.show()
