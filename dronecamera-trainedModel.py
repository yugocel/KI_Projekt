import tensorflow as tf
import numpy as np
import time
from djitellopy import tello
import cv2

file_path = "C:/Users/proje/PycharmProjects/KI_Projekt/converted_savedmodel/model.savedmodel/"


# Connect the drone
def connect_drone():
    drone = tello.Tello()
    drone.connect()
    time.sleep(5)
    drone.streamoff()
    drone.streamon()
    time.sleep(1)
    return drone


# Disconnect the drone
def disconnect_drone(drone):
    drone.streamoff()
    drone.end()


# this funtion will capture 5 perdictions and return the most common one
# resulting in a more stable prediction
def get_direction():
    model = tf.saved_model.load(file_path)

    # Open the camera [0] // connect to the drone [1]
    camera = cv2.VideoCapture(0)

    directions = [4]

    for i in range(5):

        # image = drone.get_frame_read() # comment out while dev with webcam
        # my_frame = image.frame # comment out while dev with webcam
        ret, image = camera.read()
        image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
        cv2.imshow("Webcam Image", image)  # change to my_frame while drone is connected

        # Make the image a numpy array and reshape it to the models input shape.
        image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

        # Normalize the image array
        image = (image / 127.5) - 1

        # Predicts the model
        infer = model.signatures["serving_default"]
        prediction = infer(tf.constant(image))["sequential_7"]

        # [down, right, left, up, star]
        directions[0] += prediction[0][0]
        directions[1] += prediction[0][1]
        directions[2] += prediction[0][2]
        directions[3] += prediction[0][3]
        directions[4] += prediction[0][4]

    # retry if max values are almost the same
    if max(directions) - sorted(directions)[3] <= 0.2:
        return get_direction()
    if max(directions) <= 3:
        return get_direction()

    return directions.index(max(directions))


# Pilot the drone via directions from the model / camera
def pilot_drone():
    drone = connect_drone()

    while True:
        direction = get_direction()
        if direction == 0:
            drone.move_down(30)
            print("moving down")
            time.sleep(4)
        elif direction == 1:
            drone.move_right(30)
            print("moving right")
            time.sleep(4)
        elif direction == 2:
            drone.move_left(30)
            print("moving left")
            time.sleep(4)
        elif direction == 3:
            drone.move_up(30)
            print("moving up")
            time.sleep(4)
        else:
            drone.land()
            print("Drone landed, goal reached")
            break


if __name__ == "__main__":
    pilot_drone()
    cv2.destroyAllWindows()

