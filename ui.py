import pygame
from config import *

class FilterPanel:
    def __init__(self, filters, font, window_width, window_height):
        self.filters = filters
        # Fonte para painel UI
        self.ui_font = pygame.font.SysFont('segoeui', 15, bold=True)
        if getattr(self.ui_font, 'get_height', lambda: 0)() == 0:
            self.ui_font = pygame.font.SysFont('arial', 15, bold=True)
            
        self.small_font = pygame.font.SysFont('segoeui', 13)
        if getattr(self.small_font, 'get_height', lambda: 0)() == 0:
            self.small_font = pygame.font.SysFont('arial', 13)
            
        self.window_width = window_width
        self.window_height = window_height
        self.is_open = True
        self.active_idx = -1
        self.dragging = False
        
        # Propriedades do Input de Intensidade
        self.input_rect = pygame.Rect(0, 0, 0, 0)
        self.input_active = False
        self.input_text = ""
        
        # Cache text surfaces
        self.cached_title_text = self.ui_font.render("FILTROS", True, (130, 130, 140))
        self.cached_intensity_text = self.small_font.render("Intensidade:", True, (160, 160, 170))
        self.cached_filter_names_active = [self.ui_font.render(f.name, True, ACTIVE_HIGHLIGHT) for f in self.filters]
        self.cached_filter_names_inactive = [self.ui_font.render(f.name, True, (160, 160, 170)) for f in self.filters]

        # Dimensions
        self.panel_width = PANEL_WIDTH
        self.toggle_width = 24
        self.toggle_height = 60
        
        # Rects
        self.update_rects()

    def update_rects(self):
        """Update rectangles based on whether the panel is open or closed"""
        toggle_y = (self.window_height - self.toggle_height) // 2
        if self.is_open:
            self.rect = pygame.Rect(self.window_width - self.panel_width, 0, self.panel_width, self.window_height)
            self.toggle_rect = pygame.Rect(self.rect.left - self.toggle_width, toggle_y, self.toggle_width, self.toggle_height)
        else:
            self.rect = pygame.Rect(self.window_width + self.panel_width, 0, 0, self.window_height)
            self.toggle_rect = pygame.Rect(self.window_width - self.toggle_width, toggle_y, self.toggle_width, self.toggle_height)
            
        self.slider_rect = pygame.Rect(0, 0, 0, 0)
        self.filter_rects = []
        
        if self.is_open:
            y_offset = 60
            for f in self.filters:
                r = pygame.Rect(self.rect.x + 15, self.rect.y + y_offset, self.rect.width - 30, 36)
                self.filter_rects.append(r)
                y_offset += 44

    def toggle(self):
        self.is_open = not self.is_open
        self.update_rects()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.input_active:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER or event.key == pygame.K_ESCAPE:
                    self.input_active = False
                    self.apply_input_text()
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                elif event.unicode.isdigit() and len(self.input_text) < 3:
                    self.input_text += event.unicode
                return True, False
                
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.toggle_rect.collidepoint(event.pos):
                    self.toggle()
                    return True, True
                    
                if not self.is_open:
                    return False, False
                    
                if self.input_active and not self.input_rect.collidepoint(event.pos):
                    self.input_active = False
                    self.apply_input_text()
                    
                if self.active_idx != -1 and self.input_rect.collidepoint(event.pos):
                    self.input_active = True
                    self.input_text = ""
                    return True, False
                    
                if self.active_idx != -1 and self.slider_rect.collidepoint(event.pos):
                    self.dragging = True
                    self.update_slider(event.pos[0])
                    return True, False
                
                for i, rect in enumerate(self.filter_rects):
                    if rect.collidepoint(event.pos):
                        if self.active_idx == i:
                            self.active_idx = -1
                        else:
                            self.active_idx = i
                        return True, False
                        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False
                
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging and self.active_idx != -1 and self.is_open:
                self.update_slider(event.pos[0])
                return True, False
                
        return False, False

    def apply_input_text(self):
        if not self.input_text:
            val = 0
        else:
            try:
                val = int(self.input_text)
            except ValueError:
                val = int(self.filters[self.active_idx].intensity * 100) if self.active_idx != -1 else 0
                
        val = max(0, min(100, val))
        if self.active_idx != -1:
            self.filters[self.active_idx].intensity = val / 100.0

    def update_slider(self, mouse_x):
        track_start = self.rect.x + 18
        track_end = self.rect.right - 18 - 60
        if track_end <= track_start:
            return
        val = (mouse_x - track_start) / float(track_end - track_start)
        self.filters[self.active_idx].intensity = max(0.0, min(1.0, val))
        if not self.input_active:
            self.input_text = str(int(self.filters[self.active_idx].intensity * 100))

    def get_active_filter(self):
        if self.active_idx != -1:
            return self.filters[self.active_idx]
        return None

    def draw(self, surface):
        pygame.draw.rect(surface, (50, 50, 50), self.toggle_rect, border_radius=6)
        arrow_color = (200, 200, 200)
        
        if self.is_open:
            points = [(self.toggle_rect.left + 8, self.toggle_rect.centery - 6),
                      (self.toggle_rect.left + 8, self.toggle_rect.centery + 6),
                      (self.toggle_rect.right - 8, self.toggle_rect.centery)]
        else:
            points = [(self.toggle_rect.right - 8, self.toggle_rect.centery - 6),
                      (self.toggle_rect.right - 8, self.toggle_rect.centery + 6),
                      (self.toggle_rect.left + 8, self.toggle_rect.centery)]
                      
        pygame.draw.polygon(surface, arrow_color, points)
        pygame.draw.aalines(surface, arrow_color, True, points)
        
        if not self.is_open:
            return
            
        pygame.draw.rect(surface, PANEL_BG, self.rect)
        pygame.draw.line(surface, PANEL_BORDER, (self.rect.x, self.rect.y), (self.rect.x, self.rect.bottom), 1)
        
        surface.blit(self.cached_title_text, (self.rect.x + 20, self.rect.y + 20))
        
        for i, (f, rect) in enumerate(zip(self.filters, self.filter_rects)):
            if i == self.active_idx:
                pygame.draw.rect(surface, (45, 45, 55), rect, border_radius=8)
                pygame.draw.rect(surface, ACTIVE_HIGHLIGHT, rect, width=2, border_radius=8)
                text = self.cached_filter_names_active[i]
            else:
                pygame.draw.rect(surface, (22, 22, 26), rect, border_radius=8)
                text = self.cached_filter_names_inactive[i]
                
            text_rect = text.get_rect(midleft=(rect.x + 15, rect.centery))
            surface.blit(text, text_rect)
            
        if self.active_idx != -1:
            f = self.filters[self.active_idx]
            slider_y = self.filter_rects[-1].bottom + 50
            
            surface.blit(self.cached_intensity_text, (self.rect.x + 18, slider_y - 25))
            
            track_start = self.rect.x + 18
            track_end = self.rect.right - 18 - 60
            self.slider_rect = pygame.Rect(track_start - 10, slider_y - 12, track_end - track_start + 20, 24)
            
            pygame.draw.rect(surface, (30, 30, 35), (track_start, slider_y - 3, track_end - track_start, 6), border_radius=3)
            
            filled_width = int(f.intensity * (track_end - track_start))
            if filled_width > 0:
                pygame.draw.rect(surface, ACTIVE_HIGHLIGHT, (track_start, slider_y - 3, filled_width, 6), border_radius=3)
            
            handle_x = track_start + filled_width
            pygame.draw.circle(surface, (255, 255, 255), (handle_x, slider_y), 7)
            pygame.draw.circle(surface, ACTIVE_HIGHLIGHT, (handle_x, slider_y), 7, width=2)
            
            self.input_rect = pygame.Rect(track_end + 10, slider_y - 12, 52, 22)
            border_color = (200, 200, 200) if self.input_active else (100, 100, 100)
            pygame.draw.rect(surface, (20, 20, 20), self.input_rect, border_radius=3)
            pygame.draw.rect(surface, border_color, self.input_rect, 1, border_radius=3)

            display_text = self.input_text if self.input_active else str(int(f.intensity * 100))
            txt_surf = self.small_font.render(display_text, True, (255, 255, 255))
            txt_rect = txt_surf.get_rect(center=self.input_rect.center)
            surface.blit(txt_surf, txt_rect)

            if self.input_active and pygame.time.get_ticks() % 1000 < 500:
                cursor_x = txt_rect.right + 2
                cursor_y1 = txt_rect.top
                cursor_y2 = txt_rect.bottom
                pygame.draw.line(surface, (255, 255, 255), (cursor_x, cursor_y1), (cursor_x, cursor_y2), 1)
