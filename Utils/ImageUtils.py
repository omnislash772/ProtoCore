from PIL import Image

def __has_transparancy(img):
    if img.info.get("transparency", None) is not None:
        return True
    if img.mode == "P":
        transparent = img.info.get("transparency", -1)
        for _, index in img.getcolors():
            if index == transparent:
                return True
    elif img.mode == "RGBA":
        extrema = img.getextrema()
        if extrema[3][0] < 255:
            return True

    return False

def LoadImage(fileName):
    img = Image.open(fileName)
    rgba = img.convert("RGBA")
    if __has_transparancy(rgba) and not hasattr(img, "n_frames"):
        return rgba
    return img