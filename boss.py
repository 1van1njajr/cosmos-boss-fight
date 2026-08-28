from setting import *

import math
import random
import sys
import pygame

WIDTH, HEIGHT = 1000, 700
CENTER = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
ORBIT_RADIUS = 230
FPS = 60

pygame.init()
pygame.display.set_caption("Boss Fight!")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FONT_BIG = pygame.font.SysFont("arial", 64, bold=True)
FONT_MED = pygame.font.SysFont("arial", 32, bold=True)
FONT_SMALL = pygame.font.SysFont("arial", 20, bold=True)


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def angle_diff(a, b):
    d = (a - b) % (2 * math.pi)
    if d > math.pi:
        d -= 2 * math.pi
    return d

class Player:

    ORBIT_SPEED = 2.0       
    RADIAL_SPEED = 220.0    
    MIN_RADIUS = 130
    MAX_RADIUS = 310

    def __init__(self, angle, color, dark, keys, name):
        self.angle = angle
        self.color = color
        self.dark = dark
        self.keys = keys 
        self.name = name
        self.score = 0
        self.alive = True
        self.orbit_radius = ORBIT_RADIUS
        self.direction = 1  
        self.hit_this_frame = False  

    def pos(self):
        return CENTER + pygame.Vector2(math.cos(self.angle), math.sin(self.angle)) * self.orbit_radius

    def update(self, dt, keys_pressed):
        self.hit_this_frame = False

        if not self.alive:
            return

        ccw_keys, cw_keys, out_keys, in_keys = self.keys

        if any(keys_pressed[k] for k in ccw_keys):
            self.direction = -1
        elif any(keys_pressed[k] for k in cw_keys):
            self.direction = 1
        self.angle += self.direction * self.ORBIT_SPEED * dt

        if any(keys_pressed[k] for k in out_keys):
            self.orbit_radius += self.RADIAL_SPEED * dt
        elif any(keys_pressed[k] for k in in_keys):
            self.orbit_radius -= self.RADIAL_SPEED * dt
        self.orbit_radius = clamp(self.orbit_radius, self.MIN_RADIUS, self.MAX_RADIUS)

    def take_hit(self):
        """One life only - any hit ends the run."""
        if not self.alive:
            return
        self.alive = False
        self.hit_this_frame = True

    def draw(self, surf):
        p = self.pos()
        col = self.color if self.alive else (90, 90, 90)

        facing = self.angle + math.pi / 2
        size = 16
        tip = p + pygame.Vector2(math.cos(facing), math.sin(facing)) * size
        left = p + pygame.Vector2(math.cos(facing + 2.5), math.sin(facing + 2.5)) * size
        right = p + pygame.Vector2(math.cos(facing - 2.5), math.sin(facing - 2.5)) * size
        pygame.draw.polygon(surf, self.dark, [tip, left, right])
        pygame.draw.polygon(surf, col, [tip, left, right], width=0 if self.alive else 3)
        pygame.draw.circle(surf, WHITE, (int(p.x), int(p.y)), 4)

class HomingOrb:

    def __init__(self, owner_player, target_pos, reward):
        self.owner_player = owner_player
        self.reward = reward
        self.pos = pygame.Vector2(CENTER)
        self.target = pygame.Vector2(target_pos)
        direction = (self.target - self.pos)
        if direction.length() == 0:
            direction = pygame.Vector2(1, 0)
        else:
            direction = direction.normalize()
        self.vel = direction * 260
        self.dead = False
        self.hit_player = False
        self.expired_safely = False
        self.radius = 10
        self.life = 3.0

    def update(self, dt):
        self.pos += self.vel * dt
        self.life -= dt
        if self.life <= 0 and not self.dead:
            self.dead = True
            if not self.hit_player:
                self.expired_safely = True

    def draw(self, surf):
        pygame.draw.circle(surf, (255, 140, 60), (int(self.pos.x), int(self.pos.y)), self.radius)
        pygame.draw.circle(surf, (255, 210, 140), (int(self.pos.x), int(self.pos.y)), self.radius - 4)

