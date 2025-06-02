from OpenGL.GL import *
from glfw.GLFW import *
import glm

def draw_frame(vao, MVP, unif_locs):
    glUniformMatrix4fv(unif_locs['MVP'], 1, GL_FALSE, glm.value_ptr(MVP))
    glBindVertexArray(vao)
    glDrawArrays(GL_LINES, 0, 6)