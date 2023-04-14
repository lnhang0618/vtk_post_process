'''
Created on April 11th 2023

@author:LeonRho
'''
from Post_process.vorticity_post_process import Vorticity_Post_Process
from Post_process.temperature_post_process import Temperature_Post_Process
from Post_process.velocity_post_process import Velocity_Post_Process
from Post_process.pressure_post_process import Pressure_Post_Process
import numpy as np
from enum import Enum

class Choice(Enum):
    TEMPERATURE = "temperature"
    PRESSURE = "pressure"
    VELOCITY = "velocity"
    VORTICITY = "vorticity"

params = {
    'vtk_file': '/home/lnhang/OpenFOAM/lnhang-dev/run/cavity/cavity/VTK/cavity_100.vtk',
    'x_range': (0, 1),
    'y_range': (0, 1),
    'cmap': 'coolwarm',
    'meshes': 'off',
    'normalization': 'on',
    'axis_map': {'x': 0, 'y': 1, 'z': 2},
    'z_value': 0,
    'component': 'all',
    'with_vector': 'on'
}

choices = [Choice.VELOCITY]

class PostProcessor:
    def __init__(self, params):
        self.params = params

    def process(self, choices):
        for choice in choices:
            if choice == Choice.TEMPERATURE:
                temp_post_process = Temperature_Post_Process(**self.params)
                temp_post_process.plot_temperature_contour()
            elif choice == Choice.PRESSURE:
                temp_post_process = Pressure_Post_Process(**self.params)
                temp_post_process.plot_pressure_contour()
            elif choice == Choice.VELOCITY:
                temp_post_process = Velocity_Post_Process(**self.params)
                temp_post_process.plot_velocity_contour()
            elif choice == Choice.VORTICITY:
                temp_post_process = Vorticity_Post_Process(**self.params)
                temp_post_process.plot_vorticity_contour()

post_processor = PostProcessor(params=params)
post_processor.process(choices=choices)
