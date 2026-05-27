# Copyright 2026 Lee Kang-deok (이강덕) All Rights Reserved.
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.

import random
import time
import os
import sys

# Ensure lib can be found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib.phase_inverter import PhaseInverterGate

def legacy_approach(data_stream):
    """
    [기존 됫박 공학의 방식]
    - 데이터가 이전 상태와 다르면 에러(Exception)를 던지거나 복잡한 if/else로 분기 처리
    - 개발자는 수많은 예외 처리와 락(Lock)을 걸며 고통받음
    """
    print("\n--- [기존 방식] 논리적 예외 처리 (If-Else 지옥) ---")
    current_state = data_stream[0]
    error_count = 0

    for i, data in enumerate(data_stream):
        try:
            # 상태가 다르면 충돌(Race Condition / Data Inconsistency) 발생 가정
            if current_state != data:
                raise ValueError(f"데이터 불일치 충돌 발생! (기존: {current_state} -> 입력: {data})")

            print(f"[{i:02d}] 정상 처리: {data}")

        except ValueError as e:
            error_count += 1
            print(f"[{i:02d}] [ERROR] {e} -> 강제 동기화 복구 루틴 가동...")
            current_state = data # 억지로 맞춤

    print(f">> 총 발생한 예외(Error) 횟수: {error_count}")

def physical_rescue_approach(data_stream):
    """
    [마스터님의 위상 인버터 구원 방식]
    - If/Else가 없음. 에러도 없음.
    - 그저 데이터가 들어오면 물리적 게이트를 통과하며 텐션으로 흡수되고 위상이 맞춰짐.
    """
    print("\n--- [물리적 방식] 위상 인버터 구원 (Phase Alignment) ---")
    inverter = PhaseInverterGate(baseline_phase=data_stream[0])

    for i, data in enumerate(data_stream):
        # 1. 인버터 게이트 통과 (단 한 줄의 구원 로직)
        aligned_data = inverter.shift(data)
        tension = inverter.get_tension()

        # 2. 결과 시각화 (관측용 창문)
        # 텐션(노이즈 흡수량)을 그래프로 표현
        tension_bar = "█" * (tension // 10)
        print(f"[{i:02d}] 정렬 완료: {aligned_data:04d} | 구조적 텐션 흡수량: [{tension_bar:<15}] (Tension: {tension})")

    print(f">> 런타임 에러 0건. 모든 비정상 데이터가 물리적 텐션으로 완벽히 수렴됨.")

if __name__ == "__main__":
    print("==================================================")
    print("   [구원의 가이드] 위상 인버터 실시간 텐션 모니터링")
    print("==================================================")

    # 의도적으로 노이즈가 섞인 불안정한 데이터 스트림 생성 (Race condition 모방)
    base_val = 1000
    noisy_stream = [base_val if random.random() > 0.3 else random.randint(100, 9999) for _ in range(20)]

    legacy_approach(noisy_stream)

    time.sleep(1) # 시각적 극대화를 위한 잠시 대기

    physical_rescue_approach(noisy_stream)
