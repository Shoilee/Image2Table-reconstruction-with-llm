import json


class DataSet:
    def __init__(self, dataSetName, data_path):
        self.dataSetName = dataSetName
        self.data_path = data_path
        self.data = None
        if self.dataSetName == 'pubtabnet':
            with open(f"{self.data_path}/pubtabnet/gtVal_full.json", 'r', encoding="utf-8") as f:
                self.data = json.load(f)
        elif self.dataSetName == 'scitsr':
            with open(f"{self.data_path}/SciTSR/test_1027.json", 'r', encoding="utf-8") as f:
                self.data = json.load(f)
        elif self.dataSetName == 'icdar1':
            with open(f"{self.data_path}/ICDAR2019/test_ground_truth/test_B1.json", 'r', encoding="utf-8") as f:
                self.data = json.load(f)
        elif self.dataSetName == 'icdar2':
            with open(f"{self.data_path}/ICDAR2019/test_ground_truth/test_B2.json", 'r', encoding="utf-8") as f:
                self.data = json.load(f)
        elif self.dataSetName == 'WTW':
            with open(f"{self.data_path}/WTW/test.json", 'r', encoding="utf-8") as f:
                self.data = json.load(f)
        elif self.dataSetName == 'small_pub':
            with open(f"{self.data_path}/pubtabnet/gtVal_small.json", 'r', encoding="utf-8") as f:
                self.data = json.load(f)

    def getData(self, start_id=0, end_id=-1):
        data_list = []
        if self.dataSetName == 'pubtabnet':
            for index, item in enumerate(self.data):
                if index < start_id:
                    continue
                if index == end_id:
                    break
                data_line = {
                    'image_id': item,
                    'image_path': f"{self.data_path}/pubtabnet/val/{item}"
                }
                data_line = data_line | self.data[item]
                data_line['html'] = '<table>' + data_line['html'] + '</table>'
                data_list.append(data_line)
        elif self.dataSetName == 'small_pub':
            for index, item in enumerate(self.data):
                if index < start_id:
                    continue
                if index == end_id:
                    break
                data_line = {
                    'image_id': item,
                    'image_path': f"{self.data_path}/pubtabnet/val/{item}"
                }
                data_line = data_line | self.data[item]
                data_line['html'] = data_line['html']
                data_list.append(data_line)
        elif self.dataSetName == 'scitsr':
            for index, item in enumerate(self.data):
                if index < start_id:
                    continue
                if index == end_id:
                    break
                data_line = {
                    'image_id': item,
                    'image_path': f"{self.data_path}/SciTSR/test/img/{item}"
                }
                data_line = data_line | json.loads(self.data[item])
                data_line['html'] = data_line['html']
                data_list.append(data_line)
        elif self.dataSetName == 'icdar1':
            for index, item in enumerate(self.data):
                if index < start_id:
                    continue
                if index == end_id:
                    break
                data_line = {
                    'image_id': item,
                    'image_path': f"{self.data_path}/ICDAR2019/test/TRACKB1/{item}"
                }
                data_line = data_line | self.data[item]
                data_list.append(data_line)
        elif self.dataSetName == 'icdar2':
            for index, item in enumerate(self.data):
                if index < start_id:
                    continue
                if index == end_id:
                    break
                data_line = {
                    'image_id': item,
                    'image_path': f"{self.data_path}/ICDAR2019/test/TRACKB2/{item}"
                }
                data_line = data_line | self.data[item]
                data_list.append(data_line)
        elif self.dataSetName == 'WTW':
            for index, item in enumerate(self.data):
                if index < start_id:
                    continue
                if index == end_id:
                    break
                data_line = {
                    'image_id': item,
                    'image_path': f"{self.data_path}/WTW/images/{item}"
                }
                data_line = data_line | self.data[item]
                data_list.append(data_line)
        else:
            raise "Data load error!"
        return data_list
