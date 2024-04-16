
SET_GCODE_OFFSET Z=-0.1 MOVE=1

###

Send: G29
Recv: // auto home
Recv: // Sending BLTOUCH_DEBUG COMMAND=reset
Recv: // auto level
Recv: // probe at -0.000,4.000 is z=1.003125
Recv: // probe at 50.000,4.000 is z=0.990625
Recv: // probe at 100.000,4.000 is z=0.963750
Recv: // probe at 150.000,4.000 is z=0.971250
Recv: // probe at 200.000,4.000 is z=0.986250
Recv: // probe at 200.000,41.500 is z=1.091875
Recv: // probe at 150.000,41.500 is z=1.075000
Recv: // probe at 100.000,41.500 is z=1.067500
Recv: // probe at 50.000,41.500 is z=1.103125
Recv: // probe at -0.000,41.500 is z=1.085000
Recv: // probe at -0.000,79.000 is z=1.142500
Recv: // probe at 50.000,79.000 is z=1.161250
Recv: // probe at 100.000,79.000 is z=1.118125
Recv: // probe at 150.000,79.000 is z=1.145000
Recv: // probe at 200.000,79.000 is z=1.138750
Recv: // probe at 200.000,116.500 is z=1.156875
Recv: // probe at 150.000,116.500 is z=1.157500
Recv: // probe at 100.000,116.500 is z=1.165000
Recv: // probe at 50.000,116.500 is z=1.165625
Recv: // probe at -0.000,116.500 is z=1.148125
Recv: // probe at -0.000,154.000 is z=1.112500
Recv: // probe at 50.000,154.000 is z=1.158750
Recv: // probe at 100.000,154.000 is z=1.176250
Recv: // probe at 150.000,154.000 is z=1.180000
Recv: // probe at 200.000,154.000 is z=1.149375
Recv: // Mesh Bed Leveling Complete
Recv: // Bed Mesh state has been saved to profile [default]
Recv: // for the current session.  The SAVE_CONFIG command will
Recv: // update the printer config file and restart the printer.
Recv: ok
[...]
Send: G0 X100 Y100 Z0
Recv: ok
[...]
Send: GET_POSITION
Recv: // mcu: stepper_x:14 stepper_y:-6 stepper_z:9
Recv: // stepper: stepper_x:100.000000 stepper_y:100.000000 stepper_z:-0.213750
Recv: // kinematic: X:100.000000 Y:100.000000 Z:-0.213750
Recv: // toolhead: X:100.000000 Y:100.000000 Z:-0.213832 E:0.000000
Recv: // gcode: X:100.000000 Y:100.000000 Z:0.000000 E:0.000000
Recv: // gcode base: X:0.000000 Y:0.000000 Z:0.000000 E:0.000000
Recv: // gcode homing: X:0.000000 Y:0.000000 Z:0.000000
Recv: ok
[...]
Send: SET_GCODE_OFFSET Z=0.2
Recv: ok
[...]
Send: GET_POSITION
Recv: // mcu: stepper_x:14 stepper_y:-6 stepper_z:9
Recv: // stepper: stepper_x:100.000000 stepper_y:100.000000 stepper_z:-0.213750
Recv: // kinematic: X:100.000000 Y:100.000000 Z:-0.213750
Recv: // toolhead: X:100.000000 Y:100.000000 Z:-0.213832 E:0.000000
Recv: // gcode: X:100.000000 Y:100.000000 Z:0.000000 E:0.000000
Recv: // gcode base: X:0.000000 Y:0.000000 Z:0.200000 E:0.000000
Recv: // gcode homing: X:0.000000 Y:0.000000 Z:0.200000
Recv: ok
