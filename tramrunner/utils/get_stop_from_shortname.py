import csv
import pathlib

def search_csv(rawSearchInput:str , region:str="dresden"):
    """
    returns first result for search
    """
    static_file_dir = pathlib.Path(__file__).parent.parent.parent/'data'/'static_files'
    if region.lower() == "dresden":
        csv_path = static_file_dir/'abbreviations_dresden.csv'
    elif region.lower() == "umland":
        csv_path = static_file_dir/'abbreviations_regional.csv'
    else:
        print("utils.get_stop_from_shortname -- Region not recognized")
        return None


    searchTerm = rawSearchInput.upper()
    with open(csv_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for line in csv_reader:
            if str(searchTerm) in line:
                return line[0]
    return None

def main():

    print(search_csv('rac', region="dresden"))
    #get_stop_from_shortname("rac")

if __name__ == "__main__":
    main()