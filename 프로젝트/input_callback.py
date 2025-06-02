from glfw.GLFW import *
from obj_loader import load_obj

class Callback:
    def __init__(self, window):
        # public, 얘내 세개는 main.py에서 쓸 수 있음
        self.mov_x = 0 
        self.mov_y = 0
        self.keys = set()  # 키보드 뭐 입력했는지, 여러 키가 동시에 눌린 걸 판단하기 위해 set으로
        self.mouse_pressed = False # 마우스 클릭했는지
        
        # private
        self._prev_cursor = (0,0) # 드래그 시작 지점 커서 위치, 드래그 시작 때만 업뎃

        self._register_callback(window)
    # 메소드
    def _register_callback(self, window):
        glfwSetKeyCallback(window, self._key_callback)
        glfwSetMouseButtonCallback(window, self._mouse_button_callback)
        glfwSetCursorPosCallback(window, self._cursor_position_callback)
        glfwSetDropCallback(window, self._drop_callback)
    
    def _key_callback(self, window, key, scancode, action, mods):
        if key==GLFW_KEY_ESCAPE and action==GLFW_PRESS:
            glfwSetWindowShouldClose(window, GLFW_TRUE)
        else:
            if action==GLFW_PRESS:
                self.keys.add(key)
            elif action == GLFW_RELEASE:
                self.keys.discard(key)

    def _mouse_button_callback(self, window, button, action, mods):
        if button == GLFW_MOUSE_BUTTON_LEFT:
            if action == GLFW_PRESS:
                self.mouse_pressed = True
                self._prev_cursor = glfwGetCursorPos(window) # 마우스 드래그를 할 때 첫 클릭 시점에 prev 값 초기화해줘야 함. 
            elif action == GLFW_RELEASE:
                self.mouse_pressed = False

    def _cursor_position_callback(self, window, xpos, ypos):
        if self.mouse_pressed == False: # 오버헤드 방지
            return 
        curr_cursor = (xpos, ypos)
        self.mov_x = curr_cursor[0] - self._prev_cursor[0]
        self.mov_y = curr_cursor[1] - self._prev_cursor[1]
        self._prev_cursor = curr_cursor  

    def _drop_callback(self, window, paths):
        for path in paths:
            load_obj(path)



