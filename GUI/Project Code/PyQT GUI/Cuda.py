import cv2

def check_cuda():
    has_cuda = False
    try:
        count = cv2.cuda.getCudaEnabledDeviceCount()
        if count > 0:
            has_cuda = True
    except AttributeError:
        pass

    return has_cuda

if __name__ == "__main__":
    if check_cuda():
        print("OpenCV has CUDA support.")
    else:
        print("OpenCV does not have CUDA support.")
