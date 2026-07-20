from colorPicker import run_picker
from mask import run_mask

print("Starting")

current_state = "calibrate" 

while True:

    if current_state == "calibrate":
        print("--- Opening Color Picker ---")

        run_picker() 
        
        current_state = "tracking"
        
        
    elif current_state == "tracking":
        print("--- Opening Tracker ---")
        
        needs_recalibration = run_mask() 
        
        if needs_recalibration == True:
            current_state = "calibrate"
        
        else:
            print("Shutting down")
            break