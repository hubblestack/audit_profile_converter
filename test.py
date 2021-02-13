from util import helper

list_file = '/Users/gsingal/Documents/GitHub/hubble_github/audit_profile_converter/test_data/converted/test.yaml'
source_file = '/Users/gsingal/Documents/GitHub/hubble_github/audit_profile_converter/data.log'


with open(source_file) as f:
    lines = tuple(open(filename, 'r'))

# read all lines at once
all_of_it = helper.read_file(source_file)

lines = []
with open(list_file) as f:
    lines = [line.rstrip() for line in f]

found = 0
not_found = 0
for line in lines:
    if line not in all_of_it:
        not_found += 1
    else:
        found += 1

print(found)
print(not_found)