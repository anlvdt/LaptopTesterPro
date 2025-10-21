import time
import sys
import os
import multiprocessing

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

def run_gpu_stress(duration, queue):
    try:
        import pygame
        import numpy as np
    except ImportError as e:
        queue.put({'type': 'error', 'message': f"Lỗi thiếu thư viện cho test GPU: {e.name}. Hãy chạy 'pip install pygame numpy'"})
        queue.put({'type': 'done'})
        return

    try:
        queue.put({'type': 'status', 'message': "Đang khởi tạo Pygame..."})
        pygame.init()
        screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        pygame.display.set_caption("GPU Stress Test - Nhấn ESC để thoát")
        clock = pygame.time.Clock()
        start_time = time.time()
        particles = []

        # Cài đặt font cho OSD
        try:
            font = pygame.font.SysFont("Segoe UI", 24)
            font_small = pygame.font.SysFont("Segoe UI", 18)
        except:
            font = pygame.font.Font(None, 30)
            font_small = pygame.font.Font(None, 24)
        
        queue.put({'type': 'status', 'message': "Đang chạy vòng lặp stress..."})
        running = True
        while running and (time.time() - start_time < duration):
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False

            screen.fill((10, 10, 20))
            mx, my = pygame.mouse.get_pos()
            if not mx and not my: mx, my = screen.get_width()//2, screen.get_height()//2

            for _ in range(5):
                particles.append([
                    [mx, my],
                    [np.random.randint(-50, 50) / 10, np.random.randint(0, 50) / 10 - 2],
                    np.random.randint(4, 10)
                ])

            for p in particles[:]:
                p[0][0] += p[1][0]
                p[0][1] += p[1][1]
                p[2] -= 0.1
                p[1][1] += 0.15
                
                r = min(255, max(0, 255 - int(p[2] * 20)))
                g = min(255, max(0, 200 - int(p[2] * 30)))
                b = 200
                color = (r, g, b)
                
                if p[2] > 0:
                    pygame.draw.circle(screen, color, [int(p[0][0]), int(p[0][1])], int(p[2]))
                else:
                    particles.remove(p)

            # --- Vẽ OSD (On-Screen Display) ---
            fps = clock.get_fps()
            elapsed_time = time.time() - start_time
            time_left = duration - elapsed_time
            
            fps_text = font.render(f"FPS: {fps:.1f}", True, (255, 255, 0))
            time_text = font.render(f"Thời gian còn lại: {time_left:.0f}s", True, (255, 255, 255))
            esc_text = font_small.render("Nhấn [ESC] để dừng bài test", True, (200, 200, 200))
            
            screen.blit(fps_text, (10, 10))
            screen.blit(time_text, (10, 40))
            screen.blit(esc_text, (10, screen.get_height() - 30))
            # ------------------------------------

            pygame.display.flip()
            
            progress = (time.time() - start_time) / duration
            queue.put({'type': 'update', 'progress': progress, 'fps': fps})
            
            clock.tick(120) # Chạy với FPS cao hơn để stress GPU
            
        queue.put({'type': 'result', 'status': 'OK'})

    except Exception as e:
        queue.put({'type': 'error', 'message': f"Lỗi trong quá trình test GPU: {e}"})
    finally:
        queue.put({'type': 'status', 'message': "Đang đóng Pygame..."})
        pygame.quit()
        queue.put({'type': 'done'})