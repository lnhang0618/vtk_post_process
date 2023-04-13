# vorticity_post_process.py
'''
Created on April 11th 2023

@author:LeonRho
'''
import logging
from .post_process_base import PostProcessBase
import numpy as np
import matplotlib.pyplot as plt

logging.basicConfig(filename='post_process.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

class Vorticity_Post_Process(PostProcessBase):
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
        
                
        # 获取网格的点坐标
        super().get_points()
        
        # 提取涡量数据
        vorticity = self.get_field("vorticity")
        self.vorticity_z = vorticity[:, 1]
        
        #statistics:
        logging.info("\nVorticity data statistics:")
        logging.info("Min vorticity magnitude: %s", np.min(self.vorticity_z))
        logging.info("Max vorticity magnitude: %s", np.max(self.vorticity_z))
        logging.info("Mean vorticity magnitude:%s", np.mean(self.vorticity_z))
        
        #归一化输入坐标
        if self.normalization =='on':
            super().normalization()
    
    def _draw_grid_lines(self):
        cell_points = self.get_cell_points_ids()
        print(cell_points)
            

    def plot_vorticity_contour(self):

        # 创建一个新的图形
        plt.figure()

       # 绘制网格线
        if self.grids == 'on':
           self._draw_grid_lines()
        
        # 使用三角剖分方法绘制填充的涡量等高线图
        contour = plt.tricontourf(self.x,self.y, self.vorticity_z, cmap=self.cmap,levels=12)

        # 为x和y轴添加标签
        plt.xlabel('x')
        plt.ylabel('y')
        
        # 设置x, y轴的显示范围
        plt.xlim(self.x_range)
        plt.ylim(self.y_range)

        # 添加图标题
        plt.title('Vorticity in the region where {0} < x < {1} and {2} < y < {3}'.format(*self.x_range, *self.y_range),fontsize=10)

        # 添加颜色条
        plt.colorbar(label='Vorticity', fraction=0.05, pad=0.1)

        # 显示网格线
        plt.grid()

        # 显示图形
        plt.show()
