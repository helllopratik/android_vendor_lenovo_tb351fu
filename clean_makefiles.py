import os

missing_apks = ['CarrierConfig', 'PrivateComputeServices', 'AndroidSystemIntelligence', 'AvatarPicker', 'Meet', 'SwitchAccess', 'Messages', 'YTMSetupWizard', 'EntertainmentSpace', 'talkback', 'Gemini', 'AccessibilityMenu', 'Wellbeing']

# 1. Fix tb351fu-vendor.mk
vendor_mk = 'tb351fu-vendor.mk'
if os.path.exists(vendor_mk):
    with open(vendor_mk, 'r') as f:
        lines = f.readlines()
    with open(vendor_mk, 'w') as f:
        for line in lines:
            if not any(f'\\{apk} \\' in line or f' {apk} \\' in line or line.strip() == f'PRODUCT_PACKAGES += {apk}' or line.strip() == f'{apk} \\' for apk in missing_apks):
                f.write(line)

# 2. Fix Android.bp using nested brace tracking
android_bp = 'Android.bp'
if os.path.exists(android_bp):
    with open(android_bp, 'r') as f:
        content = f.read()

    for apk in missing_apks:
        search_str = f'name: "{apk}"'
        while True:
            idx = content.find(search_str)
            if idx == -1:
                break
                
            start_idx = content.rfind('android_app_import', 0, idx)
            if start_idx == -1:
                break
                
            brace_idx = content.find('{', start_idx)
            if brace_idx == -1:
                break
                
            open_braces = 1
            curr_idx = brace_idx + 1
            while open_braces > 0 and curr_idx < len(content):
                if content[curr_idx] == '{':
                    open_braces += 1
                elif content[curr_idx] == '}':
                    open_braces -= 1
                curr_idx += 1
                
            content = content[:start_idx] + content[curr_idx:]
            
    with open(android_bp, 'w') as f:
        f.write(content)

print("Makefiles scrubbed successfully.")
