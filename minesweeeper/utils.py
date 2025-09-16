import settings


# Function to find a specific percentage of the main height
def height_prct(percentage):
    return (settings.HEIGHT / 100) * percentage


# Function to find a specific percentage of the main width
def width_prct(percentage):
    return (settings.WIDTH / 100) * percentage