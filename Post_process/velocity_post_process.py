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

class Velocity_Post_Process(PostProcessBase):
    def __init__(self, vtk_file, x_range, y_range, cmap='cividis',meshes='off',normalization='off',**kwargs):
        super().__init__(vtk_file,**kwargs)
        self.x_range = x_range
        self.y_range = y_range
        self.cmap = cmap
        self.meshes=meshes
        self.normalization=normalization
                
        #定义计算方向
        self.component = kwargs.get('component')
        self.with_vector=kwargs.get('with_vector')
        
        #statistics:
        logging.info("Input parameters:")
        logging.info("x_range: %s", self.x_range)
        logging.info("y_range: %s", self.y_range)
        logging.info("cmap: %s", self.cmap)
        logging.info("grids: %s", self.meshes)
        logging.info("normalization: %s", self.normalization)

        # 获取网格的点坐标
        super().get_points()
        
        # 提取速度数据
        velocity = self.get_field("U")
        self.velocity_x = velocity[:, self.axis_map['x']]
        self.velocity_y = velocity[:, self.axis_map['y']]
        self.velocity_all = np.sqrt(self.velocity_x**2*self.velocity_y**2)
        
        #statistics:
        logging.info("\nVelocity_{} data statistics:".format(self.component))
        logging.info("Min velocity_x: %s", np.min(self.velocity_x))
        logging.info("Max velocity_x: %s", np.max(self.velocity_x))
        logging.info("Mean velocity_x: %s", np.mean(self.velocity_x))
        logging.info("Min velocity_x: %s", np.min(self.velocity_y))
        logging.info("Max velocity_x: %s", np.max(self.velocity_y))
        logging.info("Mean velocity_x: %s", np.mean(self.velocity_y))

        
        #归一化输入坐标
        if self.normalization =='on':
            super().normalization()

       

    def plot_velocity_contour(self):
    
        # 创建一个新的图形和一个轴对象
        fig, ax = plt.subplots()
        
        # 创建一个Triangulation对象
        triangulation = tri.Triangulation(self.x, self.y, self.triangulated_cells)
    
        # 使用三角剖分方法绘制填充的速度等高线图
        if self.component=='x':
            contour = ax.tricontourf(triangulation, self.velocity_x, cmap=self.cmap, levels=12)
        elif self.component == 'y':
            contour = ax.tricontourf(triangulation, self.velocity_y, cmap=self.cmap, levels=12)
        elif self.component == 'all':
            contour = ax.tricontourf(triangulation, self.velocity_all, cmap=self.cmap, levels=12)
            if self.with_vector=='on':
                # 绘制矢量图
                ax.quiver(self.x, self.y, self.velocity_x,self.velocity_y)
                
        else:
            raise ValueError("Invalid component. Valid options are 'x', 'y', and 'all'.")
        
        # 为x和y轴添加标签
        ax.set_xlabel('x')
        ax.set_ylabel('y')
    
        # 设置x, y轴的显示范围
        ax.set_xlim(self.x_range)
        ax.set_ylim(self.y_range)

        # 添加图标题
        ax.set_title('Velocity_{} in the region where {} < x < {} and {} < y < {}'.format(self.component, *self.x_range, *self.y_range), fontsize=10)

        # 添加颜色条
        fig.colorbar(contour, ax=ax, label='Velocity_{}'.format(self.component), fraction=0.05, pad=0.1)

        # 显示网格线
        if self.meshes == 'on':
            super().draw_xy_meshes(ax)
        else:
            ax.grid()

        # 显示图形
        plt.show()
