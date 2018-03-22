import json
import os


maxValue = -1
path_to_tub_folders = '/home/pi/Desktop/safe-distance-driver-reporter/data/'
maxFolder = ''
for root, dirs, files in os.walk(path_to_tub_folders, topdown=False):
    print dirs
    for name in dirs:
        if(name.startswith('tub_')):
            startIndex = name.find('_')
            endIndex = name.find('_', startIndex +1)
            currentValue = int(name[startIndex + 1:endIndex])
            if(currentValue > maxValue):
                maxValue = currentValue
                maxFolder = name
                
            

print maxValue
print maxFolder
            
        





path_to_json = path_to_tub_folders + maxFolder + '/'

print path_to_json

maxJsonValue = 0
maxJsonFile = ''



json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]

for name in json_files:
        if(name.startswith('record_')):
            startIndex = name.find('_')
            currentValue = int(name[startIndex + 1:-5])
            if(currentValue > maxJsonValue):
                maxJsonValue = currentValue
                maxJsonFile = name

print maxJsonFile

path_to_data = path_to_json + maxJsonFile

print path_to_data


json_data = open(path_to_data).read()

data = json.loads(json_data)
print data
print data["user/throttle"]
print 'end of print'







