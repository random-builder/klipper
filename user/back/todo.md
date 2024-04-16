
###

M201 X9000 Y9000 Z500 E10000 ; sets maximum accelerations, mm/sec^2
M203 X500 Y500 Z12 E120 ; sets maximum feedrates, mm/sec
M204 P1500 R1500 T1500 ; sets acceleration (P, T) and retract acceleration (R), mm/sec^2
M205 X10.00 Y10.00 Z0.20 E2.50 ; sets the jerk limits, mm/sec
M205 S0 T0 ; sets the minimum extruding and travel feed rate, mm/sec

### TODO

Send: N2 M201 X9000 Y9000 Z500 E10000*56
Recv: // Unknown command:"M201"
Recv: ok
Send: N3 M203 X500 Y500 Z12 E120*15
Recv: // Unknown command:"M203"
Recv: ok
Send: N4 M204 P1500 R1500 T1500*83
Recv: ok
Send: N5 M205 X10.00 Y10.00 Z0.20 E2.50*58
Recv: // Unknown command:"M205"
Recv: ok
Send: N6 M205 S0 T0*37
Recv: // Unknown command:"M205"
