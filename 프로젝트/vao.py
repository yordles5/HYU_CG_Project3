from OpenGL.GL import *
from glfw.GLFW import *
import glm
import ctypes

G_GRID_SIZE = 0

def prepare_vao_mesh(vertices, index):
    # 이미 잘 구성된 vertices와 index 리스트가 파라미터로 주어질 것이라 가정
    
    vertices_array = glm.array(glm.float32, *vertices)
    indices = glm.array(glm.uint32, *index)

    # create and activate VAO & VBO
    VAO = glGenVertexArrays(1)  # create a vertex array object ID and store it to VAO variable
    glBindVertexArray(VAO)      # activate VAO
    VBO = glGenBuffers(1)   # create a buffer object ID and store it to VBO variable
    glBindBuffer(GL_ARRAY_BUFFER, VBO)  # activate VBO as a vertex buffer object

    # create and activate EBO (element buffer object)
    EBO = glGenBuffers(1)   # create a buffer object ID and store it to EBO variable
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)  # activate EBO as an element buffer objec

    # copy vertex data to VBO
    glBufferData(GL_ARRAY_BUFFER, vertices_array.nbytes, vertices_array.ptr, GL_STATIC_DRAW) # allocate GPU memory for and copy vertex data to the currently bound vertex buffer

    # copy index data to EBO
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices.ptr, GL_STATIC_DRAW) # allocate GPU memory for and copy index data to the currently bound element buffer

    # configure vertex positions
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * glm.sizeof(glm.float32), None)
    glEnableVertexAttribArray(0)

    # configure vertex normals
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * glm.sizeof(glm.float32), ctypes.c_void_p(3*glm.sizeof(glm.float32)))
    glEnableVertexAttribArray(1)

    return VAO


def prepare_vao_xzframe():
    # 상수
    AXIS_LIMIT = 10 # xz축, 격자선 최대 길이
    X_COLOR = (98/255, 136/255, 41/255) # x축 색상
    Z_COLOR = (152/255, 61/255, 74/255) # z축 색상
    # prepare vertex data (in main memory)
    vertices = glm.array(glm.float32,
        # position        # color
        -AXIS_LIMIT, 0.0, 0.0,   *X_COLOR, # x-axis start
         AXIS_LIMIT, 0.0, 0.0,   *X_COLOR, # x-axis end 
         0.0, 0.0, -AXIS_LIMIT,  *Z_COLOR, # z-axis start
         0.0, 0.0,  AXIS_LIMIT,  *Z_COLOR, # z-axis end 
    )

    # create and activate VAO (vertex array object)
    VAO = glGenVertexArrays(1)  # create a vertex array object ID and store it to VAO variable
    glBindVertexArray(VAO)      # activate VAO

    # create and activate VBO (vertex buffer object)
    VBO = glGenBuffers(1)   # create a buffer object ID and store it to VBO variable
    glBindBuffer(GL_ARRAY_BUFFER, VBO)  # activate VBO as a vertex buffer object

    # copy vertex data to VBO
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices.ptr, GL_STATIC_DRAW) # allocate GPU memory for and copy vertex data to the currently bound vertex buffer

    # configure vertex positions
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * glm.sizeof(glm.float32), None)
    glEnableVertexAttribArray(0)

    # configure vertex colors
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * glm.sizeof(glm.float32), ctypes.c_void_p(3*glm.sizeof(glm.float32)))
    glEnableVertexAttribArray(1)

    # 바인딩 해제하는 게 안전하대서 추가함
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    return VAO

def prepare_vao_grid():
    global G_GRID_SIZE

    # 상수 지역변수에 저장
    GRID_COLOR = (80/255, 80/255, 80/255) # 격자 색상
    AXIS_LIMIT = 10 # xz축, 격자선 최대 길이
    DIST = 0.4 # 격자선 간격
    GRID_SIZE = int(AXIS_LIMIT/DIST) # 격자선 개수, 나누어 떨어지지 않을 수 있으니 int로 묶어줌
    G_GRID_SIZE = GRID_SIZE
    # prepare vertex data (in main memory)
    vertices_temp = []
    for i in range(-GRID_SIZE, GRID_SIZE+1): 
        if i == 0: # x축, z축과 중복되지 않게
            continue 

        # x축 방향 라인
        vertices_temp += [DIST*i, 0, -AXIS_LIMIT, *GRID_COLOR]
        vertices_temp += [DIST*i, 0,  AXIS_LIMIT, *GRID_COLOR]
        # z축 방향 라인
        vertices_temp += [-AXIS_LIMIT, 0, DIST*i, *GRID_COLOR]
        vertices_temp += [ AXIS_LIMIT, 0, DIST*i, *GRID_COLOR]

    vertices = glm.array(glm.float32, *vertices_temp)


    # create and activate VAO (vertex array object)
    VAO = glGenVertexArrays(1)  # create a vertex array object ID and store it to VAO variable
    glBindVertexArray(VAO)      # activate VAO

    # create and activate VBO (vertex buffer object)
    VBO = glGenBuffers(1)   # create a buffer object ID and store it to VBO variable
    glBindBuffer(GL_ARRAY_BUFFER, VBO)  # activate VBO as a vertex buffer object

    # copy vertex data to VBO
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices.ptr, GL_STATIC_DRAW) # allocate GPU memory for and copy vertex data to the currently bound vertex buffer

    # configure vertex positions
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * glm.sizeof(glm.float32), None)
    glEnableVertexAttribArray(0)

    # configure vertex colors
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * glm.sizeof(glm.float32), ctypes.c_void_p(3*glm.sizeof(glm.float32)))
    glEnableVertexAttribArray(1)

    # 바인딩 해제하는 게 안전하대서 추가함
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    return VAO
