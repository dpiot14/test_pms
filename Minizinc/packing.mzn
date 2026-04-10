% Starter MiniZinc model for the 3D packing exercise.

% Data provided by the .dzn instance.
% n is the number of boxes.
int: n;
% len[i], dep[i], and hei[i] are the dimensions of box i.
array[1..n] of int: len;
array[1..n] of int: dep;
array[1..n] of int: hei;



% Decision variables: (x[i], y[i], z[i]) is the position of one corner of box i.
% Replace `var` with explicit integer domains.
array[1..n] of var int: x;
array[1..n] of var int: y;
array[1..n] of var int: z;

% X, Y, and Z are the dimensions of the enclosing container.
% Give them meaningful lower and upper bounds.

var int: X;
var int: Y;
var int: Z;


% Objective variable: minimize the sum of the container dimensions.
var int: V;
constraint V = X + Y + Z;


solve
    minimize V;



% Keep the output format below unchanged.
% The helper scripts parse the exact labels `X`, `Y`, `Z`, `V`, and `box i: ...`.
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
