import pandas as pd

file_name_w21 = "W21.txt"
file_name_w22 = "W22.txt"
file_name_tury = "tury.txt"

def process_student_input(file_path):
    extracted_data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                fields = line.strip().split(' ')
                if len(fields) >= 3:
                    index_number = fields[1]
                    surname = fields[2]
                    first_name = fields[3]
                    extracted_data.append([index_number, surname, first_name])
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    
    # Create a CSV-like string from the extracted data
    csv_string = "\n".join([",".join(row) for row in extracted_data])
    
    return csv_string

def load_tura_data(file_path):
    pierwsza_tura = []
    druga_tura = []
    trzecia_tura = []
    czwarta_tura = []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        current_tura = None
        for line in file:
            line = line.strip()
            if line.endswith("tura:"):
                current_tura = line.replace(":", "").strip()
            else:
                numbers = line.split(", ")
                if current_tura == 'pierwsza tura':
                    pierwsza_tura.extend(numbers)
                elif current_tura == 'druga tura':
                    druga_tura.extend(numbers)
                elif current_tura == 'trzecia tura':
                    trzecia_tura.extend(numbers)
                elif current_tura == 'czwarta tura':
                    czwarta_tura.extend(numbers)
    
    return pierwsza_tura, druga_tura, trzecia_tura, czwarta_tura

def process_tura_data(csv, pierwsza_tura, druga_tura, trzecia_tura, czwarta_tura):
    tura_data = {"pierwsza_tura": [], "druga_tura": [], "trzecia_tura": [], "czwarta_tura": []}
    
    lines = csv.strip().split('\n')

    for line in lines:
        fields = line.split(',')
        index_number = fields[0]
        surname = fields[1]
        first_name = fields[2]
        if index_number in pierwsza_tura:
            tura_data["pierwsza_tura"].append([index_number, surname, first_name])
        elif index_number in druga_tura:
            tura_data["druga_tura"].append([index_number, surname, first_name])
        elif index_number in trzecia_tura:
            tura_data["trzecia_tura"].append([index_number, surname, first_name])
        elif index_number in czwarta_tura:
            tura_data["czwarta_tura"].append([index_number, surname, first_name])
    return tura_data

def print_tura_row_counts(extracted_data_1, extracted_data_2):
    tura_row_counts = {"W21": {}, "W22": {}}
    
    for i, extracted_data in enumerate([extracted_data_1, extracted_data_2], start=1):
        dataset_name = f"W21" if i == 1 else f"W22"
        for tura, data in extracted_data.items():
            tura_row_counts[dataset_name][tura] = len(data)
    for tura in tura_row_counts["W21"].keys():
        print(f"{tura}: ", end="")
        for dataset_name, counts in tura_row_counts.items():
            print(f"{dataset_name} - {counts[tura]}, ", end="")
        print()

def find_common_rows(csv_string1, csv_string2):
    set1 = set(tuple(row.split(',')) for row in csv_string1.strip().split('\n'))
    set2 = set(tuple(row.split(',')) for row in csv_string2.strip().split('\n'))
    
    common_rows = set1.intersection(set2)
    
    return common_rows

def find_index_tura_combined(index, extracted_data_w21, extracted_data_w22):
    merged_data = {}

    for tura, data in extracted_data_w21.items():
        merged_data[tura] = data
    
    for tura, data in extracted_data_w22.items():
        merged_data[tura].extend(data)

    for tura, data_list in merged_data.items():
        for data in data_list:
            if index in data:
                return tura
    return None

def main():
    csv_w21 = process_student_input(file_name_w21)
    csv_w22 = process_student_input(file_name_w22)

    pierwsza_tura, druga_tura, trzecia_tura, czwarta_tura = load_tura_data(file_name_tury)
    
    extracted_data_w21 = process_tura_data(csv_w21, pierwsza_tura, druga_tura, trzecia_tura, czwarta_tura)
    extracted_data_w22 = process_tura_data(csv_w22, pierwsza_tura, druga_tura, trzecia_tura, czwarta_tura)

    print_tura_row_counts(extracted_data_w21, extracted_data_w22)

    # To find common rows that need to be manually processed to not duplicate the data
    # common_rows = find_common_rows(csv_w21, csv_w22)
    # for row in common_rows:
    #     print(','.join(row))

    index_to_find = "12345"
    combined_tura_for_index = find_index_tura_combined(index_to_find, extracted_data_w21, extracted_data_w22)

    if combined_tura_for_index:
        print(f"Index {index_to_find} is in tura: {combined_tura_for_index}.")

if __name__ == "__main__":
    main()