import matplotlib.pyplot as plt

def draw_xy_meshes(ax,sorted_cell,x,y):
    # 连接每个单元格内的点
    for sorted_cell in sorted_cell:
    # 连接每个单元格内的点
        for i in range(len(sorted_cell)):
            point1 = sorted_cell[i]
            point2 = sorted_cell[(i + 1) % len(sorted_cell)]
            x_coords = [x[point1], x[point2]]
            y_coords = [y[point1], y[point2]]
            ax.plot(x_coords, y_coords, 'k-', linewidth=0.3)