#!/usr/bin/env python3
"""
Audio Test Worker - Tích hợp stereo_test.mp3
"""

import os
import time
import threading

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    print("Warning: pygame not available for audio test")

def play_stereo_test_audio(status_callback=None):
    """
    Phát file stereo_test.mp3 nếu có, nếu không thì fallback sang generated audio
    """
    if not PYGAME_AVAILABLE:
        if status_callback:
            status_callback("❌ Pygame không có sẵn - Cài đặt: pip install pygame")
        return False
    
    # Tìm file stereo_test.mp3
    stereo_test_path = os.path.join(os.path.dirname(__file__), "assets", "stereo_test.mp3")
    
    if os.path.exists(stereo_test_path):
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)
            
            if status_callback:
                status_callback("🎵 Phát file stereo_test.mp3...")
            
            # Load và phát file
            pygame.mixer.music.load(stereo_test_path)
            pygame.mixer.music.play()
            
            # Monitor playback
            start_time = time.time()
            while pygame.mixer.music.get_busy():
                elapsed = int(time.time() - start_time)
                if status_callback:
                    status_callback(f"🎵 Phát stereo_test.mp3 ({elapsed}s)")
                time.sleep(1)
            
            if status_callback:
                status_callback("✅ Hoàn thành phát file stereo test")
            
            pygame.mixer.music.stop()
            return True
            
        except Exception as e:
            if status_callback:
                status_callback(f"❌ Lỗi phát stereo_test.mp3: {e}")
            return False
    else:
        if status_callback:
            status_callback("⚠️ Không tìm thấy file stereo_test.mp3")
        return False

def generate_test_tone(frequency=440, duration=3, status_callback=None):
    """
    Tạo tone test đơn giản
    """
    if not PYGAME_AVAILABLE:
        return False
    
    try:
        import numpy as np
        
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)
        
        sample_rate = 44100
        frames = int(duration * sample_rate)
        
        t = np.linspace(0, duration, frames)
        tone = 0.3 * np.sin(2 * np.pi * frequency * t)
        
        # Stereo
        stereo_audio = np.column_stack([tone, tone])
        sound = pygame.sndarray.make_sound((stereo_audio * 32767).astype(np.int16))
        
        if status_callback:
            status_callback(f"🎵 Phát tone {frequency}Hz ({duration}s)")
        
        sound.play()
        time.sleep(duration)
        
        return True
        
    except Exception as e:
        if status_callback:
            status_callback(f"❌ Lỗi tạo tone: {e}")
        return False

def run_audio_test(status_callback=None):
    """
    Chạy test âm thanh hoàn chỉnh
    """
    success = False
    
    # Thử phát stereo_test.mp3 trước
    if play_stereo_test_audio(status_callback):
        success = True
    else:
        # Fallback sang generated tones
        if status_callback:
            status_callback("🔄 Chuyển sang test tone tự tạo...")
        
        test_frequencies = [440, 1000, 2000]  # A4, 1kHz, 2kHz
        
        for freq in test_frequencies:
            if generate_test_tone(freq, 2, status_callback):
                success = True
            time.sleep(0.5)
    
    return success

if __name__ == "__main__":
    # Test standalone
    def print_status(msg):
        print(f"[AUDIO] {msg}")
    
    print("Testing audio worker...")
    result = run_audio_test(print_status)
    print(f"Audio test result: {result}")