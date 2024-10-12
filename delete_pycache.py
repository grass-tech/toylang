import os
import shutil


def delete_pycache(directory):
    stack = [directory]
    while stack:
        current_dir = stack.pop()
        for root, dirs, files in os.walk(current_dir):
            for dir_name in dirs:
                if dir_name == '__pycache__':
                    pycache_dir = os.path.join(root, dir_name)
                    shutil.rmtree(pycache_dir)
                    print(f"Deleted: {pycache_dir}")
            for sub_dir in dirs:
                stack.append(os.path.join(root, sub_dir))


if __name__ == "__main__":
    current_directory = os.getcwd()
    delete_pycache(current_directory)
