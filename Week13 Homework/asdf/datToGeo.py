import gmsh
import math

gmsh.initialize()
gmsh.model.add("NACA0012_Structured")

# ==========================================
# 1. 설정 (Configuration)
# ==========================================
chord = 1.0
R_far = 20.0 * chord  # 원거리장 반지름

# 격자 개수 설정 (User Request: 401 x 145)
# 에어포일은 윗면/아랫면으로 나누므로 절반씩 할당합니다.
# 점이 401개면 구간(Interval)은 400개입니다. -> 위 200칸, 아래 200칸
n_circum = 201  # 윗면 점 개수 (아랫면도 동일) -> 합치면 중복 제외 401개
n_radial = 145  # 벽면 수직 방향 점 개수

# 경계층 격자 조밀도 (Progression)
# 1.0이면 등간격, 1.1이면 10%씩 늘어남. CFD를 위해 1.05~1.1 추천
progression_radial = 1.08 

# ==========================================
# 2. 형상 생성 (Geometry)
# ==========================================
def naca0012_y(x):
    t = 0.12
    return 5 * t * (0.2969 * math.sqrt(x) - 0.1260 * x - 0.3516 * x**2 + 0.2843 * x**3 - 0.1015 * x**4)

# 주요 포인트 생성
# P1: Leading Edge (0,0)
# P2: Trailing Edge (1,0)
# P3: Farfield Leading Edge (-R, 0)
# P4: Farfield Trailing Edge (R+1, 0) - O-Grid를 위해 원형으로 배치

p_le = gmsh.model.geo.addPoint(0, 0, 0)
p_te = gmsh.model.geo.addPoint(chord, 0, 0)

# Farfield (원형) 포인트
p_far_le = gmsh.model.geo.addPoint(-R_far, 0, 0)
p_far_te = gmsh.model.geo.addPoint(chord + R_far, 0, 0)
p_far_top = gmsh.model.geo.addPoint(0.5*chord, R_far, 0)
p_far_bot = gmsh.model.geo.addPoint(0.5*chord, -R_far, 0)
p_center = gmsh.model.geo.addPoint(0.5*chord, 0, 0) # 원호 중심용

# --- 에어포일 곡선 생성 (Spline) ---
# 윗면 점들 계산
pts_upper = [p_le]
n_pts_gen = 100 # 스플라인 생성을 위한 임시 점 개수
for i in range(1, n_pts_gen - 1):
    x = chord * (1 - math.cos(i * math.pi / (n_pts_gen - 1))) / 2 # Cosine spacing
    y = naca0012_y(x)
    pts_upper.append(gmsh.model.geo.addPoint(x, y, 0))
pts_upper.append(p_te)

# 아랫면 점들 계산
pts_lower = [p_le]
for i in range(1, n_pts_gen - 1):
    x = chord * (1 - math.cos(i * math.pi / (n_pts_gen - 1))) / 2
    y = -naca0012_y(x)
    pts_lower.append(gmsh.model.geo.addPoint(x, y, 0))
pts_lower.append(p_te)

# 라인 생성
l_airfoil_upper = gmsh.model.geo.addSpline(pts_upper)
l_airfoil_lower = gmsh.model.geo.addSpline(pts_lower)

# --- Farfield 곡선 생성 (Circle Arc) ---
# O-Grid 형태를 만들기 위해 반원 2개로 나눕니다.
l_far_upper_1 = gmsh.model.geo.addCircleArc(p_far_te, p_center, p_far_top)
l_far_upper_2 = gmsh.model.geo.addCircleArc(p_far_top, p_center, p_far_le)
l_far_upper = gmsh.model.geo.addCompoundSpline([l_far_upper_1, l_far_upper_2]) # 하나로 합침

l_far_lower_1 = gmsh.model.geo.addCircleArc(p_far_le, p_center, p_far_bot)
l_far_lower_2 = gmsh.model.geo.addCircleArc(p_far_bot, p_center, p_far_te)
l_far_lower = gmsh.model.geo.addCompoundSpline([l_far_lower_1, l_far_lower_2])

# --- 연결 선 (Connector) ---
# LE와 Farfield_LE 연결, TE와 Farfield_TE 연결
l_inlet = gmsh.model.geo.addLine(p_le, p_far_le)
l_outlet = gmsh.model.geo.addLine(p_te, p_far_te)

# --- 표면(Surface) 생성 ---
# 윗면 영역 (Loop)
loop_upper = gmsh.model.geo.addCurveLoop([l_airfoil_upper, l_outlet, -l_far_upper, -l_inlet])
surf_upper = gmsh.model.geo.addPlaneSurface([loop_upper])

# 아랫면 영역 (Loop)
loop_lower = gmsh.model.geo.addCurveLoop([l_airfoil_lower, l_outlet, l_far_lower, -l_inlet])
surf_lower = gmsh.model.geo.addPlaneSurface([loop_lower])


# ==========================================
# 3. 격자 제어 (Transfinite / Structured)
# ==========================================

# (1) 에어포일 표면 & Farfield (401 포인트 관련)
# 상/하 각각 201개 점 -> 합치면 공유점 제외하고 401개 대응
gmsh.model.geo.mesh.setTransfiniteCurve(l_airfoil_upper, n_circum, "Bump", 0.2) # LE/TE 조밀하게
gmsh.model.geo.mesh.setTransfiniteCurve(l_airfoil_lower, n_circum, "Bump", 0.2)
gmsh.model.geo.mesh.setTransfiniteCurve(l_far_upper, n_circum)
gmsh.model.geo.mesh.setTransfiniteCurve(l_far_lower, n_circum)

# (2) 반경 방향 (145 포인트 관련)
# Progression을 주어 벽면에 격자를 몰아줍니다.
gmsh.model.geo.mesh.setTransfiniteCurve(l_inlet, n_radial, "Progression", 1.0/progression_radial) 
gmsh.model.geo.mesh.setTransfiniteCurve(l_outlet, n_radial, "Progression", progression_radial)

# (3) 표면을 사각형 격자(Transfinite)로 설정
gmsh.model.geo.mesh.setTransfiniteSurface(surf_upper)
gmsh.model.geo.mesh.setRecombine(2, surf_upper) # Quad(사각형)로 변환

gmsh.model.geo.mesh.setTransfiniteSurface(surf_lower)
gmsh.model.geo.mesh.setRecombine(2, surf_lower) # Quad(사각형)로 변환

gmsh.model.geo.synchronize()

# ==========================================
# 4. Physical Groups (SU2용)
# ==========================================
# SU2_CFD에서 사용할 마커 이름
gmsh.model.addPhysicalGroup(1, [l_airfoil_upper, l_airfoil_lower], name="AIRFOIL")
gmsh.model.addPhysicalGroup(1, [l_far_upper, l_far_lower], name="FARFIELD")
gmsh.model.addPhysicalGroup(2, [surf_upper, surf_lower], name="FLUID")

# ==========================================
# 5. 생성 및 저장
# ==========================================
gmsh.model.mesh.generate(2)

# 격자 품질 최적화 (선택사항)
gmsh.model.mesh.optimize("Netgen")

# SU2 호환성을 위해 포맷 지정
gmsh.option.setNumber("Mesh.MshFileVersion", 2.2)
gmsh.write("naca0012_structured_401x145.msh")

# GUI 확인 (필요시 주석 해제)
# gmsh.fltk.run()

gmsh.finalize()