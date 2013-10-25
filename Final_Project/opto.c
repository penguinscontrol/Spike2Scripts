/* Created by Language version: 6.2.0 */
/* NOT VECTORIZED */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "scoplib.h"
#undef PI
 
#include "md1redef.h"
#include "section.h"
#include "md2redef.h"

#if METHOD3
extern int _method3;
#endif

#undef exp
#define exp hoc_Exp
extern double hoc_Exp();
 
#define _threadargscomma_ /**/
#define _threadargs_ /**/
 	/*SUPPRESS 761*/
	/*SUPPRESS 762*/
	/*SUPPRESS 763*/
	/*SUPPRESS 765*/
	 extern double *getarg();
 static double *_p; static Datum *_ppvar;
 
#define t nrn_threads->_t
#define dt nrn_threads->_dt
#define i _p[0]
#define gchr2 _p[1]
#define flux _p[2]
#define No1 _p[3]
#define No2 _p[4]
#define Nc1 _p[5]
#define Nc2 _p[6]
#define DNo1 _p[7]
#define DNo2 _p[8]
#define DNc1 _p[9]
#define DNc2 _p[10]
#define _g _p[11]
#define irr	*_ppvar[0]._pval
#define _p_irr	_ppvar[0]._pval
 
#if MAC
#if !defined(v)
#define v _mlhv
#endif
#if !defined(h)
#define h _mlhh
#endif
#endif
 static int hoc_nrnpointerindex =  0;
 /* external NEURON variables */
 /* declaration of user functions */
 static int _hoc_rates();
 static int _hoc_vtrap();
 static int _mechtype;
extern int nrn_get_mechtype();
 extern void _nrn_setdata_reg(int, void(*)(Prop*));
 static void _setdata(Prop* _prop) {
 _p = _prop->param; _ppvar = _prop->dparam;
 }
 static _hoc_setdata() {
 Prop *_prop, *hoc_getdata_range();
 _prop = hoc_getdata_range(_mechtype);
   _setdata(_prop);
 ret(1.);
}
 /* connect user functions to hoc names */
 static IntFunc hoc_intfunc[] = {
 "setdata_opto", _hoc_setdata,
 "rates_opto", _hoc_rates,
 "vtrap_opto", _hoc_vtrap,
 0, 0
};
#define vtrap vtrap_opto
 extern double vtrap();
 /* declare global and static user variables */
#define N N_opto
 double N = 10;
#define U1 U1_opto
 double U1 = 15;
#define U0 U0_opto
 double U0 = 40;
#define e e_opto
 double e = 8;
#define epsilon2 epsilon2_opto
 double epsilon2 = 0.12;
#define epsilon1 epsilon1_opto
 double epsilon1 = 0.5;
#define e21 e21_opto
 double e21 = 0;
#define e12 e12_opto
 double e12 = 0;
#define go2 go2_opto
 double go2 = 1;
#define go1 go1_opto
 double go1 = 10;
#define gchr2_max gchr2_max_opto
 double gchr2_max = 0.036;
#define kr kr_opto
 double kr = 0.002;
#define kd2 kd2_opto
 double kd2 = 0.05;
#define kd1 kd1_opto
 double kd1 = 0.1;
#define ka2 ka2_opto
 double ka2 = 0;
#define ka1 ka1_opto
 double ka1 = 0;
#define sigma sigma_opto
 double sigma = 1e-08;
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "gchr2_max_opto", "S",
 "sigma_opto", "1/J",
 "kd1_opto", "/ms",
 "kd2_opto", "/ms",
 "U0_opto", "mV",
 "U1_opto", "mV",
 "go1_opto", "S",
 "go2_opto", "S",
 "kr_opto", "/ms",
 "e_opto", "mV",
 "ka1_opto", "/ms",
 "ka2_opto", "/ms",
 "e12_opto", "/ms",
 "e21_opto", "/ms",
 "i_opto", "mA/cm2",
 "gchr2_opto", "S/cm2",
 "flux_opto", "/ms",
 "irr_opto", "mW",
 0,0
};
 static double Nc20 = 0;
 static double Nc10 = 0;
 static double No20 = 0;
 static double No10 = 0;
 static double delta_t = 0.01;
 static double v = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 "gchr2_max_opto", &gchr2_max_opto,
 "epsilon1_opto", &epsilon1_opto,
 "epsilon2_opto", &epsilon2_opto,
 "sigma_opto", &sigma_opto,
 "kd1_opto", &kd1_opto,
 "kd2_opto", &kd2_opto,
 "U0_opto", &U0_opto,
 "U1_opto", &U1_opto,
 "go1_opto", &go1_opto,
 "go2_opto", &go2_opto,
 "kr_opto", &kr_opto,
 "N_opto", &N_opto,
 "e_opto", &e_opto,
 "ka1_opto", &ka1_opto,
 "ka2_opto", &ka2_opto,
 "e12_opto", &e12_opto,
 "e21_opto", &e21_opto,
 0,0
};
 static DoubVec hoc_vdoub[] = {
 0,0,0
};
 static double _sav_indep;
 static void nrn_alloc(), nrn_init(), nrn_state();
 static void nrn_cur(), nrn_jacob();
 