class Boss:
    def __init__(self):
        self.pos = pygame.Vector2(CENTER)
        self.state = "idle"      
        self.state_timer = 2.0
        self.attack_name = None
        self.beam_angle = 0.0
        self.beam_dir = 1
        self.beam_speed = 1.6
        self.shockwave_r = 0.0
        self.lock_angle = 0.0
        self.spike_arcs = []      
        self.flash = 0.0
        self.shake = 0.0
        self.bob = 0.0
        self.elapsed = 0.0       
        self.attack_landed = False  
        self.pending_reward = None  

    @property
    def phase(self):
        if self.elapsed < 20:
            return 1
        elif self.elapsed < 45:
            return 2
        return 3

    def pick_attack(self):
        options = ["beam", "shockwave", "orbs", "lock_beam"]
        if self.phase >= 2:
            options += ["slam", "spike_ring"]
        if self.phase >= 3:
            options += ["beam", "orbs", "lock_beam", "meteors"]
        return random.choice(options)

    def update(self, dt, players, orbs):
        self.bob += dt
        self.elapsed += dt
        self.pending_reward = None
        if self.flash > 0:
            self.flash -= dt
        if self.shake > 0:
            self.shake -= dt

        self.state_timer -= dt

        if self.state == "idle":
            if self.state_timer <= 0:
                self.attack_name = self.pick_attack()
                self.state = "telegraph"
                self.state_timer = 0.9 if self.phase < 3 else 0.6
                alive = [p for p in players if p.alive]
                if self.attack_name == "lock_beam" and alive:
                    self.lock_angle = alive[0].angle
                elif self.attack_name == "spike_ring":
                    num_arcs = 1 if self.phase < 3 else 2
                    self.spike_arcs = [
                        (random.uniform(0, 2 * math.pi), 0.55) for _ in range(num_arcs)
                    ]

        elif self.state == "telegraph":
            self.flash = 0.15
            if self.state_timer <= 0:
                self.start_attack(players, orbs)

        elif self.state == "attack":
            self.run_attack(dt, players, orbs)
            if self.state_timer <= 0:
                if self.attack_name not in ("orbs", "meteors") and not self.attack_landed:
                    self.pending_reward = (1, self.attack_name)
                self.state = "idle"
                base_pause = 1.4 - (self.phase - 1) * 0.35
                self.state_timer = max(0.4, base_pause)

    def start_attack(self, players, orbs):
        self.state = "attack"
        self.attack_landed = False

        if self.attack_name == "beam":
            self.beam_angle = random.uniform(0, 2 * math.pi)
            self.beam_dir = random.choice([-1, 1])
            speed_mult = 1 + (self.phase - 1) * 0.35
            self.beam_speed = 1.6 * speed_mult
            self.state_timer = 3.0

        elif self.attack_name == "shockwave":
            self.shockwave_r = 60
            self.state_timer = 1.2

        elif self.attack_name == "orbs":
            alive_players = [p for p in players if p.alive]
            for p in alive_players:
                orbs.append(HomingOrb(p, p.pos(), 1))
            self.state_timer = 0.4

        elif self.attack_name == "slam":
            self.shake = 0.5
            self.state_timer = 0.6

        elif self.attack_name == "lock_beam":
            self.state_timer = 0.35

        elif self.attack_name == "spike_ring":
            self.state_timer = 0.5

        elif self.attack_name == "meteors":
            alive_players = [p for p in players if p.alive]
            owner = alive_players[0] if alive_players else None
            count = 4 if self.phase < 3 else 6
            for _ in range(count):
                angle = random.uniform(0, 2 * math.pi)
                target = CENTER + pygame.Vector2(math.cos(angle), math.sin(angle)) * ORBIT_RADIUS
                orbs.append(HomingOrb(owner, target, 1))
            if owner is not None:
                orbs.append(HomingOrb(owner, owner.pos(), 1))
            self.state_timer = 0.3

    def run_attack(self, dt, players, orbs):
        if self.attack_name == "beam":
            self.beam_angle += self.beam_dir * self.beam_speed * dt
            for p in players:
                if not p.alive:
                    continue
                to_player = (p.pos() - self.pos)
                if to_player.length() == 0:
                    continue
                ang_to_player = math.atan2(to_player.y, to_player.x)
                if abs(angle_diff(ang_to_player, self.beam_angle)) < 0.09:
                    p.take_hit()
                    if p.hit_this_frame:
                        self.attack_landed = True

        elif self.attack_name == "shockwave":
            self.shockwave_r += 420 * dt
            for p in players:
                if not p.alive:
                    continue
                dist = p.pos().distance_to(self.pos)
                if abs(dist - self.shockwave_r) < 18:
                    p.take_hit()
                    if p.hit_this_frame:
                        self.attack_landed = True

        elif self.attack_name == "slam":
            for p in players:
                if not p.alive:
                    continue
                if p.pos().distance_to(self.pos) < 150:
                    p.take_hit()
                    if p.hit_this_frame:
                        self.attack_landed = True

        elif self.attack_name == "lock_beam":
            for p in players:
                if not p.alive:
                    continue
                if abs(angle_diff(p.angle, self.lock_angle)) < 0.11:
                    p.take_hit()
                    if p.hit_this_frame:
                        self.attack_landed = True

        elif self.attack_name == "spike_ring":
            for p in players:
                if not p.alive:
                    continue
                near_nominal_ring = abs(p.orbit_radius - ORBIT_RADIUS) < 45
                if not near_nominal_ring:
                    continue
                for center, halfwidth in self.spike_arcs:
                    if abs(angle_diff(p.angle, center)) < halfwidth:
                        p.take_hit()
                        if p.hit_this_frame:
                            self.attack_landed = True
                        break

    def draw(self, surf):
        offset = pygame.Vector2(0, math.sin(self.bob * 2) * 6)
        shake_off = pygame.Vector2(0, 0)
        if self.shake > 0:
            shake_off = pygame.Vector2(random.uniform(-6, 6), random.uniform(-6, 6))
        p = self.pos + offset + shake_off

        body_col = BOSS_COLOR_FLASH if self.flash > 0 else BOSS_COLOR

        if self.state in ("telegraph", "attack") and self.attack_name == "beam":
            self.draw_beam(surf, p)
        if self.state == "attack" and self.attack_name == "shockwave":
            pygame.draw.circle(surf, (255, 210, 90), (int(p.x), int(p.y)), int(self.shockwave_r), 6)
        if self.state in ("telegraph", "attack") and self.attack_name == "lock_beam":
            self.draw_lock_beam(surf, p)
        if self.state in ("telegraph", "attack") and self.attack_name == "spike_ring":
            self.draw_spike_arcs(surf)
        if self.state == "attack" and self.attack_name == "slam":
            pygame.draw.circle(surf, (255, 120, 90), (int(p.x), int(p.y)), 150, 5)

        pygame.draw.circle(surf, (50, 40, 60), (int(p.x), int(p.y + 4)), 62) 
        pygame.draw.circle(surf, body_col, (int(p.x), int(p.y)), 58)

        eye_offsets = [(-38, -46), (0, -62), (38, -46)]
        for ox, oy in eye_offsets:
            ex, ey = p.x + ox, p.y + oy
            pygame.draw.circle(surf, (50, 40, 60), (int(ex), int(ey)), 24)
            pygame.draw.circle(surf, EYE_WHITE, (int(ex), int(ey)), 20)
            look = pygame.Vector2(0, 0)
            pygame.draw.circle(surf, EYE_RED, (int(ex), int(ey)), 12)
            pygame.draw.circle(surf, BLACK, (int(ex), int(ey)), 6)

        mouth_open = 6 if self.state != "attack" else 14
        pygame.draw.ellipse(surf, (25, 15, 30), (p.x - 18, p.y + 6, 36, mouth_open))

    def draw_beam(self, surf, p):
        length = 900
        end = p + pygame.Vector2(math.cos(self.beam_angle), math.sin(self.beam_angle)) * length
        color = WARN_COLOR if self.state == "telegraph" else (255, 90, 70)
        width = 3 if self.state == "telegraph" else 10
        pygame.draw.line(surf, color, p, end, width)

    def draw_lock_beam(self, surf, p):
        length = 900
        end = p + pygame.Vector2(math.cos(self.lock_angle), math.sin(self.lock_angle)) * length
        color = WARN_COLOR if self.state == "telegraph" else (255, 60, 50)
        width = 2 if self.state == "telegraph" else 12
        pygame.draw.line(surf, color, p, end, width)
        reticle_pos = CENTER + pygame.Vector2(math.cos(self.lock_angle), math.sin(self.lock_angle)) * ORBIT_RADIUS
        pygame.draw.circle(surf, color, (int(reticle_pos.x), int(reticle_pos.y)), 14, 3)

    def draw_spike_arcs(self, surf):
        color = WARN_COLOR if self.state == "telegraph" else (255, 60, 50)
        width = 6 if self.state == "telegraph" else 16
        steps = 24
        for center, halfwidth in self.spike_arcs:
            points = []
            for i in range(steps + 1):
                a = center - halfwidth + (2 * halfwidth) * (i / steps)
                x = CENTER.x + math.cos(a) * ORBIT_RADIUS
                y = CENTER.y + math.sin(a) * ORBIT_RADIUS
                points.append((x, y))
            pygame.draw.lines(surf, color, False, points, width)

