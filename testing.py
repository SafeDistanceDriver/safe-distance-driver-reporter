import json
import os


directory_list = list()
maxValue = -1
path_to_tub_folders = '/home/pi/Desktop/safe-distance-driver-reporter/data/'
maxFolder = ''
for root, dirs, files in os.walk(path_to_tub_folders, topdown=False):
    for name in dirs:
        if(name.startswith('tub_')):
            directory_list.append(os.path.join(root, name))
            startIndex = name.find('_')
            endIndex = name.find('_', startIndex +1)
            currentValue = int(name[startIndex + 1:endIndex])
            if(currentValue > maxValue):
                maxValue = currentValue
                maxFolder = name
                
            

print maxValue
print maxFolder
            
        





path_to_json = path_to_tub_folders + maxFolder

print path_to_json

json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
print(json_files)
