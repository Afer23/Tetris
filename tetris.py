import math
import os
import random
import tempfile
import time
import wave
from array import array

import pygame


WIDTH, HEIGHT = 900, 700
GROUND_Y = HEIGHT - 70
FPS = 60

BLOCK_SIZE = 50
START_BLOCK_SPEED = 4.0
GRAVITY = 0.8
JUMP_POWER = -16
PLAYER_SPEED = 6


class Stickman:
    def __init__(self):
        self.w = 36
        self.h = 84
        self.x = WIDTH // 2
        self.y = GROUND_Y - self.h
        self.vy = 0
        self.on_ground = True
        self.color = (235, 235, 235)
        self.hit_flash = 0

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def move(self, direction):
        self.x += direction * PLAYER_SPEED
        self.x = max(0, min(WIDTH - self.w, self.x))

    def jump(self):
        if self.on_ground:
            self.vy = JUMP_POWER
            self.on_ground = False

    def update(self):
        self.vy += GRAVITY
        self.y += self.vy
        if self.y >= GROUND_Y - self.h:
            self.y = GROUND_Y - self.h
            self.vy = 0
            self.on_ground = True
        if self.hit_flash > 0:
            self.hit_flash -= 1

    def draw(self, screen):
        c = (255, 70, 70) if self.hit_flash > 0 else self.color
        head_center = (self.x + self.w // 2, self.y + 12)
        body_top = (self.x + self.w // 2, self.y + 25)
        body_bottom = (self.x + self.w // 2, self.y + 58)
        arm_left = (self.x + 6, self.y + 40)
        arm_right = (self.x + self.w - 6, self.y + 40)
        leg_left = (self.x + 8, self.y + self.h)
        leg_right = (self.x + self.w - 8, self.y + self.h)

        pygame.draw.circle(screen, c, head_center, 11, 3)
        pygame.draw.line(screen, c, body_top, body_bottom, 4)
        pygame.draw.line(screen, c, arm_left, arm_right, 4)
        pygame.draw.line(screen, c, body_bottom, leg_left, 4)
        pygame.draw.line(screen, c, body_bottom, leg_right, 4)


class FallingBlock:
    def __init__(self, speed, giant=False):
        size = BLOCK_SIZE * (2 if giant else 1)
        self.w = size
        self.h = size
        self.x = random.randint(0, WIDTH - self.w)
        self.y = -self.h - random.randint(0, 200)
        self.speed = speed
        self.color = random.choice([
            (62, 240, 255),
            (255, 70, 195),
            (154, 255, 72),
            (255, 204, 60),
            (140, 118, 255),
        ])

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def update(self):
        self.y += self.speed

    def draw(self, screen):
        r = self.rect
        pygame.draw.rect(screen, self.color, r, border_radius=4)
        pygame.draw.rect(screen, (255, 255, 255), r, 2, border_radius=4)


def build_techno_track(path, duration=28, sample_rate=44100):
    total_samples = duration * sample_rate
    beat = 0.38
    data = array('h')

    for i in range(total_samples):
        t = i / sample_rate
        pulse = 0.35 if (t % beat) < 0.06 else 0.0
        bass = math.sin(2 * math.pi * 55 * t + 0.6 * math.sin(2 * math.pi * 2 * t))
        arp = math.sin(2 * math.pi * (220 + 20 * math.sin(2 * math.pi * 0.5 * t)) * t)
        hi = math.sin(2 * math.pi * 880 * t) * (0.20 if (t % 0.19) < 0.02 else 0.0)
        val = 0.48 * bass + 0.30 * arp + 0.22 * hi + pulse
        sample = int(max(-1, min(1, val)) * 32767)
        data.append(sample)

    with wave.open(path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(data.tobytes())


def draw_background(screen, tick):
    screen.fill((10, 10, 20))
    for i in range(12):
        x = (i * 90 + tick * 0.6) % WIDTH
        y = int(130 + 40 * math.sin((tick + i * 17) * 0.03))
        pygame.draw.circle(screen, (30, 35, 70), (int(x), y), 26, 2)

    pygame.draw.rect(screen, (20, 22, 40), (0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y))
    for x in range(0, WIDTH, 40):
        pygame.draw.line(screen, (35, 38, 70), (x, GROUND_Y), (x + 20, HEIGHT), 1)


def main():
    pygame.init()
    pygame.display.set_caption("Stickman Drop: Neo-Tetris Arcade")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    pygame.mixer.init()
    tmp_wav = os.path.join(tempfile.gettempdir(), "dramatic_techno_loop.wav")
    if not os.path.exists(tmp_wav):
        build_techno_track(tmp_wav)
    pygame.mixer.music.load(tmp_wav)
    pygame.mixer.music.play(-1)

    font = pygame.font.SysFont("consolas", 26, bold=True)
    big = pygame.font.SysFont("consolas", 56, bold=True)

    player = Stickman()
    blocks = []

    score = 0
    level = 1
    lives = 1
    spawn_interval = 0.7
    last_spawn = 0
    start_time = time.time()
    game_over = False
    challenge_msg = "DESAFÍO: SOBREVIve AL CAOS"

    while True:
        dt = clock.tick(FPS) / 1000.0
        now = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_w, pygame.K_UP, pygame.K_SPACE):
                    player.jump()
                if game_over and event.key == pygame.K_r:
                    return main()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player.move(-1)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player.move(1)

        if not game_over:
            elapsed = now - start_time
            level = min(20, 1 + int(elapsed // 10))
            speed = START_BLOCK_SPEED + level * 0.45
            spawn_interval = max(0.16, 0.72 - level * 0.03)

            if now - last_spawn > spawn_interval:
                giant = level > 4 and random.random() < min(0.32, level / 30)
                blocks.append(FallingBlock(speed, giant=giant))
                last_spawn = now

            player.update()
            score += int(12 * dt * level)

            if level % 5 == 0:
                challenge_msg = "DESAFÍO: BLOQUES GIGANTES"
            elif level % 3 == 0:
                challenge_msg = "DESAFÍO: LLUVIA TECNO"
            else:
                challenge_msg = "DESAFÍO: REFLEJOS ARCADE"

            for b in blocks[:]:
                b.speed = speed + (2.3 if b.w > BLOCK_SIZE else 0)
                b.update()
                if b.rect.colliderect(player.rect):
                    lives -= 1
                    player.hit_flash = 20
                    game_over = True
                elif b.y > HEIGHT + 10:
                    blocks.remove(b)
                    score += 9

        draw_background(screen, pygame.time.get_ticks())
        for b in blocks:
            b.draw(screen)
        player.draw(screen)

        hud = [
            f"PUNTOS: {score}",
            f"NIVEL: {level}",
            "CONTROLES: A/D + ESPACIO",
        ]
        for i, text in enumerate(hud):
            s = font.render(text, True, (235, 240, 255))
            screen.blit(s, (20, 18 + 28 * i))

        c = font.render(challenge_msg, True, (255, 95, 170))
        screen.blit(c, (20, 106))

        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 170))
            screen.blit(overlay, (0, 0))
            g1 = big.render("GAME OVER", True, (255, 70, 70))
            g2 = font.render("El stickman fue aplastado", True, (255, 255, 255))
            g3 = font.render("Pulsa R para reiniciar", True, (255, 255, 255))
            screen.blit(g1, (WIDTH // 2 - g1.get_width() // 2, HEIGHT // 2 - 80))
            screen.blit(g2, (WIDTH // 2 - g2.get_width() // 2, HEIGHT // 2))
            screen.blit(g3, (WIDTH // 2 - g3.get_width() // 2, HEIGHT // 2 + 42))

        pygame.display.flip()


if __name__ == "__main__":
    main()
