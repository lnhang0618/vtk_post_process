import logging
import vtk
from vtk.util import numpy_support
import numpy as np
import matplotlib.pyplot as plt

logging.basicConfig(filename='post_process.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

class PostProcessBase:
    def __init__(self, vtk_file,axis_map=None,**kwargs):
        self.vtk_file = vtk_file
        
        if axis_map is None:
            self.axis_map={'x':0,'y':1,'z':2}
        else:
            self.axis_map = axis_map
            assert len(self.axis_map) == 3 and 'x' in self.axis_map and 'y' in self.axis_map and 'z' in self.axis_map, \
                "Invalid axis_map. Must be a dictionary containing 'x', 'y', and 'z' keys."
    
        self._read_vtk_file()
        self.print_info()
        self.z_value = kwargs.get('z_value', None)
    
    #读取VTK文件
    def _read_vtk_file(self):
        reader = vtk.vtkGenericDataObjectReader()
        reader.SetFileName(self.vtk_file)
        reader.Update()
        self.unstructured_grid = reader.GetOutput()

    #读取场信息
    def get_field(self, field_name):
        return numpy_support.vtk_to_numpy(self.unstructured_grid.GetPointData().GetArray(field_name))
    
    #读取点坐标
    def get_points(self):
        self.points=numpy_support.vtk_to_numpy(self.unstructured_grid.GetPoints().GetData())
        self.x = self.points[:, self.axis_map['x']]
        self.y = self.points[:, self.axis_map['y']]
        self.z = self.points[:, self.axis_map['z']]
    
    #读取单元格信息
    def get_cell_points_ids(self):
        cell_array = self.unstructured_grid.GetCells()
        cell_points_ids = []
        id_list = vtk.vtkIdList()

        cell_array.InitTraversal()
        while cell_array.GetNextCell(id_list):
            ids = [id_list.GetId(j) for j in range(id_list.GetNumberOfIds())]
            cell_points_ids.append(ids)

        return cell_points_ids
    
    #归一化
    def normalization(self):
        x_max,x_min=np.max(self.x),np.min(self.x)
        y_max,y_min=np.max(self.y),np.min(self.y)
        # 将x和y归一化
        self.x = (self.x - x_min) / (x_max - x_min)
        self.y = (self.y - y_min) / (y_max - y_min)
        
        #statistics:
        logging.info("\nNormalized coordinates range:")
        logging.info("Min normalized x: %s", np.min(self.x))
        logging.info("Max normalized x: %s", np.max(self.x))
        logging.info("Min normalized y: %s", np.min(self.y))
        logging.info("Max normalized y: %s", np.max(self.y))
        
    #读取单元格信息
    def get_cell_points_ids(self):
        cell_array = self.unstructured_grid.GetCells()
        cell_points_ids = []
        id_list = vtk.vtkIdList()

        cell_array.InitTraversal()
        while cell_array.GetNextCell(id_list):
            ids = [id_list.GetId(j) for j in range(id_list.GetNumberOfIds())]
            cell_points_ids.append(ids)

        return cell_points_ids
    
    #提取xy平面网格
    def get_xy_cells(self):
        if self.z_value == None:
            self.z_value = np.max(self.z)
            logging.info('thez_value of cross section:%s:',{self.z_value})
        
        cell_points_ids=self.get_cell_points_ids()
        xy_cells=[]
        
        for cell in cell_points_ids:
            filtered_cell = [vertex_id for vertex_id in cell if abs(self.z[vertex_id]) == self.z_value]
            xy_cells.append(filtered_cell)
        
        return xy_cells
    
    #绘画计算网格
    def draw_xy_meshes(self,ax):
        xy_cells=self.get_xy_cells()

        for cell in xy_cells:
            # 计算每个点相对于单元格质心的角度(极角)
            centroid = np.mean([[self.x[vertex_id], self.y[vertex_id]] for vertex_id in cell], axis=0)
            angles = [np.arctan2(self.y[vertex_id] - centroid[1], self.x[vertex_id] - centroid[0]) for vertex_id in cell]
            # 根据角度对点进行排序
            sorted_cell = [vertex_id for _, vertex_id in sorted(zip(angles, cell))]

            # 连接每个单元格内的点
            for i in range(len(sorted_cell)):
                point1 = sorted_cell[i]
                point2 = sorted_cell[(i + 1) % len(sorted_cell)]
                x_coords = [self.x[point1], self.x[point2]]
                y_coords = [self.y[point1], self.y[point2]]
                ax.plot(x_coords, y_coords, 'k-', linewidth=0.3)

    
    #statistics
    def print_info(self):
        logging.info(f"VTK file: {self.vtk_file}")
        logging.info(f"Number of points: {self.unstructured_grid.GetNumberOfPoints()}")
        logging.info(f"Number of cells: {self.unstructured_grid.GetNumberOfCells()}")
        logging.info(f"axis_map:{self.axis_map}")
        
        logging.info("Available data fields:")
        point_data = self.unstructured_grid.GetPointData()
        for i in range(point_data.GetNumberOfArrays()):
            logging.info(f"- {point_data.GetArrayName(i)}")
        
            