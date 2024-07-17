# Importa el modulo pygame que es un conjunto de modulos py diseñados para escribir videojuegos
# proporciona funcionalidades para crear juegos y para crear interfaces gráficas de usuario (GUI) en Python.
import pygame 
# Importa modulo sys que proporciona acceso a algunas variables de sistema y funciones para manejar el intérprete de Python.
# lo necesito para manejar funcionalidades específicas del sistema como salir del juego
import sys
# Importa modulo random que proporciona funciones para generar números aleatorios y realizar otras operaciones matemáticas
# me sirve para introducir aleatoriedad como generar enemigos aleatorios o niveles aleatorios
import random

# Inicializamos librerías 
pygame.init()
# inicializamos el mixer para cargar audios
pygame.mixer.init()

# Cargamos las imágenes que vamos a usar
fondo = pygame.image.load('imagenes/fondo1.jpg')
laser_sonido = pygame.mixer.Sound('laser.wav')
explosion_sonido = pygame.mixer.Sound('explosion.wav')
golpe_sonido = pygame.mixer.Sound('golpe.wav')

# cargamos las imágenes para la explosión y como la vamos a reproducir en secuencia vamos a usar una lista vacía
explosion_list= []
for i in range(1, 13):
    explosion = pygame.image.load(f'explosion/{i}.png')  # Corregido: Usar f-string para incluir el índice
    explosion_list.append(explosion)

# tomamos el tamaño de nuestro fondo y lo guardamos en las variables width y height
width = fondo.get_width()
height = fondo.get_height()
# creamos la variable window y usamos set_mode para definir el modo de pantalla del juego
window = pygame.display.set_mode((width, height))
# creamos el título de la ventana
pygame.display.set_caption('Space Invaders By Emiliafc17')
run = True
fps = 60
# creamos el reloj para que el juego se ejecute a 60fps
clock = pygame.time.Clock()
# creamos score
score = 0
vida = 100
WHITE = (255,255,255)
BLACK = (0,0,0)

# Creamos función para el texto de la puntuación y se muestre en la pantalla
def texto_puntuacion(frame, text, size, x, y):
    # ubicamos un SysFont para el texto (tipo de letra, tamaño, letra negrita)
    font = pygame.font.SysFont('Small Fonts', size, bold=True)
    # renderizamos el texto (texto, true, blanco color de letra, negro color de fondo)
    text_frame = font.render(text, True, WHITE, BLACK)
    # creamos un rectángulo para el texto
    text_rect = text_frame.get_rect()
    # ubicamos el rectángulo en la pantalla en las coordenadas x y 
    text_rect.midtop = (x, y)
    # mostramos el texto en la pantalla
    frame.blit(text_frame, text_rect)

# Creamos la barra de la vida
def barra_vida(frame, x, y, nivel):
    longitud = 100
    alto = 20
    # el fill es lo que va a llenar nuestra barra de vida dependiendo del nivel
    fill = int((nivel / 100) * longitud)
    # creamos un rectángulo para la barra de vida
    border = pygame.Rect(x, y, longitud, alto)
    # creamos un rectángulo para la barra de vida que se va a llenar
    fill_rect = pygame.Rect(x, y, fill, alto)  # Corregido: Nombre de la variable fill a fill_rect
    pygame.draw.rect(frame, (255, 0, 255), fill_rect)
    pygame.draw.rect(frame, BLACK, border, 4)

