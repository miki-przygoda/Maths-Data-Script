import time
import csv
import platform
import os
import gc

TEST_SIZES_MB = [0.001, 0.01, 0.1, 1, 8, 32, 128, 256, 512, 1024]
ITERATIONS = 100
FILENAME = f"bench_{platform.node()}_{int(time.time())}.csv"

def run_benchmark():
    results = []
    print(f"Starting Master Benchmark on {platform.node()}...")

    for size_mb in TEST_SIZES_MB:
        size_bytes = int(size_mb * 1024 * 1024)
        print(f"Testing {size_mb} MB block...", end=" ", flush=True)

        for i in range(ITERATIONS):
            # --- 1. RAM/CACHE TEST ---
            gc.collect()
            start_mem = time.perf_counter()
            data = bytearray(size_bytes)
            # Simple write/read to exercise the memory
            for j in range(0, size_bytes, 4096): data[j] = 1 
            _ = sum(data)
            mem_duration = time.perf_counter() - start_mem
            mem_speed = size_mb / mem_duration if mem_duration > 0 else 0

            # --- 2. DISK (NON-VOLATILE) TEST ---
            file_name = f"test_{i}.bin"
            disk_sample = os.urandom(min(size_bytes, 100 * 1024 * 1024)) # Cap at 100MB for disk speed
            
            start_disk = time.perf_counter()
            with open(file_name, "wb") as f:
                f.write(disk_sample)
                os.fsync(f.fileno())
            disk_duration = time.perf_counter() - start_disk
            os.remove(file_name)
            
            disk_speed = (len(disk_sample) / (1024*1024)) / disk_duration

            # --- 3. LOGGING EVERYTHING ---
            results.append({
                "Device": platform.node(),
                "OS": platform.system(),
                "Block_Size_MB": size_mb,
                "Iteration": i + 1,
                "RAM_Speed_MBs": round(mem_speed, 2),
                "Disk_Speed_MBs": round(disk_speed, 2),
                "Latency_ms": round((mem_duration / max(1, size_bytes/1024)) * 1000, 6)
            })
            del data
            
        print("Done.")

    # --- 4. Save to CSV ---
    if results:
        keys = results[0].keys()
        with open(FILENAME, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(results)
    
    print(f"\nCSV Generated: {FILENAME}")

if __name__ == "__main__":
    run_benchmark()