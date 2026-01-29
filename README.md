# Clap on Jarvis

A voice activation system that listens for double claps and responds to voice commands. Perfect for hands-free dev environment launches.

## Features

- **Clap Detection**: Detects double claps as a trigger mechanism
- **Voice Recognition**: Listens for voice commands via Google Speech-to-Text
- **Voice Commands**: Launch your dev environment with "let's get it started" or "go"
- **Low Latency**: Optimized for fast response times with minimal buffering
- **Cooldown Protection**: Prevents accidental repeated triggers

## Requirements

- Python 3.7+
- Microphone

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Aariyan007/Clap_on_Jarvis.git
cd Clap_on_Jarvis
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install sounddevice numpy SpeechRecognition
```

## Usage

Run the script:
```bash
python jarvis.py
```

The program will start listening for claps. To activate:
1. **Clap twice** rapidly (within 0.7 seconds)
2. **Say** one of: "let's get it started", "get it started", or "go"
3. Safari and Terminal will launch automatically

## Configuration

Edit these constants in `jarvis.py` to customize behavior:

- `CLAP_THRESHOLD`: Sensitivity of clap detection (default: 0.6)
- `CLAP_GAP`: Maximum time between two claps (default: 0.7s)
- `COOLDOWN`: Cooldown period between triggers (default: 3s)
- `SAMPLE_RATE`: Audio sampling rate (default: 44100 Hz)

## How It Works

The system operates in two phases:

**Phase 1: Clap Detection**
- Continuously monitors audio input from your microphone
- Detects sharp peaks (sudden loud sounds) with low sustained volume
- Identifies double claps within the configured time window

**Phase 2: Voice Recognition**
- When triggered, activates Google Speech-to-Text
- Listens for up to 5 seconds for voice commands
- Recognizes keywords and launches applications

## License

See LICENSE file for details.

## Requirements File

Dependencies are listed in:
```bash
pip freeze > requirements.txt
```
