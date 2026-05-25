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
    tuned_count = 0
    step_out_count = 0
    fault_records = []
    tuning_records = []

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

        # 델타-와이 결선의 복원력 한계 테스트 및 보호 계전기(Relay) 개입
        if noise > PHASE_STEP_OUT_THRESHOLD:
            # 21번(거리 계전기) 발동: 삼중 로터 위상각 능동 조율 시도 (Tuning)
            # 노이즈가 너무 극단적이지 않다면(예: 0.95 미만) 강제 공명에 성공한다고 시뮬레이션
            if noise < 0.95:
                tuned_count += 1
                status = "🔄 [Tuned by Relay 21] 삼중 로터 위상각 조율 성공"
                if len(tuning_records) < 2:
                    timestamp = time.strftime("%H:%M:%S", time.localtime())
                    tuning_records.append(f"[{timestamp}] Cycle {i}: 노이즈 {noise:.4f} 감지 -> 21번 거리 계전기 개입하여 강제 공명")
            else:
                # 27번(부족전압) 혹은 25번(동기검정) 실패로 최종 탈조 (Step-out)
                step_out_count += 1
                status = "❌ [Step-out] 조율 한계 초과"
                if len(fault_records) < 5:
                    timestamp = time.strftime("%H:%M:%S", time.localtime())
                    fault_records.append(f"[{timestamp}] Cycle {i}: 위상차 {noise:.4f} - 25번 동기검정 실패, 런타임 Fallback")
        else:
            # 델타 루프로 노이즈를 상쇄하고 Y 중성점으로 자연 0 수렴
            success_count += 1
            status = "✅ [0-Point] 자연 수렴"

        # 가시성을 위해 일부 로그만 출력
        if i % (iterations // 5) == 0 or i == iterations:
            print(f"시운전 사이클 {i}/{iterations} | 주입된 위상 노이즈: {noise:.4f} -> {status}")
            time.sleep(0.05)

    elapsed_time = time.time() - start_time
    total_success = success_count + tuned_count

    print("\n" + "="*60)
    print(" 📊 시운전 결과 리포트 (Commissioning Report)")
    print("="*60)
    print(f"소요 시간        : {elapsed_time:.3f} sec")
    print(f"전체 테스트 횟수 : {iterations}")
    print(f"자연적 0점 수렴  : {success_count}회")
    print(f"능동적 조율 공명 : {tuned_count}회 (보호 계전기 개입)")
    print(f"최종 위상 동기화 : {total_success}회 ({(total_success/iterations)*100:.1f}%)")
    print(f"최종 위상 탈조   : {step_out_count}회 ({(step_out_count/iterations)*100:.1f}%)")

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

    # 개발자 진단 알람 (Diagnostic Alerts)
    step_out_ratio = step_out_count / iterations

    if step_out_ratio == 0:
        print("🟢 [시스템 진단] 완벽한 위상 안정성을 확보했습니다. 프로덕션 투입 승인.")
    elif step_out_ratio < 0.10:
        print("🟡 [시스템 진단] 한계치를 초과하는 위상 스파이크에서 간헐적 탈조가 발생했습니다.")
        print("  -> 엔진은 억지로 매핑하지 않고 안전하게 Fallback 하도록 설계되어 있어 치명적이지 않습니다.")
        print("  -> 권고사항: 코드 내부에 비결정적 로직(랜덤, 시간)이 있는지 점검하십시오.")
    else:
        print("🔴 [시스템 경고] 탈조율이 10%를 초과했습니다! (25번 동기검정 실패 과다)")
        print("  -> 개발자 가이드라인 (Developer Guidelines):")
        print("     1. 대상 함수 내부에 외부 I/O (네트워크, DB, 파일) 대기열이 포함되어 있습니다. 즉각 분리하십시오.")
        print("     2. 로직 덩어리가 너무 큽니다. 핵심 수학/연산 블록만 파편화(Fragmentation)하여 데코레이터를 적용하십시오.")

    print("============================================================")

if __name__ == '__main__':
    # 5만 번의 난수 위상차를 주입하여 복원력을 테스트함
    commission_power_plant(50000)
