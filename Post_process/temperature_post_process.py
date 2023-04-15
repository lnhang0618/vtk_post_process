'''
Created on April 11th 2023

@author:LeonRho
'''
# Temperature_post_process.py
import logging
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri
from .post_process_base import PostProcessBase

logging.basicConfig(filename='post_process.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


class Temperature_Post_Process(PostProcessBase):
    def __init__(self, vtk_file, x_range, y_range, cmap='cividis',meshes='off',normalization='off',**kwargs):
        super().__init__(vtk_file,**kwargs)
        self.x_range = x_range
        self.y_range = y_range
        self.cmap = cmap
        self.meshes=meshes
        self.normalization = normalization
        
        #statistics:
        logging.info("Input parameters:")
        logging.info("VTK file: %s", self.vtk_file)
        logging.info("x_range: %s", self.x_range)
        logging.info("y_range: %s", self.y_range)
        logging.info("cmap: %s", self.cmap)
        logging.info("grids: %s", self.meshes)
        logging.info("normalization: %s", self.normalization)

        
        # 提取温度数据
        T = self.get_field("T")
        self.T = T

        #statistics:
        logging.info("\nTemperature data statistics:")
        logging.info("Min temperature: %s", np.min(self.T))
        logging.info("Max temperature: %s", np.max(self.T))
        logging.info("Mean temperature: %s", np.mean(self.T))

        #归一化输入坐标
        if self.normalization =='on':
            super().normalization()
            

    def plot_temperature_contour(self):
        
        # 创建一个新的图形和一个轴对象
        fig, ax = plt.subplots()
        
        # 创建一个Triangulation对象
        triangulation = tri.Triangulation(self.x, self.y, self.triangulated_cells)
    

        # 使用三角剖分方法绘制填充的等高线图
        contour = ax.tricontourf(triangulation, self.T, cmap=self.cmap,levels=12)
        
        #绘制计算网格
        if self.meshes == 'on':
            super().draw_xy_meshes(ax)
        else:
            ax.grid()
        
        
        # 为x和y轴添加标签
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        
        # 设置x, y轴的显示范围
        ax.set_xlim(self.x_range)
        ax.set_ylim(self.y_range)
        

        # 添加图标题
        ax.set_title('Temperature T in the region where {0} < x < {1} and {2} < y < {3}'.format(*self.x_range, *self.y_range), fontsize=10)

        # 添加颜色条
        fig.colorbar(contour,ax=ax,label='T', fraction=0.05, pad=0.1)


        # 显示图形
        plt.show()
