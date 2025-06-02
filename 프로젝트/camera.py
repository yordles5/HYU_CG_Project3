import glm

PAN_SPEED = 0.003
ZOOM_SPEED = 0.003
ORBIT_SPEED = 0.2

CAM_TARGET = glm.vec3(0,0,0)
CAM_DIST = 10.
CAM_AZI = 20
CAM_ELE = 30

class Camera:
    # 속성
    def __init__(self):
        # dist, azim, elev 세개로 카메라의 eye 즉 위치를 구할 수 있음.
        self.dist = CAM_DIST # distance, 구면좌표계에서 r에 해당
        self.azi = CAM_AZI # azimuth, 구면좌표계에서 세타에 해당, 카메라를 xz평면에 정사영 한 것과 z축 사이의 각도
        self.ele = CAM_ELE # elevation, 구면좌표계에서 90'-파이에 해당, 카메라를 xz평면에 정사영 한 것과 카메라 벡터 사이의 각도

        self.target = CAM_TARGET
        self.up = glm.vec3(0,1,0)
        
        # 아래 네 값은 _upadata_camera_eye 메소드를 통해 업데이트 될 것
        self.eye = glm.vec3(0,0,0)
        self.w = glm.vec3(0,0,0)
        self.u = glm.vec3(0,0,0)
        self.v = glm.vec3(0,0,0)

        self._update_camera_eye()

    # 메소드
    def _update_camera_eye(self): # private 메소드
        # glm.cos이나 glm.sin은 라디안 값을 받음
        radi_azi = glm.radians(self.azi)
        radi_ele = glm.radians(self.ele)

        # 구면좌표계 -> 직교좌표계 변환
        x = self.dist * glm.cos(radi_ele) * glm.sin(radi_azi)
        y = self.dist * glm.sin(radi_ele)
        z = self.dist * glm.cos(radi_ele) * glm.cos(radi_azi)

        # eye 업데이트, 했으면 바로 frame까지 업데이트  
        self.eye = glm.vec3(x, y, z) + self.target
        self._update_camera_frame()

    def _update_camera_frame(self): # private 메소드
        # w, u, v 벡터 갱신
        self.w = glm.normalize(self.eye - self.target)
        self.u = glm.normalize(glm.cross(self.up, self.w))
        self.v = glm.normalize(glm.cross(self.w, self.u))

    def orbit(self, mov_x, mov_y):
        self.azi += ORBIT_SPEED * mov_x
        self.ele += ORBIT_SPEED * mov_y
        self.ele = max(-89, min(89, self.ele)) # elevation 값이 너무 튀면 화면이 나가는 현상 발생 
        self._update_camera_eye()

    def pan(self, mov_x, mov_y):
        self.target += -PAN_SPEED * mov_x * self.u + PAN_SPEED * mov_y * self.v
        self._update_camera_eye()

    def zoom(self, mov_y):
        self.dist += ZOOM_SPEED * mov_y
        self.dist = max(0.1, self.dist) # zoom 너무 깊게 안 되게
        self._update_camera_eye()

    def return_matrix_V(self):
        return glm.lookAt(self.eye, self.target, self.up)
    
    def get_eye(self):
        return self.eye