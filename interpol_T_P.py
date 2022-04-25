#!/usr/bin/env python
# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sympy as sp
# 0. Datos de entrada en formato de texto o csv.
data = pd.read_csv("table.csv")
data

# 1. A manera de ejemplo, tomaremos 3 puntos y hallaremos el polinomio de Lagrange asociado a dichos puntos (P vs T). Así mismo hallaremos el polinomio asociado por sympy. +10 puntos.
x = sp.Symbol("x")
x_data = data["T"][:3].values
y_data = data["P"][:3].values
poly = sp.polys.polyfuncs.interpolating_poly(3,x,X=x_data,Y=y_data).simplify()
print("Polinomio 3 primeros puntos P vs T: ",poly)

# 2. Tabla Interpolación de P vs T, utilizando valores intermedios de temperatura. Para esto generalice el programa del punto 1. +15
# 3. Tabla Interpolación de sg vs T.+5
# 4. Tabla Interpolación de sf vs T.+5
def interpolation_table(x_var,y_var,dx=1e-2):
    x = sp.Symbol("x")
    x_table = []
    y_table = []
    i = 0
    while i < len(data)-1:
        j = 3 if i+3 < len(data) else 2
        x_data = data[x_var][i:i+j].values
        y_data = data[y_var][i:i+j].values
        poly = sp.polys.polyfuncs.interpolating_poly(j,x,X=x_data,Y=y_data)
        f = sp.lambdify(x,poly)
        x_table.append(np.arange(min(x_data),max(x_data),dx))
        y_table.append(f(x_table[-1]))
        
        i+=j-1
    
    x_table = np.concatenate(x_table)
    y_table = np.concatenate(y_table)
    return np.array([x_table,y_table]).T

for var in ["P","sg","sf"]:
    table = interpolation_table("T",var)
    np.savetxt(f"{var}vsT.dat",table,fmt='%.10f')
    print(f"guardada tabla interpolación {var}vsT.dat")

# 5. Gráficas en formato png. Los ejes deben aparecer debidamente identificados y el tamaño de las etiquetas debe ser visible. +10
for var in ["P","sg","sf"]:
    table = np.loadtxt(f"{var}vsT.dat")
    plt.figure(dpi=150)
    plt.plot(*table.T,label="interpolation")
    plt.scatter(data["T"],data[var],s=10,c='k',label="data")
    plt.ylabel(var,fontsize=15)
    plt.xlabel("T",fontsize=15)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{var}vsT.png")
    plt.close()
    print(f"guardado {var}vsT.png")

# 6. Análisis de resultados y conclusiones. +5

# Se hicieron tablas de interpolación polinomial de orden 3 para tres varaibles (P, sg, sf) 
# con respecto a la temperatura, obteniendo una gráfica suave.
#     Los polinomios de Lagrange fueron obtenidos con sympy, y luego evaluados en puntos 
# intermedios con una resolución de temperatura de 1e-2.
#     Todo este trabajo se hubiera podido hacer mucho más fácilmente con scipy.interpolate.interp1d
