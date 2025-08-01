**INPUT:** Handwritten Table Image; **OUTPUT:** Knowledge Graph

**PROBLEM:** End-to-end process is unreliable and lack of transparency

**SOLUTION REQUIREMENT:** So, what we want a way of traceability or triples with it data (source) provenance.

**SOLUTION:**
1. **Step-1**: Reconstrcut the table (Task --> TSR & HTR); Image to structure table (e.g., HTML)
2. **Step-2**: Use table indexes or cell bounding boxes to trace piece of information (*Triple level provenance* -- **key contribution of the paper**) (data model or semweb technique supporting this; explore rdf 1.2 or PROV-O)
3. **Step-3**: Convert these pieces of information in triples (Information Extraction & KG Construction) (text to triple)


## Step-1: Reconstrcut Table
### Manual Table Reconstruction Annotation
- if uncertain about a character, place underscore (_)
- for unclear word(s), add _____ 


### Experiment

Task: Image to structured table (e.g., HTML) table

Techniques will be compared: 
1.  LLM (a: vannila b: chain-of-thought) 
2.  LORE 
3.  Loghi (*retraining Laypa with row and cell hierarchy detection; the output will not be a pageXML anymore, rather HTML*)

Evaluation Metric: (1) Tree Edit Distance (TED), considers content (2) TEDS-structs, considers table structure similarity only

Evaluation sample (n=5): ___ENTER IMAGE NAMES___

|strategy | # |TEDS|TEDS-struct|
|---|---|---|---|
| llama-4-maverick-17b-128e-instruct (**Vannila**) | 2  |   |   |
| llama-4-maverick-17b-128e-instruct (**Chain-of-Thought**)  |  2 |  |   |   |
|   |   |   |   |   |


### Evaluation Metric

| What it measures | Metric | -- |
|---|---|---|
|Tree structure similarity-with content| Tree Edit Distance|TED|
|Tree structure similarity-without content| Tree Edit Distance (ignore content)|TEDS-struct|
|Bounding Box overlap| |IoU|

###### Prompt: Vanilla
```
Identify the structure of the table and return it to me in HTML format.
Note: 
1. Use the <thead> and <tbody> tags to distinguish the table header from the table body.
2. Use only five tags: <table>, <thead>, <tr>, <td>, and <tbody>.
```


###### Prompt: Chain-of-thought
```
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
```
