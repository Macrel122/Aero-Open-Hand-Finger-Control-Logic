# This specific test serves to allow the user limited control over the Aero hand fingers.
# A = thumb
# Up = 2nd finger
# Down = 3rd finger
# Left = 4th finger
# Right = 5th finger

import time
from aero_open_sdk.aero_hand import AeroHand

try:
    from pynput import keyboard
except ModuleNotFoundError:
    raise SystemExit(
        "\nERROR: 'pynput' is not installed.\n"
        "Install it using:\n"
        "    pip install pynput\n"
    )

class KeyboardController:
    def __init__(self):
        self.grasped = False
        self.state = 0

        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def on_press(self, key):
        try:
            if key == keyboard.Key.up:
                self.state = 1
                # state 1
            elif key == keyboard.Key.down:
                self.state = 2
                # state 2
            elif key == keyboard.Key.left:
                self.state = 3
                # state 3
            elif key == keyboard.Key.right:
                self.state = 4
                # state 4
            elif key == keyboard.Key.space:
                self.state = 5
                # state 5
        except Exception:
            # Don't let any error in the listener kill the program
            pass

def main():
    hand = AeroHand("/dev/cu.usbmodem11401")

    idle = [100.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    pose1 = [100.0, 0.0, 0.0, 50.0, 0.0, 0.0, 0.0]
    pose2 = [100.0, 0.0, 0.0, 0.0, 50.0, 0.0, 0.0]
    pose3 = [100.0, 0.0, 0.0, 0.0, 0.0, 50.0, 0.0]
    pose4 = [100.0, 0.0, 0.0, 0.0, 0.0, 0.0, 50.0]
    pose5 = [100.0, 50.0, 50.0, 0.0, 0.0, 0.0, 0.0]

    controller = KeyboardController()
    speed = 80  # from 0 to 32766
    torque = 400  # from 0 to 1000
    for i in range(7):
        # Manual setting of speed and torque is optional. 
        # When not set, the speed and torque are what was set last time.
        # When you reboot the hand (power off and on), the speed and torque are reset back to the default values.
        # The default speed is 32766 and the default torque is 1000.
        hand.set_speed(i, speed)
        time.sleep(0.01)
        hand.set_torque(i, torque)
        time.sleep(0.01)

    try:
        while True:
            if controller.state == 0:
                hand.set_joint_positions(idle)
            elif controller.state == 1:
                hand.set_joint_positions(pose1)
            elif controller.state == 2:
                hand.set_joint_positions(pose2)
            elif controller.state == 3:
                hand.set_joint_positions(pose3)
            elif controller.state == 4:
                hand.set_joint_positions(pose4)
            elif controller.state == 5:
                hand.set_joint_positions(pose5)
            time.sleep(0.01)
    except KeyboardInterrupt:
        controller.listener.stop()
        # Set the joint positions to 0 when the program is interrupted.
        hand.set_joint_positions([0.0] * 16)
        hand.close()
        print("Joint positions set to 0")


if __name__ == "__main__":
    main() 
