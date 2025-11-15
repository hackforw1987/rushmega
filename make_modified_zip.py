import zipfile, os, shutil, re

# === মূল ফাইলের নাম ===
source_zip = "rushmega.com.zip"
work_dir = "rushmega_work"
output_zip = "rushmega_modified.zip"

# === নতুন স্লাইডার ফাইল ===
new_files = ["video.mp4", "image1.jpg", "image2.jpg", "image3.jpg"]

# === ধাপ ১: পুরনো জিপ আনজিপ ===
if os.path.exists(work_dir):
    shutil.rmtree(work_dir)
with zipfile.ZipFile(source_zip, 'r') as zip_ref:
    zip_ref.extractall(work_dir)

# === ধাপ ২: স্লাইডার ফোল্ডার খুঁজে পুরনো ব্যানার মুছুন ===
assets_dir = None
for root, dirs, files in os.walk(work_dir):
    if "assets" in root:
        assets_dir = root
        break

if not assets_dir:
    raise FileNotFoundError("❌ assets ফোল্ডার খুঁজে পাওয়া যায়নি!")

# পুরনো বড় ব্যানার/স্লাইডার ইমেজ ডিলিট
for f in os.listdir(assets_dir):
    if re.search(r"(banner|slide|carousel|hero).*", f, re.IGNORECASE) or f.endswith((".jpg", ".jpeg", ".png", ".webp", ".mp4")):
        os.remove(os.path.join(assets_dir, f))

# === ধাপ ৩: নতুন ফাইল কপি ===
for f in new_files:
    shutil.copy(f, assets_dir)

# === ধাপ ৪: index.html বা JS-এ path আপডেট ===
index_file = None
for root, dirs, files in os.walk(work_dir):
    for file in files:
        if file.startswith("index") and (file.endswith(".html") or file.endswith(".js")):
            index_file = os.path.join(root, file)
            break
    if index_file:
        break

if index_file:
    with open(index_file, "r", encoding="utf-8") as f:
        content = f.read()

    # পুরনো স্লাইড ইমেজ path পরিবর্তন করে নতুনগুলো বসানো
    content = re.sub(r"assets/[^\"']+\.(jpg|jpeg|png|webp|mp4)",
                     lambda m, i=[0]: f"assets/{new_files[i[0] % len(new_files)]}" if not i.__setitem__(0, i[0]+1) else None,
                     content)

    with open(index_file, "w", encoding="utf-8") as f:
        f.write(content)

# === ধাপ ৫: নতুন জিপ বানানো ===
if os.path.exists(output_zip):
    os.remove(output_zip)
with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as newzip:
    for root, dirs, files in os.walk(work_dir):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, work_dir)
            newzip.write(full_path, rel_path)

print("✅ rushmega_modified.zip তৈরি হয়েছে সফলভাবে!")
