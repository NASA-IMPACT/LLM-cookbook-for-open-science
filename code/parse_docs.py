# code with all the best practices followed

import os
import re
import sys

import fire
from tqdm import tqdm


def parse_docs(txt_file, store_path):
    """parse the txt file, get the pdf file, store it in a folder and return the path

    Args:
        txt_file (txt file with links)
        store_path (path to store the pdf files)
    """
    with open(txt_file, "r") as f:
        lines = f.readlines()
        for i, line in tqdm(enumerate(lines)):
            if line.startswith("http"):
                pdf_path = os.path.join(store_path, str(i) + ".pdf")
                os.system(f"wget -O {pdf_path} {line}")
                print(f"pdf file stored at {pdf_path}")
    return store_path


if __name__ == "__main__":
    fire.Fire(parse_docs)