# Creamos clase jugador
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # cargamos imagen y usamos el convert_alpha para quitarle el fondo de la imagen
        self.image = pygame.image.load('imagenes/A1.png').convert_alpha()
        # Esa misma imagen la colocamos como icono del juego
        pygame.display.set_icon(self.image)
        # creamos un rectángulo para el jugador, da las coordenadas de imagen y me sirve para luego posicionar la imagen
        self.rect = self.image.get_rect()
        # ubicamos el rectángulo en la pantalla en las coordenadas que saldrá sera en la mitad del ancho de la imagen de fondo
        self.rect.centerx = (width // 2)
        # coordenadas horizontales y le restamos 50 para que suba un poco más la nave 
        self.rect.centery = (height - 50)
        # creamos una variable para el movimiento del jugador en x para moverlo de derecha e izquierda
        self.velocidad_x = 0
        self.vida = 100
    
    # Creamos método update para actualizar
    def update(self):
        # iniciamos la velocidad en 0
        self.velocidad_x = 0
        # creamos un evento para que el jugador se mueva a la derecha por el teclado
        keystate = pygame.key.get_pressed()
        # condición para que cuando se presione la tecla izquierda se disminuya la velocidad en -5
        if keystate[pygame.K_LEFT]:
            self.velocidad_x = -5
        # condición para que cuando se presione la tecla derecha se sume la velocidad en 5
        elif keystate[pygame.K_RIGHT]:
            self.velocidad_x = 5
        # generamos las condiciones para que la nave se mantenga en la pantalla 
        self.rect.x += self.velocidad_x
        if self.rect.right > width:
            self.rect.right = width 
        elif self.rect.left < 0:
            self.rect.left = 0
    
    def disparar(self):
        # creamos una variable para el disparo, el self.rect.centerx establece la posición donde saldrá la bala
        # y en la parte superior de la imagen con self.rect.top
        bala = Balas(self.rect.centerx, self.rect.top)
        # agregamos la bala a la lista de balas
        grupo_jugador.add(bala)
        grupo_balas_jugador.add(bala)
        # reproducimos sonido cuando se activa la opción de disparar
        laser_sonido.play()

# Creamos clase enemigo
class Enemigos(pygame.sprite.Sprite):
    # iniciamos en la posición x y donde va a aparecer el enemigo
    def __init__(self, x, y):
        super().__init__()
        # cargamos imagen y usamos el convert_alpha para quitarle el fondo de la imagen
        self.image = pygame.image.load('imagenes/E1.png').convert_alpha()
        # obtenemos las coordenadas de la imagen
        self.rect = self.image.get_rect()
        # usamos random para buscar un valor aleatorio entre 1 y el ancho de la ventana -50 
        self.rect.x = random.randrange(1, width - 50)
        self.rect.y = 10
        # creamos una velocidad aleatoria 
        self.velocidad_y = random.randrange(1, 5)  # Corregido: Velocidad positiva
    
    def update(self):
        # con el get_ticks obtenemos el tiempo transcurrido cuando iniciamos el juego y lo pasamos a milisegundos
        # pero de manera errónea porque lo definimos hasta 5000 
        self.time = random.randrange(-1, pygame.time.get_ticks() // 5000)
        # a medida que el tiempo aumenta los enemigos se mueven más rápido
        self.rect.x += self.time
        # condición de la posición en x cuando sea mayor al ancho lo regresamos a 0 como en la parte inicial
        if self.rect.x >= width:
            self.rect.x = 0
            # acá sumamos a 50 para que vayan bajando hasta llegar al jugador en caso de que no dispare
            self.rect.y += 50

    def disparar_enemigos(self):
        # ejecutamos la clase de las balas del enemigo, recibe las coordenadas que salen del enemigo que van a bajar de la parte superior
        bala = Balas_enemigos(self.rect.centerx, self.rect.bottom)
        grupo_jugador.add(bala)
        grupo_balas_enemigos.add(bala)
        laser_sonido.play()

# Creamos clase de balas
class Balas(pygame.sprite.Sprite):
    # las coordenadas que recibe son x y
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('imagenes/B2.png').convert_alpha()
        self.rect = self.image.get_rect()
        # centramos en x
        self.rect.centerx = x
        self.rect.y = y
        # como las balas van hacia arriba ponemos un valor que va disminuyendo 
        self.velocidad_y = -18
    
    # creamos método update de la velocidad que será asignada en el eje y
    def update(self):  # Corregido: Identación
        self.rect.y += self.velocidad_y  # Corregido: Nombre de la variable
        # condición cuando la coordenada de rect sea menor a 0 
        if self.rect.bottom < 0:
            # se eliminan los objetos que teníamos en la lista (enemigos)
            self.kill()

class Balas_enemigos(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('imagenes/B1.png').convert_alpha()
        # transform.rotate nos sirve para rotar la imagen que tenemos, ingresamos la imagen "self.image" y ubicamos un giro de 180
        self.image = pygame.transform.rotate(self.image, 180)
        # obtenemos coordenadas de la imagen con el .get_rect() y crea como un rectángulo
        self.rect = self.image.get_rect()
        # centramos en x
        self.rect.centerx = x
        # establecemos para y un valor variado entre 10 y el ancho de la ventana
        self.rect.y = random.randrange(10, width)
        # establecemos una velocidad
        self.velocidad_y = 4
    
    # Creamos el método update
    def update(self):
        # establecemos la velocidad en y que va aumentando
        self.rect.y += self.velocidad_y
        if self.rect.bottom > height:
            self.kill()

# Creamos clase Explosión
class Explosion(pygame.sprite.Sprite):
    # definimos el elemento position para definir donde se realizará la explosión
    def __init__(self, position):
        super().__init__()
        # cargamos la primera imagen de la lista que hemos creado de imágenes de la explosión
        self.image = explosion_list[0]
        # reducimos el tamaño de la imagen un 20%
        img_escala = pygame.transform.scale(self.image, (20, 20))  # Corregido: Nombre de la variable img_scala a img_escala
        self.rect = img_escala.get_rect()
        self.rect.center = position
        # con get_ticks obtenemos el tiempo que nos sirve para hacer la secuencia de imágenes y se ejecute como si fuese un video
        self.time = pygame.time.get_ticks()
        # Velocidad de la explosión que define la demora del cambio de imagen
        self.velocidad_explo = 30 
        self.frame = 0
    
    def update(self):
        tiempo = pygame.time.get_ticks()
        # si el tiempo es mayor a la velocidad de la explosión
        if tiempo - self.time > self.velocidad_explo:
            self.time = tiempo
            self.frame += 1
            if self.frame == len(explosion_list):
                self.kill()
            else:
                position = self.rect.center
                self.image = explosion_list[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = position

# Creamos los grupos de las clases creadas
grupo_jugador = pygame.sprite.Group()
grupo_enemigos = pygame.sprite.Group()
grupo_balas_jugador = pygame.sprite.Group()
grupo_balas_enemigos = pygame.sprite.Group()

# Creamos objeto player del avión y lo asignamos al grupo jugador
player = Jugador()
grupo_jugador.add(player)

# Creamos 10 enemigos
for x in range(10):
    enemigo = Enemigos(10, 10)
    grupo_enemigos.add(enemigo)

# Nos permite ejecutar la ventana
while run:
    # recibe los fotogramas por segundo
    clock.tick(fps)
    window.blit(fondo, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.disparar()
    
    grupo_jugador.update()
    grupo_enemigos.update()
    grupo_balas_jugador.update()
    grupo_balas_enemigos.update()
    # colocamos al jugador para que se muestre en la ventana
    grupo_jugador.draw(window)

    # colisiones balas_jugador - enemigo
    # colocamos 2 true para que desaparezca tanto el enemigo como la bala
    colision1 = pygame.sprite.groupcollide(grupo_enemigos, grupo_balas_jugador, True, True)  # Corregido: Nombre de la variable colicion1 a colision1
    for i in colision1:
        score += 10
        enemigo = Enemigos(300, 10)  # Corregido: Creación del nuevo enemigo
        grupo_enemigos.add(enemigo)
        explo = Explosion(i.rect.center)
        grupo_jugador.add(explo)
        explosion_sonido.set_volume(0.3)
        explosion_sonido.play()

    # colisiones jugador - balas_enemigo
    colision2 = pygame.sprite.spritecollide(player, grupo_balas_enemigos, True)  # Corregido: Nombre de la variable colicion2 a colision2
    for j in colision2:
        player.vida -= 10
        if player.vida <= 0:
            run = False
        explo1 = Explosion(j.rect.center)
        grupo_jugador.add(explo1)
        golpe_sonido.play()

    # colisiones jugador - enemigo
    hits = pygame.sprite.spritecollide(player, grupo_enemigos, False)
    for hit in hits:
        player.vida -= 100
        enemigos = Enemigos(10, 10)
        grupo_jugador.add(enemigos)
        grupo_enemigos.add(enemigos)
        if player.vida <= 0:
            run = False

    texto_puntuacion(window, (' SCORE: '+ str(score)+'       '), 30, width - 85, 2)
    barra_vida(window, width - 285, 0, player.vida)
    pygame.display.flip()
pygame.quit()
