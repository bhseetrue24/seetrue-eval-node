# Brainhack SeeTrue 2024 - Custom Evaluation Node for ComfyUI

## Nodes
### Evaluation Node
This node takes in an image within the workflow and evaluates it. The evaluation results will be output as text (output the text into another node to view the results).
### Evaluate from Folder Node
This node allows the user to pass in a directory path, and will run the evaluation on all valid images (.jpg/.jpeg/.png) in the directory. The evaluation results will be output as text (output the text into another node to view the results).
#### IMPORTANT
The metadata will be stripped, which will void the image for submission. Please duplicate the image **before** evaluating.


## Setup
1. Clone this repository into the `custom_nodes` folder in your ComfyUI directory
2. Refresh ComfyUI (if it is running)
