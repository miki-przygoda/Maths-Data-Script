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