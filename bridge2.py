import subprocess
import random

def clear_terminal():
    subprocess.call('clear', shell=True)


class Sims():
    def __init__(self):
        self.instruction_list = []
        # Add flags here (check Drake to see supported flags)
        self.instruction_list.append("bazel run drake/automotive:demo --")
        self.instruction_list.append(" --dragway_length=1000")
        self.instruction_list.append(" --num_maliput_railcar=2")
        self.instruction_list.append(" --num_dragway_lanes=")
        self.instruction_list.append(" --driving_command_gui_names=0")
        self.instruction_list.append(" --simulation_sec=")
        self.instruction_list.append(" --maliput_start_s_offset=")
        self.instruction_list.append(" --maliput_start_speed_offset=")
        # include lane index support


    def add_instruction_args(self, num_lanes, sim_time, position_offset,
                             speed_offset):
        self.instruction_list[3] += str(num_lanes)
        self.instruction_list[5] += str(sim_time)
        self.instruction_list[6] += str(position_offset)
        self.instruction_list[7] += str(speed_offset)

    def gen_simulation(self, num_lanes, sim_time, position_offset,
                       speed_offset):
        self.add_instruction_args(num_lanes, sim_time, position_offset,
                                  speed_offset)

        # BUILDING the FULL instruction
        instruction = self.instruction_list[0]
        for i in range(1, len(self.instruction_list)):
            instruction += self.instruction_list[i]

        # cmd line execution of the instruction
        # simulation_instance = subprocess.Popen(instruction, shell=True)
        # simulation_instance.wait()

        # simulation_instance = subprocess.call(instruction, shell=True)
        # print "return value is " + str(simulation_instance) + "\n"

    def gen_simulation_file(self, num_lanes, sim_time, car_info, total_cars):
        # write values to a file
        with open("/tmp/drake-dryvr/sim1.txt", 'w') as f:
            # write some meta-data into the file such as number of numbers, and a random number
            format_number = "1 "
            random_number = random.randint(1000,10000)

            f.write(format_number)
            f.write(str(random_number) + " ")

            # write header info for general commands such as num_of_lanes, sim_time etc...
            f.write(str(num_lanes) + " ")
            f.write(str(sim_time) + " ")
            f.write(str(total_cars) + " ")

            # info
            for i in range(len(car_info)):
                f.write(str(car_info[i].car_type) + " ")
                f.write(str(car_info[i].car_number) + " ")
                f.write(str(car_info[i].position_offset) + " ")
                f.write(str(car_info[i].speed_offset) + " ")
                f.write(str(car_info[i].lane_number) + " ")
        f.close()

    def gen_simulation_wrapper(self, num_lanes, sim_time, car_info, total_cars):
        self.gen_simulation(num_lanes, sim_time, car_info[0].position_offset,
                       car_info[0].speed_offset)
        self.gen_simulation_file(num_lanes, sim_time, car_info, total_cars)

class car_sim_info():
    def __init__(self):
        self.car_number = 0
        self.car_type = -1 # 0 for maliput, 1 for mobil, 2 for mobil2, 3 for mobil3
        self.position_offset = -1
        self.speed_offset = -1
        self.lane_number = -1




def main():
    clear_terminal()

    main_numlanes = 0
    main_sim_time = 0
    all_cars = []
    total_cars = 0

    i_or_f = -1
    ff = -1

    while i_or_f <0 or i_or_f > 1:
        i_or_f = input("Instantiate simulation through interface(0) or file(1)? ")

    if i_or_f == 1:
        while ff < 0 or ff > 1:
            ff = input("\nNew file(0) or previous file(1)? ")

        if ff == 0:
            #while valid_file:
            #    sim_file = input("\n")
            return
        else:
            return

    while total_cars <= 0:
        print "\nHow many cars do you want to populate your simulation with,"
        print "how many lanes do you want present on the dragway and"
        print "for how long do you want to run the simulation?"
        total_cars = input("\nEnter valid total number of cars (>0): ")
        if total_cars <=0:
            clear_terminal()

    while main_numlanes <= 0:
        main_numlanes = input("Enter valid number of lanes (>0): ")
    while main_sim_time <= 0:
        main_sim_time = input("Enter valid simulation time(in seconds) (>0): ")

    for i in range(1, total_cars+1):
        print "\nEnter info for car " + str(i)

        inp = car_sim_info()
        inp.car_number = i-1

        while inp.car_type <0 or inp.car_type >3:
            inp.car_type = input("Enter valid car type (0 - maliput, 1 - mobil, 2 - mobil2, 3 - mobil3): ")
        while inp.position_offset < 0:
            inp.position_offset = input("Enter valid position offset (>=0): ")
        while inp.speed_offset < 0:
            inp.speed_offset = input("Enter valid speed offset (>=0): ")
        while inp.lane_number < 0 or inp.lane_number >= main_numlanes:
            inp.lane_number = input("Enter valid lane number (0 till num_lanes-1): ")
            # if inp.lane_number >= main_numlanes:
            #     #print "INVALID lane number, please enter again!"
            #     inp.lane_number = -1
            # try:
            #     choice = int(raw_input("Enter choice 1, 2 or 3:"))
            #     if not (1 <= choice <= 3):
            #         raise ValueError()
            # except ValueError:
            #     print "Invalid Option, you needed to type a 1, 2 or 3...."
            # else:
            #     print "Your choice is", choice
        all_cars.append(inp)


    print "\nBEGINNING SIMULATION\n"
    # all the simulation info is in list all_cars, main_numlanes, main_sim_time
    scenario = Sims()
    scenario.gen_simulation_wrapper(main_numlanes, main_sim_time, all_cars, total_cars)



if __name__ == '__main__':
    main()
