from PIL import Image
import pyheif
import argparse
import pathlib
from os import path
import os
import re
import asyncio


# heic files
pattern = ".*\.(heic|HEIC)"


def conv(image_path):
    new_png_file = path.splitext(path.basename(image_path))[0] + '.png'
    new_png_path = path.join(path.dirname(image_path), new_png_file)

    try:
        heif_file = pyheif.read(image_path)
        data = Image.frombytes(
            heif_file.mode,
            heif_file.size,
            heif_file.data,
            "raw",
            heif_file.mode,
            heif_file.stride,
            )
        data.save(new_png_path, "PNG")
        # Remove HEIC
        os.remove(image_path)
        print("Success convert PNG:", new_png_path)
    except:
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Target dir path")
    parser.add_argument("dir", metavar="dir", type=pathlib.Path, help="Target dir path")
    args = parser.parse_args()

    heic_files = [f for f in os.listdir(path=args.dir) if re.search(pattern, f, re.IGNORECASE)]

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    for f in heic_files:
        loop.run_in_executor(None, conv, path.abspath(path.join(args.dir, f)))
    print("converting HEIC -> PNG...")