static int _ode_count(), _ode_map(), _ode_spec(), _ode_matsol();
 
#define _cvode_ieq _ppvar[1]._i
 /* connect range variables in _p that hoc is supposed to know about */
 static char *_mechanism[] = {
 "6.2.0",
"opto",
 0,
 "i_opto",
 "gchr2_opto",
 "flux_opto",
 0,
 "No1_opto",
 "No2_opto",
 "Nc1_opto",
 "Nc2_opto",
 0,
 "irr_opto",
 0};
 
static void nrn_alloc(_prop)
	Prop *_prop;
{
	Prop *prop_ion, *need_memb();
	double *_p; Datum *_ppvar;
 	_p = nrn_prop_data_alloc(_mechtype, 12, _prop);
 	/*initialize range parameters*/
 	_prop->param = _p;
 	_prop->param_size = 12;
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 2, _prop);
 	_prop->dparam = _ppvar;
 	/*connect ionic variables to this model*/
 
}
 static _initlists();
  /* some states have an absolute tolerance */
 static Symbol** _atollist;
 static HocStateTolerance _hoc_state_tol[] = {
 0,0
};
 _opto_reg() {
	int _vectorized = 0;
  _initlists();
 	register_mech(_mechanism, nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init, hoc_nrnpointerindex, 0);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
     _nrn_setdata_reg(_mechtype, _setdata);
  hoc_register_dparam_size(_mechtype, 2);
 	hoc_register_cvode(_mechtype, _ode_count, _ode_map, _ode_spec, _ode_matsol);
 	hoc_register_tolerance(_mechtype, _hoc_state_tol, &_atollist);
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 opto /cygdrive/c/Users/JuanandKimi/Desktop/NEURON 7.3/Final_Project/opto.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
static int _reset;
static char *modelname = "";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static _modl_cleanup(){ _match_recurse=1;}
static rates();
 
static int _ode_spec1(), _ode_matsol1();
 static int _slist1[4], _dlist1[4];
 static int states();
 
/*CVODE*/
 static int _ode_spec1 () {_reset=0;
 {
   rates ( _threadargs_ ) ;
   DNo1 = ka1 * Nc1 - ( kd1 + e12 ) * No1 + e21 * No2 ;
   DNo2 = ka2 * Nc2 - ( kd2 + e21 ) * No2 + e12 * No1 ;
   DNc2 = kd2 * No2 - ( ka2 + kr ) * Nc2 ;
   DNc1 = kd1 * No1 - ka1 * Nc1 + kr * Nc2 ;
   }
 return _reset;
}
 static int _ode_matsol1 () {
 rates ( _threadargs_ ) ;
 DNo1 = DNo1  / (1. - dt*( ( - (( kd1 + e12 ))*(1.0) ) )) ;
 DNo2 = DNo2  / (1. - dt*( ( - (( kd2 + e21 ))*(1.0) ) )) ;
 DNc2 = DNc2  / (1. - dt*( ( - (( ka2 + kr ))*(1.0) ) )) ;
 DNc1 = DNc1  / (1. - dt*( ( - (ka1)*(1.0) ) )) ;
}
 /*END CVODE*/
 static int states () {_reset=0;
 {
   rates ( _threadargs_ ) ;
    No1 = No1 + (1. - exp(dt*(( - (( kd1 + e12 ))*(1.0) ))))*(- ( (ka1)*(Nc1) + (e21)*(No2) ) / ( ( - (( kd1 + e12 ))*(1.0)) ) - No1) ;
    No2 = No2 + (1. - exp(dt*(( - (( kd2 + e21 ))*(1.0) ))))*(- ( (ka2)*(Nc2) + (e12)*(No1) ) / ( ( - (( kd2 + e21 ))*(1.0)) ) - No2) ;
    Nc2 = Nc2 + (1. - exp(dt*(( - (( ka2 + kr ))*(1.0) ))))*(- ( (kd2)*(No2) ) / ( ( - (( ka2 + kr ))*(1.0)) ) - Nc2) ;
    Nc1 = Nc1 + (1. - exp(dt*(( - (ka1)*(1.0) ))))*(- ( (kd1)*(No1) + (kr)*(Nc2) ) / ( ( - (ka1)*(1.0)) ) - Nc1) ;
   }
  return 0;
}
 
static int  rates (  )  {
    e12 = .011 + 0.005 * log ( flux / 0.024 ) ;
   e21 = 0.008 + 0.004 * log ( flux / 0.024 ) ;
   ka1 = epsilon1 * flux ;
   ka2 = epsilon2 * flux ;
     return 0; }
 
static int _hoc_rates() {
  double _r;
   _r = 1.;
 rates (  ) ;
 ret(_r);
}
 
double vtrap (  _lx , _ly )  
	double _lx , _ly ;
 {
   double _lvtrap;
 if ( fabs ( _lx / _ly ) < 1e-6 ) {
     _lvtrap = _ly * ( 1.0 - _lx / _ly / 2.0 ) ;
     }
   else {
     _lvtrap = _lx / ( exp ( _lx / _ly ) - 1.0 ) ;
     }
   
return _lvtrap;
 }
 
static int _hoc_vtrap() {
  double _r;
   _r =  vtrap (  *getarg(1) , *getarg(2) ) ;
 ret(_r);
}
 
static int _ode_count(_type) int _type;{ return 4;}
 
static int _ode_spec(_NrnThread* _nt, _Memb_list* _ml, int _type) {
   Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
     _ode_spec1 ();
 }}
 
