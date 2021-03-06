# Conjuntos
set BANCOS;
set NODOS;

# Parametros
param n; #cantidad de bancos
param COSTO{i in NODOS, j in NODOS};
param MONTOS{i in NODOS};
param Dinero_Inicial;
param Dinero_Maximo;
param M:=100000;
/* set conexiones */
set E, within NODOS cross NODOS;

/* x[i,j] = 1 si va de i a j */
var x{ i in NODOS, j in NODOS}, binary;
var dinero_acumulado{i in BANCOS};
var U{ i in BANCOS }, integer;

/* minimizar distancias */
minimize total: sum{i in NODOS, j in NODOS} COSTO[i,j] * x[i,j];

/* el camion sale de todas las ciudades */
s.t. sale{i in NODOS}: sum{j in NODOS: i!=j } x[i,j] = 1;

/* el camion entra a todas las ciudades */
s.t. entra{j in NODOS}: sum{i in NODOS: i!=j} x[i,j] = 1;

/* Para cerrar el grafo*/
s.t. orden{i in BANCOS, j in BANCOS: i!=j }: U[i] - U[j] + n * x[i,j] <= n-1;

/*El orden de las ciudades va de 1 a 10*/
s.t. valoresU{i in BANCOS}: 10 >= U[i] >= 1;

/*Restriccion entre lo inicial y todos los bancos debe sumar un valor val*/
s.t. dineroTotalMaximo: Dinero_Maximo >= sum{i in NODOS} MONTOS[i] + Dinero_Inicial >= 0;
/*Restriccion acumulado*/
s.t. rest_Din_acum{i in BANCOS }: Dinero_Maximo >= dinero_acumulado[i] >= 0;

/*MODELO 3*/
/*Defino acumulado[i]*/
s.t. dineroSiguienteMenor{i in BANCOS, j in BANCOS: i != j }: -M*(1 - x[i,j]) <= dinero_acumulado[i] + MONTOS[i] - dinero_acumulado[j];

s.t. dineroSiguienteMayor{i in BANCOS, j in BANCOS: i != j }: dinero_acumulado[i] + MONTOS[i] - dinero_acumulado[j] <= ( 1 - x[i,j])*M;

solve;

printf "Camino recorrido %d\n",
   sum{i in NODOS, j in NODOS} COSTO[i,j] * x[i,j];

printf "Ciudad - Orden - Dinero_acumulado:\n";
printf{i in BANCOS} " %s \t %d \t %d \n", i, U[i], dinero_acumulado[i] + MONTOS[i];

end;