class Game:
    def __init__(self):
        self.high_score = 0
        self.reset()

    def reset(self):
        self.boss = Boss()
        self.p1 = Player(
            math.pi, P1_COLOR, P1_DARK,
            (
                (pygame.K_LEFT, pygame.K_a),  
                (pygame.K_RIGHT, pygame.K_d),   
                (pygame.K_UP, pygame.K_w),    
                (pygame.K_DOWN, pygame.K_s),  
            ),
            "Player",
        )
        self.players = [self.p1]
        self.orbs = []
        self.popups = [] 
        self.state = "playing"  
        self.stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT), random.uniform(1, 2.4))
                      for _ in range(60)]

    def add_score(self, player, points, pos):
        player.score += points
        self.popups.append([f"+{points}", pygame.Vector2(pos), 1.0])

    def update(self, dt, keys_pressed):
        if self.state != "playing":
            return

        for p in self.players:
            p.update(dt, keys_pressed)

        self.boss.update(dt, self.players, self.orbs)

        if self.boss.pending_reward:
            points, _name = self.boss.pending_reward
            self.add_score(self.p1, points, self.p1.pos())

        for o in self.orbs:
            o.update(dt)
            for p in self.players:
                if p.alive and not o.hit_player and o.pos.distance_to(p.pos()) < 22:
                    p.take_hit()
                    o.hit_player = True
                    o.dead = True
        for o in self.orbs:
            if o.dead and o.expired_safely and o.owner_player is not None:
                self.add_score(o.owner_player, o.reward, o.owner_player.pos())
        self.orbs = [o for o in self.orbs if not o.dead]

        for pop in self.popups:
            pop[2] -= dt
            pop[1].y -= 40 * dt
        self.popups = [pop for pop in self.popups if pop[2] > 0]

        if all(not p.alive for p in self.players):
            self.state = "lose"
            self.high_score = max(self.high_score, self.p1.score)

    def draw(self, surf):
        surf.fill(BG_PURPLE)
        for (x, y, s) in self.stars:
            pygame.draw.circle(surf, (200, 130, 210), (x, y), s)

        pygame.draw.circle(surf, RING_COLOR, (int(CENTER.x), int(CENTER.y)), ORBIT_RADIUS, 2)

        for o in self.orbs:
            o.draw(surf)

        self.boss.draw(surf)
        for p in self.players:
            p.draw(surf)

        for text, pos, life in self.popups:
            alpha_col = (255, 230, 90)
            label = FONT_MED.render(text, True, alpha_col)
            surf.blit(label, (pos.x - label.get_width() // 2, pos.y - 50))

        self.draw_hud(surf)

        if self.state == "lose":
            self.draw_center_text(surf, "GAME OVER", RED_HP,
                                   f"Score: {self.p1.score}   Best: {self.high_score}   Press R to try again")

    def draw_hud(self, surf):
        label = FONT_SMALL.render(
            f"PHASE {self.boss.phase}   -   Survived {int(self.boss.elapsed)}s", True, WHITE)
        surf.blit(label, (WIDTH // 2 - label.get_width() // 2, 20))

        self.draw_player_panel(surf, self.p1, (20, 20))

    def draw_player_panel(self, surf, p, top_left):
        x, y = top_left
        pygame.draw.rect(surf, p.dark, (x, y, 220, 60), border_radius=10)
        pygame.draw.rect(surf, p.color, (x, y, 220, 60), width=3, border_radius=10)
        name = FONT_SMALL.render(f"Score: {p.score}", True, WHITE)
        surf.blit(name, (x + 10, y + 8))
        status_col = (90, 220, 110) if p.alive else (200, 60, 60)
        status_text = "ALIVE" if p.alive else "HIT!"
        pygame.draw.circle(surf, status_col, (x + 18, y + 42), 8)
        st = FONT_SMALL.render(status_text, True, WHITE)
        surf.blit(st, (x + 34, y + 34))

    def draw_center_text(self, surf, text, color, sub):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        surf.blit(overlay, (0, 0))
        t = FONT_BIG.render(text, True, color)
        surf.blit(t, (WIDTH // 2 - t.get_width() // 2, HEIGHT // 2 - 60))
        s = FONT_MED.render(sub, True, WHITE)
        surf.blit(s, (WIDTH // 2 - s.get_width() // 2, HEIGHT // 2 + 20))


def main():
    game = Game()
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_r and game.state != "playing":
                    game.reset()

        keys_pressed = pygame.key.get_pressed()
        game.update(dt, keys_pressed)
        game.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()