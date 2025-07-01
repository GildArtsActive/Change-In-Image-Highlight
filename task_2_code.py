import cv2
import numpy as np
import os
import argparse

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Detect and highlight missing objects in after images.')
    parser.add_argument('--input', type=str, required=True, help='Path to the input folder containing paired images.')
    parser.add_argument('--output', type=str, default='task_2_output', 
                      help='Path to the output folder for processed images. Defaults to "task_2_output" in the current directory.')
    args = parser.parse_args()
    
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    
    after_images = [f for f in os.listdir(args.input) if f.endswith('~2.jpg')]
    
    for after_img_name in after_images:
        base_name = after_img_name.replace('~2.jpg', '')
        before_img_name = base_name + '.jpg'
        
        before_path = os.path.join(args.input, before_img_name)
        after_path = os.path.join(args.input, after_img_name)
        
        if not os.path.exists(before_path):
            print(f"Before image {before_img_name} not found. Skipping {after_img_name}.")
            continue
            
        img_before = cv2.imread(before_path)
        img_after = cv2.imread(after_path)
        
        if img_before is None:
            print(f"Failed to load {before_path}. Skipping.")
            continue
        if img_after is None:
            print(f"Failed to load {after_path}. Skipping.")
            continue
            
        if img_before.shape != img_after.shape:
            print(f"Image sizes differ for {before_img_name} and {after_img_name}. Skipping.")
            continue
            
        gray_before = cv2.cvtColor(img_before, cv2.COLOR_BGR2GRAY)
        gray_after = cv2.cvtColor(img_after, cv2.COLOR_BGR2GRAY)
        
        diff = cv2.absdiff(gray_before, gray_after)
        _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
        
        kernel = np.ones((5,5), np.uint8)
        thresh = cv2.dilate(thresh, kernel, iterations=1)
        
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        output_img = img_after.copy()
        for contour in contours:
            if cv2.contourArea(contour) < 100:
                continue
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(output_img, (x, y), (x+w, y+h), (0, 0, 255), 2)
        
        output_path = os.path.join(args.output, after_img_name)
        cv2.imwrite(output_path, output_img)
        print(f"Processed {after_img_name}")

if __name__ == "__main__":
    main()