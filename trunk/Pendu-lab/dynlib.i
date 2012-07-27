%module dynlib
%{
#include "dynlib.h"
#include <matrix.h>
#include "Meschach/matrix.h"


%}


%typemap(in) MAT* {
  static MAT *res;
  int i,j;
  double dat;

  int n = PyList_Size($input);
  int m = PyList_Size(PyList_GetItem($input,0));
  /*res = m_get(n,m);*/
  m_resize_vars(n,m,&res,NULL);
  mem_stat_reg_vars(0,TYPE_MAT,&res,NULL);
  for(i=0;i<n;i++) {
    for(j=0;j<m;j++) {
      dat = PyFloat_AsDouble(PyList_GetItem(PyList_GetItem($input,i),j));
      res->me[i][j]=dat;
    }
  }
  $1= res;
}

%typemap(out) MAT* {
  PyObject *res;
  PyObject *fila;
  int i,j;
  double dat;

  int n = $1->m;
  int m = $1->n;

  res = PyList_New(n);
  for(i=0;i<n;i++) {
    fila = PyList_New(m);
    for(j=0;j<m;j++) {
      dat = $1->me[i][j];
      PyList_SetItem(fila,j,PyFloat_FromDouble(dat));
    }
    PyList_SetItem(res,i,fila);
  }
  $result= res;
}

%typemap(in) VEC* {
  static VEC *res;
  int i;
  double dat;

  int n = PyList_Size($input);

  if (REAL == DOUBLE) {
    v_resize_vars(n,&res,NULL);
    mem_stat_reg_vars(0,TYPE_VEC,&res,NULL);
    for(i=0;i<n;i++) {
      dat = PyFloat_AsDouble(PyList_GetItem($input,i));
      res->ve[i]=dat;
    }
  }
  $1 = res;
}


%typemap(out) VEC* {
  PyObject *res;
  int i;
  double dat;

  int n = $1->dim;

  if (REAL == DOUBLE) {
    res = PyList_New(n);
    for(i=0;i<n;i++) {
      dat = $1->ve[i];
      PyList_SetItem(res,i,PyFloat_FromDouble(dat));
    }
  }
  $result = res;
}
void odesolver(MAT* SimParam,MAT* X,int i,MAT *u);
void dynmodel(MAT* SimParam,MAT* X,int i,double Tau,VEC* out);
void controller(MAT* SimParam,MAT* X,int i,int ui,double *Tau,VEC* out);
void swing_up(MAT* SimParam,MAT* X,int i,int ui,double *Tau,VEC* out);
double dcmotors(MAT *SimParam,double u,MAT* X,int i);
MAT *dyncorec(MAT *SimParam,MAT *X,MAT *u);
void odefunc(MAT* SimParam,MAT* X,int i,MAT *u,int ui,VEC* out);
