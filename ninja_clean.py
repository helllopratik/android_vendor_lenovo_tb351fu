import os
import re

log_file = '../../../log.txt'
vendor_mk = 'tb351fu-vendor.mk'

if not os.path.exists(log_file) or not os.path.exists(vendor_mk):
    print("Files not found.")
    exit(1)

missing_files = []
with open(log_file, 'r') as f:
    for line in f:
        if 'missing and no known rule to make it' in line:
            # Extract the missing file path
            match = re.search(r"FAILED: ninja: '([^']+)'", line)
            if match:
                missing_files.append(match.group(1))

missing_files = list(set(missing_files))

if not missing_files:
    print("No missing ninja targets found.")
    exit(0)

print(f"Removing missing ninja targets: {missing_files}")

with open(vendor_mk, 'r') as f:
    lines = f.readlines()

with open(vendor_mk, 'w') as f:
    for line in lines:
        keep = True
        for mf in missing_files:
            # Check if this line tries to copy the missing file
            if mf + ':' in line:
                keep = False
                break
        if keep:
            f.write(line)
            
print("Ninja targets scrubbed successfully.")
