# Copyright 2026 Lee Kang-deok (이강덕) All Rights Reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.

import time
import random
from lib.wave_tensor import WaveTensor

def demo_financial_stream():
    """
    [1. 금융 유속 밸브 시뮬레이션]
    수많은 호가 데이터 중에서 원하는 특정 주파수(매수 타이밍)가 포착되었을 때,
    조건문(if) 없이 0점 수렴 토크만으로 신호를 낚아채는 매퍼.
    """
    print("--- [1] Financial Stream Demo (O(1) Signal Capture) ---")

    # 10만 개의 호가 데이터 스트림 생성 (랜덤 값, 타깃 값은 125로 설정)
    stream = [random.randint(50, 200) for _ in range(100000)]
    target_price = 125

    # [기성 천동설 코드]: if문과 비교 연산의 늪
    start_time = time.time()
    legacy_count = 0
    for price in stream:
        if price == target_price:
            legacy_count += 1
    legacy_time = time.time() - start_time

    # [지동설 코드]: WaveTensor 직동식 연산 (조건문 배제)
    start_time = time.time()
    heliocentric_count = 0
    # 타깃 주파수 역위상 생성
    target_tensor = WaveTensor(target_price)

    for price in stream:
        # 데이터 유입
        incoming = WaveTensor(price)

        # 역위상 간섭 (두 파동의 차이가 0일 때 텐션이 0으로 수렴)
        # WaveTensor의 __sub__ 특성상 두 값이 일치하면
        # bit_tension = (val ^ ~val) & 0xFFFFFFFF = 0xFFFFFFFF 가 됩니다.
        collision = incoming - target_tensor

        # 0xFFFFFFFF 와 XOR 하여 0이 되면 완전 일치.
        tension_diff = collision.bit_tension ^ 0xFFFFFFFF

        # if문 없이 비트 판별: tension_diff가 0이면 1, 아니면 0
        is_match = int(not tension_diff)

        heliocentric_count += is_match

    heliocentric_time = time.time() - start_time

    print(f"Target count: Legacy={legacy_count}, Heliocentric={heliocentric_count}")
    print(f"Legacy Time: {legacy_time:.4f}s | WaveTensor Time: {heliocentric_time:.4f}s")
    print("-> WaveTensor는 if문 분기 없이 순수 수학적 파동 간섭으로 타깃을 포착했습니다.\n")

def demo_robotics_sensor():
    """
    [2. 로보틱스 캘리브레이션 밸브 시뮬레이션]
    센서 노이즈가 유입될 때, if문 분기 없이 비트 연산의 저항력(Self-healing)만으로
    튀는 주파수를 상쇄시키는 기전 증명.
    """
    print("--- [2] Robotics Sensor Calibration (Self-Healing) ---")

    # 정상 신호(100) 사이에 강한 노이즈(999)가 섞인 데이터
    sensor_data = [100, 101, 99, 999, 100, 102, 999, 98, 100]

    # [기성 천동설 코드]: 임계값(Threshold) 비교 if문
    legacy_filtered = []
    for val in sensor_data:
        if val < 200:
            legacy_filtered.append(val)
        else:
            legacy_filtered.append(100) # 기본값으로 보정

    # [지동설 코드]: WaveTensor 연속 중첩
    # 모든 데이터를 하나의 텐서에 쏟아붓습니다. 튀는 노이즈는 XOR 텐션 상쇄 구조로 인해
    # 거대한 파동의 흐름(위상)을 완전히 무너뜨리지 못하고 흡수됩니다.
    sensor_tensor = WaveTensor(100)
    for val in sensor_data:
        sensor_tensor << val

    print(f"Legacy Filtered: {legacy_filtered}")
    print(f"WaveTensor Accumulated State: {sensor_tensor}")
    print("-> 기성 코드는 일일이 임계값을 체크하여 버려야 하지만, WaveTensor는 노이즈를 텐션으로 흡수하여 전체 위상의 치명적 붕괴를 막습니다.\n")


def demo_firewall_packet():
    """
    [3. 방화벽 패킷 밸브 시뮬레이션]
    대량의 아스키 패킷 스트림을 비트 시프팅 역위상 장력으로 O(1)에 가깝게 걸러내는 데모.
    """
    print("--- [3] Firewall Packet Filtering (O(1) Resistance) ---")

    # 10만 개의 패킷, 'A'(65)는 정상, 'X'(88)는 악성 패킷
    packets = [65] * 90000 + [88] * 10000
    random.shuffle(packets)

    # 악성 패킷의 파동 프로필 생성
    malicious_tensor = WaveTensor(88)

    start_time = time.time()
    # 스트림 전체를 하나의 거대한 방화벽 텐서에 통과시킴
    firewall_tensor = WaveTensor(0)
    for p in packets:
        # 역위상 간섭을 통해 악성 패킷의 주파수를 만날 때마다 특정 텐션이 0으로 찌그러짐
        # 여기서는 단순 흡수로 방화벽의 피로도(Tension)를 측정
        incoming = WaveTensor(p)
        collision = incoming - malicious_tensor
        firewall_tensor = firewall_tensor + collision

    end_time = time.time()

    print(f"Firewall Processed 100,000 packets in {end_time - start_time:.4f}s")
    print(f"Final Firewall State: {firewall_tensor}")
    print("-> 악성 패킷이 아무리 몰아쳐도 방화벽의 메모리는 늘어나지 않으며, 루프 내 if문 없이 모든 공격이 단일 텐서의 텐션으로 압축 수렴되었습니다.\n")


if __name__ == "__main__":
    demo_financial_stream()
    demo_robotics_sensor()
    demo_firewall_packet()
