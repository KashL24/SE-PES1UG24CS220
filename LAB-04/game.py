import random
import pygame

WIDTH, HEIGHT = 800, 600
GROUND_Y = HEIGHT - 40
INTERCEPTOR_SPEED, EXPLOSION_MAX, EXPLOSION_TIME = 420, 45, 1.2
AMMO_PER_BATTERY = 10

# ============================================================
# CITY DESTRUCTION WARNING
# ============================================================

city_warning_text = ""
city_warning_until = 0


# ============================================================
# TASK 2: EXPLOSION COLOR
# ============================================================

def explosion_color(progress):
    """
    Explosion color changes from white-hot to red
    as the explosion progresses.

    0.0 -> White
    0.5 -> Yellow
    1.0 -> Red
    """

    progress = max(0.0, min(1.0, progress))

    if progress < 0.5:
        # White -> Yellow
        t = progress / 0.5

        r = 255
        g = 255
        b = int(255 * (1 - t))

    else:
        # Yellow -> Red
        t = (progress - 0.5) / 0.5

        r = 255
        g = int(255 * (1 - t))
        b = 0

    return (r, g, b)


# ============================================================
# TASK 3: CITY DESTROYED CALLBACK
# ============================================================

def on_city_destroyed(city):
    """
    Called when a city is destroyed.

    Displays a visible warning inside the game.
    """

    global city_warning_text
    global city_warning_until

    city_warning_text = "CITY DESTROYED!"
    city_warning_until = pygame.time.get_ticks() + 1500


# ============================================================
# TASK 4: CITY REPAIR THRESHOLD
# ============================================================

def city_repair_threshold():
    """
    A destroyed city is rebuilt every time the score
    crosses a multiple of 2000.
    """

    return 2000


# ============================================================
# BATTERY
# ============================================================

class Battery:

    def __init__(self, x):

        self.pos = pygame.Vector2(
            x,
            GROUND_Y
        )

        self.ammo = AMMO_PER_BATTERY
        self.alive = True


# ============================================================
# CITY
# ============================================================

class City:

    def __init__(self, x):

        self.pos = pygame.Vector2(
            x,
            GROUND_Y
        )

        self.alive = True


# ============================================================
# INTERCEPTOR
# ============================================================

class Interceptor:

    def __init__(self, origin, target):

        self.pos = pygame.Vector2(origin)
        self.origin = pygame.Vector2(origin)
        self.target = pygame.Vector2(target)

    def update(self, dt):

        offset = self.target - self.pos

        if offset.length() < 6:
            return True

        self.pos += (
            offset.normalize()
            * INTERCEPTOR_SPEED
            * dt
        )

        return False


# ============================================================
# EXPLOSION
# ============================================================

class Explosion:

    def __init__(
        self,
        pos,
        max_radius=EXPLOSION_MAX
    ):

        self.pos = pygame.Vector2(pos)
        self.max_radius = max_radius
        self.age = 0.0

    @property
    def progress(self):

        return self.age / EXPLOSION_TIME

    @property
    def radius(self):

        return self.max_radius * (
            1 - abs(
                2 * self.progress - 1
            )
        )

    @property
    def done(self):

        return self.age >= EXPLOSION_TIME


# ============================================================
# MISSILE
# ============================================================

class Missile:

    def __init__(
        self,
        target,
        speed
    ):

        self.origin = pygame.Vector2(
            random.randint(20, WIDTH - 20),
            0
        )

        self.pos = pygame.Vector2(
            self.origin
        )

        self.target = target

        self.velocity = (
            target.pos - self.origin
        ).normalize() * speed

    def update(self, dt):

        self.pos += self.velocity * dt

        return (
            self.pos.y
            >= GROUND_Y - 4
        )


# ============================================================
# GAME
# ============================================================

