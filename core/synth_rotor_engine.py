# Copyright 2026 Lee Kang-deok (이강덕)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0

import time
import math
import cmath
import ctypes
import threading
import random
import sys

# ---------------------------------------------------------
# Elysia Synth Compiler - Variable Rotor Engine
# Single Layer 4D Complex Tensor Interference Engine
# ---------------------------------------------------------

class HardwareBridge:
    """
    Simulates the bidirectional mapping bridge between Python (Phase) and Hardware (Binary).
    Uses ctypes to represent direct memory access to a simulated hardware register.
    """
    def __init__(self):
        # Simulating a 1-byte hardware register (binary 00000000 to 11111111)
        self.hardware_register = ctypes.c_uint8(0)
        self.hardware_noise_level = 0.0

    def top_down_modulate(self, binary_val):
        """Top-Down: Python master phase modulates the physical binary gap."""
        self.hardware_register.value = binary_val & 0xFF

    def bottom_up_sense(self):
        """Bottom-Up: Hardware spike modulates Python Delta-Y state."""
        return self.hardware_noise_level

    def inject_noise(self, intensity=1.0):
        """Virtual Hardware Noise Injector"""
        self.hardware_noise_level = intensity

class PIDController:
    """PID to smooth out tension variations and return to zero-point balance."""
    def __init__(self, p=0.1, i=0.01, d=0.05):
        self.k_p = p
        self.k_i = i
        self.k_d = d
        self.integral = 0
        self.prev_error = 0

    def update(self, error, dt):
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt if dt > 0 else 0
        self.prev_error = error
        return self.k_p * error + self.k_i * self.integral + self.k_d * derivative

class PLL:
    """Phase-Locked Loop to sync 1000Hz QPC loop precisely."""
    def __init__(self):
        self.phase_error = 0
        self.locked_phase = 0

    def sync(self, target_phase, current_phase):
        self.phase_error = target_phase - current_phase
        # Simplified locking mechanism with damping
        self.locked_phase += self.phase_error * 0.1
        return self.locked_phase

class SynthRotorEngine:
    def __init__(self):
        self.master_phase = 0.0 # Master knob (theta)

        # Sub-rotors (amplitude, frequency) entangled with master phase
        self.base_freq = 432.0 # Hz
        self.base_amp = 1.0

        self.bridge = HardwareBridge()
        self.pid = PIDController(p=0.5, i=0.05, d=0.1) # Aggressive PID for visualizer
        self.pll = PLL()

        self.connection_mode = 'DELTA' # 'DELTA' (Concentration) or 'Y' (Stabilization)

        self.running = False
        self.t_prime = 0.0 # Modulated time axis (t')

    def draw_visualizer(self, noise, error, mode, binary_val):
        """Terminal visualizer demonstrating Phase-Locking and Noise Absorption."""
        width = 40
        center = width // 2

        # Visualize tension/error mapping
        offset = int(error * 10)
        pos = max(0, min(width - 1, center + offset))

        bar = ['-'] * width
        bar[center] = '|' # Absolute Zero Point

        if mode == 'Y':
            marker = 'O' # Stabilization
        else:
            marker = 'X' # Concentration

        bar[pos] = marker
        bar_str = "".join(bar)

        binary_str = f"{binary_val:08b}"

        sys.stdout.write(f"\r[ {mode} ] {bar_str} | HW Byte: {binary_str} | Noise: {noise:.2f} | Error: {error:.4f} ")
        sys.stdout.flush()

    def run_qpc_loop(self):
        """1000Hz QPC interrupt loop simulation."""
        self.running = True
        dt = 0.001 # 1ms (1000Hz)

        while self.running:
            start_time = time.perf_counter()

            # 1. Hardware Bridge: Bottom-Up Sense
            noise_level = self.bridge.bottom_up_sense()

            if noise_level > 0.5:
                self.connection_mode = 'Y' # Auto-switch to stabilization

            # 2. Modulate Time Axis (t -> t') based on connection mode and master phase
            if self.connection_mode == 'DELTA':
                # Concentration/Acceleration
                t_delta = dt * (1.0 + math.sin(self.master_phase)) + random.uniform(-noise_level, noise_level) * 0.01
            else: # 'Y' mode
                # Stabilization/Neutral
                t_delta = dt * 1.0 + random.uniform(-noise_level*0.1, noise_level*0.1) * 0.01

            self.t_prime += t_delta

            # 3. PID Control: Smooth out tension on t'
            error = dt - t_delta
            correction = self.pid.update(error, dt)
            self.t_prime += correction

            # 4. PLL: Phase lock the sub-rotors
            target_sub_phase = self.t_prime * self.base_freq * 2 * math.pi
            locked_sub_phase = self.pll.sync(target_sub_phase, self.master_phase)

            # 5. Double-Helix Rotor Logic & Complex Tensor Interference
            z1 = cmath.rect(self.base_amp, locked_sub_phase) # Yang spiral
            z2 = cmath.rect(self.base_amp, -locked_sub_phase + math.pi) # Yin spiral
            interference = z1 + z2

            # 6. Hardware Bridge: Top-Down Modulate
            amp_magnitude = abs(interference)
            binary_out = 255 if amp_magnitude > self.base_amp else 0
            self.bridge.top_down_modulate(binary_out)

            # 7. Visualizer
            self.draw_visualizer(noise_level, error, self.connection_mode, self.bridge.hardware_register.value)

            # Decay noise
            if self.bridge.hardware_noise_level > 0:
                self.bridge.hardware_noise_level *= 0.99
                if self.bridge.hardware_noise_level < 0.01:
                    self.bridge.hardware_noise_level = 0
                    self.connection_mode = 'DELTA' # Auto-switch back

            # Sleep to maintain ~1000Hz (simplified simulation)
            elapsed = time.perf_counter() - start_time
            sleep_time = max(0, dt - elapsed)
            time.sleep(sleep_time)

    def set_master_phase(self, phase):
        self.master_phase = phase

    def trigger_hardware_spike(self, intensity=2.0):
        self.bridge.inject_noise(intensity)

    def start(self):
        self.thread = threading.Thread(target=self.run_qpc_loop)
        self.thread.daemon = True
        self.thread.start()
        print("\n[ Elysia Synth Compiler - Variable Rotor Engine Started ]\n")

    def stop(self):
        self.running = False
        self.thread.join()
        print("\n\n[ Engine Stopped ]\n")

if __name__ == "__main__":
    engine = SynthRotorEngine()
    engine.start()

    time.sleep(2)

    # 1. Inject Noise to see Bottom-Up 'Y' mode stabilization
    print("\n\n>>> INJECTING HARDWARE NOISE (Observe Y-Mode Stabilization) <<<")
    engine.trigger_hardware_spike(2.5)
    time.sleep(4)

    # 2. Change Phase and observe Delta mode concentration
    print("\n\n>>> TURNING MASTER PHASE KNOB (Observe Delta Tension) <<<")
    engine.set_master_phase(1.57) # ~Pi/2
    time.sleep(3)

    engine.stop()
