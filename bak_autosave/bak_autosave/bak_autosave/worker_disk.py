import os
import time
import tempfile
import psutil # Cần psutil để kiểm tra dung lượng

def run_benchmark(queue, duration, file_size_mb=512): # Duration không dùng nhưng giữ lại để đồng bộ
    """
    Chạy benchmark tốc độ đọc/ghi tuần tự, tạo file trong thư mục tạm an toàn của hệ thống.
    Đã được cải tiến để kiểm tra dung lượng và báo cáo tốc độ trung bình.
    """
    test_file_path = None
    try:
        # Sử dụng thư mục tạm thời của hệ thống. Đây là cách an toàn và đảm bảo nhất.
        test_dir = tempfile.gettempdir()
        queue.put({'type': 'status', 'message': f"Sử dụng thư mục test: {test_dir}"})

        # CẢI TIẾN: Kiểm tra dung lượng trống trước khi chạy
        free_space_mb = psutil.disk_usage(test_dir).free / (1024 * 1024)
        if free_space_mb < file_size_mb * 1.1: # Cần thêm 10% dự phòng
            queue.put({'type': 'error', 'message': f"Không đủ dung lượng trống. Cần {file_size_mb}MB, còn lại {free_space_mb:.0f}MB."})
            return

        file_size_bytes = file_size_mb * 1024 * 1024
        chunk_size = 4 * 1024 * 1024  # 4MB chunk
        chunks = file_size_bytes // chunk_size
        
        test_file_path = os.path.join(test_dir, f"laptoptester_speedtest_{os.getpid()}.tmp")
        
        data_chunk = os.urandom(chunk_size)

        # --- Ghi tuần tự (Sequential Write) ---
        queue.put({'type': 'status', 'message': f"Đang ghi tuần tự file {file_size_mb}MB..."})
        write_start_time = time.time()
        
        total_bytes_written = 0
        with open(test_file_path, "wb") as f:
            for i in range(chunks):
                chunk_start_time = time.time()
                f.write(data_chunk)
                chunk_duration = time.time() - chunk_start_time
                
                total_bytes_written += chunk_size
                total_write_time = time.time() - write_start_time

                chunk_speed = (chunk_size / (1024*1024)) / chunk_duration if chunk_duration > 0 else 0
                avg_speed = (total_bytes_written / (1024*1024)) / total_write_time if total_write_time > 0 else 0
                progress = ((i + 1) / chunks) * 0.5
                queue.put({'type': 'update', 'progress': progress, 'operation': 'Write', 'speed': chunk_speed, 'avg_speed': avg_speed})
            
            queue.put({'type': 'status', 'message': "Đang xả cache ghi xuống đĩa..."})
            f.flush()
            os.fsync(f.fileno())

        write_duration = time.time() - write_start_time
        write_speed = (file_size_mb / write_duration) if write_duration > 0 else 0
        
        # --- Đọc tuần tự (Sequential Read) ---
        queue.put({'type': 'status', 'message': f"Đang đọc tuần tự file {file_size_mb}MB..."})
        read_start_time = time.time()
        
        total_bytes_read = 0
        with open(test_file_path, "rb") as f:
            for i in range(chunks):
                chunk_start_time = time.time()
                _ = f.read(chunk_size)
                chunk_duration = time.time() - chunk_start_time

                total_bytes_read += chunk_size
                total_read_time = time.time() - read_start_time
                
                chunk_speed = (chunk_size / (1024*1024)) / chunk_duration if chunk_duration > 0 else 0
                avg_speed = (total_bytes_read / (1024*1024)) / total_read_time if total_read_time > 0 else 0
                progress = 0.5 + ((i + 1) / chunks) * 0.5
                queue.put({'type': 'update', 'progress': progress, 'operation': 'Read', 'speed': chunk_speed, 'avg_speed': avg_speed})

        read_duration = time.time() - read_start_time
        read_speed = (file_size_mb / read_duration) if read_duration > 0 else 0
        
        result_data = {
            'status': 'OK',
            'write_speed': f"{write_speed:.2f}",
            'read_speed': f"{read_speed:.2f}"
        }
        queue.put({'type': 'result', 'data': result_data})
        
    except Exception as e:
        queue.put({'type': 'error', 'message': f"{e.__class__.__name__}: {e}"})
    finally:
        if test_file_path and os.path.exists(test_file_path):
            try:
                os.remove(test_file_path)
            except Exception as e:
                queue.put({'type': 'error', 'message': f"Không thể xóa file tạm: {e}"})
        queue.put({'type': 'done'})