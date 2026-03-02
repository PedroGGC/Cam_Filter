import time
import pygame
from ui import FilterPanel

class DummyFilter:
    def __init__(self, name, intensity):
        self.name = name
        self.intensity = intensity

def run_benchmark():
    pygame.init()
    # No need to open a window
    # pygame.display.set_mode((800, 600))
    pygame.font.init()
    filters = [DummyFilter(f"Filter {i}", 0.5) for i in range(10)]
    panel = FilterPanel(filters, None, 800, 600)
    surface = pygame.Surface((800, 600))

    # warmup
    for _ in range(100):
        panel.draw(surface)

    start = time.perf_counter()
    for _ in range(10000):
        panel.draw(surface)
    end = time.perf_counter()

    print(f"Time taken for 10000 draw calls: {end - start:.4f} seconds")

if __name__ == "__main__":
    run_benchmark()
