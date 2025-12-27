'''
Docstring for end_time_predictor
TODO
 - Add frontend
 - 
'''

import sys, logging, os
from mat_velocity_predictor import mat_velocity_predictor
from load_time_calculator import load_time_calculator


logger = logging.getLogger(__name__)

def clear_terminal():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')
        
def delete_lines(n):
    for _ in range(n):
        sys.stdout.write("\x1b[1A")
        sys.stdout.write("\x1b[2K")
        sys.stdout.flush()
    
def main(argv=None):
    logger.info("##### STARTED PREDICTOR #####\n")
    
    clear_terminal()
    
    # parser = argparse.ArgumentParser(
    #     description="Fetch boutsPerHourReport with JSESSIONID cookie"
    # )
    # parser.add_argument("--jsessionid", "-c", help="Value of JSESSIONID cookie")
    # parser.add_argument("--event-id", type=int, required=True, help="eventId")
    # parser.add_argument("--start-time", required=True, help="Start time of day in HH:MM format")
    # parser.add_argument("--bouts", type=int, default=20, required=True, help="Number of total bouts for the day")
    
    # parser.add_argument("--division-ids", type=int, default=-1, help="divisionIds (default: -1)")
    # parser.add_argument("--host", default="172.16.28.210:9090", help="host:port (default: 172.16.28.210:9090)")
    # parser.add_argument("--prepare-only", action="store_true", help="Do not send; print the prepared request")
    # parser.add_argument("--timeout", type=int, default=20, help="Request timeout seconds (default: 20)")

    # args = parser.parse_args(argv)
    # logger.info(f"Arguments detected: {args}\n")

    # jsid = args.jsessionid
    # if not jsid:
    #     jsid = input(
    #         "Enter JSESSIONID (from Application -> Cookies -> JSESSIONID): \n"
    #     ).strip()

    print(r"""
 __  __     ______     ______   __     __   __     ______     ______   ______     ______    
/\ \/ /    /\  __ \   /\  == \ /\ \   /\ "-.\ \   /\  __ \   /\__  _\ /\  __ \   /\  == \   
\ \  _"-.  \ \  __ \  \ \  _-/ \ \ \  \ \ \-.  \  \ \  __ \  \/_/\ \/ \ \ \/\ \  \ \  __<   
 \ \_\ \_\  \ \_\ \_\  \ \_\    \ \_\  \ \_\\"\_\  \ \_\ \_\    \ \_\  \ \_____\  \ \_\ \_\ 
  \/_/\/_/   \/_/\/_/   \/_/     \/_/   \/_/ \/_/   \/_/\/_/     \/_/   \/_____/   \/_/ /_/ 

""")
    while True:
        print(r"""Select a tool:
(1) Mat Velocity Predictor
(2) Load Time Calculator
(3) Exit
""")
        cmd = int(input("> "))
        line_count = 1
        while cmd < 1 or cmd > 3:
            delete_lines(line_count)
            print(f"Invalid option: {cmd}\nPlease select a valid tool.")
            cmd = int(input("> "))
            line_count = 3
        
        delete_lines(5 + line_count)
        if cmd == 1:
            mat_velocity_predictor()
        elif cmd == 2:
            load_time_calculator()
        elif cmd == 3:
            print("Goodbye!")
            exit(1)
            
        delete_lines(6)
        # IN WEB INTERFACE: dropdown for date epoch @ 00:00:00    
        
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
    