static int _ode_map(_ieq, _pv, _pvdot, _pp, _ppd, _atol, _type) int _ieq, _type; double** _pv, **_pvdot, *_pp, *_atol; Datum* _ppd; { 
 	int _i; _p = _pp; _ppvar = _ppd;
	_cvode_ieq = _ieq;
	for (_i=0; _i < 4; ++_i) {
		_pv[_i] = _pp + _slist1[_i];  _pvdot[_i] = _pp + _dlist1[_i];
		_cvode_abstol(_atollist, _atol, _i);
	}
 }
 
static int _ode_matsol(_NrnThread* _nt, _Memb_list* _ml, int _type) {
   Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
 _ode_matsol1 ();
 }}

static void initmodel() {
  int _i; double _save;_ninits++;
 _save = t;
 t = 0.0;
{
  Nc2 = Nc20;
  Nc1 = Nc10;
  No2 = No20;
  No1 = No10;
 {
   rates ( _threadargs_ ) ;
   No1 = 0.0 ;
   No2 = 0.0 ;
   Nc1 = N ;
   Nc2 = 0.0 ;
   }
  _sav_indep = t; t = _save;

}
}

static void nrn_init(_NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; double _v; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
#if EXTRACELLULAR
 _nd = _ml->_nodelist[_iml];
 if (_nd->_extnode) {
    _v = NODEV(_nd) +_nd->_extnode->_v[0];
 }else
#endif
 {
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 }
 v = _v;
 initmodel();
}}

static double _nrn_current(double _v){double _current=0.;v=_v;{ {
    flux = irr * sigma * ( 1e6 ) ;
     gchr2 = gchr2_max * ( No1 / N + ( go2 / go1 ) * No2 / N ) * ( 1.0 - exp ( - ( v + 8.0 ) / U0 ) ) / ( ( v + 8.0 ) / U1 ) ;
   i = gchr2 * ( v + 8.0 ) ;
    }
 _current += i;

} return _current;
}

static void nrn_cur(_NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; int* _ni; double _rhs, _v; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
#if EXTRACELLULAR
 _nd = _ml->_nodelist[_iml];
 if (_nd->_extnode) {
    _v = NODEV(_nd) +_nd->_extnode->_v[0];
 }else
#endif
 {
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 }
 _g = _nrn_current(_v + .001);
 	{ _rhs = _nrn_current(_v);
 	}
 _g = (_g - _rhs)/.001;
#if CACHEVEC
  if (use_cachevec) {
	VEC_RHS(_ni[_iml]) += _rhs;
  }else
#endif
  {
	NODERHS(_nd) += _rhs;
  }
#if EXTRACELLULAR
 if (_nd->_extnode) {
   *_nd->_extnode->_rhs[0] += _rhs;
 }
#endif
 
}}

static void nrn_jacob(_NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml];
 _nd = _ml->_nodelist[_iml];
#if CACHEVEC
  if (use_cachevec) {
	VEC_D(_ni[_iml]) -= _g;
  }else
#endif
  {
	NODED(_nd) -= _g;
  }
#if EXTRACELLULAR
 if (_nd->_extnode) {
   *_nd->_extnode->_d[0] += _g;
 }
#endif
 
}}

static void nrn_state(_NrnThread* _nt, _Memb_list* _ml, int _type){
 double _break, _save;
Node *_nd; double _v; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
 _nd = _ml->_nodelist[_iml];
#if EXTRACELLULAR
 _nd = _ml->_nodelist[_iml];
 if (_nd->_extnode) {
    _v = NODEV(_nd) +_nd->_extnode->_v[0];
 }else
#endif
 {
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 }
 _break = t + .5*dt; _save = t;
 v=_v;
{
 { {
 for (; t < _break; t += dt) {
 error =  states();
 if(error){fprintf(stderr,"at line 71 in file opto.mod:\n	\n"); nrn_complain(_p); abort_run(error);}
 
}}
 t = _save;
 }}}

}

static terminal(){}

static _initlists() {
 int _i; static int _first = 1;
  if (!_first) return;
 _slist1[0] = &(No1) - _p;  _dlist1[0] = &(DNo1) - _p;
 _slist1[1] = &(No2) - _p;  _dlist1[1] = &(DNo2) - _p;
 _slist1[2] = &(Nc2) - _p;  _dlist1[2] = &(DNc2) - _p;
 _slist1[3] = &(Nc1) - _p;  _dlist1[3] = &(DNc1) - _p;
_first = 0;
}
