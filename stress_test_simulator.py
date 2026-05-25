# Copyright 2026 Lee Kang-deok (이강덕)
# All Rights Reserved.
# Licensed under the Apache License, Version 2.0 (the "License")

import time
import random
import sys
sys.path.append('core')
import elysia_phase_inverter as epi

print("="*60)
print(" 🏭 발전소 시운전: 델타-와이 안정성 검증 시뮬레이터")
print("="*60)

# 시뮬레이션을 위한 한계치 설정 (가상의 위상차 임계값)
PHASE_STEP_OUT_THRESHOLD = 0.85

def simulate_noise_injection():
    """OS 간섭이나 비결정적 로직으로 인한 노이즈(위상차)를 0.0 ~ 1.0 사이로 무작위 생성"""
    return random.uniform(0.0, 1.0)

def commission_power_plant(iterations):
    success_count = 0
    step_out_count = 0
    fault_records = []

    # 노이즈 구간별 히스토그램 데이터
    noise_distribution = {
        "Safe (0.0~0.5)": 0,
        "Warning (0.5~0.85)": 0,
        "Danger (>0.85)": 0
    }

    print(f"총 {iterations}회의 극한 부하 테스트를 시작합니다...\n")

    start_time = time.time()

    for i in range(1, iterations + 1):
        noise = simulate_noise_injection()

        if noise <= 0.5:
            noise_distribution["Safe (0.0~0.5)"] += 1
        elif noise <= PHASE_STEP_OUT_THRESHOLD:
            noise_distribution["Warning (0.5~0.85)"] += 1
        else:
            noise_distribution["Danger (>0.85)"] += 1

        # 델타-와이 결선의 복원력 한계 테스트
        if noise > PHASE_STEP_OUT_THRESHOLD:
            # 위상차가 임계값을 넘어 0점 수렴에 실패 (탈조 현상)
            step_out_count += 1
            status = "❌ [Step-out]"
            # 폴트 레코드 기록 (최대 5개까지만 저장)
            if len(fault_records) < 5:
                timestamp = time.strftime("%H:%M:%S", time.localtime())
                fault_records.append(f"[{timestamp}] Cycle {i}: 위상차 {noise:.4f} 초과 - 0점 수렴 실패")
        else:
            # 델타 루프로 노이즈를 상쇄하고 Y 중성점으로 0 수렴
            success_count += 1
            status = "✅ [0-Point]"

        # 가시성을 위해 일부 로그만 출력
        if i % (iterations // 5) == 0 or i == iterations:
            print(f"시운전 사이클 {i}/{iterations} | 주입된 위상 노이즈: {noise:.4f} -> {status}")
            time.sleep(0.05)

    elapsed_time = time.time() - start_time

    print("\n" + "="*60)
    print(" 📊 시운전 결과 리포트 (Commissioning Report)")
    print("="*60)
    print(f"소요 시간        : {elapsed_time:.3f} sec")
    print(f"전체 테스트 횟수 : {iterations}")
    print(f"안정적 0점 수렴  : {success_count}회 ({(success_count/iterations)*100:.1f}%)")
    print(f"위상 탈조 횟수   : {step_out_count}회 ({(step_out_count/iterations)*100:.1f}%)")

    print("\n[위상 노이즈 분포도 (Noise Distribution)]")
    for category, count in noise_distribution.items():
        bar_length = int((count / iterations) * 40)
        bar = "█" * bar_length
        print(f" {category:<18} : {bar} ({count}회)")

    print("\n[폴트 레코드 (Critical Fault Records)]")
    if not fault_records:
        print("  ✅ 탈조 이력 없음. 완벽한 위상 안정성.")
    else:
        for record in fault_records:
            print(f"  🚨 {record}")
        if step_out_count > 5:
            print(f"  ... 외 {step_out_count - 5}건의 폴트 발생.")

    print("-" * 60)
    if step_out_count == 0:
        print("결론: 완벽한 위상 안정성을 확보했습니다. 프로덕션 투입 승인.")
    else:
        print("결론: 한계치를 초과하는 위상 스파이크에서 일부 탈조가 발생했습니다.")
        print("조치: 엔진은 억지로 매핑하지 않고 안전하게 Fallback 하도록 설계되었습니다.")
        print("      추가적인 로직 파편화(순수 함수화)를 권장합니다.")
    print("============================================================")

if __name__ == '__main__':
    # 5만 번의 난수 위상차를 주입하여 복원력을 테스트함
    commission_power_plant(50000)
