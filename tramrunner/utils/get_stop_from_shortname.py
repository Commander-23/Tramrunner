import os, csv
import pathlib

def search_csv(rawSearchInput, csv_path=None):
    if csv_path is None:
        csv_path = os.path.join(os.path.dirname(__file__), 'shortnames_dresden.csv')
    searchTerm = rawSearchInput.upper()
    with open(csv_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for line in csv_reader:
            if str(searchTerm) in line:
                return line[0]
    return None

def main():

    base_dir = pathlib.Path(__file__).parent.parent
    csv_path = base_dir / 'local_data' / 'files' / 'shortnames_dresden.csv'
    print(csv_path)
    print(base_dir)
    print(search_csv('', csv_path))
    #get_stop_from_shortname("rac")

if __name__ == "__main__":
    main()