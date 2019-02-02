from sc2 import Race, Difficulty


class Opponent:
    def __init__(self, bot):
        self.bot = bot
        self.logger = bot.logger

        self.known_race = None
        self.known_base_locations = []
        self.unverified_hq_locations = bot.enemy_start_locations
        self.next_potential_location = None
        self.army_strength = 0
        self.units = None
        self.structures = None

        if bot.enemy_race != Race.Random:
            self._set_race(bot.enemy_race)

        if len(bot.enemy_start_locations) == 1:
            self.logger.log("We know exactly where our enemy HQ is")
            self.known_base_locations.append(bot.enemy_start_locations[0])
            self.unverified_hq_locations = []

    def _set_race(self, race):
        self.logger.log("Enemy is now known to be " + str(race))
        self.known_race = race

    def refresh(self):
        if self.bot.known_enemy_units:
            self.units = self.bot.known_enemy_units

            if self.known_race is None:
                self._set_race(self.units.first.race)

        if self.bot.known_enemy_structures:
            self.structures = self.bot.known_enemy_structures

        if self.unverified_hq_locations:
            for i, base in enumerate(self.unverified_hq_locations):
                if self.bot.units.closest_distance_to(base) < 10:
                    self.unverified_hq_locations.pop(i)
                    if self.bot.known_enemy_structures and self.bot.known_enemy_structures.closest_distance_to(base) < 20:
                        self.known_base_locations.append(base)
                        self.logger.log(f"Found a new enemy base {base}")
                    else:
                        self.logger.log(f"Scouted potential enemy hq location {base} which turned out empty")

    def get_next_potential_base(self):
        raise NotImplementedError

    def get_next_potential_base_closest_to(self, source):
        if self.structures.exists:
            return self.structures.closest_to(source).position
        elif self.known_base_locations:
            return self.known_base_locations.closest_to(source).position
        elif self.next_potential_location:
            return self.next_potential_location
        elif self.unverified_hq_locations:
            return self.unverified_hq_locations.closest_to(source).position
        else:
            self.logger.error("Our army has no idea where to go")
            return None
