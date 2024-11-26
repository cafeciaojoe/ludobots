
# Initialize lists to store fitness values
quad_fitness = []
hex_fitness = []
octo_fitness = []

# Read the file and parse the fitness values
with open('hexvquad_fitness_disp.txt', 'r') as file:
    for line in file:
        if line.startswith('quad fitness:'):
            quad_fitness.append(float(line.split(': ')[1]))
        elif line.startswith('hex fitness:'):
            hex_fitness.append(float(line.split(': ')[1]))
        elif line.startswith('octo fitness:'):
            octo_fitness.append(float(line.split(': ')[1]))

# Calculate the average fitness for each category
average_quad_fitness = sum(quad_fitness) / len(quad_fitness) if quad_fitness else 0
average_hex_fitness = sum(hex_fitness) / len(hex_fitness) if hex_fitness else 0
average_octo_fitness = sum(octo_fitness) / len(octo_fitness) if octo_fitness else 0

# Print the results
print(f'Average quad fitness: {average_quad_fitness}')
print(f'Average hex fitness: {average_hex_fitness}')
print(f'Average octo fitness: {average_octo_fitness}')