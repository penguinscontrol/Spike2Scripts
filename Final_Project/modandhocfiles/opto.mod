: 4 state model of optogenetics

NEURON {
	SUFFIX opto
	USEION na WRITE ina
	RANGE gchr2
	GLOBAL ka1, ka2, e12, e21
}

UNITS {
	(S)  = (siemens)
	(mV) = (millivolt)
	(mA) = (milliamp)
}

PARAMETER {
	gchr2 = 0.036  (S/cm2)
	epsilon1  = 0.5    
	epsilon2  = 0.12   
	kd1   = 0.1    (/ms)
	kd2   = 0.05   (/ms)
	U0    = 40     (mV)
	U1    = 15     (mV)
	go1   = 100     (S/cm2) :WRONG
	go2   = 1      (S/cm2) :WRONG
	flux = 5 (/ms)
	kr =.002(/ms)
	N =10
	e = 8 (mV)
}

ASSIGNED {
	v  (mV)
	:e(mV)
	ina  (mA/cm2)
	ka1 (/ms)
	ka2 (/ms)
	e12 (/ms)
	e21  (/ms)
}

STATE {
	No1
	No2
	Nc1
	Nc2
}

INITIAL{
	rates(v)
	No1=0
	No2=0
	Nc1=N
	Nc2=0	
}

BREAKPOINT{
	SOLVE states METHOD cnexp
	UNITSOFF
	gchr2=(No1/N + (go2/go1)*No2/N)*(1-exp(-(v+8)/U0))/((v+8)/U1)
	UNITSON
	ina  = gchr2*(v+8)
	
}

DERIVATIVE states{
rates(v)
No1'= ka1*Nc1-(kd1+e12)*No1+e21*No2
No2'= ka2*Nc2-(kd2+e21)*No2+e12*No1
Nc2' = kd2*No2-(ka2+kr)*Nc2
Nc1' = kd1*No1-ka1*Nc1 +kr*Nc2
}

UNITSOFF

PROCEDURE rates(v(mV)) {  :Computes rate and other constants at current v.
                      :Call once from HOC to initialize inf at resting v.
		e12=.011+0.005*log(flux/0.024)
		e21=0.008+0.004*log(flux/0.024)	
		ka1=epsilon1*flux
		ka2=epsilon2*flux
		}
		
FUNCTION vtrap(x,y) {  :Traps for 0 in denominator of rate eqns.
        if (fabs(x/y) < 1e-6) {
                vtrap = y*(1 - x/y/2)
        }else{
                vtrap = x/(exp(x/y) - 1)
        }
}
UNITSON

