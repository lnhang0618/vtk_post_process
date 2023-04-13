'''
Created on April 11th 2023

@author:LeonRho
'''
from Post_process.vorticity_post_process import Vorticity_Post_Process
from Post_process.temperature_post_process import Temperature_Post_Process
from Post_process.velocity_post_process import Velocity_Post_Process
from Post_process.pressure_post_process import Pressure_Post_Process
import numpy as np

vtk_file = \
(
    #'/home/lnhang/OpenFOAM/lnhang-dev/run/2D_Flat/turbulence2/VTK/turbulence2_200000.vtk'
    "/home/lnhang/OpenFOAM/lnhang-dev/run/cavity/cavity/VTK/cavity_100.vtk"
)
x_range = (0,1)
y_range = (0,1)
#cmap推荐：’jet','cividis','coolwarm','hsv','Blues','hot'
cmap = 'jet'
meshes= 'on'
normalization = 'on'
axis_map={'x':0,'y':1,'z':2}


choices=[]
#在此添加感兴趣的量
choices.append('velocity')

def PostChoice(choices):
    for choice in choices:
        if choice == 'temperature':
            temp_post_process =Temperature_Post_Process(vtk_file, x_range, y_range,cmap=cmap,meshes=meshes,normalization=normalization,axis_map=axis_map)
            temp_post_process.plot_temperature_contour()
        if choice == 'pressure':
            temp_post_process = Pressure_Post_Process(vtk_file, x_range, y_range,cmap=cmap,meshes=meshes,normalization=normalization,axis_map=axis_map)
            temp_post_process.plot_pressure_contour()
        if choice == 'velocity':
            temp_post_process =Velocity_Post_Process(vtk_file, x_range, y_range,cmap=cmap,meshes=meshes,normalization=normalization,axis_map=axis_map)
            temp_post_process.plot_velocity_x_contour()
            temp_post_process.plot_U_vector()
        if choice == 'vorticity':
            temp_post_process =Vorticity_Post_Process(vtk_file, x_range, y_range,cmap=cmap,meshes=meshes,normalization=normalization,axis_map=axis_map)
            temp_post_process.plot_vorticity_contour() 


PostChoice(choices)