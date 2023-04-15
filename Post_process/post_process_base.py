import logging

from Utils import vtk_mesh_utils
from Utils import transform_utils
from Utils import drawing_utils

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
    
        self.prepare_vtk()
        self.z_value = kwargs.get('z_value', None)
        self.prepare_sort_xy_meshes_input()
        self.print_info()

    #读取VTK文件
    def prepare_vtk(self):
        self.computed_grid=vtk_mesh_utils._read_vtk_file(self.vtk_file)
        self.points,self.x,self.y,self.z=\
        vtk_mesh_utils.get_points(self.computed_grid,self.axis_map)
    
    #读取场信息
    def get_field(self, field_name):
        return vtk_mesh_utils._get_field(field_name,self.computed_grid)
    
    #归一化
    def normalization(self):
        self.x,self.y = transform_utils.normalization(self.x,self.y)
    
    
    #计算网格点顺序
    def prepare_sort_xy_meshes_input(self):
        cell_points_ids=vtk_mesh_utils.get_cell_points_ids(self.computed_grid)
        xy_cells=vtk_mesh_utils.get_xy_cells(self.z_value,cell_points_ids,self.z)
        self.sorted_cell,self.triangulated_cells=vtk_mesh_utils.sort_xy_meshes(xy_cells,self.x,self.y)
    
    def draw_xy_meshes(self,ax):
        drawing_utils.draw_xy_meshes(ax,self.sorted_cell,self.x,self.y)
        
    #statistics
    def print_info(self):
        logging.info('\nBasic information of VTK')
        logging.info(f"VTK file: {self.vtk_file}")
        logging.info(f"Number of points: {self.computed_grid.GetNumberOfPoints()}")
        logging.info(f"Number of cells: {self.computed_grid.GetNumberOfCells()}")
        logging.info(f"axis_map:{self.axis_map}")
        
        logging.info("Available data fields:")
        point_data = self.computed_grid.GetPointData()
        for i in range(point_data.GetNumberOfArrays()):
            logging.info(f"- {point_data.GetArrayName(i)}")