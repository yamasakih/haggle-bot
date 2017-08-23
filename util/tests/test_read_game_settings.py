import yaml
import os
import sys

if __name__ == '__main__':
    libdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    if os.path.exists(libdir):
        sys.path.insert(0, libdir)
    input_path = os.path.join(sys.path[2], 'haggle', 'game_settings', 'card_haggle_1.yaml')
    f = open(input_path, 'r')
    data = yaml.load(f)
    print(data)
    for key, value in data.items():
        print(key, value)
