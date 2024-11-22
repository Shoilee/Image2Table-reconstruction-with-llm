import base64
import io
import os
import cv2
import subprocess
from PIL import ImageEnhance
from PIL import Image as PILImage
from ultralytics import YOLOv10


class Tools:
    def __init__(self):
        self.yolo_model_path = "models/best.pt"
        self.upscale_model_path = "models"
        self.upscale_model_name = "remacri"
        self.contrast_factor = 1.1
        self.brightness_factor = 0.9
        self.line_thickness = 2
        self.binarize_thresh = 180
        self.toolBox = {
            "a": self.upscale_image,
            "b": self.enhance_table_lines,
            "c": self.binarize_image_forward,
            "d": self.enhance_image,
            "e": self.crop_and_save_image,
        }

    def detect_table(self, image):
        model = YOLOv10(self.yolo_model_path)
        results = model.predict(image)
        preds = results[0].boxes.cpu().numpy()
        box = preds[0]
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        return min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)

    def upscale_image(self, input_path, index=0):
        command = [
            r"upscayl-bin.exe",
            "-i", input_path,
            "-o", f"process_img_cache/{index}_current_image.png",
            "-s", "2",
            "-m", self.upscale_model_path,
            "-n", self.upscale_model_name
        ]
        try:
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}")
        return f"process_img_cache/{index}_current_image.png"

    def enhance_table_lines(self, image_path, index=0):
        image = cv2.imread(image_path, 1)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        binary = cv2.adaptiveThreshold(~gray, 255,
                                       cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, -10)
        rows, cols = binary.shape
        scale = 5

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (cols // scale, 1))
        eroded = cv2.erode(binary, kernel, iterations=2)
        dilated_col = cv2.dilate(eroded, kernel, iterations=2)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, rows // scale))
        eroded = cv2.erode(binary, kernel, iterations=2)
        dilated_row = cv2.dilate(eroded, kernel, iterations=2)

        merge = cv2.add(dilated_col, dilated_row)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (self.line_thickness, self.line_thickness))
        enhanced_lines = cv2.dilate(merge, kernel, iterations=self.line_thickness)

        mask = cv2.bitwise_not(enhanced_lines)
        enhanced_lines_colored = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

        result = image.copy()
        result[mask == 0] = cv2.addWeighted(image, 0.1, enhanced_lines_colored, 0.8, 0)[mask == 0]

        cv2.imwrite(f"process_img_cache/{index}_current_image.png", result)
        return f"process_img_cache/{index}_current_image.png"

    def binarize_image(self, image_path, index=0):
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, self.binarize_thresh, 255, cv2.THRESH_BINARY_INV)
        cv2.imwrite(f"process_img_cache/{index}_current_image.png", binary)
        return f"process_img_cache/{index}_current_image.png"

    def binarize_image_forward(self, image_path, index=0):
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, self.binarize_thresh, 255, cv2.THRESH_BINARY)
        cv2.imwrite(f"process_img_cache/{index}_current_image.png", binary)
        return f"process_img_cache/{index}_current_image.png"

    def enhance_image(self, image_path, index=0):
        image = PILImage.open(image_path)
        enhancer = ImageEnhance.Contrast(image)
        image_contrasted = enhancer.enhance(self.contrast_factor)

        enhancer = ImageEnhance.Brightness(image_contrasted)
        image_enhanced = enhancer.enhance(self.brightness_factor)

        image_enhanced.save(f"process_img_cache/{index}_current_image.png")
        return f"process_img_cache/{index}_current_image.png"

    def crop_and_save_image(self, image_path, index=0):
        try:
            img = PILImage.open(image_path)
            x1, y1, x2, y2 = self.detect_table(image_path)
            cropped_img = img.crop((x1, y1, x2, y2))
            cropped_img.save(f"process_img_cache/{index}_current_image.png")
        except Exception as e:
            print(f"crop errror!: {e}")
            return image_path
        return f"process_img_cache/{index}_current_image.png"

    def encode_image(self, image_path, index=0):
        with PILImage.open(image_path) as image:
            if image.format == "PNG":
                image = image.convert("RGB")
                buffer = io.BytesIO()
                image.save(buffer, format="JPEG")
                buffer.seek(0)
                encoded_image = base64.b64encode(buffer.read()).decode('utf-8')
            else:
                with open(image_path, "rb") as image_file:
                    encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

        return encoded_image