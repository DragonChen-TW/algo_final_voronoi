from PyQt5.QtWidgets import QFileDialog

def from_text(f_name):
    print('f_name', f_name)
    with open(f_name, encoding='utf-8') as f:
        raw_data = f.readlines()
        print('raw_lines', raw_data[:100])
        raw_data = [l.replace('\n', '') for l in raw_data
                    if l[0] not in ('#', '\n')]
        print('raw2', raw_data[:10])
    data = []
    i = 0
    while i < len(raw_data) and raw_data[i] != '0':
        try:
            l = int(raw_data[i])
        except:
            print('e1', raw_data[i])
            break
        if l == 0:
            break
        # try:
        #     l = int(raw_data[i])
        # except:
        #     print('err1')
        #     print(raw_data[i - 3:i + 3])
        #     break
        i += 1
        try:
            data.append([l] + [tuple([int(s_str) for s_str in s.split(' ')]) for s in raw_data[i:i + l]])
        except:
            print('e2', raw_data[i:i + l])
            break
        i += l
    return data

def from_result(f_name):
    with open(f_name, encoding='utf-8') as f:
        raw_data = f.readlines()
        raw_data = [l[:-1] for l in raw_data
                    if l[0] not in ('#', '\n')]

    point_data = [(int(l.split(' ')[1]), int(l.split(' ')[2]))
                    for l in raw_data if l[0] == 'P']
    edge_data = [[int(s) for s in l.split(' ')[1:]]
                    for l in raw_data if l[0] == 'E']

    return point_data, edge_data

def select_file(self):
    file_name, _ = QFileDialog.getOpenFileName(self)
    return file_name


if __name__ == '__main__':
    f_name = 'input/data.in'
    data = from_text(f_name)
    print(data[-5:])
