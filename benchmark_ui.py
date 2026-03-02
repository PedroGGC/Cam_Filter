import time
import pygame
from ui import FilterPanel

class DummyFilter:
    def __init__(self, name, intensity):
        self.name = name
        self.intensity = intensity

def dummy_filter(frame, intensity):
    return frame

def run_benchmark():
    pygame.init()
    surface = pygame.Surface((800, 600))
    filters = [
        DummyFilter("Filter 1", 0.5),
        DummyFilter("Filter 2", 0.5),
        DummyFilter("Filter 3", 0.5),
        DummyFilter("Filter 4", 0.5),
    ]

    font = pygame.font.SysFont('arial', 15)

    panel = FilterPanel(filters, font, 800, 600)
    panel.active_idx = 0  # Activate a filter

    # Warmup
    for _ in range(100):
        panel.draw(surface)

    iterations = 10000
    start_time = time.time()
    for _ in range(iterations):
        panel.draw(surface)
    end_time = time.time()

    elapsed = end_time - start_time
    print(f"Time for {iterations} draws: {elapsed:.4f} seconds")
    return elapsed

if __name__ == "__main__":
    run_benchmark()
