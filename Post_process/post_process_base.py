import logging
import vtk
from vtk.util import numpy_support
import numpy as np

logging.basicConfig(filename='post_process.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

class PostProcessBase:
    def __init__(self, vtk_file):
        self.vtk_file = vtk_file
        self._read_vtk_file()
        self.print_info()
    
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
        points=numpy_support.vtk_to_numpy(self.unstructured_grid.GetPoints().GetData())
        self.x = points[:, 0]
        self.y = points[:, 2]
    
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
    



    def print_info(self):
        logging.info(f"VTK file: {self.vtk_file}")
        logging.info(f"Number of points: {self.unstructured_grid.GetNumberOfPoints()}")
        logging.info(f"Number of cells: {self.unstructured_grid.GetNumberOfCells()}")

        logging.info("Available data fields:")
        point_data = self.unstructured_grid.GetPointData()
        for i in range(point_data.GetNumberOfArrays()):
            logging.info(f"- {point_data.GetArrayName(i)}")