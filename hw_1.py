import asyncio
import os
import shutil
import argparse
import logging

logging.basicConfig(level=logging.ERROR)

async def read_folder(source_folder, destination_folder):
    for root, _, files in os.walk(source_folder):
        tasks = []
        for file in files:
            source_path = os.path.join(root, file)
            destination_path = os.path.join(destination_folder, os.path.splitext(file)[1][1:], file)
            tasks.append(copy_file(source_path, destination_path))
        await asyncio.gather(*tasks)

async def copy_file(source_path, destination_path):
    try:
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        shutil.copy(source_path, destination_path)
        print(f"Copied {source_path} to {destination_path}")
    except Exception as e:
        logging.error(f"Error copying {source_path}: {e}")

async def main():
    parser = argparse.ArgumentParser(description="Async file sorter")
    parser.add_argument("source_folder", help="Source folder path")
    parser.add_argument("destination_folder", help="Destination folder path")
    args = parser.parse_args()

    source_folder = args.source_folder
    destination_folder = args.destination_folder

    await read_folder(source_folder, destination_folder)

if __name__ == "__main__":
    asyncio.run(main())
