'''
Created on Apr 15th 2023

@author:lnhang

'''
#Utils/vtk_utils.py

import vtk
from vtk.util import numpy_support
import numpy as np
import logging


#读取VTK文件
def _read_vtk_file(vtk_file):
    reader = vtk.vtkGenericDataObjectReader()
    reader.SetFileName(vtk_file)
    reader.Update()
    computed_grid = reader.GetOutput()
    return computed_grid

#读取场信息
def _get_field(field_name,computed_grid):
    return numpy_support.vtk_to_numpy(computed_grid.GetPointData().GetArray(field_name))

#读取点坐标
def get_points(computed_grid,axis_map):
    points=numpy_support.vtk_to_numpy(computed_grid.GetPoints().GetData())
    x = points[:, axis_map['x']]
    y = points[:, axis_map['y']]
    z = points[:, axis_map['z']]
    return points,x,y,z

#读取单元格信息
def get_cell_points_ids(computed_grid):
    cell_array = computed_grid.GetCells()
    cell_points_ids = []
    id_list = vtk.vtkIdList()

    cell_array.InitTraversal()
    while cell_array.GetNextCell(id_list):
        ids = [id_list.GetId(j) for j in range(id_list.GetNumberOfIds())]
        cell_points_ids.append(ids)

    logging.info('\n Information of get_cell_points_ids')
    logging.info('number of cell_points_ids :%s',{len(cell_points_ids)})
    
    return cell_points_ids

#提取xy平面单元格
def get_xy_cells(z_value,cell_points_ids,z):
    if z_value == None:
        z_value = np.max(z)      
    else:
        z_value=np.float32(z_value)

    xy_cells=[]
        
    for cell in cell_points_ids:
        filtered_cell = [vertex_id for vertex_id in cell if z[vertex_id] == z_value]
        xy_cells.append(filtered_cell)
    
    logging.info('\nInformation of get_xy_cells')
    logging.info('number of xy_cells :%s',{len(xy_cells)})
    
    return xy_cells

#计算网格点顺序
def sort_xy_meshes(xy_cells,x,y):
    sorted_cell=[]
    triangulated_cells = []

    for cell in xy_cells:
        # 计算每个点相对于单元格质心的角度(极角)
        centroid = np.mean([[x[vertex_id], y[vertex_id]] for vertex_id in cell], axis=0)
        angles = [np.arctan2(y[vertex_id] - centroid[1], x[vertex_id] - centroid[0]) for vertex_id in cell]
        # 根据角度对点进行排序
        tmp = [vertex_id for _, vertex_id in sorted(zip(angles, cell))]
        sorted_cell.append(tmp)
            
        # 对于四边形，将其划分为两个三角形
        if len(tmp) == 4:
            triangulated_cells.append([tmp[0], tmp[1], tmp[2]])
            triangulated_cells.append([tmp[2], tmp[3], tmp[0]])
        # 对于三角形，直接添加到triangulated_cells中
        elif len(tmp) == 3:
            triangulated_cells.append(tmp)
        
    logging.info('\nInformation about sort_xy_meshed')
    logging.info('number of cells in tmp:%s',{len(tmp)})
    logging.info('number of sorted_cell:%s',{len(sorted_cell)})
    logging.info('number of trianglulated_cells:%s',{len(triangulated_cells)})
    return sorted_cell,triangulated_cells

