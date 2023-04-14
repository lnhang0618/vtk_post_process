# vorticity_post_process.py
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

class Vorticity_Post_Process(PostProcessBase):
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
        
        # 提取涡量数据
        vorticity = self.get_field("vorticity")
        self.vorticity_z = vorticity[:, self.axis_map['z']]
        
        #statistics:
        logging.info("\nVorticity data statistics:")
        logging.info("Min vorticity magnitude: %s", np.min(self.vorticity_z))
        logging.info("Max vorticity magnitude: %s", np.max(self.vorticity_z))
        logging.info("Mean vorticity magnitude:%s", np.mean(self.vorticity_z))
        
        #归一化输入坐标
        if self.normalization =='on':
            super().normalization()
    
            

    def plot_vorticity_contour(self):

        # 创建一个新的图形和一个轴对象
        fig, ax = plt.subplots()
        
        # 创建一个Triangulation对象
        triangulation = tri.Triangulation(self.x, self.y, self.triangulated_cells)

        
        # 使用三角剖分方法绘制填充的涡量等高线图
        contour = ax.tricontourf(triangulation, self.vorticity_z, cmap=self.cmap,levels=12)

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
        ax.set_title('Vorticity in the region where {0} < x < {1} and {2} < y < {3}'.format(*self.x_range, *self.y_range),fontsize=10)

        # 添加颜色条
        plt.colorbar(contour,ax=ax,label='Vorticity', fraction=0.05, pad=0.1)
        
        #绘制计算网格
        if self.meshes == 'on':
            super().draw_xy_meshes(ax)
        else:
            ax.grid()


        # 显示图形
        plt.show()
