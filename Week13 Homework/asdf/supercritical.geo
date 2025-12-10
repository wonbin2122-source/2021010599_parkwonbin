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
Point(85) = {-0.5, ymax, 0, 1.0};
//+
Point(86) = {-0.5, -ymax, 0, 1.0};
//+
Point(87) = {1, ymax, 0, 1.0};
//+
Point(88) = {1, -ymax, 0, 1.0};
//+
Point(89) = {xmax, ymax, 0, 1.0};
//+
Point(90) = {xmax, -ymax, 0, 1.0};
//+
Point(91) = {xmax, 0, 0, 1.0};
//+
//+
Circle(3) = {86, 40, 85};
//+
Line(4) = {26, 85};
//+
Line(5) = {53, 86};
//+
Line(6) = {86, 88};
//+
Line(7) = {85, 87};
//+
Line(8) = {81, 88};
//+
Line(9) = {81, 87};
//+
Line(10) = {87, 89};
//+
Line(11) = {88, 90};
//+
Line(12) = {91, 90};
//+
Line(13) = {91, 89};
//+
Line(14) = {91, 81};
//+
Split Curve {1} Point {26, 53};
//+
Transfinite Curve {3, 16} = n_inlet Using Progression 1;
//+
Transfinite Curve {4, 9, 13, 5, 8, 12} = n_vertical Using Progression r_vertical;
//+
Transfinite Curve {7, 15, 2, 17, 6} = n_airfoil Using Progression 1;
//+
Transfinite Curve {10, 14, 11} = n_wake Using Progression r_wake;
//+
Curve Loop(1) = {3, -4, 16, 5};
//+
Plane Surface(1) = {1};
//+
Curve Loop(2) = {4, 7, -9, 2, 15};
//+
Plane Surface(2) = {2};
//+
Curve Loop(3) = {5, 6, -8, -17};
//+
Plane Surface(3) = {3};
//+
Curve Loop(4) = {8, 11, -12, 14};
//+
Plane Surface(4) = {4};
//+
Curve Loop(5) = {9, 10, -13, 14};
//+
Plane Surface(5) = {5};
//+
Transfinite Surface {1};
//+
Transfinite Surface {2};
//+
Transfinite Surface {5};
//+
Transfinite Surface {4};
//+
Transfinite Surface {3};
//+
Recombine Surface {1, 2, 5, 4, 3};
//+
Physical Curve("farfield", 18) = {3, 6, 7, 10, 13, 12, 11};
//+
Physical Curve("airfoil", 19) = {16, 15, 17, 2};
