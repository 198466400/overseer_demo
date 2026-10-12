# Overseer Demo

A lightweight overseer system that manages multiple worker threads, detects failures, and automatically restarts dead workers. Designed for Termux-safe execution with guaranteed visible output and deterministic behavior.

## Features
- Continuous worker heartbeat
- Automatic failure detection
- Automatic worker restart
- Overseer heartbeat loop
- Clean shutdown handling
- Single-file drag-and-drop deployment

## Usage
Run the overseer:

```bash
python3 overseer.py
```

Workers print alive signals every 2 seconds. The overseer prints a heartbeat every 3 seconds and restarts any worker that dies.

## Author
Dakota Moses (198466400)

