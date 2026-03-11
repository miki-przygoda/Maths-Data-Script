import time
import psutil
import platform
import pandas as pd

def collect_performance_data(iterations=200):
    results = []
    print(f"Starting data collection on {platform.node()}...")

    battery_info = psutil.sensors_battery()
    power_source = "Charger" if (battery_info is None or battery_info.power_plugged) else "Battery"
    
    for i in range(iterations):
        cpu_usage = psutil.cpu_percent(interval=0.1)
        ram_available = psutil.virtual_memory().available / (1024 * 1024) # MB
        
        start_time = time.perf_counter()
        _ = [x**2 for x in range(1000000)]
        end_time = time.perf_counter()

        battery = psutil.sensors_battery()
        power_plugged = battery.power_plugged if battery else True
        process_count = len(psutil.pids())
        
        exec_time = (end_time - start_time) * 1000
        
        results.append({
            'Member_Name': platform.node(),
            'OS_Type': platform.system(),
            'Trial': i + 1,
            'CPU_Usage_Pct': cpu_usage,
            'RAM_Free_MB': ram_available,
            'Clock_Speed_GHz': psutil.cpu_freq().current / 1000 if psutil.cpu_freq() else 0,
            'Execution_Time_ms': exec_time,
            'Power_Plugged': 1 if power_plugged else 0,
            'Process_Count': process_count,
        })
        time.sleep(0.1) # Brief pause between trials
        
    df = pd.DataFrame(results)
    output_file = f"data_{platform.node()}_{power_source}.csv"
    df.to_csv(output_file, index=False)
    print(f"Success! File saved as {output_file}")

collect_performance_data()