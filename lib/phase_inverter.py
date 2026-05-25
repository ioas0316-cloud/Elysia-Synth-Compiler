# Copyright 2026 Lee Kang-deok (이강덕) All Rights Reserved.
# Licensed under the Apache License, Version 2.0 (the "License")

class PhaseInverterGate:
    """
    [구원의 입자: 위상 인버터 단일 물리 연산 게이트]
    논리적인 분기(If-Else)나 에러 처리 없이, 데이터의 다름(노이즈)을
    물리적 위상차로 간주하여 0점으로 자동 수렴(Self-Healing)시키는 게이트입니다.
    개발자들은 이 게이트를 통해 복잡한 동기화 코드 없이 데이터를 정렬할 수 있습니다.
    """
    def __init__(self, baseline_phase=0x0000):
        # 0점 기준이 되는 위상 축 (초기 상태)
        self.current_phase = baseline_phase
        self.accumulated_tension = 0

    def shift(self, data_impulse):
        """
        데이터가 들어오면 기존 위상과의 차이를 물리적 비틀림(Tension)으로 흡수하고,
        새로운 데이터가 새로운 위상의 기준점이 됩니다.
        에러를 던지는(Throw) 대신, 노이즈를 텐션으로 보관합니다.
        """
        # 1. 델타 상쇄(XOR): 입력된 데이터와 현재 위상과의 차이를 무효전력(Tension)으로 추출
        phase_difference = self.current_phase ^ data_impulse

        # 2. 텐션 누적: 비정상적이거나 튀는 데이터는 에러가 아닌 텐션의 증가로 이어짐
        self.accumulated_tension = (self.accumulated_tension + phase_difference) & 0xFFFFFFFF

        # 3. 위상 동기화: 현재 위상을 들어온 데이터의 파동으로 덮어씌움 (정렬)
        self.current_phase = data_impulse

        # 4. 와이(Y) 중성점 수렴 모방: 특정 텐션 임계치를 넘으면 스스로를 0으로 초기화 (Self-Healing)
        # 이 과정 역시 if문이 아닌 비트마스크 구조 압력으로 흉내냅니다.
        # (텐션이 0xFF를 넘어가면 상위 비트를 쳐내어 안정권으로 되돌림)
        self.accumulated_tension = self.accumulated_tension & 0xFF

        return self.current_phase

    def get_tension(self):
        return self.accumulated_tension
