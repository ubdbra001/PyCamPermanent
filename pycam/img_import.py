# -*- coding: utf-8 -*-

"""Custom picam image import function"""

from datetime import datetime
import cv2
import numpy as np


def load_picam_png(file_path, meta={}, **kwargs):
    """Load PiCam png files and import meta information"""

    raw_img = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
    
    # cv2 returns None if file failed to load
    if raw_img is None:
        raise FileNotFoundError(f"Image from {file_path} could not be loaded.") 

    img = np.array(raw_img)

    # Split both forward and backward slashes, to account for both formats
    file_name = file_path.split('\\')[-1].split('/')[-1]

    # Update metadata dictionary
    meta["bit_depth"] = 10
    meta["device_id"] = "picam-1"
    meta["file_type"] = "png"
    meta["start_acq"] = datetime.strptime(file_name.split('_')[0], "%Y-%m-%dT%H%M%S")
    meta["texp"] = float([f for f in file_name.split('_') if 'ss' in f][0].replace('ss', '')) * 10 ** -6  # exposure in seconds
    meta["read_gain"] = 1
    meta["pix_width"] = meta["pix_height"] = 5.6e-6  # pixel width in m

    return img, meta

