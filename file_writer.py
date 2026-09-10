import os

def write_file(project_name, file_name, content):
    os.makedirs(project_name, exist_ok=True)

    file_path = os.path.join(project_name, file_name)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Created: {file_name}")