import cv2
import pygame
import numpy as np
import pyvirtualcam
from main import Filters_cam

class VirtualFilters_cam(Filters_cam):
    def __init__(self):
        super().__init__()
        # Painel Remoto: Janela pequena e compacta (Apenas Interface)
        self.window_width = 300
        self.window_height = 680
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Filtros - Controle Remoto")
        
        # Oculta o toggle esticando o painel pelo total da nova janelinha
        self.filter_panel.panel_width = self.window_width 
        self.filter_panel.window_width = self.window_width
        self.filter_panel.window_height = self.window_height
        self.filter_panel.is_open = True
        self.filter_panel.update_rects()
        
        # Resolução fixa INVISÍVEL da câmera virtual para o OBS/Discord
        self.v_width = 1280
        self.v_height = 720
        self.camera_surface = pygame.Surface((self.v_width, self.v_height))
        
        # Recalcular grid ASCII para a resolução pesada do OBS, e não da janelinha local
        self.ascii_width = self.v_width
        self.ascii_height = self.v_height
        self.cols = self.ascii_width // self.char_width
        self.rows = self.ascii_height // self.char_height
        self.xs = [j * self.char_width for j in range(self.cols)]
        self.ys = [i * self.char_height for i in range(self.rows)]

    def run(self):
        try:
            # Trava o RGB para o OBS entender a codificação gráfica de cor perfeitamente
            with pyvirtualcam.Camera(width=self.v_width, height=self.v_height, fps=30, fmt=pyvirtualcam.PixelFormat.RGB) as cam:
                print(f"====================================")
                print(f"Câmera Virtual Iniciada com Sucesso!")
                print(f"Painel Remoto Local: {self.window_width}x{self.window_height}")
                print(f"Transmissão no OBS/Discord: {cam.width}x{cam.height} @ {cam.fps}fps")
                print(f"====================================")

                while self.running:
                    self.screen.fill((15, 15, 18))
                    
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
                        active_filter = self.filter_panel.get_active_filter()
                        
                        # Limpa o canvas fantasma interno
                        self.camera_surface.fill((0, 0, 0))
                        
                        if active_filter is not None and active_filter.is_ascii:
                            indices = self.frame_to_ascii(frame, active_filter)
                            
                            if self.invert:
                                self.camera_surface.fill((255, 255, 255))
                                chars = self.char_surfaces_inverted
                            else:
                                chars = self.char_surfaces_normal
                                
                            blits_data = [
                                (chars[char_idx], (self.xs[j], self.ys[i]))
                                for i in range(self.rows)
                                for j, char_idx in enumerate(indices[i])
                                if char_idx != 0 
                            ]
                            self.camera_surface.blits(blits_data)
                        else:
                            if active_filter is not None:
                                filtered_frame = active_filter.apply_fn(frame, active_filter.intensity)
                            else:
                                filtered_frame = frame
                                
                            rgb_frame = cv2.cvtColor(filtered_frame, cv2.COLOR_BGR2RGB)
                            py_img = pygame.image.frombuffer(rgb_frame.tobytes(), (rgb_frame.shape[1], rgb_frame.shape[0]), "RGB")
                            scaled_img = pygame.transform.smoothscale(py_img, (self.v_width, self.v_height))
                            self.camera_surface.blit(scaled_img, (0, 0))
                            
                        # Extrair a matrix da surface EXCLUSIVA e transpor para o formato nativo da cam virtual
                        pixel_data = pygame.surfarray.array3d(self.camera_surface)
                        frame_vcam = np.transpose(pixel_data, (1, 0, 2))
                        
                        try:
                            # Contíguo garante que a memória numpy seja linear para envio rápido
                            cam.send(np.ascontiguousarray(frame_vcam))
                            cam.sleep_until_next_frame()
                        except RuntimeError:
                            pass
                        
                    # Desenhar SOMENTE a interface na janela mini local
                    self.filter_panel.draw(self.screen)
                    pygame.display.flip()

        except Exception as e:
            print("====================================")
            print("Erro Crítico da Câmera Virtual!")
            print(f"Log: {e}")
            print("====================================")
        finally:
            print("Encerrando captura e transmissao...")
            self.cap.release()
            pygame.quit()

if __name__ == "__main__":
    app = VirtualFilters_cam()
    app.run()
