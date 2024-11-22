tsr_html_prompt = """
Identify the structure of the table and return it to me in HTML format.
Note: 
1. Use the <thead> and <tbody> tags to distinguish the table header from the table body.
2. Use only five tags: <table>, <thead>, <tr>, <td>, and <tbody>.
"""

tsr_html_background = """
### Instruction
Identify the structure of the table and return it to me in HTML format.
Note: 
1. Use only three tags: <table>, <tr>, <td>.
2. Pay attention to the structure of the table. Use rowspan and colspan to better interpret the structure information of the table.
3. Even if some cells are empty, they count as part of the table. Don't ignore any table information.



### supplementary information
1. Scene information in the picture: {scene}
2. The content information of the picture: {picture}
3. The information in the table in the picture: {table}



### answer
"""

get_background = """
### Instruction
Describe the scene in which the picture takes place and briefly describe the information in the picture.
Then the content information and structure information of the table are given.
Just give me a brief description of the table structure. For example, this table is a wireless table.
Note: Even if some cells are empty, they count as part of the table. Don't ignore any form information.

You must organize your answer into the following json format:
{
    "chain_of_thought": "Your thought process for answering this question.",
    "object": "The main items in the picture."
    "scene": "Your description of the scene in the picture.",
    "picture": "Your description of the information in the picture.",
    "table": "Use a paragraph to describe the structure of the table. This includes the type of table, whether the table has row dividers, column dividers, and so on."
}


### answer
"""

few_shot_tsr_html = """
## Instruction
Identify the structure of the table and return it to me in HTML format.
Note: 
1. Use the <thead> and <tbody> tags to distinguish the table header from the table body.
2. Use only five tags: <table>, <thead>, <tr>, <td>, and <tbody>.



## example"""

tsr_html_decomposition = """
### Instruction
You are now an OCR expert, and you are very good at recognizing tabular data in pictures and the structure of tables.
Now you need to Identify the structure of the table and return it to me in HTML format.
Please follow my instructions and complete the task step by step.



### step 1
Take a look,, there's a table in the picture.
Pay attention to the macro information of the table, especially the number of rows and columns in the table.
There may be an operation to merge cells in the table. Do not ignore this structural information.
Note that empty cells are also part of the table, so don't leave out all empty cells.



### step 2
This is some additional information that you can use to better understand the structure of the table and the contents of the table.
1. Scene information in the picture: {scene}
2. The content information of the picture: {picture}
3. The information in the table in the picture: {table}
This table is an {obj}, which is analyzed according to your previous data about the {obj}.
Please give the possible structure of this picture with your knowledge of the world.



### step 3
Please give me table OCR result by HTML format based on your previous analysis.
Before giving me the HTML result, take a deep breath, think deeply and describe the process you went through to achieve this HTML format.



### Note: 
1. Use only three tags: <table>, <tr>, <td>.
2. Pay attention to the structure of the table. Use rowspan and colspan to better interpret the structure information of the table.
3. There may be distracting information in the picture, ignore them and focus only on the structure and content of the table.
4. Please do not omit and give me all the results.



### answer
"""

tsr_getToolsChain = """
## Instruction
You are an image processing expert with a talent for selecting the optimal tools to enhance image processing, thereby improving the accuracy and effectiveness of downstream table recognition tasks.
Now, you have access to a set of image processing tools, described below:

a. Image up scaling: Performs super-resolution enhancement on an image. When an image lacks clarity, use this tool to enhance its sharpness.
b. Table line enhancement.: Enhances horizontal and vertical table lines within an image. This tool works on tables with full borders, not borderless or three-bordered tables.
c. Image binarization.: Converts an image to black-and-white, resulting in a binary image. However, this operation may cause the image to lose a lot of details at once.
d. Image enhancement: Enhances the brightness and contrast of an image to improve its overall visual effect. Enhancing visual effects may improve dim images, but it can lead to information loss in normal images.
e. Table area detection and cropping: Crops an image based on coordinates detected by the Table detection algorithm. This approach works well for images containing additional background details, but it doesn't apply as effectively when the entire image is just a table.

Based on the input image and task requirements, analyze which tools would be best suited to achieve the desired effect, and create a sequence of tool actions, outputting it in JSON format.
You need to create {path_n} distinct toolchains, each comprising up to {tool_num} different tools. Use fewer than {tool_num} tools if you feel they are sufficient for the task.



## Output format
```json
{
    "chain_of_thought": "Your thought process for answering this question.",
    "chain_of_tools_1": "acd",
    "chain_of_tools_2": "ce",
    ...,
    "chain_of_tools_{path_n}": "eb"
}
```



## answer
```json"""


tsr_getOneToolsChain = """
## Instruction
You are an image processing expert with a talent for selecting the optimal tools to enhance image processing, thereby improving the accuracy and effectiveness of downstream table recognition tasks.
Now, you have access to a set of image processing tools, described below:

a. Image up scaling: Performs super-resolution enhancement on an image. When an image lacks clarity, use this tool to enhance its sharpness.
b. Table line enhancement.: Enhances horizontal and vertical table lines within an image. This tool works on tables with full borders, not borderless or three-bordered tables.
c. Image binarization.: Converts an image to black-and-white, resulting in a binary image. However, this operation will cause the image to lose a lot of details at once.
d. Image enhancement: Enhances the brightness and contrast of an image to improve its overall visual effect. Enhancing visual effects may improve dim images, but it can lead to information loss in normal images.
e. Table area detection and cropping: Crops an image based on coordinates detected by the Table detection algorithm. This approach works well for images containing additional background details, but it doesn't apply as effectively when the entire image is just a table.

Based on the input image and task requirements, analyze which tools would be best suited to achieve the desired effect, and create a sequence of tool actions, outputting it in JSON format.
You need to create a distinct toolchains, which comprising up to {tool_num} different tools. Use fewer than {tool_num} tools if you feel they are sufficient for the task.



## Output format
```json
{
    "chain_of_thought": "Your thought process for answering this question.",
    "chain_of_tools": "acd"
}
```



## answer
```json"""

html_repair = """
## Instruction
The HTML code has a parsing error. Please correct the HTML code.
{error_html}



## answer
```html"""


image_reflection = """
## Instruction
You are an expert in identifying information. You will be given two images below. Now you need to analyze which of the two image contains more information.
The first image is the image before processing, and the second image is the image after processing.
If you think that the image has not lost any information before and after processing, then choose the second image.



## Output format if you select image 1
```json
{
    "chain_of_thought": "Your thought process for making this choice.",
    "choice": 1
}
```


## Output format if you select image 2
```json
{
    "chain_of_thought": "Your thought process for making this choice.",
    "choice": 2
}
```



## Task
Below is the first image
"""
