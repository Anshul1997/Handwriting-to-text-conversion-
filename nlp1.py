import importlib
importlib.import_module('ginger')

from ginger import get_ginger_result

original_text="Deluxe"

fixed_text = original_text
results = get_ginger_result(original_text)

# Incorrect grammar
color_gap, fixed_gap = 0, 0
for result in results["LightGingerTheTextResult"]:
    if(result["Suggestions"]):
        from_index = result["From"] + color_gap
        to_index = result["To"] + 1 + color_gap
        suggest = result["Suggestions"][0]["Text"]
        fixed_text = fixed_text[:from_index-fixed_gap] + suggest + fixed_text[to_index-fixed_gap:]
        fixed_gap += to_index-from_index-len(suggest)

#print("from: " + original_text)
print("to:   " + fixed_text)
