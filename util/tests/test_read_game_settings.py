import yaml
import os
import sys
import toml

if __name__ == '__main__':
    libdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    if os.path.exists(libdir):
        sys.path.insert(0, libdir)

    print('using yaml')
    yaml_input_path = os.path.join(sys.path[2], 'haggle', 'game_settings', 'card_haggle_1.yaml')
    yaml_file = open(yaml_input_path, 'r')
    data = yaml.load(yaml_file)
    print(data)
    for key, value in data.items():
        print(key, value)

    print('')

    print('using toml')
    toml_input_path = os.path.join(sys.path[2], 'haggle', 'game_settings', 'card_haggle_1.toml')
    #toml_file = open(toml_input_path, 'r')
    #data = toml.load(toml_file)
    data = toml.load(toml_input_path)
    print(data)
    for key, value in data.items():
        print(key, value)
