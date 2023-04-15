import numpy as np
import logging

#归一化
def normalization(x,y):
    x_max,x_min=np.max(x),np.min(x)
    y_max,y_min=np.max(y),np.min(y)
    # 将x和y归一化
    x = (x - x_min) / (x_max - x_min)
    y = (y - y_min) / (y_max - y_min)
        
    #statistics:
    logging.info("\nNormalized coordinates range:")
    logging.info("Min normalized x: %s", np.min(x))
    logging.info("Max normalized x: %s", np.max(x))
    logging.info("Min normalized y: %s", np.min(y))
    logging.info("Max normalized y: %s", np.max(y))
    
    return x,y
    
    
