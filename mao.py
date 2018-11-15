import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Incluir Créditos
# Código adaptado para Python 3 por Rafael Augusto de Oliveira
# Universidade Tecnológica Federal do Paraná - Caampus Medianeira
# Ciência da Computação - 2018/2
# Lógica e comentários originais do autor


# Variáveis globais para os ângulos
ang = 0
ang2 = 0
ang3 = 0

class Osso(object):

    def __init__(self, a, l):
        self._altura = a
        self._largura = l
        self._angulo = 0
        self._conexao = None

    def set_conexao(self, osso, ang):
        self._conexao = osso
        self._angulo = ang

    def set_angulo(self, ang):
        self._angulo = ang
    
    def get_angulo(self):
        return self._angulo
    
    def desenha(self):
        glPushMatrix() # Salva o contexto(1)
        glTranslatef(0, self._altura / 2, 0) # Vai para o meio do osso

        glPushMatrix() # Salva o contexto(2)
        glScalef(self._largura, self._altura, self._largura) # Escala para o tamanho do osso
        glutSolidCube(self._largura) # Desenha o osso
        glPopMatrix() # Restaura o contexto(2)

        glTranslatef(0, self._altura / 2, 0)  # Vai para a ponta do osso
        glutSolidSphere(0.85 * self._largura, 8, 8) # Desenha a bolinha

        if(self._conexao):
            glRotatef(self._angulo, 1, 0, 0) # Rotaciona para o angulo da conexão
            self._conexao.desenha()
        glPopMatrix() # Restaura o contexto(1)

#////////////////////////////////////////////////////////////

class Dedo(object):
    def __init__(self, comprimento, largura):
        self._comprimento = comprimento
        self._largura = largura
        self._a = Osso(self._comprimento * 0.4, self._largura)
        self._b = Osso(self._comprimento * 0.35, self._largura)
        self._c = Osso(self._comprimento * 0.25, self._largura)

        self._a.set_conexao(self._b, 0)
        self._b.set_conexao(self._c, 0)

    def set_curvatura(self, curvatura):
        self._a.set_angulo(curvatura * 0.9)
        self._b.set_angulo(curvatura * 0.9)

    def get_curvatura(self): return self._a.get_angulo() * 100 / 90
    
    def desenha(self): self._a.desenha()
    
class Dedao(object):
    def __init__(self, comprimento, largura):
        self._comprimento = comprimento
        self._largura = largura
        self._a = Osso(self._comprimento * 0.5, self._largura)
        self._b = Osso(self._comprimento * 0.5, self._largura)

        self._a.set_conexao(self._b, 0)

    def set_curvatura(self, curvatura):
        self._a.set_angulo(curvatura * 0.9)

    def get_curvatura(self): return self._a.get_angulo() * 100 / 90
    
    def desenha(self): self._a.desenha()

#////////////////////////////////////////////////////////////

