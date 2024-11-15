import time

from djitellopy import tello
import cv2


def FlightStreamTest(drone):
    # start
    drone.connect()

    # infos
    print("Battery: ", drone.get_battery())
    print("Height: ", drone.get_height())

    drone.streamoff()
    drone.streamon()

    while True:
        # Get the frame
        frame_read = drone.get_frame_read()
        my_frame = frame_read.frame

        #drone.takeoff()

        # Display the frame
        cv2.imshow("Stream", my_frame)

        # Wait for the frame
        if cv2.waitKey(1) & 0xFF == ord('q'):
            drone.land()
            drone.end()


def basic_flight(drone):
    # drone.set_wifi_credentials('Y>gX,+L', 'ichliebeRonan')
    # start
    drone.connect()
    time.sleep(5)
    # infos
    print("Battery: ", drone.get_battery())
    print("Height: ", drone.get_height())

    drone.takeoff()
    time.sleep(5)

    # move in 8 shape
    drone.move_left(50)
    time.sleep(5)
    drone.move_up(50)
    time.sleep(5)
    drone.move_right(50)
    time.sleep(5)
    drone.move_down(50)
    time.sleep(5)
    drone.move_right(50)
    time.sleep(5)
    drone.move_up(50)
    time.sleep(5)
    drone.move_left(50)
    time.sleep(5)
    drone.move_down(50)




def main():
    drone = tello.Tello()
    #basic_flight(drone)
    FlightStreamTest(drone)

if __name__ == "__main__":
    main()
