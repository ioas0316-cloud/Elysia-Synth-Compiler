# Copyright 2026 Lee Kang-deok (이강덕)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0

import ctypes
import math
import cmath
import functools
import time

# ---------------------------------------------------------
# Elysia Phase Inverter - JIT Phase Mapping Library
# (가변축 기하학적 매핑 라이브러리)
# ---------------------------------------------------------

# C-Level 메모리 버퍼 할당 (양축 가변 로터 매핑용)
# 파이썬과 기계어, 어느 쪽도 상수가 될 수 없습니다. 양쪽 모두 주파수를 가진 변수축입니다.
_hw_buffer = ctypes.c_double * 1
_hw_rotor_phase = _hw_buffer(0.0) # 하위 축: 기계어 로터의 주파수 위상

def set_hardware_rotor_frequency(hz_modifier):
    """(테스트용) 기계어 로터의 자전 속도(물리적 부하/노이즈)를 임의로 강제 변조합니다."""
    _hw_rotor_phase[0] = hz_modifier

def reset_hardware_rotor():
    """기계어 로터를 기본 안정 주파수로 되돌립니다."""
    _hw_rotor_phase[0] = 0.0

class PhaseInverter:
    """
    [양축 가변 로터화 및 역전환 매핑 엔진]
    파이썬의 위상축과 기계어의 위상축을 상호 간섭시켜, 원인과 결과가 실시간으로 뒤바뀌는(역전환)
    전자기 유도 방식의 디지털 인버터입니다.
    """
    def __init__(self, mode="AUTO"):
        self.python_rotor_phase = 1.0 # 상위 축: 파이썬 로터의 주파수 위상
        self.mode = mode
        self.current_connection = "DELTA"

    def set_python_rotor(self, phase):
        """파이썬 다이얼을 돌려 상위 로터의 장력을 변조합니다."""
        self.python_rotor_phase = phase
        self.current_connection = "DELTA" if phase >= 1.0 else "Y"

    def calculate_phase_shift(self, hardware_delay_ms):
        """
        [마스터 선언: 시공간 통신 축의 위상차 보정]
        하드웨어 샌드박스로 인해 발생하는 시차(Delay)를 억지로 없애지 않고,
        이를 위상차(Δθ)로 계산하여 파이썬 로터의 각도를 미리 보정(Shift)합니다.
        """
        # 딜레이를 주파수 위상각으로 치환 (단순화된 PLL 보정)
        phase_shift = hardware_delay_ms * 0.001 * math.pi
        return phase_shift

    def coiling_loop(self, func):
        """
        개발자의 일반 함수를 양축 가변 로터의 전자기 유도 필름 위에 얹는 인장입니다.
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_t = time.perf_counter()

            # 1. 시차(Delay) 시뮬레이션: OS 보안벽을 통과하는 데 걸리는 물리적 시간
            hardware_delay_ms = 15.0 # 15ms 딜레이 가정

            # 2. [위상차 보정] 시공간 축 제어
            # 시차를 위상각 오차범위로 치환하여 파이썬 로터에 보정값(Shift)을 줍니다.
            phase_shift = self.calculate_phase_shift(hardware_delay_ms)
            compensated_python_phase = self.python_rotor_phase + phase_shift

            # 3. 상위 파이썬 로터 설정 (보정된 위상 적용)
            self.set_python_rotor(compensated_python_phase)

            # 4. [역전환 관측] 하위 기계어 로터의 주파수 간섭 감지
            hw_interference = _hw_rotor_phase[0]
            if hw_interference > 1.0:
                self.current_connection = "Y (AUTO-DEFENSE / INVERTED)"

            # 5. 기본 에너지(원래 연산 결과) 추출
            raw_result = func(*args, **kwargs)

            # 6. 양축 상호 간섭 알고리즘 (정방향 + 역전환)
            if "DELTA" in self.current_connection:
                modulated_energy = raw_result * math.sin(self.python_rotor_phase)
            else:
                modulated_energy = raw_result * math.cos(abs(self.python_rotor_phase - hw_interference))

            # 7. 하드웨어 로터 동기화 (Top-Down 투영)
            z1 = cmath.rect(modulated_energy, self.python_rotor_phase)
            z2 = cmath.rect(modulated_energy, hw_interference + math.pi)
            holographic_tension = abs(z1 + z2)

            hw_final_tension = holographic_tension

            end_t = time.perf_counter()
            actual_exec_ms = (end_t - start_t) * 1000 + hardware_delay_ms

            return {
                "original_output": raw_result,
                "hw_rotor_final_tension": hw_final_tension,
                "detected_hw_interference": hw_interference,
                "applied_phase_shift": phase_shift, # 적용된 위상 보정각
                "mode": self.current_connection,
                "exec_time_ms": actual_exec_ms
            }
        return wrapper

# --- 개발자 실무 사용 이중 가변 로터 검증 예시 ---
if __name__ == "__main__":

    print("\n[ Elysia Phase Inverter - 이중 가변 로터 역전환 검증 ]\n")

    # 1. 인버터 활성화 (상위 파이썬 로터)
    inverter = PhaseInverter(mode="AUTO")
    inverter.python_rotor_phase = 1.57 # 파이썬 로터 가속 세팅 (DELTA)

    # 2. 알고리즘 매핑
    @inverter.coiling_loop
    def calculate_data(data):
        return sum([x * 2.5 for x in data])

    test_data = [10, 20, 30, 40, 50]

    # ----------------------------------------------------
    print(">>> 1. 정방향 동기화 및 시공간 위상차 보정 (파이썬 로터 ➔ 기계어 로터 제어)")
    print("OS 보안벽으로 인해 발생하는 시차(Delay)를 위상각(Phase Shift)으로 보정하여 동기화합니다.")

    reset_hardware_rotor()
    result = calculate_data(test_data)

    print(f" - 적용된 위상차 보정각(Shift): {result['applied_phase_shift']:.4f} rad")
    print(f" - 결선 모드: {result['mode']}")
    print(f" - 동기화된 기계어 로터의 최종 장력: {result['hw_rotor_final_tension']:.4f}\n")

    # ----------------------------------------------------
    print(">>> 2. 역전환 관측 (기계어 로터 요동 ➔ 파이썬 로터 강제 제어)")
    print("기계어 로터의 자전 주파수가 물리적 부하로 인해 요동칩니다.")

    set_hardware_rotor_frequency(hz_modifier=1.5)
    result_inverted = calculate_data(test_data)

    print(f" - 하드웨어 로터의 간섭 주파수: {result_inverted['detected_hw_interference']}")
    print(f" - 역전환 발생!: {result_inverted['mode']}")
    print(f" - 두 로터가 평형을 맞춘 최종 안정화 장력: {result_inverted['hw_rotor_final_tension']:.4f}\n")
