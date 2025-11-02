
Include "airfoil.geo";
//+

ymax = 4;
xmax = 10;
n_inlet = 60;
n_vertical = 90;
r_vertical = 1/0.95;
n_airfoil = 50;
n_wake = 100;
r_wake = 1/0.95;

//+
Point(149) = {-0.5, ymax, 0, 1.0};
//+
Point(150) = {-0.5, -ymax, 0, 1.0};
//+
Point(151) = {1, ymax, 0, 1.0};
//+
Point(152) = {1, -ymax, 0, 1.0};
//+
Point(153) = {xmax, ymax, 0, 1.0};
//+
Point(154) = {xmax, -ymax, 0, 1.0};
//+
Point(155) = {xmax, 0, 0, 1.0};
//+
Circle(2) = {150, 75, 149};
//+
Line(3) = {66, 149};
//+
Line(4) = {84, 150};
//+
Line(5) = {149, 151};
//+
Line(6) = {150, 152};
//+
Line(7) = {151, 153};
//+
Line(8) = {152, 154};
//+
Line(9) = {155, 154};
//+
Line(10) = {155, 153};
//+
Line(11) = {1, 151};
//+
Line(12) = {1, 152};
//+
Line(13) = {1, 155};
//+
Split Curve {1} Point {66, 84};
//+
Split Curve {15} Point {1};
//+
Transfinite Curve {2, 14} = n_inlet Using Progression 1;
//+
Transfinite Curve {3, 11, 10, 4, 12, 9} = n_vertical Using Progression r_vertical;
//+
Transfinite Curve {17, 16} = n_airfoil Using Bump 0.1;
//+
Transfinite Curve {5, 6} = n_airfoil Using Bump 2;
//+
Transfinite Curve {13} = n_wake Using Progression r_wake;
//+
Transfinite Curve {7, 8} = n_wake Using Bump 0.2;
//+
Curve Loop(1) = {2, -3, 14, 4};
//+
Plane Surface(1) = {1};
//+
Curve Loop(2) = {3, 5, -11, 17};
//+
Plane Surface(2) = {2};
//+
Curve Loop(3) = {11, 7, -10, -13};
//+
Plane Surface(3) = {3};
//+
Curve Loop(4) = {4, 6, -12, -16};
//+
Plane Surface(4) = {4};
//+
Curve Loop(5) = {12, 8, -9, -13};
//+
Plane Surface(5) = {5};
//+
Transfinite Surface {1};
//+
Transfinite Surface {2};
//+
Transfinite Surface {3};
//+
Transfinite Surface {4};
//+
Transfinite Surface {5};
//+
Recombine Surface {1, 2, 3, 4, 5};
//+//+
Physical Curve("farfield", 18) = {2, 5, 7, 10, 9, 8, 6};
//+
Physical Curve("airfoil", 19) = {17, 16, 14};
