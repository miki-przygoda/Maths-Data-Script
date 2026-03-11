# Maths Data Script

A script for collecting system performance data for coursework.

## Setup

### 1. Create a virtual environment

```bash
python3 -m venv venv
```

### 2. Activate the virtual environment

On macOS/Linux:

```bash
source venv/bin/activate
```

On Windows (PowerShell):

```powershell
venv\Scripts\Activate.ps1
```

### 3. Install required libraries

```bash
pip install pandas psutil
```

## Run the script

From the project root:

```bash
python main.py
```

## Output

The script creates a CSV file in the project root with your device name and power source in the filename, for example:

- `data_Mikolajs-MacBook-Pro.local_Charger.csv`
- `data_Mikolajs-MacBook-Pro.local_Battery.csv`

- Try to run it twice, once on battery and once on the charger since it will give us higher quality results. Then take both of the csv files and send them to be on email: mm6659o@gre.ac.uk

- You can vary the runs in some way you think is interesting but just note that when you send me the data, if you do both runs on the charger and on battery try to keep the runs moderetly similar between one another, so dont open new apps or new tabs on your browser

- If you need any extra help with running it just send me a message or again email me and Ill try to get back to you as soon as I can to help.

- The type of data it collects is:
Member_Name, OS_Type, Trial,CPU_Usage_Pct, RAM_Free_MB, Clock_Speed_GHz, Execution_Time_ms, Power_Plugged, Process_Count

- Here is the code below, place it into a python file called main.py

```python

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
        time.sleep(0.1)
        
    df = pd.DataFrame(results)
    output_file = f"data_{platform.node()}_{power_source}.csv"
    df.to_csv(output_file, index=False)
    print(f"Success! File saved as {output_file}")

collect_performance_data()


```