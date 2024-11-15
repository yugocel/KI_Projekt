import djitellopy.tello
import tensorflow as tf  # Install tensorflow
import cv2  # Install opencv-python
import numpy as np
import time
from djitellopy import tello
import cv2

file_path = "C:/Users/proje/PycharmProjects/KI_Projekt/converted_savedmodel/model.savedmodel/"
text_path = "C:/Users/proje/PycharmProjects/KI_Projekt/converted_savedmodel/labels.txt"


def connect_drone():
    drone = tello.Tello()
    drone.connect()
    time.sleep(5)
    drone.streamoff()
    drone.streamon()
    time.sleep(1)
    return drone


def main():
    # Disable scientific notation for clarity
    np.set_printoptions(suppress=True)

    # Load the model + labels
    model = tf.saved_model.load(file_path)
    class_names = open(text_path, "r").readlines()

    # Open the camera // connect to the drone
    camera = cv2.VideoCapture(0)
    #connect_drone()

    while True:
        # Grab the camera's image
        # image = drone.get_frame_read() #comment out while working with webcam
        # my_frame = image.frame #comment out while working with webcam
        ret, image = camera.read()

        # Resize the raw image for the model
        image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

        # Show the image in a window
        cv2.imshow("Webcam Image", image)  # change to my_frame while drone is connected

        # Make the image a numpy array and reshape it to the models input shape.
        image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

        # Normalize the image array
        image = (image / 127.5) - 1

        # Predicts the model
        infer = model.signatures["serving_default"]
        prediction = infer(tf.constant(image))["sequential_7"]
        print(prediction)
        index = np.argmax(prediction)
        class_name = class_names[index]
        confidence_score = prediction[0][index]

        # Print prediction and confidence score
        print("Class:", class_name[2:], end="")
        print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")

        # Listen to the keyboard for presses.
        keyboard_input = cv2.waitKey(1)

        # 27 is the ASCII for the esc key on your keyboard.
        if keyboard_input == 27:
            break

    cv2.destroyAllWindows()
    camera.release()
    # drone.end() #comment out while dev


if __name__ == "__main__":
    main()
