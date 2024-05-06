import numpy as np
import hashlib
import io
import os
import requests
from PIL import Image
import json


class EvaluationNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image_in": ("IMAGE", {}),
                "eval_url": ("STRING", {"default": ""})
            },
        }

    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("image_out", "string_out")
    FUNCTION = "evaluate"
    CATEGORY = "dsta_custom_node"

    def evaluate(self, image_in, eval_url):
        # send http request to the api
        # image_in is a tensor, convert to image and send as multipart form data
        for (batch_number, image) in enumerate(image_in):
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            # Image to byte-like object
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='png')
            img_byte_arr = img_byte_arr.getvalue()

            ### For connecting to local in house api evaluator

            image_tuple = ('image.png', img_byte_arr)
            
            files = {'images': image_tuple}
            
            response = requests.post(eval_url, files=files)
            # check if response is successful
            if response.status_code != 200:
                return image_in, f"Error: {response.status_code} - {response.json()['error']}"
            
            prediction = response.json()['predictions'][0]
            prediction['probability'] = round(prediction['probability'], 2)

            return image_in, f"Image is {prediction['classification']}. Fake Percentage - {prediction['probability'] * 100}%"
            
class EvaluateFromFolderNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "folder_path" : ("STRING", {"default": ""}),
                "eval_url": ("STRING", {"default": ""})
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string_out",)
    FUNCTION = "evaluate_from_folder"
    CATEGORY = "dsta_custom_node"

    def evaluate_from_folder(self, folder_path, eval_url):
        for root, subdirs, files in os.walk(folder_path):
            for file in files:
                if '.jpeg' in file or '.jpg' in file or '.png' in file:
                    file_path = os.path.join(root, file)
                    img = Image.open(file_path)
                    img.save(file_path)
        files_to_send = []
        for root, subdirs, files in os.walk(folder_path):
            for file in files:
                if '.jpeg' in file or '.jpg' in file or '.png' in file:
                    file_path = os.path.join(root, file)
                    img = Image.open(file_path)
                    # Image to byte-like object
                    img_byte_arr = io.BytesIO()
                    img.save(img_byte_arr, format='png')
                    img_byte_arr = img_byte_arr.getvalue()
                    
                    image_tuple = (file_path, img_byte_arr)
                    file_to_send = ('images', image_tuple)
                    files_to_send.append(file_to_send)
                    
        ### For connecting to local in house api evaluator
        
        response = requests.post(eval_url, files=files_to_send)
        # check if response is successful
        if response.status_code != 200:
            return (f"Error: {response.status_code} - {response.json()['error']}",)
        predictions = response.json()['predictions']
        for prediction in predictions:
            prediction['probability'] = round(prediction['probability'], 2)

        return (str(predictions),)
        
    @classmethod
    def IS_CHANGED(cls, text):
        m = hashlib.sha256()
        m.update(text)
        return m.digest().hex()
        
NODE_CLASS_MAPPINGS = {
"EvaluationNode": EvaluationNode,
"EvaluateFromFolderNode": EvaluateFromFolderNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
"EvaluationNode": "Evaluation Node",
"EvaluateFromFolderNode": "Evaluate From Folder Node",
}
        