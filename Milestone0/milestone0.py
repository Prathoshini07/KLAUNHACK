import csv
import math

def care_areas(filename):
    care_area = []
    try:
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                care_area.append(
                    {
                        'ID': int(row[0]),
                        'x1': float(row[1]),
                        'x2': float(row[2]),
                        'y1': float(row[3]),
                        'y2': float(row[4])
                    }
                )
    except FileNotFoundError:
        print(f"Cannot open file: {filename}")
    except Exception as e:
        print(f"Exception: {e}")
    return care_area

def get_metadata(filename):
    try:
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            meta = list(reader)
            main_field_size = float(meta[0][0])
            sub_field_size = float(meta[0][1])
    except FileNotFoundError:
        print(f"Cannot open file: {filename}")
        return 0, 0  # Default values
    except Exception as e:
        print(f"Exception: {e}")
        return 0, 0  # Default values
    return main_field_size, sub_field_size

def save_main_fields(filename, main_fields):
    try:
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            for i, field in enumerate(main_fields):
                writer.writerow([i, field['x1'], field['x2'], field['y1'], field['y2']])
    except Exception as e:
        print(f"Error: {e}")

def save_sub_fields(filename, sub_fields):
    try:
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            #writer.writerow(['ID', 'x1', 'x2', 'y1', 'y2', 'MF_ID'])  # Write header
            for i, field in enumerate(sub_fields):
                writer.writerow([i, field['x1'], field['x2'], field['y1'], field['y2'], field['MF_ID']])
    except Exception as e:
        print(f"Error: {e}")

def generate_fields(care, main_field_size, sub_field_size):
    main_fields = []
    sub_fields = []
    for area in care:
        mf_x1, mf_y1 = area['x1'], area['y1']
        mf_x2, mf_y2 = mf_x1 + main_field_size, mf_y1 + main_field_size
        main_fields.append(
            {
                'x1': mf_x1,
                'x2': mf_x2,
                'y1': mf_y1,
                'y2': mf_y2
            }
        )
        for i in range(math.ceil(mf_x1), math.ceil(area['x2']), math.ceil(sub_field_size)):
            for j in range(math.ceil(mf_y1), math.ceil(area['y2']), math.ceil(sub_field_size)):
                sub_x1, sub_y1 = i, j
                sub_x2, sub_y2 = sub_x1 + sub_field_size, sub_y1 + sub_field_size
                if sub_x2 <= mf_x2 and sub_y2 <= mf_y2:
                    sub_fields.append({'x1': sub_x1, 'x2': sub_x2, 'y1': sub_y1, 'y2': sub_y2, 'MF_ID': len(main_fields)-1})
    return main_fields, sub_fields

def main():
    care_area = care_areas(r'D:\KLAUNHACK\KLAUNHACK\Milestone0\CareAreas.csv')
    if not care_area:
        print("Care area data is missing or invalid. Exiting.")
        return

    main_field_size, sub_field_size = get_metadata(r'D:\KLAUNHACK\KLAUNHACK\Milestone0\metadata.csv')
    if main_field_size == 0 or sub_field_size == 0:
        print("Metadata is missing or invalid. Exiting.")
        return

    main_fields, sub_fields = generate_fields(care_area, main_field_size, sub_field_size)
    save_main_fields(r"D:\KLAUNHACK\KLAUNHACK\Milestone0\mainfields.csv", main_fields)
    save_sub_fields(r"D:\KLAUNHACK\KLAUNHACK\Milestone0\subfields.csv", sub_fields)

if __name__ == "__main__":
    main()
