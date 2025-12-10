import numpy as np
import os

# 1. 경로 설정 (파일 위치 자동 찾기)
script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, 'airfoil.dat')
output_path = os.path.join(script_dir, 'airfoil.geo')

# 2. 데이터 읽기 및 분리
print(f"읽는 중: {input_path}")
try:
    data = np.loadtxt(input_path, skiprows=3) # 헤더가 3줄이라고 가정
except Exception as e:
    print(f"데이터 읽기 실패: {e}")
    exit()

# 데이터 반으로 나누기 (NACA 데이터 구조 가정)
# 보통 데이터가 [Trailing Edge -> Leading Edge -> Trailing Edge] 순서라고 가정
split_idx = len(data) // 2
top_data = data[:split_idx]       # 윗면 (또는 아랫면)
bottom_data = data[split_idx:]    # 아랫면 (또는 윗면)

# 3. Geo 파일 작성 시작
print(f"쓰는 중: {output_path}")
f = open(output_path, 'w')

# 격자 사이즈 변수 (나중에 Gmsh에서 수정 가능)
lc = 0.1 

top_indices = []
bottom_indices = []
point_counter = 1

# --- [1] 점(Point) 생성 ---

# 윗면 점 찍기
f.write("// Upper Surface Points\n")
for pt in top_data:
    # Gmsh 문법: Point(ID) = {x, y, z, lc};
    f.write(f"Point({point_counter}) = {{{pt[0]}, {pt[1]}, 0, {lc}}};\n")
    top_indices.append(point_counter)
    point_counter += 1

# 아랫면 점 찍기
f.write("\n// Lower Surface Points\n")
for pt in bottom_data:
    f.write(f"Point({point_counter}) = {{{pt[0]}, {pt[1]}, 0, {lc}}};\n")
    bottom_indices.append(point_counter)
    point_counter += 1

# --- [2] 선(Spline & Line) 생성 ---

# 리스트를 콤마로 구분된 문자열로 변환 (예: "1, 2, 3, 4")
top_str = ", ".join(map(str, top_indices))
bottom_str = ", ".join(map(str, bottom_indices))

f.write("\n// Lines and Splines\n")

# 윗면 스플라인 (Spline)
# 곡선이므로 Spline 사용
f.write(f"Spline(1) = {{{top_str}}};\n")

# 아랫면 스플라인 (Spline)
f.write(f"Spline(2) = {{{bottom_str}}};\n")

# 뒷전 (Trailing Edge) 직선 (Line)
# 윗면의 시작점과 아랫면의 끝점을 직선으로 연결
# (데이터 순서에 따라 인덱스는 달라질 수 있으나, 보통 양 끝단을 연결하면 됨)
te_start = top_indices[0]   # 윗면 데이터의 첫 점 (보통 TE)
te_end = bottom_indices[-1] # 아랫면 데이터의 끝 점 (보통 TE)

# 두 점이 같은 위치가 아닐 경우에만 선을 생성 (닫힌 뒷전 방지)
f.write(f"Line(3) = {{{te_end}, {te_start}}};\n")

f.close()
print("변환 완료! airfoil.geo 파일에 Spline과 Line이 생성되었습니다.")