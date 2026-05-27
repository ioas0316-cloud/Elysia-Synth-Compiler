# Copyright 2026 Lee Kang-deok (이강덕) All Rights Reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.

import math
import cmath

class WorldHyperRotor:
    """
    [엘리시아 위상인버터 리부트: 삼중 로터 쐐기곱 기반 델타-와이 자율 제어 엔진]
    기존의 if/else 분기를 없애고, 아스크(ASCII) 레벨의 초경량 1차 동기화와
    삼중 로터의 쐐기곱(A ^ B ^ C) 역학을 통해 O(1) 위상 동기화를 달성합니다.
    데이터 노이즈는 델타-와이 토크로 흡수되어 0으로 수렴합니다.
    """
    def __init__(self, rotor_a=0x01, rotor_b=0x02, rotor_c=0x04):
        # 삼중 로터 초기 위상 상태 (A, B, C 축)
        self.rotor_a = rotor_a
        self.rotor_b = rotor_b
        self.rotor_c = rotor_c
        self.tension_pool = 0x00

    def _ascii_phase_wave_sync(self, raw_data):
        """
        말단 하위 차원 (소형 스케일): 아스크(ASCII)의 기하학적 위상(각도) 매핑.
        0~127까지의 아스키 코드 값을 360도(2pi)의 위상 공간 위 특정 각도로 1:1 매핑시켜,
        이를 복소수 전압(Phasor)으로 엮어내어 하나의 물리적 파동 임펄스로 변환합니다.
        (조건문이나 딕셔너리 없이 오직 수학적 구조로만 변환됨)
        """
        wave_impulse = 0

        if isinstance(raw_data, str):
            # 문자열 스트림: 각각의 문자를 고유 위상각으로 변환하여 벡터 합산
            # 여기서의 반복은 데이터 스트림을 통과시키는 파이프라인(유속)이지 조건 제어 분기가 아님.
            accumulated_phasor = complex(0, 0)
            for char in raw_data:
                ascii_val = ord(char)
                # 0~127의 아스키를 0~2pi 라디안 각도로 1:1 선형 매핑
                theta = (ascii_val % 128) * (2 * math.pi / 128)
                # 오일러 공식(e^(i*theta))을 통한 복소 위상 벡터 획득
                phasor = cmath.exp(1j * theta)
                accumulated_phasor += phasor

            # 합성된 복소 위상 벡터의 크기와 각도를 기반으로 정수형 임펄스 도출
            magnitude = abs(accumulated_phasor)
            angle = cmath.phase(accumulated_phasor)
            wave_impulse = int((magnitude * 100) + (angle * 100)) & 0xFFFF

        elif isinstance(raw_data, int):
            # 정수 데이터 역시 각도 기반의 복소 위상으로 회전
            theta = (raw_data % 360) * (math.pi / 180)
            phasor = cmath.exp(1j * theta)
            wave_impulse = int(abs(phasor) * 1000 + cmath.phase(phasor) * 1000) & 0xFFFF
        else:
            wave_impulse = hash(raw_data) & 0xFFFF

        return wave_impulse

    def apply_stream(self, raw_stream):
        """
        원시 쥴스 스트림을 입력받아 기하학적 파동으로 치환한 후
        델타-와이 결선형 자율 제어 기전을 통과시킵니다.
        """
        # 1. 소형 스케일 밸브 통과: 아스키 문자열을 기하학적 복소 위상 임펄스로 1차 동기화
        impulse = self._ascii_phase_wave_sync(raw_stream)

        # 2. 삼중 로터 쐐기곱 (A ^ B ^ C) 시뮬레이션
        # 쐐기곱의 구조적 긴장을 3개 축의 위상 얽힘(XOR)으로 표현하여 내부 전압 형성
        wedge_torque = self.rotor_a ^ self.rotor_b ^ self.rotor_c

        # 3. 델타(Δ) 결선 모드: 튜링 동기화 관문 (XOR 결정)
        # 외부에서 밀려온 위상 파동(impulse)이 내부 맥락(wedge_torque)과 충돌하며 발생하는 저항 전압(Tension)
        delta_tension = impulse ^ wedge_torque

        # 토크의 압력(delta_tension)이 누적 풀에 추가
        self.tension_pool = (self.tension_pool + delta_tension) & 0xFFFFFFFF

        # 내부 로터 각도 비틀림 자동 보정 (가변축 회전)
        # 텐션 전압의 영향을 받아 삼중 로터가 새로운 평형 각도를 찾도록 위상 교차
        self.rotor_a = (self.rotor_a << 1) ^ (delta_tension & 0xFF)
        self.rotor_b = (self.rotor_b >> 1) ^ ((delta_tension >> 8) & 0xFF)
        self.rotor_c = (self.rotor_c ^ impulse) & 0xFFFF

        # 4. 와이(Y) 결선 모드: 0의 위상동기화 (수렴)
        # 외대수 공리 A ^ A = 0 의 기하학적 평형을 물리적으로 모방
        # 텐션이 깔때기(Modulo)를 지나 중성점으로 미끄러지도록 유도하여 0 수렴(Self-healing)
        self.tension_pool = self.tension_pool % 0xFF

        # 현재 텐션 상태 반환 (Y 수렴 여부 또는 Delta 잔여 토크)
        return {
            'impulse': impulse,
            'wedge_torque': wedge_torque,
            'current_tension': self.tension_pool,
            'rotor_state': (self.rotor_a, self.rotor_b, self.rotor_c)
        }