class Mao(object):
    def __init__(self, grossura):
        self._grossura = grossura
        self._mindinho = Dedo(4 * self._grossura, self._grossura)
        self._anelar = Dedo(6 * self._grossura, self._grossura)
        self._maior = Dedo(7 * self._grossura, self._grossura)
        self._indicador = Dedo(6 * self._grossura, self._grossura)
        self._dedao = Dedao(4 * self._grossura, self._grossura)
        self._curvatura = [0 for _ in range(5)]

    def get_curvatura(self, dedo): return self._curvatura[dedo]

    def desenha(self):
        glPushMatrix()
        glTranslatef(0,6 * self._grossura, 0)
        glPushMatrix()

        glTranslatef(-3 * self._grossura,0, 0)
        glutSolidSphere(self._grossura, 8, 8)
        glRotatef(self._curvatura[0] * 0.9, 1, 0, 0)
        self._mindinho.desenha()

        glPopMatrix()

        glPushMatrix()
        glTranslatef(-1.5 * self._grossura, 0, 0)
        glutSolidSphere(self._grossura, 8, 8)
        glRotatef(self._curvatura[1] * 0.9, 1, 0, 0)
        self._anelar.desenha()
        glPopMatrix()

        glPushMatrix()
        glutSolidSphere(self._grossura, 8, 8)
        glRotatef(self._curvatura[2] * 0.9, 1, 0, 0)
        self._maior.desenha()
        glPopMatrix()

        glPushMatrix()
        glTranslatef(1.5 * self._grossura, 0, 0)
        glutSolidSphere(self._grossura, 8, 8)
        glRotatef(self._curvatura[3] * 0.9, 1, 0, 0)
        self._indicador.desenha()
        glPopMatrix()

        glPushMatrix()
        glTranslatef(2 * self._grossura,-4 * self._grossura, 0)
        glRotatef(-80, 0, 0, 1)
        glRotatef(-20, 0, 1, 0)
        glRotatef(self._curvatura[4] * 0.5, 1, 0, 0)
        glScalef(1.5,1,1)
        glutSolidSphere(self._grossura, 8, 8)
        self._dedao.desenha()
        glPopMatrix()

        glPopMatrix()
        glPushMatrix()
        glTranslatef(-0.75 * self._grossura, 3 * self._grossura, 0)
        glScalef(5.5 * self._grossura, 6 * self._grossura, 1.25 * self._grossura)
        glutSolidCube(1)
        glPopMatrix()

    def set_curvatura(self, dedo, curv):
        self._curvatura[dedo] = curv

        if dedo is 0: self._mindinho.set_curvatura(curv)
        elif dedo is 1: self._anelar.set_curvatura(curv)
        elif dedo is 2: self._maior.set_curvatura(curv)
        elif dedo is 3: self._indicador.set_curvatura(curv)
        elif dedo is 4: self._dedao.set_curvatura(curv)
    
    def abrir(self, tudo_junto=False):
        if tudo_junto:
            j = self.get_curvatura(1)
            while j >= 0:
                i = 4
                while i >= 0:
                    self.set_curvatura(i, j)
                    i -= 1
                display()
                j -= 5
        else:
            i = 4
            while i >= 0:
                j = self.get_curvatura(i)
                while j >= 0:
                    self.set_curvatura(i, j)
                    display()
                    j -= 5
                i -= 1

    def fechar(self, tudo_junto=False):
        if tudo_junto:
            j = self.get_curvatura(1)
            while j <= 100:
                i = 0
                while i < 5:
                    self.set_curvatura(i, j)
                    i += 1
                display()
                j += 5
        else:
            i = 0
            while i < 5:
                j = self.get_curvatura(i)
                while j <= 100:
                    self.set_curvatura(i, j)
                    display()
                    j += 5
                i += 1

    def tchau(self):
        global ang3
        self.abrir(True)
        for _ in range(3):
            ang3 += 5
            display()
       
        for _ in range(3):
            for _ in range(6):
                ang3 -= 5
                display()
            for _ in range(6):
                ang3 += 5
                display()
        
        for _ in range(3):
            ang3 -= 5
            display()

    def fuck(self):
        i = 0
        global ang

        while i < 180:
            ang += 20
            display()
            i += 20
        
        self.fechar(True)
        
        j = self.get_curvatura(2)

        while j >= 0:
            self.set_curvatura(2, j)
            display()
            j -= 20

    def hangloose(self):
        global ang, ang3
        self.fechar(True)

        j = self.get_curvatura(2)

        while j >= 0:
            self.set_curvatura(0, j)
            self.set_curvatura(4, j)
            ang3 += 3
            display()
            j -= 20

        for _ in range(3):
            ang += 5
            display()

        for _ in range(3):
            for _ in range(6):
                ang -= 5
                display()
            
            for _ in range(6):
                ang += 5
                display()
        
        for _ in range(3):
            ang -= 5
            display()
        
        for _ in range(6):
            ang3 == 3
            display()

    def vem_pro_pau(self):
        global ang, ang2

        self.abrir(True)

        i = 0
        while i < 180:
            ang += 20
            ang2 -= 10
            display()
            i += 20

        j = self.get_curvatura(1)
        while j <= 30:
            for i in range(4):
                self.set_curvatura(i, j)
            display()
            j += 10

        j = 30
        while j >= 0:
            for i in range(4):
                self.set_curvatura(i, j)
            display()
            j -= 10

        j = self.get_curvatura(1)
        while j <= 30:
            for i in range(4):
                self.set_curvatura(i, j)
            display()
            j += 10
        
        j = 30
        while j >= 0:
            for i in range(4):
                self.set_curvatura(i, j)
            display()
            j -= 10

    def home(self):
        self.abrir(True)
        global ang, ang2, ang3

        if ang < 0: ang += 360
        if ang2 < 0: ang2 += 360
        if ang3 < 0: ang3 += 360

        while ang > 0:
            ang -= 10
            display()
        ang = 0

        while ang2 > 0:
            ang2 -= 10
            display()
        ang2 = 0

        while ang3 > 0:
            ang3 -= 10
            display()
        ang3 = 0
        display()

    def dedo_duro(self):
        pass
    
    def positivo(self):
        pass

