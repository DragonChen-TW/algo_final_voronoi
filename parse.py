def from_text(f_name):
    with open(f_name, encoding='utf-8') as f:
        raw_data = f.readlines()
        raw_data = [l[:-1] for l in raw_data
                    if l[0] not in ('#', '\n')]
    data = []
    i = 0
    while i < len(raw_data) and raw_data[i] != '0':
        l = int(raw_data[i])
        i += 1
        data.append([l] + [s.split(' ') for s in raw_data[i:i + l]])
        i += l
    return data

if __name__ == '__main__':
    f_name = 'input/data.in'
    data = from_text(f_name)
    print(data[-5:])
