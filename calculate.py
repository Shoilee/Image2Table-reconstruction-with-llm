import json
from metric import TEDS
from parse import extract_HTML, format_td

def calculate_teds_scores(image_name, pred):
    """  
    Args:
        image (str): The image file name.
        pred (str): The predicted HTML string.
    Returns:
        dict: A dictionary containing the TEDS score and the TEDS structure score.
    """
    with open(f"example/stamboeken/context.json", 'r', encoding='utf-8') as f:
        context_label = json.load(f)
    true_html = context_label[image_name]["html"]
    true_html = format_td(true_html)  # Assuming this function formats the HTML correctly

    pred_html = extract_HTML(pred)  # Assuming this function extracts the HTML from the prediction string
    pred_html = format_td(pred_html)  # Format the predicted HTML

    # Calculate TEDS scores
    teds = TEDS(structure_only=False)
    teds_struct = TEDS(structure_only=True)

    # Assuming TEDS is a class with an evaluate method that takes two HTML strings
    # and returns a score between 0 and 1.
    teds_score = teds.evaluate(true_html, pred_html)
    teds_struct_score = teds_struct.evaluate(true_html, pred_html)

    # Prepare the output dictionary
    output = {
        "image_id": image_name,
        "TEDS_score": teds_score,
        "TEDS_struct": teds_struct_score,
    }

    return output
    
if __name__ == "__main__":
    main_image_name = "NL-HaNA_2.10.50_72_0036.jpg"
    with open("output/chatGPT/chain_of_thought/NL-HaNA_2.10.50_72_0036.html", "r", encoding="utf-8") as f:
        main_pred = f.read()
    result = calculate_teds_scores(main_image_name, main_pred)
    print(result)