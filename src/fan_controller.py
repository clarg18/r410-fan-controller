import psutil
from os import system
from time import sleep
from datetime import datetime

class FanController:
    """
    Class to control the speed of system fans on a dell r410 11th gen rack mount server.
    """

    def __init__(self, fan_curve=lambda temp: int(temp ** 3 / 6000)):
        self.status = 0
        self.cpu_temp_history = {}
        self.previous_speed = ""
        self.fan_curve = fan_curve

        print(datetime.now().strftime("%H:%M:%S") + ": Setting fans to manual control")
        self.__run_ipmi_command("raw 0x30 0x30 0x01 0x00")

    def exec(self, test_temp=False):
        if test_temp:
            current_avg_cpu_temp = test_temp
        else:
            current_avg_cpu_temp = self.__get_cpu_temp()

        if current_avg_cpu_temp >= 70 and self.status == 0:
            print(datetime.now().strftime("%H:%M:%S") + ": System too hot, suspending manual fan control.")
            self.__set_fan_control_mode(1)
            self.previous_speed = 'auto'
        elif current_avg_cpu_temp < 70 and self.status == 1:
            print(datetime.now().strftime("%H:%M:%S") + ": Resuming manual fan control")
            self.__set_fan_control_mode(0)
            self.__sef_set_system_fan_speed(current_avg_cpu_temp)
        else:
            self.__sef_set_system_fan_speed(current_avg_cpu_temp)

    def get_status(self):
        return self.status

    def __run_ipmi_command(self, cmd):
        system(f"ipmitool {cmd}")

    def __get_cpu_temp(self):
        cpu_temps = []
        for sensor in psutil.sensors_temperatures()["coretemp"]:
            cpu_temps.append(sensor.current)
        avg_cpu_temps = int(round(sum(cpu_temps) / len(cpu_temps), 0))
        return avg_cpu_temps

    def __set_fan_control_mode(self, mode):
        if mode == 1 and self.status == 0:
            self.__run_ipmi_command("raw 0x30 0x30 0x01 0x01")
            self.status = 1
        elif mode == 0 and self.status == 1:
            self.__run_ipmi_command("raw 0x30 0x30 0x01 0x00")
            self.status = 0

    def __sef_set_system_fan_speed(self, temp):
        speed_to_set = self.fan_curve(temp)
        if speed_to_set > 8:
            speed = hex(speed_to_set)
        else:
            speed = hex(8)
        if speed != self.previous_speed:
            self.__run_ipmi_command(f"raw 0x30 0x30 0x02 0xff {str(speed)}")
            self.previous_speed = speed
            print(datetime.now().strftime("%H:%M:%S") + ": Setting fan speed to " + str(speed)
                  + ". Current temp: " + str(temp))


if __name__ == '__main__':
    sleep_time = 5
    fc = FanController()

    while True:
        fc.exec()
        sleep(sleep_time)
