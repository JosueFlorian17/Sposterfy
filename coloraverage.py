import cv2
import numpy as np
import matplotlib.pyplot as plt

def average_color(image_path):
    """Calculate the average color of an image."""
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    avg_color_per_channel = np.mean(image, axis=(0, 1))
    avg_color = tuple(map(int, avg_color_per_channel))
    return avg_color

def extract_dominant_colors(image_path, k=5):
    """Extract the k most dominant colors from an image using K-means clustering."""
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Reshape image to a 2D array of pixels
    pixels = image.reshape((-1, 3))
    
    # Apply K-means clustering
    kmeans = cv2.kmeans(
        np.float32(pixels), k, None,
        (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2),
        10, cv2.KMEANS_RANDOM_CENTERS
    )
    
    _, labels, centers = kmeans
    centers = np.uint8(centers)  # Convert to integers
    return centers

def display_colors(colors):
    """Display extracted colors as a horizontal bar."""
    num_colors = len(colors)
    bar = np.zeros((50, num_colors * 100, 3), dtype="uint8")

    for i, color in enumerate(colors):
        bar[:, i * 100:(i + 1) * 100] = color

    plt.figure(figsize=(10, 2))
    plt.axis("off")
    plt.imshow(bar)
    plt.show()

# Load image and process colors
image_path ="Sposterfy\img.png"
average = average_color(image_path)
dominant_colors = extract_dominant_colors(image_path, k=5)

print(f'Average Color (RGB): {average}')
print(f'Dominant Colors (RGB): {dominant_colors}')

# Display colors
display_colors(dominant_colors)
