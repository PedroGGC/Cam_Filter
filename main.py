import cv2
import pygame
import numpy as np
import sys

# --- Constantes Configuráveis ---
FONT_SIZE = 14
FG_COLOR = (255, 255, 255)  # Branco
BG_COLOR = (0, 0, 0)        # Preto
ASCII_CHARS = " .':-=+*#%@$"  # Escala de 12 níveis de densidade

# Configurações do Painel Lateral
PANEL_WIDTH = 220
PANEL_BG = (30, 30, 30)
PANEL_BORDER = (60, 60, 60)
ACTIVE_HIGHLIGHT = (0, 255, 65)  # Borda lateral colorida

class Filter:
    def __init__(self, name, apply_fn):
        self.name = name
        self.apply_fn = apply_fn
        self.intensity = 0.5

def apply_grayscale(frame, intensity):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    return cv2.addWeighted(frame, 1.0 - intensity, gray_bgr, intensity, 0)

def apply_deep_dive(frame, intensity):
    levels = max(2, int(2 + intensity * 30))
    ratio = 256.0 / levels
    quantized = np.floor(frame / ratio) * ratio
    return quantized.astype(np.uint8)

def apply_noise(frame, intensity):
    max_noise = int(intensity * 80)
    if max_noise <= 0:
        return frame
    noise = np.random.randint(0, max_noise + 1, frame.shape, dtype=np.uint8)
    return cv2.add(frame, noise)

def apply_embossed(frame, intensity):
    kernel = np.array([[-2, -1, 0],
                       [-1,  1, 1],
                       [ 0,  1, 2]], dtype=np.float32)
    embossed = cv2.filter2D(frame, -1, kernel)
    return cv2.addWeighted(frame, 1.0 - intensity, embossed, intensity, 0)

