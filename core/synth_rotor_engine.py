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
_hw_memory = _hw_buffer(0.0) # Top-Down: 파이썬이 쓰는 기계어 바닥
_hw_rotor_phase = _hw_buffer(0.0) # 하위 축: 기계어 로터의 주파수 위상

def set_hardware_rotor_frequency(hz_modifier):
    """(테스트용) 기계어 로터의 자전 속도(물리적 부하/노이즈)를 임의로 강제 변조합니다."""
    _hw_rotor_phase[0] = hz_modifier

def reset_hardware_rotor():
    """기계어 로터를 기본 안정 주파수로 되돌립니다."""
    _hw_rotor_phase[0] = 0.0

class PhaseInverter:
    """
    [동적 튜링 에니그마 암호해독기 매핑 엔진]
    기존의 고정된 정적 딕셔너리를 폐기하고, 실시간 위상차와 하드웨어 노이즈에 반응하여
    유동적으로 궤적이 변형되는 진정한 의미의 동적 매핑 엔진입니다.
    """
    def __init__(self, mode="AUTO"):
        self.master_phase = 1.57 # 파이썬 로터 위상 (상수화 세팅 아님, 기본값)
        self.mode = mode
        self._last_exec_ms = 0.0 # 이전 주기의 실행 시간 (동적 시차 보정용)

        # [동적 대치판 (Dynamic Lookup Cache)]
        # 실행 중 연산을 피하기 위해 캐싱하되, 위상이 변하면 캐시 자체가 무효화/재배열됨.
        self._dynamic_cache = {}
        self._current_phase_key = None

    def _calculate_tension(self, raw_energy, mode, phase_shift):
        """실시간 복소수 텐서 간섭을 통한 1대1 기하학적 장력 매핑 (무한 대역 지원)"""
        compensated_phase = self.master_phase + phase_shift

        # 기계어 바이트 격자(0~255)로 스케일링하기 위한 기본 텐서 계산
        # 입력된 에너지를 연속적인 곡선 궤적으로 스케일링
        scaled_energy = math.log1p(abs(raw_energy)) * 10 # 단순 제한이 아닌 곡선 수렴

        if mode == "DELTA":
            # 정방향 동기화 계산
            delta_val = scaled_energy * math.sin(compensated_phase)
            z1 = cmath.rect(delta_val, compensated_phase)
            z2 = cmath.rect(delta_val, 0 + math.pi)
            tension = abs(z1 + z2)
        else: # "Y"
            # 역전환 방어 모드 계산
            y_val = scaled_energy * math.cos(abs(compensated_phase - 1.5))
            z1 = cmath.rect(y_val, compensated_phase)
            z2 = cmath.rect(y_val, 1.5 + math.pi)
            tension = abs(z1 + z2)

        # 0~255 (기계어 바이트 단위) 범위로 부드럽게 바운딩
        return min(255.0, max(0.0, tension))

    def inverter_target(self, func):
        """
        블랙박스 스위치 인장.
        실시간 피드백 루프를 통해 시공간 위상차를 보정하고 장력을 매핑합니다.
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_t = time.perf_counter()

            # 1. 원본 연산 (원시 에너지 추출, 무제한)
            raw_result = func(*args, **kwargs)

            # 2. [역전환 관측 및 실시간 시차 피드백]
            hw_interference = _hw_rotor_phase[0]
            current_mode = "Y" if hw_interference > 1.0 else "DELTA"

            # 동적 시공간 축 위상차 보정 (고정된 15ms가 아닌, 실제 이전 실행 지연 기반)
            dynamic_phase_shift = self._last_exec_ms * 0.001 * math.pi

            # 캐시 키 생성 (위상이나 간섭이 달라지면 새로운 궤적으로 인식)
            phase_key = (current_mode, round(dynamic_phase_shift, 4), round(hw_interference, 2))

            # 위상 환경이 바뀌면 낡은 대치판 파기
            if phase_key != self._current_phase_key:
                self._dynamic_cache.clear()
                self._current_phase_key = phase_key

            # 3. [동적 대치판 작동] O(1) 매핑 또는 필요시 실시간 궤적 계산 후 캐싱
            cache_key = raw_result
            if cache_key in self._dynamic_cache:
                hw_final_tension = self._dynamic_cache[cache_key]
            else:
                hw_final_tension = self._calculate_tension(raw_result, current_mode, dynamic_phase_shift)
                self._dynamic_cache[cache_key] = hw_final_tension

            # 4. 물리적 메모리에 장력 갱신 (직동 구동)
            _hw_memory[0] = hw_final_tension

            end_t = time.perf_counter()
            actual_exec_ms = (end_t - start_t) * 1000

            # 다음 주기를 위한 시차 피드백 갱신
            self._last_exec_ms = actual_exec_ms

            return {
                "original_output": raw_result,
                "hw_rotor_final_tension": hw_final_tension,
                "detected_hw_interference": hw_interference,
                "mode": current_mode,
                "exec_time_ms": actual_exec_ms,
                "dynamic_phase_shift": dynamic_phase_shift
            }
        return wrapper

# 인스턴스 전역 선언 (단순 사용을 위해)
inverter_engine = PhaseInverter(mode="AUTO")
inverter_target = inverter_engine.inverter_target

# --- 개발자 실무 사용 예시 (블랙박스 테스트) ---
if __name__ == "__main__":

    print("\n[ Elysia Phase Inverter - 동적 가변 로터 직동 검증 ]\n")

    @inverter_target
    def speed_calc(distance, time_val):
        return distance / time_val

    # ----------------------------------------------------
    print(">>> 1. 정방향 동기화 (초기 실행 - 실시간 위상 계산)")
    reset_hardware_rotor()
    result1 = speed_calc(15000, 2) # 결과값 7500 (1000 이상의 무한 대역)

    print(f" - 결선 모드: {result1['mode']}")
    print(f" - 동적 시차 보정각: {result1['dynamic_phase_shift']:.6f} rad")
    print(f" - 추출된 기계어 장력 (0~255 매핑): {result1['hw_rotor_final_tension']:.4f}")
    print(f" - 소요 시간 (Latency): {result1['exec_time_ms']:.4f} ms\n")

    # ----------------------------------------------------
    print(">>> 2. 정방향 동기화 (두 번째 실행 - 동적 대치판 캐시 적중 O(1))")
    result2 = speed_calc(15000, 2)
    print(f" - 동적 시차 보정각: {result2['dynamic_phase_shift']:.6f} rad")
    print(f" - 추출된 기계어 장력: {result2['hw_rotor_final_tension']:.4f}")
    print(f" - 소요 시간 (Latency): {result2['exec_time_ms']:.4f} ms\n")

    # ----------------------------------------------------
    print(">>> 3. 역전환 관측 방어 (노이즈 유입 시 실시간 궤적 재배열)")
    set_hardware_rotor_frequency(hz_modifier=1.5)
    result3 = speed_calc(50000, 1) # 결과값 50000

    print(f" - 하드웨어 로터 간섭 주파수: {result3['detected_hw_interference']}")
    print(f" - 역전환 발생!: {result3['mode']} (AUTO-DEFENSE)")
    print(f" - 동적 시차 보정각: {result3['dynamic_phase_shift']:.6f} rad")
    print(f" - 재배열된 방어 장력: {result3['hw_rotor_final_tension']:.4f}")
    print(f" - 소요 시간 (Latency): {result3['exec_time_ms']:.4f} ms\n")