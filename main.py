import cv2
import pygame
import numpy as np
import sys
from config import *
from filters import *
from ui import FilterPanel

class Filters_cam:
    def __init__(self):
        pygame.init()
        info = pygame.display.Info()
        self.screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.NOFRAME)
        self.window_width, self.window_height = self.screen.get_size()
        pygame.display.set_caption("Filters_cam - Real-time Filters")
        self.clock = pygame.time.Clock()
        
        self.font = pygame.font.SysFont('couriernew', FONT_SIZE, bold=True)
        if getattr(self.font, 'get_height', lambda: 0)() == 0:
            self.font = pygame.font.SysFont('monospace', FONT_SIZE, bold=True)
            
        self.char_width, self.char_height = self.font.size("A")
        
        if self.char_width <= 0 or self.char_height <= 0:
            print("Erro ao carregar a fonte. Verifique a instalação de fontes do SO.")
            sys.exit(1)
            
        filters = [
            Filter("ASCII Matrix", apply_ascii_contrast, is_ascii=True),
            Filter("Gameboy Camera", apply_gameboy),
            Filter("Blueprint Plan", apply_blueprint),
            Filter("CRT Monitor", apply_crt),
            Filter("Neon Edges", apply_neon_edges),
            Filter("Halftone Art", apply_halftone),
            Filter("Ghost Trails", apply_ghost_trails),
            Filter("Pixelate TV", apply_pixelate),
            Filter("Pencil Sketch", apply_pencil_sketch),
            Filter("Glitch RGB", apply_glitch),
            Filter("Deep Dive", apply_deep_dive)
        ]
        
        self.filter_panel = FilterPanel(filters, self.font, self.window_width, self.window_height)
        self.filter_panel.active_idx = -1
        self.aspect_ratio_correction = 0.55
        self.ascii_chars = list(ASCII_CHARS)
        self.invert = False
        self.running = True
        
        self.recalculate_ascii_grid()
        self._prerender_fonts()
        
        self.screen.fill(BG_COLOR)
        loading_font = pygame.font.SysFont('segoeui', 22, bold=True)
        if getattr(loading_font, 'get_height', lambda: 0)() == 0:
            loading_font = pygame.font.SysFont('arial', 22, bold=True)
            
        text_surf = loading_font.render("Iniciando lente da câmera...", True, (200, 200, 200))
        text_rect = text_surf.get_rect(center=(self.window_width//2, self.window_height//2))
        self.screen.blit(text_surf, text_rect)
        pygame.display.flip()
        
        # Tenta Iniciar o DirectShow primeiro (Muito mais rápido no Windows para evitar tela preta)
        self.cap = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            self.cap = cv2.VideoCapture(CAMERA_INDEX)
            
        if not self.cap.isOpened():
            print(f"Erro: Câmera {CAMERA_INDEX} não encontrada ou não pode ser aberta.")
            sys.exit(1)

    def recalculate_ascii_grid(self):
        panel_space = self.filter_panel.toggle_width
        if self.filter_panel.is_open:
            panel_space += self.filter_panel.panel_width
            
        self.ascii_width = self.window_width - panel_space
        self.ascii_height = self.window_height
        
        self.cols = self.ascii_width // self.char_width
        self.rows = self.ascii_height // self.char_height
        
        self.xs = [j * self.char_width for j in range(self.cols)]
        self.ys = [i * self.char_height for i in range(self.rows)]

    def _prerender_fonts(self):
        self.char_surfaces_normal = [self.font.render(c, True, FG_COLOR) for c in self.ascii_chars]
        self.char_surfaces_inverted = [self.font.render(c, True, BG_COLOR) for c in self.ascii_chars]

    def capture_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        return cv2.flip(frame, 1)

    def frame_to_ascii(self, frame, active_filter=None):
        if active_filter and active_filter.is_ascii:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = active_filter.apply_fn(gray, active_filter.intensity)
        else:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
        orig_h, orig_w = gray.shape
        target_ratio = (self.cols / self.rows) * self.aspect_ratio_correction
        camera_ratio = orig_w / orig_h
        
        if camera_ratio > target_ratio:
            new_w = int(orig_h * target_ratio)
            x_offset = (orig_w - new_w) // 2
            gray = gray[:, x_offset:x_offset+new_w]
        else:
            new_h = int(orig_w / target_ratio)
            y_offset = (orig_h - new_h) // 2
            gray = gray[y_offset:y_offset+new_h, :]
            
        resized = cv2.resize(gray, (self.cols, self.rows))
        
        num_chars = len(self.ascii_chars)
        step = 256 / num_chars
        indices = (resized / step).astype(np.uint8)
        indices = np.clip(indices, 0, num_chars - 1)
        
        return indices

    def render_ascii(self, indices):
        if self.invert:
            self.screen.fill(FG_COLOR)
            chars = self.char_surfaces_inverted
        else:
            self.screen.fill(BG_COLOR)
            chars = self.char_surfaces_normal

        blits_data = [
            (chars[char_idx], (self.xs[j], self.ys[i]))
            for i in range(self.rows)
            for j, char_idx in enumerate(indices[i])
            if char_idx != 0 
        ]
        
        self.screen.blits(blits_data)
        
    def render_image_filter(self, frame, active_filter):
        self.screen.fill(BG_COLOR)
        
        if active_filter is not None:
            filtered_frame = active_filter.apply_fn(frame, active_filter.intensity)
        else:
            filtered_frame = frame
        
        rgb_frame = cv2.cvtColor(filtered_frame, cv2.COLOR_BGR2RGB)
        py_img = pygame.image.frombuffer(rgb_frame.tobytes(), (rgb_frame.shape[1], rgb_frame.shape[0]), "RGB")
        
        orig_h, orig_w = py_img.get_height(), py_img.get_width()
        
        target_w = self.ascii_width
        target_h = self.ascii_height
        
        target_ratio = target_w / target_h
        camera_ratio = orig_w / orig_h
        
        if camera_ratio > target_ratio:
            display_w = target_w
            display_h = int(target_w / camera_ratio)
        else:
            display_h = target_h
            display_w = int(target_h * camera_ratio)
            
        scaled_img = pygame.transform.smoothscale(py_img, (display_w, display_h))
        
        x_pos = (target_w - display_w) // 2
        y_pos = (target_h - display_h) // 2
        
        self.screen.blit(scaled_img, (x_pos, y_pos))

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_i:
                        self.invert = not self.invert
                
                handled, needs_resize = self.filter_panel.handle_event(event)
                if needs_resize:
                    self.recalculate_ascii_grid()

            frame = self.capture_frame()
            if frame is not None:
                active_filter = self.filter_panel.get_active_filter()
                
                if active_filter is not None and active_filter.is_ascii:
                    indices = self.frame_to_ascii(frame, active_filter)
                    self.render_ascii(indices)
                else:
                    self.render_image_filter(frame, active_filter)
                
            self.filter_panel.draw(self.screen)
            pygame.display.flip()
                
            self.clock.tick(60)
            
        self.cap.release()
        pygame.quit()

if __name__ == "__main__":
    app = Filters_cam()
    app.run()