def apply_style(frame, intensity):
    h, w = frame.shape[:2]
    small = cv2.resize(frame, (w // 2, h // 2))
    sigma_s = float(max(1.0, intensity * 100))
    styled = cv2.stylization(small, sigma_s=sigma_s, sigma_r=0.45)
    return cv2.resize(styled, (w, h))

class FilterPanel:
    def __init__(self, filters, font, panel_rect):
        self.filters = filters
        self.font = font
        self.small_font = pygame.font.Font(None, 20)
        self.rect = panel_rect
        self.active_idx = -1
        self.dragging = False
        self.slider_rect = pygame.Rect(0, 0, 0, 0)
        self.filter_rects = []
        
        y_offset = 60
        for f in self.filters:
            r = pygame.Rect(self.rect.x, self.rect.y + y_offset, self.rect.width, 40)
            self.filter_rects.append(r)
            y_offset += 40

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.active_idx != -1 and self.slider_rect.collidepoint(event.pos):
                    self.dragging = True
                    self.update_slider(event.pos[0])
                    return True
                
                for i, rect in enumerate(self.filter_rects):
                    if rect.collidepoint(event.pos):
                        if self.active_idx == i:
                            self.active_idx = -1
                        else:
                            self.active_idx = i
                        return True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging and self.active_idx != -1:
                self.update_slider(event.pos[0])
                return True
        return False

    def update_slider(self, mouse_x):
        track_start = self.rect.x + 20
        track_end = self.rect.right - 20
        # Protect against division by zero 
        if track_end <= track_start:
            return
        val = (mouse_x - track_start) / float(track_end - track_start)
        self.filters[self.active_idx].intensity = max(0.0, min(1.0, val))

    def get_active_filter(self):
        if self.active_idx != -1:
            return self.filters[self.active_idx]
        return None

    def draw(self, surface):
        pygame.draw.rect(surface, PANEL_BG, self.rect)
        pygame.draw.line(surface, PANEL_BORDER, (self.rect.x, self.rect.y), (self.rect.x, self.rect.bottom), 1)
        
        if self.active_idx != -1:
            active_name = self.filters[self.active_idx].name
            title_text = self.font.render(active_name, True, (255, 255, 255))
        else:
            title_text = self.font.render("Filtros", True, (150, 150, 150))
            
        surface.blit(title_text, (self.rect.x + 20, self.rect.y + 20))
        
        for i, (f, rect) in enumerate(zip(self.filters, self.filter_rects)):
            if i == self.active_idx:
                pygame.draw.rect(surface, (60, 60, 60), rect)
                pygame.draw.rect(surface, ACTIVE_HIGHLIGHT, (rect.x, rect.y, 3, rect.height))
                color = (255, 255, 255)
            else:
                color = (180, 180, 180)
                
            text = self.font.render(f.name, True, color)
            surface.blit(text, (rect.x + 20, rect.y + 10))
            
        if self.active_idx != -1:
            f = self.filters[self.active_idx]
            slider_y = self.filter_rects[-1].bottom + 50
            
            val_text = self.small_font.render(f"Intensidade: {int(f.intensity * 100)}%", True, (200, 200, 200))
            surface.blit(val_text, (self.rect.x + 20, slider_y - 25))
            
            track_start = self.rect.x + 20
            track_end = self.rect.right - 20
            self.slider_rect = pygame.Rect(track_start - 10, slider_y - 10, track_end - track_start + 20, 20)
            
            pygame.draw.line(surface, (80, 80, 80), (track_start, slider_y), (track_end, slider_y), 4)
            handle_x = int(track_start + f.intensity * (track_end - track_start))
            pygame.draw.circle(surface, (200, 200, 200), (handle_x, slider_y), 8)


class ASCIICamera:
    def __init__(self):
        pygame.init()
        info = pygame.display.Info()
        self.screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.NOFRAME)
        window_width, window_height = self.screen.get_size()
        pygame.display.set_caption("ASCIICamera - Real-time ASCII")
        self.clock = pygame.time.Clock()
        
        self.font = pygame.font.SysFont('couriernew', FONT_SIZE, bold=True)
        if getattr(self.font, 'get_height', lambda: 0)() == 0:
            self.font = pygame.font.SysFont('monospace', FONT_SIZE, bold=True)
            
        self.char_width, self.char_height = self.font.size("A")
        
        if self.char_width <= 0 or self.char_height <= 0:
            print("Erro ao carregar a fonte. Verifique a instalação de fontes do SO.")
            sys.exit(1)
            
        filters = [
            Filter("Grayscale", apply_grayscale),
            Filter("Deep Dive", apply_deep_dive),
            Filter("Noise", apply_noise),
            Filter("Embossed", apply_embossed),
            Filter("Style", apply_style)
        ]
        
        panel_rect = pygame.Rect(window_width - PANEL_WIDTH, 0, PANEL_WIDTH, window_height)
        self.filter_panel = FilterPanel(filters, self.font, panel_rect)
            
        self.ascii_width = window_width - PANEL_WIDTH
        self.cols = self.ascii_width // self.char_width
        self.rows = window_height // self.char_height
        
        self.aspect_ratio_correction = 0.55
        self.ascii_chars = list(ASCII_CHARS)
        self.invert = False
        self.running = True
        
        self.xs = [j * self.char_width for j in range(self.cols)]
        self.ys = [i * self.char_height for i in range(self.rows)]
        
        self._prerender_fonts()
        
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Erro: Câmera não encontrada ou não pode ser aberta.")
            sys.exit(1)

    def _prerender_fonts(self):
        self.char_surfaces_normal = [self.font.render(c, True, FG_COLOR) for c in self.ascii_chars]
        self.char_surfaces_inverted = [self.font.render(c, True, BG_COLOR) for c in self.ascii_chars]

    def capture_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        frame = cv2.flip(frame, 1)
        
        active_filter = self.filter_panel.get_active_filter()
        if active_filter:
            frame = active_filter.apply_fn(frame, active_filter.intensity)
            
        return frame

    def frame_to_ascii(self, frame):
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

    def render(self, indices):
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
        
        self.filter_panel.draw(self.screen)
        
        pygame.display.flip()

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
                
                self.filter_panel.handle_event(event)

            frame = self.capture_frame()
            if frame is not None:
                indices = self.frame_to_ascii(frame)
                self.render(indices)
                
            self.clock.tick(60)
            
        self.cap.release()
        pygame.quit()

if __name__ == "__main__":
    app = ASCIICamera()
    app.run()
