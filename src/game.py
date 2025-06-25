import pygame
import random
import config
from objects import Krug, Bier, Zapfhahn

class Game:
    def __init__(self):
        self.krug = Krug()
        self.zapfhaehne = [Zapfhahn(x) for x in config.ZAPFHAHN_POSITIONS]
        self.biere = []
        self.score = 0
        self.lives = config.START_LIVES
        self.game_over = False
        self.spawn_timer = 0
        self.spawn_interval = 60  # ca. 1 Sekunde bei 60 FPS
        self.tropf_timer = [0, 0, 0]  # Ein Timer für jeden Zapfhahn
        self.stange_anzeige_timer = 0
        self.stange_anzeige_state = None  # None, "leer", "voll"
        self.stange_leer_img = pygame.transform.smoothscale(
            pygame.image.load("assets/stange_leer.png"), (80, 80)
        )
        self.stange_voll_img = pygame.transform.smoothscale(
            pygame.image.load("assets/stange_voll.png"), (80, 80)
        )
        self.krug_ersetzt = False
        self.highscore = 0

    def reset(self):
        self.__init__()

    def update(self, keys):
        if self.game_over:
            return

        # Krug bewegen
        if keys[pygame.K_LEFT]:
            self.krug.move("left")
        if keys[pygame.K_RIGHT]:
            self.krug.move("right")

        # Biere erzeugen
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            idx = random.randrange(len(self.zapfhaehne))
            zapfhahn = self.zapfhaehne[idx]
            self.biere.append(Bier(zapfhahn.x))
            self.spawn_timer = 0
            self.tropf_timer[idx] = 25  # Zapfhahn tropft für 20 Frames (langsamer)

        # Tropf-Status aktualisieren
        for i, zapfhahn in enumerate(self.zapfhaehne):
            tropft = self.tropf_timer[i] > 0
            zapfhahn.update(tropft)
            if self.tropf_timer[i] > 0:
                self.tropf_timer[i] -= 1

        # Biere bewegen und Kollision prüfen
        for bier in self.biere[:]:
            bier.update()
            if bier.is_caught_by(self.krug):
                self.score += 1
                self.biere.remove(bier)
            elif bier.is_missed():
                self.lives -= 1
                self.biere.remove(bier)
                if self.lives <= 0:
                    self.game_over = True

        # Krug füllen, sobald mindestens 1 Punkt
        self.krug.set_voll(self.score > 0)

        # Literanzeige voll? Dann Animation starten und Krug dauerhaft ersetzen
        if self.score >= 20 and not self.krug_ersetzt:
            self.stange_anzeige_state = "leer"
            self.stange_anzeige_timer = 30  # Frames für "leer"
            self.score = 0
            self.krug_ersetzt = True

        # Animation ablaufen lassen
        if self.stange_anzeige_state == "leer":
            self.stange_anzeige_timer -= 1
            if self.stange_anzeige_timer <= 0:
                self.stange_anzeige_state = "voll"
                # kein Timer mehr, bleibt auf "voll"

    def draw(self, screen, font):
        screen.fill(config.BG_COLOR)
        # Zapfhähne
        for zapfhahn in self.zapfhaehne:
            zapfhahn.draw(screen)
        # Biere
        for bier in self.biere:
            bier.draw(screen)
        # Krug
        self.krug.draw(screen)

        # Krug/Stangen-Anzeige unten
        if self.stange_anzeige_state == "leer":
            screen.blit(self.stange_leer_img, self.krug.rect)
        elif self.stange_anzeige_state == "voll" or self.krug_ersetzt:
            screen.blit(self.stange_voll_img, self.krug.rect)
        else:
            self.krug.draw(screen)

        # Liter-Anzeige (wie gehabt, aber startet wieder bei 0)
        bar_x = 30
        bar_y = 80
        bar_width = 40
        bar_height = 300

        # Hintergrund (Glas-Umriss)
        pygame.draw.rect(screen, (200, 180, 100), (bar_x, bar_y, bar_width, bar_height), 4, border_radius=10)
        # Highscore-Umriss
        if self.highscore > 0:
            hs_fill = bar_height * min(self.highscore / 20, 1.0)  # z.B. 20 Punkte = voll
            pygame.draw.rect(screen, (230, 230, 230), (bar_x-3, bar_y+bar_height-hs_fill, bar_width+6, hs_fill), 2, border_radius=10)
        # Füllstand (Bier)
        if self.score > 0:
            fill = bar_height * min(self.score / 20, 1.0)
            pygame.draw.rect(screen, (255, 210, 60), (bar_x, bar_y+bar_height-fill, bar_width, fill), 0, border_radius=10)
            # Schaumkrone
            if self.score >= self.highscore:
                pygame.draw.ellipse(screen, (255,255,255), (bar_x-5, bar_y-18, bar_width+10, 30))

        # UI
        lives_text = font.render(f"Leben: {self.lives}", True, config.TEXT_COLOR)
        screen.blit(lives_text, (config.SCREEN_WIDTH - 10 - lives_text.get_width(), 10))
        # Game Over
        if self.game_over:
            go_text = font.render("Game Over! Drücke R zum Neustart.", True, (200, 0, 0))
            screen.blit(go_text, (config.SCREEN_WIDTH // 2 - go_text.get_width() // 2, config.SCREEN_HEIGHT // 2))
