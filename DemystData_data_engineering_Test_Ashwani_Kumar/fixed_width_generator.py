import sys
import csv

def read_spec(spec_file_path):
    """Parse the specification string into a dictionary with field names and lengths."""
    field_specs = {}
    with open(spec_file_path, 'r') as file:
        spec_content = file.read().strip()
    parts = spec_content.split(',')
    for part in parts:
        name, length = part.split('<')
        field_specs[name] = int(length)
    return field_specs
    
    
#def read_spec(spec_file_path):
#    """Read the spec file and return a list of (field name, length) tuples."""
#    with open(spec_file_path, 'r') as file:
#        spec_content = file.read().strip()
#    spec_list = [s.split('<') for s in spec_content.split(',')]
#    return [(name, int(length)) for name, length in spec_list]

def generate_sample_data(num_records):
    """Generate sample data."""
    data = []
    for i in range(num_records):
        data.append({
            'first_name': f'First{i}',
            'last_name': f'Last{i}',
            'address': f'Address{i}',
            'date_of_birth': '1980-01-01'
        })
    return data

def write_fixed_width_file(filename, spec_file_path, data):
    """Generate a fixed-width file based on the provided specification and data."""
    #field_specs = parse_spec(spec)
    field_specs=read_spec(spec_file_path)
    print(field_specs)

    with open(filename, 'w') as f:
        for record in data:
            line = ''.join(f"{str(record.get(key, '')).ljust(field_specs[key])}" for key in field_specs)
            f.write(line + '\n')

def read_fixed_width_file(filename, spec_file_path):
    """Read a fixed-width file and convert it to a list of dictionaries."""
    field_specs = read_spec(spec_file_path)
    field_names = list(field_specs.keys())
    offsets = [0] + [sum(field_specs[field] for field in field_names[:i]) for i in range(1, len(field_names) + 1)]

    data = []
    with open(filename, 'r') as f:
        for line in f:
            record = {field_names[i]: line[offsets[i]:offsets[i + 1]].strip() for i in range(len(field_names))}
            data.append(record)
    return data

def write_csv_file(csv_output, data):
    """Write a list of dictionaries to a CSV file."""
    if data:
        fieldnames = data[0].keys()
        with open(csv_output, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

def main():
    if len(sys.argv) < 3:
        print("Usage: python fixed_width_generator.py <spec> <output_fixed_width_filename> [<use_sample_data> <num_records>]")
        sys.exit(1)

    spec_file_path = sys.argv[1]
    output_fixed_width_filename = sys.argv[2]
    use_sample_data = sys.argv[3].lower() == 'true' if len(sys.argv) > 3 else True
    csv_output=sys.argv[4]
    num_records = int(sys.argv[5]) if len(sys.argv) > 5 else 1000

    if use_sample_data:
        data = generate_sample_data(num_records)
    else:
        # Example of how to get data from user input; in practice, you might load from a file or other source.
        data = []
        print("Enter your data in the following format:")
        print("first_name last_name address date_of_birth")
        for _ in range(num_records):
            user_input = input("Enter data: ")
            first_name, last_name, address, date_of_birth = user_input.split()
            data.append({
                'first_name': first_name,
                'last_name': last_name,
                'address': address,
                'date_of_birth': date_of_birth
            })

    write_fixed_width_file(output_fixed_width_filename, spec_file_path, data)
    parsed_data = read_fixed_width_file(output_fixed_width_filename, spec_file_path)
    write_csv_file(csv_output, parsed_data)

if __name__ == "__main__":
    main()