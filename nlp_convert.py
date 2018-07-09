import importlib
importlib.import_module('ginger')

from ginger import get_ginger_result

with open('converted_file.txt', 'r') as myfile:
    data=myfile.read().replace('\n', ' \n ').split(' ')
#data1=data.split(' ')
#print(len(data))
for i in range(0,len(data)):
    fixed_text = data[i]
    if data[i]!='\n':
        results=get_ginger_result(data[i])
        fixed_gap = 0
        for result in results["LightGingerTheTextResult"]:
            if(result["Suggestions"]):
                from_index = result["From"]
                to_index = result["To"] + 1
                suggest = result["Suggestions"][0]["Text"]
                fixed_text = fixed_text[:from_index-fixed_gap] + suggest + fixed_text[to_index-fixed_gap:]
                fixed_gap += to_index-from_index-len(suggest)
    data[i]=fixed_text
data=' '.join(data)
#for i in range(0,len(data)):
#    print(data[i])
fixed_text = data
results=get_ginger_result(data[i])
fixed_gap = 0
for result in results["LightGingerTheTextResult"]:
    if(result["Suggestions"]):
        from_index = result["From"]
        to_index = result["To"] + 1
        suggest = result["Suggestions"][0]["Text"]
        fixed_text = fixed_text[:from_index-fixed_gap] + suggest + fixed_text[to_index-fixed_gap:]
        fixed_gap += to_index-from_index-len(suggest)
data=fixed_text
print(data)

text_file = open("new_converted_file.txt", "w")
text_file.write(data)
text_file.close()
