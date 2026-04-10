int: n;
array[1..n] of int: len;
array[1..n] of int: dep;
array[1..n] of int: hei;

int: X_SUM = sum(len);
int: Y_SUM = sum(dep);
int: Z_SUM = sum(hei);


int: X_LB = max(len);
int: Y_LB = max(dep);
int: Z_LB = max(hei);

int: X_UB = 3* X_SUM  ;
int: Y_UB = 3* Y_SUM  ;
int: Z_UB = 3* Z_SUM  ;

array[1..n] of var 0..X_UB: x;
array[1..n] of var 0..Y_UB: y;
array[1..n] of var 0..Z_UB: z;

var X_LB..X_UB : X;
var Y_LB..Y_UB : Y;
var Z_LB..Z_UB : Z ;


array[1..n,1..n] of var bool: bx;
array[1..n,1..n] of var bool: by;
array[1..n,1..n] of var bool: bz;

%init disjunction
constraint forall(i in 1..n) (
    bx[i,i] = false /\
    by[i,i] = false /\
    bz[i,i] = false
);

%end
constraint forall(i in 1..n) (
    x[i] + len[i] <= X /\
    y[i] + dep[i] <= Y /\
    z[i] + hei[i] <= Z
);

%disjunctions
constraint forall(i, j in 1..n where i != j) (
    (bx[i,j] -> x[i] + len[i] <= x[j]) /\
    (by[i,j] -> y[i] + dep[i] <= y[j]) /\
    (bz[i,j] -> z[i] + hei[i] <= z[j])
);

%At least one disjunction per pair
constraint forall(i, j in 1..n where i < j) (
    bx[i,j] \/ bx[j,i] \/
    by[i,j] \/ by[j,i] \/
    bz[i,j] \/ bz[j,i]
);

%implied constraints on the disjunctions
constraint forall(i, j in 1..n where i < j) (
    not (bx[i,j] /\ bx[j,i])
);
constraint forall(i, j in 1..n where i < j) (
    not (by[i,j] /\ by[j,i])
);
constraint forall(i, j in 1..n where i < j) (
    not (bz[i,j] /\ bz[j,i])
);




int: Scenario_1 = X_SUM + max(dep) + max(hei) ;
int: Scenario_2 = max(len)  + Y_SUM + max(hei) ;
int: Scenario_3 = max(len)   + max(dep) + Z_SUM ;

int: O_LB = X_LB + Y_LB + Z_LB;
int: O_UB = min([Scenario_1, Scenario_2, Scenario_3]);



var O_LB .. O_UB: V;
constraint V = X + Y + Z;


solve
    :: int_search(
        [x[i] | i in 1..n] ++ [y[i] | i in 1..n] ++ [z[i] | i in 1..n],
        first_fail,
        indomain_split
    )
    minimize V;

output
[
  "X = " ++ show(X) ++ "\n" ++
  "Y = " ++ show(Y) ++ "\n" ++
  "Z = " ++ show(Z) ++ "\n" ++
  "V = " ++ show(V) ++ "\n\n"
]
++
[
  "box " ++ show(i) ++
  ": x=" ++ show(x[i]) ++
  " y=" ++ show(y[i]) ++
  " z=" ++ show(z[i]) ++ "\n"
  | i in 1..n
];
