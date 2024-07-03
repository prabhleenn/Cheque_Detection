import os
import cv2
import numpy as np
from PIL import Image, ImageEnhance


def main(input_dir, output_dir, operation, **kwargs):
    def grayscale_image(image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def rotate_image(image, angle):
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        return cv2.warpAffine(image, matrix, (w, h))

    def blur_image(image, ksize=(5, 5)):
        return cv2.GaussianBlur(image, ksize, 0)

    def adjust_contrast(image, factor):
        pil_img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        enhancer = ImageEnhance.Contrast(pil_img)
        enhanced_img = enhancer.enhance(factor)
        return cv2.cvtColor(np.array(enhanced_img), cv2.COLOR_RGB2BGR)

    def process_images(input_dir, output_dir, operation, **kwargs):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for filename in os.listdir(input_dir):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                img_path = os.path.join(input_dir, filename)
                img = cv2.imread(img_path)
                if img is not None:
                    processed_img = operation(img, **kwargs)
                    output_path = os.path.join(output_dir, filename)
                    cv2.imwrite(output_path, processed_img)

    # Call the specified operation
    if operation == 'grayscale':
        process_images(input_dir, output_dir, grayscale_image)
    elif operation == 'rotate':
        process_images(input_dir, output_dir, rotate_image, angle=kwargs.get('angle', 45))
    elif operation == 'blur':
        process_images(input_dir, output_dir, blur_image, ksize=kwargs.get('ksize', (5, 5)))
    elif operation == 'contrast':
        process_images(input_dir, output_dir, adjust_contrast, factor=kwargs.get('factor', 1.5))


if __name__ == "__main__":
    input_dir = "C:/Users/lenovo/OneDrive/Desktop/data_aug/input_dir"
    output_dir = "C:/Users/lenovo/OneDrive/Desktop/data_aug/output_dir"

    # Example of calling the grayscale operation
    main(input_dir, output_dir, operation='grayscale')

    # Example of calling the rotation operation with a specified angle
    main(input_dir, output_dir, operation='rotate', angle=90)

    # Example of calling the blur operation with a specified kernel size
    main(input_dir, output_dir, operation='blur', ksize=(7, 7))

    # Example of calling the contrast adjustment operation with a specified factor
    main(input_dir, output_dir, operation='contrast', factor=2.0)