#////////////////////////////////////////////////////////////

m = Mao(1)

def init():
    #loadtexture
    glClearColor(0, 0, 0, 0)
    glClearDepth(1) # Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LEQUAL) # The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST) # Enables Depth Testing
    glShadeModel(GL_SMOOTH) # Enables Smooth Color Shading

def display():
    global m, ang, ang2, ang3
    glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    #glBindTexture(GL_TEXTURE_2D, texture[0])
   #//////////////ISSO AQUI EH PRA LUZ///////////E EU AINDA N SEI COMO FUNCA/////
    diffuseLight = [1, 1, 1, 1]
    ambientLight = [0.2, 0.2, 0.4, 1]
    lightPos = [0, 500, 100, 1]
    glEnable(GL_LIGHTING)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLight)
    glLightfv(GL_LIGHT0, GL_SPECULAR, diffuseLight)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColor3f(1, 1, 1)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, diffuseLight )
    glMateriali(GL_FRONT_AND_BACK, GL_SHININESS, 50)
    #//////////////////////////////////////////////////////////////////////////

    glPushMatrix()

    glTranslatef (0, -5, -15)
    glRotatef (ang3, 0, 0, 1)
    glRotatef (ang, 0, 1, 0)
    glRotatef (ang2, 1, 0, 0)
    glColor3f(1, 0.8, 0)

    m.desenha()

    glPopMatrix()

    glutSwapBuffers()

def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(55, w / h, 1, 40)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0, 0, -10)

def idle():
    pass

def keyboard(key, x, y):
    global ang, ang2, ang3, m

    key = key.decode("utf-8")

    if key is 'q':
        if m.get_curvatura(0) < 100:
            m.set_curvatura(0, m.get_curvatura(0) + 5)
    if key is 'a':
        if m.get_curvatura(0) > 0:
            m.set_curvatura(0, m.get_curvatura(0) - 5)
    if key is 'w':
        if m.get_curvatura(1) < 100:
            m.set_curvatura(1, m.get_curvatura(1) + 5)
    if key is 's':
        if m.get_curvatura(1) > 0:
            m.set_curvatura(1, m.get_curvatura(0) - 5)
    if key is 'e':
        if m.get_curvatura(2) < 100:
            m.set_curvatura(2, m.get_curvatura(2) + 5)
    if key is 'd':
        if m.get_curvatura(2) > 0:
            m.set_curvatura(2, m.get_curvatura(2) - 5)
    if key is 'r':
        if m.get_curvatura(3) < 100:
            m.set_curvatura(3, m.get_curvatura(3) + 5)
    if key is 'f':
        if m.get_curvatura(3) > 0:
            m.set_curvatura(3, m.get_curvatura(3) - 5)
    if key is 't':
        if m.get_curvatura(4) < 100:
            m.set_curvatura(4, m.get_curvatura(4) + 5)
    if key is 'g':
        if m.get_curvatura(4) > 0:
            m.set_curvatura(4, m.get_curvatura(4) - 5)
    if key is '.': # //>
        ang += 5
        if ang > 360:
            ang -= 360
    if key is ',': # //<
        ang -= 5
        if ang < 0:
            ang += 360
    if key is ']':
        ang2 += 5
        if ang2 > 360:
            ang2 -= 360
    if key is '[':
        ang2 -= 5
        if ang2 < 0:
            ang2 += 360
    if key is '+': m.abrir()
    if key is '*': m.abrir(True)
    if key is '/': m.fechar(True)
    if key is '-': m.fechar()
    if key is chr(27): sys.exit(0)
    if key is '9':
        ang3 += 5
        if ang3 > 360:
            ang3 -= 360
    if key is '0':
        ang3 -= 5
        if ang3 < 0:
            ang3 += 360
    if key is '1': m.tchau()
    if key is '2': m.fuck()
    if key is '3': m.hangloose()
    if key is '4': m.vem_pro_pau()
    if key is 'h': m.home()

    glutPostRedisplay()


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(300, 300)
    glutInitWindowPosition(200, 200)
    glutCreateWindow("Mão")
    init()

    if input("FullScreen? (y/n) ") is 'y': glutFullScreen()
    
    glutIdleFunc(idle)
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutMainLoop()

if __name__ == '__main__':  main()