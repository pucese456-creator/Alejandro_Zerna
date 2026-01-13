import pygame
import random
import sys
import math

# Inicialización de Pygame
pygame.init()

# Constantes del juego
ANCHO = 800
ALTO = 600
FPS = 60
GRAVEDAD = 0.8
VELOCIDAD_SALTO = -15
VELOCIDAD_MOVIMIENTO = 5

# Colores mejorados
CIELO = (107, 140, 255)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (200, 0, 0)
ROJO_CLARO = (255, 100, 100)
AZUL = (0, 100, 200)
VERDE = (34, 139, 34)
MARRON = (139, 69, 19)
MARRON_CLARO = (180, 120, 70)
AMARILLO = (255, 215, 0)
NARANJA = (255, 140, 0)
ROSA = (255, 182, 193)
CYAN = (0, 255, 255)
MORADO = (147, 112, 219)

class Estrella:
    """Clase para efectos de estrellas brillantes"""
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.velocidad_x = random.uniform(-2, 2)
        self.velocidad_y = random.uniform(-4, -1)
        self.vida = 40
        self.tamaño = random.randint(4, 8)
        self.rotacion = random.uniform(0, 360)
        self.velocidad_rotacion = random.uniform(-10, 10)
        
    def actualizar(self):
        self.x += self.velocidad_x
        self.y += self.velocidad_y
        self.velocidad_y += 0.2
        self.vida -= 1
        self.tamaño = max(1, self.tamaño - 0.15)
        self.rotacion += self.velocidad_rotacion
        
    def dibujar(self, pantalla):
        if self.vida > 0:
            # Dibujar estrella de 4 puntas
            puntos = []
            for i in range(8):
                angulo = math.radians(self.rotacion + i * 45)
                radio = self.tamaño if i % 2 == 0 else self.tamaño / 2
                px = self.x + math.cos(angulo) * radio
                py = self.y + math.sin(angulo) * radio
                puntos.append((int(px), int(py)))
            
            if len(puntos) >= 3:
                pygame.draw.polygon(pantalla, self.color, puntos)
                # Brillo en el centro
                pygame.draw.circle(pantalla, BLANCO, (int(self.x), int(self.y)), max(1, int(self.tamaño / 3)))


class Particula:
    """Clase para efectos visuales de partículas coloridas"""
    def __init__(self, x, y, color, velocidad_x, velocidad_y):
        self.x = x
        self.y = y
        self.color = color
        self.velocidad_x = velocidad_x
        self.velocidad_y = velocidad_y
        self.vida = 30
        self.tamaño = random.randint(3, 6)
        
    def actualizar(self):
        self.x += self.velocidad_x
        self.y += self.velocidad_y
        self.velocidad_y += 0.3
        self.vida -= 1
        self.tamaño = max(1, self.tamaño - 0.1)
        
    def dibujar(self, pantalla):
        if self.vida > 0:
            pygame.draw.circle(pantalla, self.color, (int(self.x), int(self.y)), int(self.tamaño))


class Nube:
    """Clase para nubes decorativas en el cielo"""
    def __init__(self, x, y, velocidad):
        self.x = x
        self.y = y
        self.velocidad = velocidad
        self.rebote = 0
        self.direccion_rebote = 1
        
    def actualizar(self):
        self.x += self.velocidad
        if self.x > ANCHO + 100:
            self.x = -100
        
        # Rebote suave vertical
        self.rebote += 0.05 * self.direccion_rebote
        if abs(self.rebote) > 3:
            self.direccion_rebote *= -1
            
    def dibujar(self, pantalla):
        y_actual = self.y + self.rebote
        # Nube blanca con múltiples círculos
        pygame.draw.circle(pantalla, BLANCO, (int(self.x), int(y_actual)), 25)
        pygame.draw.circle(pantalla, BLANCO, (int(self.x + 20), int(y_actual)), 30)
        pygame.draw.circle(pantalla, BLANCO, (int(self.x + 40), int(y_actual)), 25)
        pygame.draw.circle(pantalla, BLANCO, (int(self.x + 20), int(y_actual - 15)), 20)


