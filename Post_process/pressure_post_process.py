'''
Created on April 11th 2023

@author:LeonRho
'''
import logging
from .post_process_base import PostProcessBase
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri

logging.basicConfig(filename='post_process.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

class Pressure_Post_Process(PostProcessBase):
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
        
        # 获取网格的点坐标
        super().get_points()
        
        # 提取压力数据
        pressure = self.get_field("p")
        self.pressure = pressure
        
        #statistics:
        logging.info("\nPressure data statistics:")
        logging.info("Min pressure magnitude: %s", np.min(self.pressure))
        logging.info("Max pressure magnitude: %s", np.max(self.pressure))
        logging.info("Mean pressure magnitude: %s", np.mean(self.pressure))

        
        #归一化输入坐标
        if self.normalization =='on':
            super().normalization()
            
    def _draw_grid_lines(self):
        cell_points_ids = self.get_cell_points_ids()        
    
    def plot_pressure_contour(self):
        
        # 创建一个新的图形和一个轴对象
        fig, ax = plt.subplots()
        
        # 创建一个Triangulation对象
        triangulation = tri.Triangulation(self.x, self.y, self.triangulated_cells)

        # 使用三角剖分方法绘制填充的压力等高线图
        contour = plt.tricontourf(triangulation, self.pressure, cmap=self.cmap,levels=12)


        # 为x和y轴添加标签
        ax.set_xlabel('x')
        ax.set_ylabel('y')
    
        # 设置x, y轴的显示范围
        ax.set_xlim(self.x_range)
        ax.set_ylim(self.y_range)

        # 添加图标题
        ax.set_title('Pressure in the region where {0} < x < {1} and {2} < y < {3}'.format(*self.x_range, *self.y_range),fontsize=10)

        # 添加颜色条
        plt.colorbar(contour, ax=ax,label='Pressure', fraction=0.05, pad=0.1)


        # 显示网格线
        if self.meshes == 'on':
            super().draw_xy_meshes(ax)
        else:
            ax.grid()

        # 显示图形
        plt.show()
