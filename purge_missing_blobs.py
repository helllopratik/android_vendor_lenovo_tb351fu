import os

vendor_mk = 'tb351fu-vendor.mk'

if not os.path.exists(vendor_mk):
    print("tb351fu-vendor.mk not found!")
    exit(1)

with open(vendor_mk, 'r') as f:
    lines = f.readlines()

new_lines = []
missing_count = 0

for line in lines:
    # PRODUCT_COPY_FILES format:
    # vendor/lenovo/tb351fu/proprietary/path/to/file:$(TARGET_COPY_OUT_VENDOR)/path/to/file \
    stripped = line.strip()
    
    if stripped.startswith('vendor/lenovo/tb351fu/proprietary/'):
        # Extract the source path (everything before the colon)
        src_path = stripped.split(':')[0].strip()
        
        if not os.path.exists(src_path):
            print(f"Purging missing file: {src_path}")
            missing_count += 1
            continue # Skip adding this line
            
    new_lines.append(line)

with open(vendor_mk, 'w') as f:
    f.writelines(new_lines)

print(f"Successfully purged {missing_count} missing proprietary files from vendor.mk!")
