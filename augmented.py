import os
import cv2

# Define the source and destination folders
source_folder = 'normal img'
destination_folder = 'output_image_wp'

# Define augmentation parameters
num_augmentations = 15  # Number of augmented images per input image

# Augmentation functions
def augment_image(image):
    augmented_images = []

    for _ in range(num_augmentations):
        augmented_image = image.copy()  # Create a copy of the original image

        # Apply augmentation
        rotation_angle = 30  # Angle to rotate the image
        horizontal_flip = True  # Apply horizontal flip
        vertical_flip = False  # Apply vertical flip
        brightness_factor = 1.2  # Adjust brightness

        if rotation_angle != 0:
            rows, cols, _ = augmented_image.shape
            rotation_matrix = cv2.getRotationMatrix2D((cols / 2, rows / 2), rotation_angle, 1)
            augmented_image = cv2.warpAffine(augmented_image, rotation_matrix, (cols, rows))

        if horizontal_flip:
            augmented_image = cv2.flip(augmented_image, 1)

        if vertical_flip:
            augmented_image = cv2.flip(augmented_image, 0)

        if brightness_factor != 1.0:
            augmented_image = cv2.convertScaleAbs(augmented_image, alpha=brightness_factor, beta=0)

        augmented_images.append(augmented_image)

    return augmented_images

# Create the destination folder if it doesn't exist
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# Iterate through the files in the source folder
for filename in os.listdir(source_folder):
    if filename.endswith(('.jpg', '.jpeg', '.png')):  # Ensure you process only image files
        # Load the image using OpenCV
        image = cv2.imread(os.path.join(source_folder, filename))

        # Apply augmentation and get the augmented images
        augmented_images = augment_image(image)

        # Save the augmented images in the destination folder
        base_filename, file_extension = os.path.splitext(filename)
        for i, augmented_image in enumerate(augmented_images):
            augmented_filename = f'{base_filename}_aug_{i}{file_extension}'
            destination_path = os.path.join(destination_folder, augmented_filename)
            cv2.imwrite(destination_path, augmented_image)
