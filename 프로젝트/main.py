from OpenGL.GL import *
from glfw.GLFW import *
import glm

import input_callback
import shader
import vao
import camera
import obj_loader

# 상수
BACKGROUND_COLOR = 63/255
WIN_WIDTH = 1200
WIN_HEIGHT = 1200

def main():
    # initialize glfw
    if not glfwInit():
        return
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3)   # OpenGL 3.3
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3)
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)  # Do not allow legacy OpenGl API calls

    # create a window and OpenGL context
    window = glfwCreateWindow(WIN_WIDTH, WIN_HEIGHT, '2021027329', None, None)
    if not window:
        glfwTerminate()
        return
    glfwMakeContextCurrent(window)

    # register event callbacks
    callback = input_callback.Callback(window)

    # load shaders
    shader_lighting = shader.load_shaders(shader.g_vertex_shader_src_lighting, shader.g_fragment_shader_src_lighting)
    unif_names = ['MVP', 'M', 'view_pos', 'material_color']
    unif_locs_lighting = {}
    for name in unif_names:
        unif_locs_lighting[name] = glGetUniformLocation(shader_lighting, name)

    shader_color = shader.load_shaders(shader.g_vertex_shader_src_color, shader.g_fragment_shader_src_color)
    unif_names = ['MVP']
    unif_locs_color = {}
    for name in unif_names:
        unif_locs_color[name] = glGetUniformLocation(shader_color, name)

    # prepare vaos
    vao_xzframe = vao.prepare_vao_xzframe()
    vao_grid = vao.prepare_vao_grid()

    # 배경색 밝은 회색으로
    glClearColor(BACKGROUND_COLOR, BACKGROUND_COLOR, BACKGROUND_COLOR, 1.0)    

    cam = camera.Camera()

    vao_meshs = []

    glDisable(GL_CULL_FACE)

    # loop until the user closes the window
    while not glfwWindowShouldClose(window):
        
        # 새로 들어온 vao가 있는지 확인, 한번만 prepare 해주기 위해 다음과 같은 과정
        for meshs in obj_loader.obj_meshs:
            if meshs['isVao'] == False:
                VAO = vao.prepare_vao_mesh(meshs['vertices'], meshs['indices'])
                vao_meshs.append({
                    'VAO': VAO,
                    'size' : len(meshs['indices'])
                })
        obj_loader.obj_meshs.clear()

        # camera callback 처리
        if callback.mouse_pressed:
            mov_x = callback.mov_x
            mov_y = callback.mov_y
            if (GLFW_KEY_LEFT_ALT in callback.keys) and (GLFW_KEY_LEFT_SHIFT in callback.keys):
                # Pan
                cam.pan(mov_x, mov_y)
            elif (GLFW_KEY_LEFT_ALT in callback.keys) and (GLFW_KEY_LEFT_CONTROL in callback.keys):
                # Zoom
                cam.zoom(mov_y)
            elif GLFW_KEY_LEFT_ALT in callback.keys: # Orbit을 맨 마지막 순서에 놓아야 Pan이 제대로 작동 가능
                # Orbit
                cam.orbit(mov_x, mov_y)
                # print("Orbit 됨")
            V = cam.return_matrix_V()

        callback.mov_x = 0
        callback.mov_y = 0

        # enable depth test (we'll see details later)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)

        # projection matrix
        # use orthogonal projection (we'll see details later)
        aspect =  WIN_WIDTH / WIN_HEIGHT
        P = glm.perspective(glm.radians(45), aspect, 1, 100)

        # view matrix
        # rotate camera position with g_cam_ang / move camera up & down with g_cam_height
        V = cam.return_matrix_V()
        
        # draw world frame, xz축
        glUseProgram(shader_color)
        MVP = P*V
        glUniformMatrix4fv(unif_locs_color['MVP'], 1, GL_FALSE, glm.value_ptr(MVP))
        glLineWidth(1.5) # 선 너비 설정, 상수가 너무 많으니 일단 냅두고 나중에 constant.py 따로 만드는 게 나을듯?
        glBindVertexArray(vao_xzframe)
        glDrawArrays(GL_LINES, 0, 4)
        
        # xz평면의 격자선
        glLineWidth(0.8)
        glBindVertexArray(vao_grid)
        glDrawArrays(GL_LINES, 0, 8*vao.G_GRID_SIZE)

        # set view_pos uniform in shader_lighting
        glUseProgram(shader_lighting)
        eye = cam.get_eye()
        glUniform3f(unif_locs_lighting['view_pos'], eye.x, eye.y, eye.z)
        
        # obj 그리기

        num = 0
        for meshs in vao_meshs:
            vao_id = meshs['VAO']
            size = meshs['size']

            M = glm.translate(glm.mat4(), glm.vec3(num*2,0,0))
            MVP = P*V*M
            glUniformMatrix4fv(unif_locs_lighting['MVP'], 1, GL_FALSE, glm.value_ptr(MVP))
            glUniformMatrix4fv(unif_locs_lighting['M'], 1, GL_FALSE, glm.value_ptr(M))
            matcolor = glm.vec3(.5,.5,.5)
            glUniform3f(unif_locs_lighting['material_color'], matcolor.r, matcolor.g, matcolor.b)

            glBindVertexArray(vao_id)
            glDrawElements(GL_TRIANGLES, size, GL_UNSIGNED_INT, None)

            num+=1

        # swap front and back buffers
        glfwSwapBuffers(window)

        # poll events
        glfwPollEvents()
        
    # terminate glfw
    glfwTerminate()

if __name__ == "__main__":
    main()
