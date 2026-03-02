import cv2
import numpy as np

class Filter:
    def __init__(self, name, apply_fn, is_ascii=False):
        self.name = name
        self.apply_fn = apply_fn
        self.intensity = 0.5
        self.is_ascii = is_ascii

def apply_deep_dive(frame, intensity):
    levels = max(2, int(32 - (intensity * 30)))
    ratio = 256.0 / levels
    quantized = np.floor(frame / ratio) * ratio
    return quantized.astype(np.uint8)

def apply_gameboy(frame, intensity):
    palette_bgr = np.array([
        [15, 56, 15],       
        [48, 98, 48],       
        [15, 172, 139],     
        [15, 188, 155],     
    ], dtype=np.uint8)
    
    h, w = frame.shape[:2]
    block = max(1, int(intensity * 15) + 1)
    
    if block > 1:
        small = cv2.resize(frame, (w // block, h // block), interpolation=cv2.INTER_LINEAR)
    else:
        small = frame
        
    gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
    quantized = np.clip(gray // 64, 0, 3).astype(np.uint8)
    color_frame = palette_bgr[quantized]
    return cv2.resize(color_frame, (w, h), interpolation=cv2.INTER_NEAREST)

def apply_blueprint(frame, intensity):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Laplacian(blur, cv2.CV_8U, ksize=5)
    _, edges = cv2.threshold(edges, 50, 255, cv2.THRESH_BINARY)
    
    bg = np.full_like(frame, (150, 50, 20)) # (BGR)
    
    if intensity > 0.1:
        grid_size = max(15, int(70 - intensity * 50))
        bg[::grid_size, :] = (180, 80, 40)
        bg[:, ::grid_size] = (180, 80, 40)
        
    edges_colored = np.zeros_like(frame)
    edges_colored[edges > 0] = [255, 255, 255]
    
    return cv2.addWeighted(bg, 1.0, edges_colored, 1.0 + (intensity * 2.0), 0)

def apply_crt(frame, intensity):
    h, w = frame.shape[:2]
    if intensity > 0:
        k1 = intensity * 0.2
        k2 = intensity * 0.05
        x, y = np.meshgrid(np.arange(w), np.arange(h))
        x_norm = (x - w / 2) / (w / 2)
        y_norm = (y - h / 2) / (h / 2)
        
        r2 = x_norm**2 + y_norm**2
        radial = 1 + k1 * r2 + k2 * r2**2
        
        x_distorted = x_norm * radial * (w / 2) + w / 2
        y_distorted = y_norm * radial * (h / 2) + h / 2
        
        distorted = cv2.remap(frame, x_distorted.astype(np.float32), y_distorted.astype(np.float32), 
                              cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0))
    else:
        distorted = frame.copy()

    scanlines = np.ones((h, w, 3), dtype=np.float32)
    scanlines[::2, :] = 0.7 
    
    x_ker = cv2.getGaussianKernel(w, w/2)
    y_ker = cv2.getGaussianKernel(h, h/2)
    kernel = y_ker * x_ker.T
    mask = kernel / kernel.max()
    vignette = cv2.cvtColor(mask.astype(np.float32), cv2.COLOR_GRAY2BGR)
        
    result = cv2.multiply(distorted.astype(np.float32), scanlines)
    result = cv2.multiply(result, vignette)
    
    return np.clip(result, 0, 255).astype(np.uint8)

def apply_neon_edges(frame, intensity):
    blur = cv2.GaussianBlur(frame, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)
    kernel = np.ones((2, 2), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=1)
    
    edges_bgr = np.zeros_like(frame)
    edges_bgr[edges > 0] = [0, 255, 65]
    
    glow = cv2.GaussianBlur(edges_bgr, (15, 15), 0)
    edges_with_glow = cv2.addWeighted(edges_bgr, 1.0, glow, 2.0, 0)
    
    dark = (frame * max(0.0, 1.0 - intensity)).astype(np.uint8)
    res = cv2.addWeighted(dark, 1.0, edges_with_glow, intensity * 2.0, 0)
    return np.clip(res, 0, 255).astype(np.uint8)

def apply_pixelate(frame, intensity):
    h, w = frame.shape[:2]
    block = max(1, int(intensity * 100))
    if block == 1:
        return frame
    small = cv2.resize(frame, (max(1, w // block), max(1, h // block)), interpolation=cv2.INTER_LINEAR)
    return cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)

def apply_glitch(frame, intensity):
    shift = int(intensity * 100)
    if shift <= 0:
        return frame
    result = np.zeros_like(frame)
    result[:, :, 0] = np.roll(frame[:, :, 0], -shift, axis=1)
    result[:, :, 1] = frame[:, :, 1]
    result[:, :, 2] = np.roll(frame[:, :, 2], shift, axis=1)
    return result

def apply_pencil_sketch(frame, intensity):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    inv = cv2.bitwise_not(gray)
    blur_size = int(intensity * 40) * 2 + 1 
    if blur_size < 3: blur_size = 3
    blur = cv2.GaussianBlur(inv, (blur_size, blur_size), 0)
    sketch = cv2.divide(gray, 255 - blur, scale=256)
    sketch_bgr = cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)
    weight = min(1.0, intensity * 1.5)
    return cv2.addWeighted(frame, 1.0 - weight, sketch_bgr, weight, 0)

def apply_halftone(frame, intensity):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    h, w = frame.shape[:2]
    block_size = max(4, int(intensity * 24))
    
    X = np.arange(w)
    Y = np.arange(h)
    xx, yy = np.meshgrid(X, Y)
    
    cx = xx % block_size - block_size // 2
    cy = yy % block_size - block_size // 2
    dist_sq = cx**2 + cy**2
    
    max_r_sq = (block_size // 2) ** 2
    normalized_luma = gray.astype(np.float32) / 255.0
    radii_sq = (1.0 - normalized_luma) * max_r_sq
    
    halftone = np.ones_like(gray) * 230 
    halftone[dist_sq <= radii_sq] = 10
    return cv2.cvtColor(halftone, cv2.COLOR_GRAY2BGR)

def apply_ghost_trails(frame, intensity):
    frame_float = frame.astype(np.float32)
    alpha = 1.0 - (intensity * 0.95) 
    
    if not hasattr(apply_ghost_trails, "last_frame"):
        apply_ghost_trails.last_frame = frame_float
        
    res = cv2.addWeighted(frame_float, alpha, apply_ghost_trails.last_frame, 1.0 - alpha, 0)
    apply_ghost_trails.last_frame = res
    return res.astype(np.uint8)

import threading

_CLAHE_LOCAL = threading.local()

def get_clahe():
    if not hasattr(_CLAHE_LOCAL, "clahe"):
        _CLAHE_LOCAL.clahe = cv2.createCLAHE(tileGridSize=(8,8))
    return _CLAHE_LOCAL.clahe

def apply_ascii_contrast(gray_frame, intensity):
    limit = 1.0 + (intensity * 4.0)
    clahe = get_clahe()
    clahe.setClipLimit(limit)
    enhanced = clahe.apply(gray_frame)
    alpha = 1.0 + (intensity * 1.5)
    beta = (intensity - 0.5) * 50
    return cv2.convertScaleAbs(enhanced, alpha=alpha, beta=beta)
