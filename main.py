'''
Created on April 11th 2023

@author:LeonRho
'''
from Post_process.vorticity_post_process import Vorticity_Post_Process
from Post_process.temperature_post_process import Temperature_Post_Process
from Post_process.velocity_post_process import Velocity_Post_Process
from Post_process.pressure_post_process import Pressure_Post_Process
import numpy as np
params = {
    'vtk_file': '/home/lnhang/OpenFOAM/lnhang-dev/run/tutorials/incompressible/pimpleFoam/RAS/pitzDaily/VTK/pitzDaily_1206.vtk',
    'x_range': (0, 1),
    'y_range': (0, 1),
    'cmap': 'jet',
    'meshes': 'on',
    'normalization': 'on',
    'axis_map': {'x': 0, 'y': 1, 'z': 2},
    #'z_value': 0.0005,
}


choices=[]
#在此添加感兴趣的量
choices.append('velocity')

def PostChoice(choices):
    for choice in choices:
        if choice == 'temperature':
            temp_post_process =Temperature_Post_Process(**params)
            temp_post_process.plot_temperature_contour()
        if choice == 'pressure':
            temp_post_process = Pressure_Post_Process(**params)
            temp_post_process.plot_pressure_contour()
        if choice == 'velocity':
            temp_post_process =Velocity_Post_Process(**params)
            temp_post_process.plot_velocity_x_contour()
            temp_post_process.plot_U_vector()
        if choice == 'vorticity':
            temp_post_process =Vorticity_Post_Process(**params)
            temp_post_process.plot_vorticity_contour() 


PostChoice(choices)