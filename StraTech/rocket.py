class Rocket:
    def __init__(self, engine_count, acceleration_per_engine_m_s2):
        self.engine_count = engine_count
        self.acceleration_per_engine_m_s2 = acceleration_per_engine_m_s2

    def get_total_acceleration(self):
        return self.engine_count * self.acceleration_per_engine_m_s2