import cv2
import numpy as np

def average_color(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    avg_color_per_channel = np.mean(image, axis=(0, 1))
    avg_color = tuple(map(int, avg_color_per_channel))
    return avg_color

image_path = 'img.png'
average = average_color(image_path)
print(f'Color promedio (RGB): {average}')