class Jugador:
    """Clase que representa a Mario con animación mejorada"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ancho = 40
        self.alto = 50
        self.velocidad_y = 0
        self.en_suelo = False
        self.vidas = 3
        self.puntos = 0
        self.direccion = 1
        self.animacion_frame = 0
        self.animacion_contador = 0
        self.saltando = False
        self.invencible = 0
        self.escala_y = 1.0
        self.escala_x = 1.0
        
    def mover(self, teclas, plataformas):
        """Maneja el movimiento del jugador"""
        moviendo = False
        
        # Movimiento horizontal
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.x -= VELOCIDAD_MOVIMIENTO
            self.direccion = -1
            moviendo = True
            if self.x < 0:
                self.x = 0
                
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.x += VELOCIDAD_MOVIMIENTO
            self.direccion = 1
            moviendo = True
            if self.x > ANCHO - self.ancho:
                self.x = ANCHO - self.ancho
        
        # Animación de caminar
        if moviendo and self.en_suelo:
            self.animacion_contador += 1
            if self.animacion_contador >= 5:
                self.animacion_frame = (self.animacion_frame + 1) % 4
                self.animacion_contador = 0
        else:
            self.animacion_frame = 0
        
        # Salto con efecto de estiramiento
        if (teclas[pygame.K_SPACE] or teclas[pygame.K_UP] or teclas[pygame.K_w]) and self.en_suelo:
            self.velocidad_y = VELOCIDAD_SALTO
            self.en_suelo = False
            self.saltando = True
            self.escala_y = 1.2
            self.escala_x = 0.9
        
        # Aplicar gravedad
        self.velocidad_y += GRAVEDAD
        self.y += self.velocidad_y
        
        # Animación de squash and stretch
        if not self.en_suelo:
            if self.velocidad_y < 0:
                self.escala_y = min(1.15, self.escala_y + 0.02)
                self.escala_x = max(0.9, self.escala_x - 0.01)
            else:
                self.escala_y = max(0.9, self.escala_y - 0.02)
                self.escala_x = min(1.1, self.escala_x + 0.01)
        else:
            self.escala_y = 1.0 + abs(math.sin(pygame.time.get_ticks() * 0.01)) * 0.05
            self.escala_x = 1.0
        
        # Verificar colisiones con plataformas
        self.en_suelo = False
        for plataforma in plataformas:
            if self.colision_con(plataforma):
                if self.velocidad_y > 0:
                    self.y = plataforma.y - self.alto
                    self.velocidad_y = 0
                    self.en_suelo = True
                    self.saltando = False
                    # Efecto de aterrizaje
                    self.escala_y = 0.85
                    self.escala_x = 1.15
                elif self.velocidad_y < 0:
                    self.y = plataforma.y + plataforma.alto
                    self.velocidad_y = 0
        
        # Reducir invencibilidad
        if self.invencible > 0:
            self.invencible -= 1
        
        # Límite inferior
        if self.y > ALTO:
            self.perder_vida()
            
    def colision_con(self, otro):
        """Detecta colisión con otro objeto"""
        return (self.x < otro.x + otro.ancho and
                self.x + self.ancho > otro.x and
                self.y < otro.y + otro.alto and
                self.y + self.alto > otro.y)
    
    def perder_vida(self):
        """Reduce vidas y reinicia posición"""
        if self.invencible == 0:
            self.vidas -= 1
            self.x = 100
            self.y = 300
            self.velocidad_y = 0
            self.invencible = 120
        
    def dibujar(self, pantalla, particulas):
        """Dibuja a Mario con mejor diseño y animación"""
        # Efecto de parpadeo cuando es invencible
        if self.invencible > 0 and self.invencible % 10 < 5:
            return
        
        # Aplicar escala
        alto_escalado = int(self.alto * self.escala_y)
        ancho_escalado = int(self.ancho * self.escala_x)
        offset_y = self.alto - alto_escalado
        
        # Sombra
        pygame.draw.ellipse(pantalla, (0, 0, 0, 100), (self.x + 5, self.y + self.alto, 30, 8))
        
        # Calcular centro para escalar desde el centro
        centro_x = self.x + self.ancho / 2
        x_escalado = centro_x - ancho_escalado / 2
        
        # Gorra (roja con M)
        pygame.draw.rect(pantalla, ROJO, (x_escalado + 6, self.y + offset_y, 28 * self.escala_x, 10 * self.escala_y), border_radius=5)
        pygame.draw.circle(pantalla, ROJO, (int(centro_x), int(self.y + 8 * self.escala_y + offset_y)), int(14 * self.escala_x))
        
        # Letra M en la gorra
        fuente_m = pygame.font.Font(None, int(18 * self.escala_x))
        texto_m = fuente_m.render("M", True, BLANCO)
        pantalla.blit(texto_m, (centro_x - 5, self.y + 3 * self.escala_y + offset_y))
        
        # Cabeza (piel)
        pygame.draw.circle(pantalla, (255, 220, 177), (int(centro_x), int(self.y + 18 * self.escala_y + offset_y)), int(11 * self.escala_x))
        
        # Ojos
        ojo_x_izq = centro_x - 4 if self.direccion == 1 else centro_x + 4
        ojo_x_der = centro_x + 4 if self.direccion == 1 else centro_x - 4
        pygame.draw.circle(pantalla, NEGRO, (int(ojo_x_izq), int(self.y + 16 * self.escala_y + offset_y)), 2)
        pygame.draw.circle(pantalla, NEGRO, (int(ojo_x_der), int(self.y + 16 * self.escala_y + offset_y)), 2)
        
        # Nariz
        pygame.draw.circle(pantalla, (255, 200, 160), (int(centro_x + (2 * self.direccion)), int(self.y + 20 * self.escala_y + offset_y)), 3)
        
        # Bigote
        bigote_puntos = [
            (centro_x - 8, self.y + 22 * self.escala_y + offset_y),
            (centro_x - 5, self.y + 23 * self.escala_y + offset_y),
            (centro_x - 2, self.y + 22 * self.escala_y + offset_y)
        ]
        pygame.draw.polygon(pantalla, MARRON, bigote_puntos)
        bigote_puntos_r = [
            (centro_x + 8, self.y + 22 * self.escala_y + offset_y),
            (centro_x + 5, self.y + 23 * self.escala_y + offset_y),
            (centro_x + 2, self.y + 22 * self.escala_y + offset_y)
        ]
        pygame.draw.polygon(pantalla, MARRON, bigote_puntos_r)
        
        # Cuerpo (overol azul)
        pygame.draw.rect(pantalla, AZUL, (x_escalado + 10, self.y + 26 * self.escala_y + offset_y, 20 * self.escala_x, 18 * self.escala_y), border_radius=3)
        
        # Tirantes
        pygame.draw.rect(pantalla, ROJO, (x_escalado + 14, self.y + 26 * self.escala_y + offset_y, 3 * self.escala_x, 12 * self.escala_y))
        pygame.draw.rect(pantalla, ROJO, (x_escalado + 23, self.y + 26 * self.escala_y + offset_y, 3 * self.escala_x, 12 * self.escala_y))
        
        # Botones dorados
        pygame.draw.circle(pantalla, AMARILLO, (int(x_escalado + 15), int(self.y + 30 * self.escala_y + offset_y)), 2)
        pygame.draw.circle(pantalla, AMARILLO, (int(x_escalado + 25), int(self.y + 30 * self.escala_y + offset_y)), 2)
        
        # Brazos con animación
        brazo_offset = -2 if self.animacion_frame in [1, 3] else 0
        brazo_y = self.y + 28 * self.escala_y + offset_y + brazo_offset
            
        pygame.draw.rect(pantalla, (255, 220, 177), (x_escalado + 5, brazo_y, 6 * self.escala_x, 12 * self.escala_y), border_radius=3)
        pygame.draw.rect(pantalla, (255, 220, 177), (x_escalado + 29, brazo_y, 6 * self.escala_x, 12 * self.escala_y), border_radius=3)
        
        # Guantes blancos
        pygame.draw.circle(pantalla, BLANCO, (int(x_escalado + 8), int(brazo_y + 11 * self.escala_y)), int(4 * self.escala_x))
        pygame.draw.circle(pantalla, BLANCO, (int(x_escalado + 32), int(brazo_y + 11 * self.escala_y)), int(4 * self.escala_x))
        
        # Piernas con animación
        pierna_offset = 0
        if self.animacion_frame == 1:
            pierna_offset = 2
        elif self.animacion_frame == 3:
            pierna_offset = -2
            
        pygame.draw.rect(pantalla, AZUL, (x_escalado + 12 + pierna_offset, self.y + 44 * self.escala_y + offset_y, 6 * self.escala_x, 6 * self.escala_y), border_radius=2)
        pygame.draw.rect(pantalla, AZUL, (x_escalado + 22 - pierna_offset, self.y + 44 * self.escala_y + offset_y, 6 * self.escala_x, 6 * self.escala_y), border_radius=2)
        
        # Zapatos
        pygame.draw.ellipse(pantalla, MARRON, (x_escalado + 10 + pierna_offset, self.y + 48 * self.escala_y + offset_y, 10 * self.escala_x, 5 * self.escala_y))
        pygame.draw.ellipse(pantalla, MARRON, (x_escalado + 20 - pierna_offset, self.y + 48 * self.escala_y + offset_y, 10 * self.escala_x, 5 * self.escala_y))


class Plataforma:
    """Clase que representa plataformas del nivel con diseño mejorado"""
    def __init__(self, x, y, ancho, alto, tipo="ladrillo"):
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.tipo = tipo
        
    def dibujar(self, pantalla):
        """Dibuja la plataforma con textura de ladrillos"""
        if self.tipo == "ladrillo":
            pygame.draw.rect(pantalla, MARRON, (self.x, self.y, self.ancho, self.alto))
            
            ladrillo_ancho = 30
            ladrillo_alto = 20
            for i in range(0, self.ancho, ladrillo_ancho):
                for j in range(0, self.alto, ladrillo_alto):
                    pygame.draw.rect(pantalla, MARRON_CLARO, 
                                   (self.x + i + 1, self.y + j + 1, ladrillo_ancho - 2, ladrillo_alto - 2))
                    pygame.draw.rect(pantalla, (100, 50, 20), 
                                   (self.x + i, self.y + j, ladrillo_ancho, ladrillo_alto), 2)
                    pygame.draw.line(pantalla, MARRON, 
                                   (self.x + i + 5, self.y + j + 5),
                                   (self.x + i + 10, self.y + j + 5), 1)
        elif self.tipo == "pasto":
            pygame.draw.rect(pantalla, (101, 67, 33), (self.x, self.y, self.ancho, self.alto))
            for i in range(0, self.ancho, 10):
                pygame.draw.line(pantalla, VERDE, 
                               (self.x + i, self.y), 
                               (self.x + i, self.y - 5), 2)


class Enemigo:
    """Clase que representa a los Goombas con animación de rebote"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.y_base = y
        self.ancho = 35
        self.alto = 35
        self.velocidad = 2
        self.direccion = -1
        self.vivo = True
        self.animacion_frame = 0
        self.animacion_contador = 0
        self.aplastado_contador = 0
        self.rebote = 0
        self.rebote_velocidad = 0.15
        
    def mover(self, plataformas):
        """Movimiento automático del enemigo con rebote"""
        if not self.vivo:
            if self.aplastado_contador > 0:
                self.aplastado_contador -= 1
            return
            
        self.x += self.velocidad * self.direccion
        
        # Animación
        self.animacion_contador += 1
        if self.animacion_contador >= 10:
            self.animacion_frame = (self.animacion_frame + 1) % 2
            self.animacion_contador = 0
        
        # Rebote al caminar
        self.rebote += self.rebote_velocidad
        if abs(math.sin(self.rebote)) > 0.99:
            self.rebote_velocidad *= -1
        
        # Cambiar dirección en los bordes
        if self.x <= 0 or self.x >= ANCHO - self.ancho:
            self.direccion *= -1
            
    def dibujar(self, pantalla):
        """Dibuja al Goomba con animación de rebote"""
        if not self.vivo and self.aplastado_contador <= 0:
            return
            
        if not self.vivo:
            # Goomba aplastado con estrellitas
            pygame.draw.ellipse(pantalla, MARRON, (self.x, self.y + 25, self.ancho, 10))
            # Dibuja X en los ojos
            pygame.draw.line(pantalla, NEGRO, (self.x + 10, self.y + 27), (self.x + 14, self.y + 31), 2)
            pygame.draw.line(pantalla, NEGRO, (self.x + 14, self.y + 27), (self.x + 10, self.y + 31), 2)
            pygame.draw.line(pantalla, NEGRO, (self.x + 22, self.y + 27), (self.x + 26, self.y + 31), 2)
            pygame.draw.line(pantalla, NEGRO, (self.x + 26, self.y + 27), (self.x + 22, self.y + 31), 2)
            return
        
        # Aplicar rebote
        y_rebote = self.y_base + math.sin(self.rebote) * 3
        
        # Sombra
        pygame.draw.ellipse(pantalla, (0, 0, 0, 100), (self.x + 3, self.y_base + 35, 30, 6))
        
        # Cuerpo (forma de hongo)
        pygame.draw.ellipse(pantalla, (150, 100, 50), (self.x, y_rebote + 12, self.ancho, 25))
        
        # Cabeza/sombrero
        pygame.draw.circle(pantalla, MARRON, (int(self.x + 17), int(y_rebote + 12)), 16)
        
        # Detalles del sombrero
        pygame.draw.arc(pantalla, (100, 60, 30), (self.x + 5, y_rebote + 2, 25, 20), 0, 3.14, 3)
        
        # Ojos grandes y enfadados
        pygame.draw.ellipse(pantalla, BLANCO, (self.x + 8, y_rebote + 15, 10, 12))
        pygame.draw.ellipse(pantalla, BLANCO, (self.x + 20, y_rebote + 15, 10, 12))
        
        # Pupilas animadas
        pupila_offset = 1 if self.animacion_frame == 1 else -1
        pygame.draw.circle(pantalla, NEGRO, (int(self.x + 12 + pupila_offset), int(y_rebote + 20)), 4)
        pygame.draw.circle(pantalla, NEGRO, (int(self.x + 24 + pupila_offset), int(y_rebote + 20)), 4)
        
        # Ceño fruncido
        pygame.draw.line(pantalla, NEGRO, (self.x + 6, y_rebote + 13), (self.x + 12, y_rebote + 16), 2)
        pygame.draw.line(pantalla, NEGRO, (self.x + 22, y_rebote + 16), (self.x + 28, y_rebote + 13), 2)
        
        # Boca
        puntos_boca = [
            (self.x + 13, y_rebote + 28),
            (self.x + 17, y_rebote + 30),
            (self.x + 21, y_rebote + 28)
        ]
        pygame.draw.polygon(pantalla, BLANCO, puntos_boca)
        
        # Pies que se alternan
        pie_offset = 2 if self.animacion_frame == 1 else -2
        pygame.draw.ellipse(pantalla, MARRON, (self.x - 3 + pie_offset, y_rebote + 32, 14, 7))
        pygame.draw.ellipse(pantalla, MARRON, (self.x + 24 - pie_offset, y_rebote + 32, 14, 7))
    
    def aplastar(self):
        """Marca al enemigo como aplastado"""
        self.vivo = False
        self.aplastado_contador = 30


