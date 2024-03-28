from PIL import Image

def find_non_transparent_pixel(image, start_x, start_y):
    """
    Finds the first non-transparent pixel starting from the specified coordinates.
    Returns the coordinates of the non-transparent pixel.
    """
    width, height = image.size
    pixels = image.load()

    for x in range(start_x, width):
        for y in range(start_y, height):
            if pixels[x, y][3] != 0:  # Check alpha value of pixel
                return x, y
    return None, None  # No non-transparent pixel found


def remove_colors(image_path):
    # Open the image
    image = Image.open(image_path)
    width, height = image.size
    pixels = image.load()

    # Get the first and second pixel colors
    first_pixel_color = pixels[0, 0]
    second_pixel_color = pixels[1, 0]

    # Remove the first and second pixel colors from the entire image
    for x in range(width):
        for y in range(height):
            if pixels[x, y] == first_pixel_color or pixels[x, y] == second_pixel_color:
                pixels[x, y] = (0, 0, 0,0)  # Set the pixel color to black

    # Save the modified image
    image.save("output/image_without_colors.png")


def get_bounding_box(image, start_x, start_y):
    """
    Finds the bounding box of a non-transparent object starting from the specified coordinates.
    Returns the coordinates of the bounding box.
    """
    width, height = image.size
    pixels = image.load()

    # Find left boundary
    left_boundary = start_x
    while left_boundary > 0 and pixels[left_boundary - 1, start_y][3] != 0:
        left_boundary -= 1

    # Find right boundary
    right_boundary = start_x
    while right_boundary < width - 1 and pixels[right_boundary + 1, start_y][3] != 0:
        right_boundary += 1

    # Find top boundary
    top_boundary = start_y
    while top_boundary > 0 and pixels[start_x, top_boundary - 1][3] != 0:
        top_boundary -= 1

    # Find bottom boundary
    bottom_boundary = start_y
    while bottom_boundary < height - 1 and pixels[start_x, bottom_boundary + 1][3] != 0:
        bottom_boundary += 1

    return left_boundary, top_boundary, right_boundary, bottom_boundary


def crop_objects(image_path):
    # Open the image
    image = Image.open(image_path)
    width, height = image.size
    pixels = image.load()

    # Iterate over the image to find and crop objects
    object_count = 0
    while True:
        # Find the first non-transparent pixel
        start_x, start_y = find_non_transparent_pixel(image, 0, 0)

        if start_x is None or start_y is None:
            break  # No more non-transparent pixels found

        # Get the bounding box of the object
        left, top, right, bottom = get_bounding_box(image, start_x, start_y)

        # Check the size of the object
        object_width = right - left + 1
        object_height = bottom - top + 1
        if object_width >= 10 and object_height >= 10:
            # Crop the object
            obj = image.crop((left, top, right + 1, bottom + 1))

            # Save the cropped object
            obj.save(f"output/object_{object_count}.png")

            # Fill the object area with transparent pixels
            for x in range(left, right + 1):
                for y in range(top, bottom + 1):
                    pixels[x, y] = (0, 0, 0, 0)

            object_count += 1
        else:
            # Fill the object area with transparent pixels without saving it
            for x in range(left, right + 1):
                for y in range(top, bottom + 1):
                    pixels[x, y] = (0, 0, 0, 0)

# Example usage:
image_path = input("Image Name: ")

remove_colors(image_path)
crop_objects("output/image_without_colors.png")