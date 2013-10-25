: Light Stimulation

NEURON{
	POINT_PROCESS LitClamp
	RANGE del, dur, amp, irr
}

UNITS {
	(mW) = (milliwatt)
	(um) = (micrometer)
	(J)  = (joule)
	(kW) = (kilowatt)
}

PARAMETER {
	del (ms)
	dur (ms) <0, 1e9>
	amp (mW)
}

ASSIGNED {
	irr (mW)
}

INITIAL{
	irr = 1e-20
}

BREAKPOINT{
	at_time(del)
	at_time(del+dur)
	
	if(t<del+dur && t>del) {
		irr=amp
		} 
	else {
		irr=1e-20
	}
}