class Game:

    def __init__(self):

        self.font = pygame.font.Font(
            None,
            26
        )

        self.warning_font = pygame.font.Font(
            None,
            42
        )

        self.reset()

    # ========================================================
    # RESET
    # ========================================================

    def reset(self):

        self.batteries = [
            Battery(60),
            Battery(WIDTH / 2),
            Battery(WIDTH - 60)
        ]

        xs = [
            150,
            230,
            310,
            490,
            570,
            650
        ]

        self.cities = [
            City(x)
            for x in xs
        ]

        self.score = 0
        self.wave = 1
        self.state = "play"

        self.repairs_awarded = 0

        self.start_wave()

    # ========================================================
    # START WAVE
    # ========================================================

    def start_wave(self):

        self.missiles = []
        self.interceptors = []
        self.explosions = []

        self.to_spawn = (
            6 + self.wave * 2
        )

        self.spawn_timer = 1.0

        for battery in self.batteries:

            battery.alive = True
            battery.ammo = AMMO_PER_BATTERY

    # ========================================================
    # TASK 1: FIX BATTERY SELECTION
    # ========================================================

    def nearest_battery(self, target):

        available = [
            battery
            for battery in self.batteries
            if battery.alive
            and battery.ammo > 0
        ]

        if not available:
            return None

        return min(
            available,
            key=lambda battery:
            battery.pos.distance_squared_to(
                target
            )
        )

    # ========================================================
    # LAUNCH INTERCEPTOR
    # ========================================================

    def launch(self, target):

        target = pygame.Vector2(
            target
        )

        if (
            self.state != "play"
            or target.y > GROUND_Y - 20
        ):
            return

        battery = self.nearest_battery(
            target
        )

        # No usable battery
        if battery is None:
            return

        battery.ammo -= 1

        self.interceptors.append(
            Interceptor(
                battery.pos,
                target
            )
        )

    # ========================================================
    # SPAWN MISSILE
    # ========================================================

    def spawn_missile(self):

        targets = (
            [
                city
                for city in self.cities
                if city.alive
            ]
            +
            [
                battery
                for battery in self.batteries
                if battery.alive
            ]
        )

        if targets:

            self.missiles.append(
                Missile(
                    random.choice(targets),
                    45 + self.wave * 6
                )
            )

    # ========================================================
    # UPDATE
    # ========================================================

    def update(self, dt):

        if self.state != "play":
            return

        # ====================================================
        # TASK 4: CITY REPAIR
        # ====================================================

        threshold = city_repair_threshold()

        if (
            threshold
            and
            self.score // threshold
            > self.repairs_awarded
        ):

            self.repairs_awarded = (
                self.score // threshold
            )

            # Repair one destroyed city
            for city in self.cities:

                if not city.alive:

                    city.alive = True

                    break

        # ====================================================
        # SPAWN MISSILES
        # ====================================================

        self.spawn_timer -= dt

        if (
            self.to_spawn > 0
            and self.spawn_timer <= 0
        ):

            self.spawn_missile()

            self.to_spawn -= 1

            self.spawn_timer = random.uniform(
                0.6,
                1.6
            )

        # ====================================================
        # UPDATE INTERCEPTORS
        # ====================================================

        for interceptor in self.interceptors[:]:

            if interceptor.update(dt):

                self.interceptors.remove(
                    interceptor
                )

                self.explosions.append(
                    Explosion(
                        interceptor.pos
                    )
                )

        # ====================================================
        # UPDATE EXPLOSIONS
        # ====================================================

        for explosion in self.explosions:

            explosion.age += dt

            for missile in self.missiles[:]:

                if (
                    missile.pos.distance_squared_to(
                        explosion.pos
                    )
                    <
                    explosion.radius ** 2
                ):

                    self.missiles.remove(
                        missile
                    )

                    self.score += 25

        self.explosions = [
            explosion
            for explosion in self.explosions
            if not explosion.done
        ]

        # ====================================================
        # UPDATE MISSILES
        # ====================================================

        for missile in self.missiles[:]:

            if missile.update(dt):

                self.missiles.remove(
                    missile
                )

                self.impact(missile)

        # ====================================================
        # FINISH WAVE
        # ====================================================

        if (
            not self.missiles
            and self.to_spawn == 0
            and not self.explosions
        ):

            self.finish_wave()

    # ========================================================
    # MISSILE IMPACT
    # ========================================================

    def impact(self, missile):

        target = missile.target

        if target.alive:

            target.alive = False

            # TASK 3
            if isinstance(
                target,
                City
            ):

                on_city_destroyed(
                    target
                )

        self.explosions.append(
            Explosion(
                missile.pos,
                30
            )
        )

        # Game over if all cities destroyed
        if not any(
            city.alive
            for city in self.cities
        ):

            self.state = "lose"

    # ========================================================
    # FINISH WAVE
    # ========================================================

    def finish_wave(self):

        self.score += (
            100
            *
            sum(
                city.alive
                for city in self.cities
            )
            +
            5
            *
            sum(
                battery.ammo
                for battery in self.batteries
            )
        )

        self.wave += 1

        self.start_wave()

    # ========================================================
    # DRAW
    # ========================================================

    def draw(self, screen):

        # Background
        screen.fill(
            (5, 5, 25)
        )

        # Ground
        pygame.draw.rect(
            screen,
            (150, 110, 50),
            (
                0,
                GROUND_Y,
                WIDTH,
                HEIGHT - GROUND_Y
            )
        )

        # ====================================================
        # DRAW CITIES
        # ====================================================

        for city in self.cities:

            if city.alive:

                for i, h in enumerate(
                    (18, 28, 22)
                ):

                    pygame.draw.rect(
                        screen,
                        (90, 190, 230),
                        (
                            city.pos.x - 18 + i * 12,
                            GROUND_Y - h,
                            10,
                            h
                        )
                    )

        # ====================================================
        # DRAW BATTERIES
        # ====================================================

        for battery in self.batteries:

            if battery.alive:

                x = battery.pos.x

                pygame.draw.polygon(
                    screen,
                    (220, 220, 80),
                    [
                        (
                            x - 22,
                            GROUND_Y
                        ),
                        (
                            x + 22,
                            GROUND_Y
                        ),
                        (
                            x,
                            GROUND_Y - 24
                        )
                    ]
                )

                label = self.font.render(
                    str(battery.ammo),
                    True,
                    (20, 20, 20)
                )

                screen.blit(
                    label,
                    label.get_rect(
                        center=(
                            x,
                            GROUND_Y + 14
                        )
                    )
                )

        # ====================================================
        # DRAW MISSILES
        # ====================================================

        for missile in self.missiles:

            pygame.draw.line(
                screen,
                (200, 60, 60),
                missile.origin,
                missile.pos,
                1
            )

            pygame.draw.circle(
                screen,
                (255, 255, 255),
                missile.pos,
                3
            )

        # ====================================================
        # DRAW INTERCEPTORS
        # ====================================================

        for interceptor in self.interceptors:

            pygame.draw.line(
                screen,
                (80, 180, 255),
                interceptor.origin,
                interceptor.pos,
                1
            )

            pygame.draw.circle(
                screen,
                (80, 180, 255),
                interceptor.target,
                5,
                1
            )

        # ====================================================
        # DRAW EXPLOSIONS
        # ====================================================

        for explosion in self.explosions:

            color = explosion_color(
                explosion.progress
            )

            pygame.draw.circle(
                screen,
                color,
                explosion.pos,
                max(
                    1,
                    int(explosion.radius)
                )
            )

        # ====================================================
        # HUD
        # ====================================================

        hud = self.font.render(
            f"Score {self.score}   "
            f"Wave {self.wave}   "
            f"Click to fire   "
            f"R = reset",
            True,
            (240, 240, 240)
        )

        screen.blit(
            hud,
            (10, 8)
        )

        # ====================================================
        # CITY DESTROYED WARNING
        # ====================================================

        global city_warning_text
        global city_warning_until

        current_time = pygame.time.get_ticks()

        if (
            city_warning_text
            and current_time < city_warning_until
        ):

            warning = self.warning_font.render(
                "⚠ CITY DESTROYED!",
                True,
                (255, 80, 80)
            )

            warning_rect = warning.get_rect(
                center=(
                    WIDTH // 2,
                    55
                )
            )

            # Dark background behind warning
            background_rect = warning_rect.inflate(
                30,
                15
            )

            pygame.draw.rect(
                screen,
                (40, 5, 5),
                background_rect,
                border_radius=8
            )

            screen.blit(
                warning,
                warning_rect
            )

        else:

            city_warning_text = ""

        # ====================================================
        # GAME OVER
        # ====================================================

        if self.state == "lose":

            label = self.font.render(
                "ALL CITIES LOST - Press R",
                True,
                (255, 255, 120)
            )

            screen.blit(
                label,
                label.get_rect(
                    center=(
                        WIDTH // 2,
                        HEIGHT // 2
                    )
                )
            )


# ============================================================
# MAIN
# ============================================================

def main():

    pygame.init()

    screen = pygame.display.set_mode(
        (WIDTH, HEIGHT)
    )

    pygame.display.set_caption(
        "Missile Command"
    )

    clock = pygame.time.Clock()

    game = Game()

    running = True

    while running:

        dt = min(
            clock.tick(60) / 1000,
            0.05
        )

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                running = False

            elif (
                event.type
                == pygame.MOUSEBUTTONDOWN
                and event.button == 1
            ):

                game.launch(
                    event.pos
                )

            elif (
                event.type
                == pygame.KEYDOWN
                and event.key == pygame.K_r
            ):

                game.reset()

        game.update(dt)

        game.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
