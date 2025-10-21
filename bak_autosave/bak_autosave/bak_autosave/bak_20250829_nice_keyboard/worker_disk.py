import os
import sys
import time
import tempfile

def run_benchmark(queue, file_size_mb=256):
    test_file_path = None
    try:
        file_size_bytes = file_size_mb * 1024 * 1024
        chunk_size = 4 * 1024 * 1024
        if file_size_bytes < chunk_size:
            chunk_size = file_size_bytes
        chunks = file_size_bytes // chunk_size
        
        queue.put({'type': 'status', 'message': "Đang tạo file test trong thư mục tạm..."})
        temp_dir = tempfile.gettempdir()
        test_file_path = os.path.join(temp_dir, f"laptoptester_speedtest_{os.getpid()}.tmp")
        
        # --- Ghi ---
        queue.put({'type': 'status', 'message': f"Đang ghi file {file_size_mb}MB..."})
        data_chunk = os.urandom(chunk_size)
        write_start_time = time.time()
        with open(test_file_path, "wb") as f:
            for i in range(chunks):
                chunk_start_time = time.time()
                f.write(data_chunk)
                f.flush() # Đảm bảo dữ liệu được ghi
                os.fsync(f.fileno()) # Ép ghi xuống đĩa vật lý
                chunk_duration = time.time() - chunk_start_time
                
                chunk_speed = (chunk_size / (1024*1024)) / chunk_duration if chunk_duration > 0 else 0
                progress = ((i + 1) / chunks) * 0.5
                queue.put({'type': 'update', 'progress': progress, 'operation': 'Write', 'speed': chunk_speed})
        
        write_duration = time.time() - write_start_time
        write_speed = (file_size_mb / write_duration) if write_duration > 0 else 0
        
        # --- Đọc ---
        queue.put({'type': 'status', 'message': f"Đang đọc file {file_size_mb}MB..."})
        read_start_time = time.time()
        with open(test_file_path, "rb") as f:
            for i in range(chunks):
                chunk_start_time = time.time()
                f.read(chunk_size)
                chunk_duration = time.time() - chunk_start_time
                
                chunk_speed = (chunk_size / (1024*1024)) / chunk_duration if chunk_duration > 0 else 0
                progress = 0.5 + ((i + 1) / chunks) * 0.5
                queue.put({'type': 'update', 'progress': progress, 'operation': 'Read', 'speed': chunk_speed})

        read_duration = time.time() - read_start_time
        read_speed = (file_size_mb / read_duration) if read_duration > 0 else 0
        
        result_data = {
            'write_speed': f"{write_speed:.2f}",
            'read_speed': f"{read_speed:.2f}"
        }
        queue.put({'type': 'result', 'data': result_data})
        
    except Exception as e:
        queue.put({'type': 'error', 'message': f"{e.__class__.__name__}: {e}"})
    finally:
        if test_file_path and os.path.exists(test_file_path):
            try:
                queue.put({'type': 'status', 'message': "Đang dọn dẹp file test..."})
                os.remove(test_file_path)
            except OSError as e:
                 queue.put({'type': 'error', 'message': f"Không thể xóa file tạm: {e}"})
        queue.put({'type': 'done'})