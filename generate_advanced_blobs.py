import os

prop_dir = "proprietary"
mk_file = "tb351fu-vendor-blobs.mk"
android_mk_file = "Android.mk"

lines = ["PRODUCT_COPY_FILES += \\"]
apk_modules = []
android_mk_lines = ["LOCAL_PATH := $(call my-dir)\n"]

for root, dirs, files in os.walk(prop_dir):
    for f in files:
        full_path = os.path.join(root, f)
        rel_path = os.path.relpath(full_path, prop_dir)
        
        if rel_path.startswith("system/"):
            dest = f"$(TARGET_COPY_OUT_SYSTEM)/{rel_path[7:]}"
            mod_path = f"$(TARGET_OUT)/{os.path.dirname(rel_path[7:])}"
        elif rel_path.startswith("vendor/"):
            dest = f"$(TARGET_COPY_OUT_VENDOR)/{rel_path[7:]}"
            mod_path = f"$(TARGET_OUT_VENDOR)/{os.path.dirname(rel_path[7:])}"
        elif rel_path.startswith("product/"):
            dest = f"$(TARGET_COPY_OUT_PRODUCT)/{rel_path[8:]}"
            mod_path = f"$(TARGET_OUT_PRODUCT)/{os.path.dirname(rel_path[8:])}"
        elif rel_path.startswith("system_ext/"):
            dest = f"$(TARGET_COPY_OUT_SYSTEM_EXT)/{rel_path[11:]}"
            mod_path = f"$(TARGET_OUT_SYSTEM_EXT)/{os.path.dirname(rel_path[11:])}"
        else:
            continue
            
        if f.endswith(".apk"):
            mod_name = os.path.splitext(f)[0]
            apk_modules.append(mod_name)
            priv = "true" if "priv-app" in rel_path else "false"
            
            android_mk_lines.append(f"""include $(CLEAR_VARS)
LOCAL_MODULE := {mod_name}
LOCAL_MODULE_TAGS := optional
LOCAL_MODULE_CLASS := APPS
LOCAL_CERTIFICATE := PRESIGNED
LOCAL_SRC_FILES := proprietary/{rel_path}
LOCAL_MODULE_PATH := {mod_path}
LOCAL_PRIVILEGED_MODULE := {priv}
include $(BUILD_PREBUILT)
""")
        else:
            lines.append(f"    vendor/lenovo/tb351fu/proprietary/{rel_path}:{dest} \\")

if len(lines) > 1:
    lines[-1] = lines[-1].rstrip(" \\")
else:
    lines = []

with open(mk_file, "w") as f:
    f.write("\n".join(lines) + "\n")
    if apk_modules:
        f.write("\nPRODUCT_PACKAGES += \\\n")
        f.write(" \\\n".join([f"    {m}" for m in apk_modules]) + "\n")

# Android.mk generation disabled to prevent duplicate module definitions.