class Moneda:
    """Clase que representa monedas coleccionables con animación brillante"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.y_base = y
        self.ancho = 25
        self.alto = 25
        self.recolectada = False
        self.valor = 100
        self.animacion_frame = 0
        self.animacion_contador = 0
        self.brillo_offset = 0
        self.flotando = 0
        
    def actualizar(self):
        """Actualiza la animación de la moneda"""
        if not self.recolectada:
            self.animacion_contador += 1
            if self.animacion_contador >= 8:
                self.animacion_frame = (self.animacion_frame + 1) % 8
                self.animacion_contador = 0
            self.brillo_offset = math.sin(self.animacion_frame * 0.4) * 3
            
            # Efecto de flotación
            self.flotando += 0.1
            self.y = self.y_base + math.sin(self.flotando) * 5
        
    def dibujar(self, pantalla):
        """Dibuja la moneda con efecto de rotación y brillo"""
        if not self.recolectada:
            centro_x = int(self.x + self.ancho // 2)
            centro_y = int(self.y + self.alto // 2 + self.brillo_offset)
            
            # Escala de rotación (simula 3D)
            escala = abs(math.cos(self.animacion_frame * 0.4))
            ancho_moneda = int(20 * escala) + 5
            
            # Brillo externo parpadeante
            if self.animacion_frame % 4 == 0:
                for i in range(3):
                    pygame.draw.circle(pantalla, (255, 255, 200, 50), 
                                     (centro_x, centro_y), ancho_moneda + i * 3, 1)
            
            # Sombra
            pygame.draw.ellipse(pantalla, (200, 150, 0), 
                              (centro_x - ancho_moneda // 2, centro_y - 12, ancho_moneda, 24))
            
            # Moneda dorada
            pygame.draw.ellipse(pantalla, AMARILLO, 
                              (centro_x - ancho_moneda // 2 + 1, centro_y - 11, ancho_moneda - 2, 22))
            
            # Borde naranja
            pygame.draw.ellipse(pantalla, NARANJA, 
                              (centro_x - ancho_moneda // 2, centro_y - 12, ancho_moneda, 24), 2)
            
            # Símbolo $
            if escala > 0.3:
                fuente_moneda = pygame.font.Font(None, 18)
                texto_moneda = fuente_moneda.render("$", True, NARANJA)
                texto_rect = texto_moneda.get_rect(center=(centro_x, centro_y))
                pantalla.blit(texto_moneda, texto_rect)
            
            # Brillo blanco
            pygame.draw.circle(pantalla, BLANCO, (centro_x - 3, centro_y - 5), 3)


class Juego:
    """Clase principal que maneja el juego con interfaz mejorada"""
    def __init__(self):
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("🍄 Super Mario Bros 3 - Retro Edition")
        self.reloj = pygame.time.Clock()
        
        # Fuentes mejoradas
        self.fuente_hud = pygame.font.Font(None, 32)
        self.fuente_grande = pygame.font.Font(None, 72)
        self.fuente_menu = pygame.font.Font(None, 48)
        
        self.jugador = Jugador(100, 300)
        self.game_over = False
        self.victoria = False
        self.particulas = []
        self.estrellas = []
        
        # Elementos decorativos
        self.nubes = [
            Nube(100, 80, 0.3),
            Nube(400, 120, 0.2),
            Nube(650, 60, 0.25),
        ]
        
        # Crear nivel con diseño mejorado
        self.plataformas = [
            Plataforma(0, 550, ANCHO, 50, "pasto"),
            Plataforma(200, 450, 150, 20, "ladrillo"),
            Plataforma(450, 380, 120, 20, "ladrillo"),
            Plataforma(150, 280, 100, 20, "ladrillo"),
            Plataforma(400, 200, 150, 20, "ladrillo"),
            Plataforma(650, 320, 120, 20, "ladrillo"),
        ]
        
        # Crear enemigos
        self.enemigos = [
            Enemigo(300, 515),
            Enemigo(500, 515),
            Enemigo(600, 285),
        ]
        
        # Crear monedas
        self.monedas = [
            Moneda(230, 410),
            Moneda(270, 410),
            Moneda(310, 410),
            Moneda(480, 340),
            Moneda(180, 240),
            Moneda(450, 160),
            Moneda(680, 280),
        ]
        
    def crear_estrellas(self, x, y, cantidad=8):
        """Crea estrellas brillantes de colores"""
        colores = [AMARILLO, CYAN, ROSA, BLANCO, NARANJA, MORADO]
        for _ in range(cantidad):
            color = random.choice(colores)
            self.estrellas.append(Estrella(x, y, color))
        
    def crear_particulas(self, x, y, color, cantidad=10):
        """Crea un efecto de partículas coloridas"""
        for _ in range(cantidad):
            velocidad_x = random.uniform(-3, 3)
            velocidad_y = random.uniform(-5, -1)
            self.particulas.append(Particula(x, y, color, velocidad_x, velocidad_y))
        
    def verificar_colisiones(self):
        """Verifica colisiones entre objetos"""
        # Colisión con enemigos
        for enemigo in self.enemigos:
            if enemigo.vivo and self.jugador.colision_con(enemigo):
                # Si Mario cae sobre el enemigo
                if self.jugador.velocidad_y > 0 and self.jugador.y + self.jugador.alto - 10 < enemigo.y:
                    enemigo.aplastar()
                    self.jugador.velocidad_y = -10
                    self.jugador.puntos += 200
                    # Efecto de estrellitas alegres
                    self.crear_estrellas(enemigo.x + 17, enemigo.y + 20, 12)
                else:
                    self.jugador.perder_vida()
                    if self.jugador.vidas > 0:
                        # Efecto de daño con estrellas azules
                        self.crear_estrellas(self.jugador.x + 20, self.jugador.y + 25, 15)
                    
        # Colisión con monedas
        for moneda in self.monedas:
            if not moneda.recolectada and self.jugador.colision_con(moneda):
                moneda.recolectada = True
                self.jugador.puntos += moneda.valor
                # Efecto brillante de estrellitas doradas
                self.crear_estrellas(moneda.x + 12, moneda.y + 12, 10)
                
        # Verificar victoria
        if all(m.recolectada for m in self.monedas):
            self.victoria = True
            
    def dibujar_hud(self):
        """Dibuja el HUD mejorado"""
        # Panel superior con fondo semi-transparente
        superficie_hud = pygame.Surface((ANCHO, 50))
        superficie_hud.set_alpha(200)
        superficie_hud.fill((20, 20, 20))
        self.pantalla.blit(superficie_hud, (0, 0))
        
        # Icono y texto de vidas
        corazon_x = 20
        for i in range(self.jugador.vidas):
            self.dibujar_corazon(self.pantalla, corazon_x + i * 35, 15, 20)
        
        # Puntos con icono de moneda
        self.dibujar_icono_moneda(self.pantalla, ANCHO - 180, 15, 20)
        texto_puntos = self.fuente_hud.render(f"{self.jugador.puntos}", True, AMARILLO)
        self.pantalla.blit(texto_puntos, (ANCHO - 150, 12))
        
        # Contador de monedas
        monedas_restantes = sum(1 for m in self.monedas if not m.recolectada)
        texto_monedas = self.fuente_hud.render(f"x{monedas_restantes}/{len(self.monedas)}", True, BLANCO)
        self.pantalla.blit(texto_monedas, (ANCHO - 80, 12))
        
    def dibujar_corazon(self, pantalla, x, y, tamaño):
        """Dibuja un corazón animado para las vidas"""
        # Efecto de latido
        pulso = abs(math.sin(pygame.time.get_ticks() * 0.005)) * 2
        tamaño_actual = tamaño + pulso
        
        puntos = [
            (x + tamaño_actual // 2, y + tamaño_actual),
            (x, y + tamaño_actual // 3),
            (x + tamaño_actual // 4, y),
            (x + tamaño_actual // 2, y + tamaño_actual // 6),
            (x + 3 * tamaño_actual // 4, y),
            (x + tamaño_actual, y + tamaño_actual // 3)
        ]
        pygame.draw.polygon(pantalla, ROJO_CLARO, puntos)
        pygame.draw.polygon(pantalla, ROJO, puntos, 2)
        
        # Brillo
        pygame.draw.circle(pantalla, ROSA, (int(x + tamaño_actual // 3), int(y + tamaño_actual // 4)), int(tamaño_actual // 8))
        
    def dibujar_icono_moneda(self, pantalla, x, y, tamaño):
        """Dibuja un icono de moneda giratorio"""
        tiempo = pygame.time.get_ticks() * 0.005
        escala = abs(math.cos(tiempo)) * 0.5 + 0.5
        
        pygame.draw.circle(pantalla, AMARILLO, (x + tamaño // 2, y + tamaño // 2), int(tamaño // 2 * escala))
        pygame.draw.circle(pantalla, NARANJA, (x + tamaño // 2, y + tamaño // 2), int(tamaño // 2 * escala), 2)
        
        if escala > 0.3:
            fuente_mini = pygame.font.Font(None, 16)
            texto = fuente_mini.render("$", True, NARANJA)
            pantalla.blit(texto, (x + 6, y + 5))
    
    def dibujar(self):
        """Dibuja todos los elementos del juego"""
        # Cielo con degradado
        for y in range(ALTO):
            color = (
                int(107 + (200 - 107) * y / ALTO),
                int(140 + (220 - 140) * y / ALTO),
                int(255)
            )
            pygame.draw.line(self.pantalla, color, (0, y), (ANCHO, y))
        
        # Actualizar y dibujar nubes
        for nube in self.nubes:
            nube.actualizar()
            nube.dibujar(self.pantalla)
        
        # Dibujar elementos del juego
        for plataforma in self.plataformas:
            plataforma.dibujar(self.pantalla)
            
        for moneda in self.monedas:
            moneda.actualizar()
            moneda.dibujar(self.pantalla)
            
        for enemigo in self.enemigos:
            enemigo.mover(self.plataformas)
            enemigo.dibujar(self.pantalla)

        # Dibujar jugador
        self.jugador.dibujar(self.pantalla, self.particulas)

        # Dibujar estrellas
        for estrella in self.estrellas[:]:
            estrella.actualizar()
            estrella.dibujar(self.pantalla)
            if estrella.vida <= 0:
                self.estrellas.remove(estrella)

        # Dibujar partículas
        for particula in self.particulas[:]:
            particula.actualizar()
            particula.dibujar(self.pantalla)
            if particula.vida <= 0:
                self.particulas.remove(particula)

        # HUD
        self.dibujar_hud()

        # Pantalla de victoria con confeti
        if self.victoria:
            # Crear confeti de celebración
            if len(self.estrellas) < 50:
                for _ in range(5):
                    x = random.randint(0, ANCHO)
                    color = random.choice([AMARILLO, CYAN, ROSA, VERDE, NARANJA, MORADO])
                    self.estrellas.append(Estrella(x, -10, color))
            
            # Fondo semi-transparente
            superficie_victoria = pygame.Surface((ANCHO, ALTO))
            superficie_victoria.set_alpha(150)
            superficie_victoria.fill((0, 0, 0))
            self.pantalla.blit(superficie_victoria, (0, 0))
            
            texto = self.fuente_grande.render("¡NIVEL COMPLETADO!", True, AMARILLO)
            texto_rect = texto.get_rect(center=(ANCHO // 2, ALTO // 2 - 40))
            # Sombra del texto
            texto_sombra = self.fuente_grande.render("¡NIVEL COMPLETADO!", True, NARANJA)
            self.pantalla.blit(texto_sombra, (texto_rect.x + 3, texto_rect.y + 3))
            self.pantalla.blit(texto, texto_rect)

            texto2 = self.fuente_menu.render("Presiona ESC para salir", True, BLANCO)
            self.pantalla.blit(texto2, texto2.get_rect(center=(ANCHO // 2, ALTO // 2 + 20)))

        # Game Over
        if self.jugador.vidas <= 0:
            self.game_over = True
            
            # Fondo semi-transparente
            superficie_go = pygame.Surface((ANCHO, ALTO))
            superficie_go.set_alpha(150)
            superficie_go.fill((0, 0, 0))
            self.pantalla.blit(superficie_go, (0, 0))
            
            texto = self.fuente_grande.render("GAME OVER", True, ROJO_CLARO)
            texto_rect = texto.get_rect(center=(ANCHO // 2, ALTO // 2 - 20))
            # Sombra del texto
            texto_sombra = self.fuente_grande.render("GAME OVER", True, ROJO)
            self.pantalla.blit(texto_sombra, (texto_rect.x + 3, texto_rect.y + 3))
            self.pantalla.blit(texto, texto_rect)

            texto2 = self.fuente_menu.render("Presiona ESC para salir", True, BLANCO)
            self.pantalla.blit(texto2, texto2.get_rect(center=(ANCHO // 2, ALTO // 2 + 40)))

    def ejecutar(self):
        """Bucle principal del juego"""
        ejecutando = True
        while ejecutando:
            self.reloj.tick(FPS)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        ejecutando = False

            teclas = pygame.key.get_pressed()

            if not self.game_over and not self.victoria:
                self.jugador.mover(teclas, self.plataformas)
                self.verificar_colisiones()

            self.dibujar()
            pygame.display.flip()

        pygame.quit()
        sys.exit()


# =========================
# INICIAR EL JUEGO
# =========================
if __name__ == "__main__":
    juego = Juego()
    juego.ejecutar()