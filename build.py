import zipfile
import os

def create_difypkg(output_name='rapidocr-tool.difypkg'):
    files_to_pack = [
        'manifest.yaml',
        'tools/rapidocr-tool.py',
        'tools/rapidocr-tool.yaml',
        'provider/rapidocr.py',
        'provider/rapidocr.yaml',
        'icon.svg',
        'requirements.txt',
        'README.md',
        'PRIVACY.md'
    ]
    
    with zipfile.ZipFile(output_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in files_to_pack:
            if os.path.exists(file_path):
                zipf.write(file_path, file_path)
                print(f"Added: {file_path}")
            else:
                print(f"Warning: {file_path} not found")
    
    print(f"\nPackage created: {output_name}")

if __name__ == '__main__':
    create_difypkg()