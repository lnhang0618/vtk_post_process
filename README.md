# vtk_post_process

# Python-based Post-Processing Tool for OpenFOAM Simulations
This post-processing tool is designed to process and visualize the results of OpenFOAM simulations using Python. It can handle various output variables such as temperature, pressure, velocity, and vorticity. 
The tool is designed to be flexible and can be customized for different applications.

## Features

-Supports generating contour plots of temperature, pressure, velocity, and vorticity fields.
-Allows for customization of axis mapping and normalization.
-Offers various colormap options for better data visualization.
-Provides options to display or hide mesh lines.
-Supports only 2D simulation data now.

## Requirements
-Python 3.6 or higher
-NumPy
-Matplotlib
-VTK
-Enum

## Installation
Clone this repository to your local machine:
```bash
Copy code
git clone https://github.com/yourusername/post_process.git
```
Navigate to the repository folder:
```bash
Copy code
cd post_process
```
Install the required Python packages:
```bash
Copy code
pip install -r requirements.txt
```
## Usage
Edit the 'params' dictionary in 'main.py' to specify the input VTK file, desired variable ranges, colormap, and other settings.

Choose the variables you want to visualize by adding them to the 'choices' list in 'main.py'.

Run 'main.py':

```bash
Copy code
python main.py
```
The script will generate and display the specified plots.

## Example
```python
Copy code
params = {
    'vtk_file': 'path/to/your/vtk_file.vtk',
    'x_range': (0.4, 0.6),
    'y_range': (0.4, 0.6),
    'cmap': 'coolwarm',
    'meshes': 'off',
    'normalization': 'on',
    'axis_map': {'x': 0, 'y': 1, 'z': 2},
    'z_value': 0.0005,
    'component': 'all',
    'with_vector': 'on'
}

choices = [Choice.VELOCITY]

post_processor = PostProcessor(params=params)
post_processor.process(choices=choices)
```
This example will visualize the velocity field for the specified VTK file.

## Contributing
We welcome contributions to improve this tool. Please submit issues or pull requests on the GitHub repository.

## License
This project is released under the MIT License.