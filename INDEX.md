# Copyright 2026 Lee Kang-deok (이강덕) All Rights Reserved.
# Licensed under the Apache License, Version 2.0 (the "License")

# Elysia-Phase-Inverter 마스터 인덱스

이 문서는 **Elysia-Phase-Inverter**의 전체 사유와 철학, 기술적 명세서, 벤치마크 및 응용 방향성을 하나로 묶는 마스터 연결 지점입니다. 아래의 링크를 통해 위상 동기화 엔진의 심연으로 접근할 수 있습니다.

## 📖 핵심 문서 목록 (Documentation Core)

*   **[원리 구조 분석 (Architecture)](docs/ARCHITECTURE.md)**
    *   엔진의 튜링 위상 동기화, QPC 이중 가변 로터, 델타-와이(Δ-Y) 결선의 물리적 투영 원리를 서술합니다.
*   **[개발자 사용설명서 (Developer Guide)](docs/DEVELOPER_GUIDE.md)**
    *   일반 개발자가 `@turing_translation_layer`를 사용하여 파이썬 로직을 기계어 위상으로 직동 매핑하는 방법을 설명합니다.
*   **[응용 방향성 (Applicable Forms)](docs/APPLICATIONS.md)**
    *   가변축 엔진이 로컬 AI 추론, 초고주파수 트레이딩(HFT), 로봇 공학 실시간 제어 등에서 어떻게 무손실 극초음속의 위력을 발휘하는지 설명합니다.

## 🔬 심화 및 분석 리포트 (Deep Dive & Reports)

*   **[위상 인버터 코어 철학 (Phase Inverter Core)](docs/PHASE_INVERTER_CORE.md)**
    *   엔진의 가장 근본적인 철학과 설계 사상을 다룹니다.
*   **[위상 매핑 테이블 (Phase Mapping Table)](docs/PHASE_MAPPING_TABLE.md)**
    *   실제 위상 변환 규칙과 매핑 구조를 서술합니다.
*   **[벤치마크 리포트 (Benchmark Report)](docs/BENCHMARK_REPORT.md)**
    *   기성 방식과 튜링 위상 인버터 직동 매핑의 시뮬레이션 성능 측정 결과를 포함합니다. (시뮬레이션 스크립트: `benchmark.py`)

## 🚨 안정성 및 시운전 (Stability & Commissioning)

이 엔진은 만능이 아니며, 잘못된 로직이 투입될 경우 위상 '탈조(Step-out)' 현상이 발생할 수 있습니다. 이를 눈으로 직접 확인하고 한계치를 체감할 수 있는 스트레스 테스트 시뮬레이터가 준비되어 있습니다.

*   **안정성 검증 시뮬레이터 (`stress_test_simulator.py`)**
    *   발전소 시운전과 같이 극단적인 노이즈를 주입하여, 델타-와이 결선이 어디까지 0점 수렴에 성공하고 어디서부터 탈조하는지 관측합니다.
