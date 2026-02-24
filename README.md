# Beam Centre Finder
## Overview

This project provides a beam centre finding solution specifically designed for **Gaussian beam profiles** that Optimized for slow (~5 s/readout) and fast detector modes

Main goals:
- Minimize slow detector readouts (critical when each acquisition takes ~5 seconds)
- High robustness against noise and measurement errors
- Long-term maintainability and clarity
- Strict separation between hardware access, algorithms, and simulation

**All spatial coordinates and movements are in microns (µm)** to match real hardware systems.

## Project Structure

```
beam_finder/
├── algorithms/               # Pure math and fitting strategies
│   ├── coarse_gaussian_finder.py
│   └── continuous_gaussian_finder.py
├── hardware/                 # Interfaces to real devices
│   ├── detector_interface.py
│   └── motor_interface.py
├── simulation/               # Hardware-free testing environment
│   ├── beam_model.py
│   ├── simulated_detector.py
│   └── simulated_motor.py
├── utils/                    # Shared utilities
│   └── fitting.py
├── config.py                 # Central configuration & constants
└── main.py                   # Main workflow / entry point
```
## Design Principles

## Implemented Strategies

### 1. Coarse Search + Gaussian Fit (Slow Mode)

Ideal when detector readout is expensive (~5 s per point).

**Steps:**
1. Directional adaptive coarse grid search  
2. Refined fine scan around approximate peak  
3. 1D Gaussian fitting  

→ Keeps number of detector reads low while remaining reliable.

### 2. Continuous Fly-Scan (Fast Mode)

For high-speed detectors that support continuous acquisition.

**Steps:**
1. Constant-velocity motor movement  
2. Continuous / triggered detector sampling  
3. Position reconstruction (from timestamps or encoder data)  
4. Gaussian profile fitting  

→ Significantly faster when hardware supports it.

## Mathematical Model

Assumed intensity distribution:

I(x) = A ⋅ exp( − (x − x₀)² / (2σ²) )
Full Width at Half Maximum:
FWHM = 2.355 σ

## Simulation Support

Complete simulation layer for development and debugging:

- `GaussianBeamModel` — realistic beam intensity generation
- `SimulatedMotor` — virtual motorized stages
- `SimulatedDetector` — noise + slow/fast readout emulation

No physical hardware required during testing.

How to Run

```bash
# Run the program
python main.py

Maintainability Features

All units and parameters in one place: config.py
Algorithms do not know anything about hardware
Gaussian fitting logic isolated in utils/fitting.py
Tracks number of measurements taken

Current Assumptions

Beam profile is approximately Gaussian
Detector noise model is configurable
Motor positioning uses micron units
Readout time dominates in slow mode

Planned Improvements

Unit tests (pytest)
Real-time visualization of search path and fit
