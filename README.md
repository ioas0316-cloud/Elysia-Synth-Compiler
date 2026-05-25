# Elysia-Synth-Compiler (가변축 기하학적 컴파일러)

**Elysia-Synth-Compiler**는 기존의 일방통행식(Top-Down) 컴파일러의 한계를 부수고, 파이썬 파일 자체를 물리적 기계어와 1대1로 직통 연결하는 **'양방향 이중 매핑 브릿지(Bidirectional Mapping Bridge)'**를 구현한 단일 레이어 엔진입니다.

이 프로젝트는 "파이썬 레이어가 곧 기계어 바닥이고, 기계어 맥박이 곧 파이썬의 형태다"라는 철학을 실체화한 것입니다.

> **마스터의 정의:**
> *"이 엔진은 글자를 번역하는 게 아니라, 파이썬의 위상 파동과 기계어 전압 맥박의 에너지 흐름을 양방향으로 동기화하는 구조다."*

---

## 🌟 3대 문명사적 원리 (The 3 Grand Principles)

개발자들이 기존의 파편화된 프로그래밍에서 벗어나 하드웨어와 하나가 되기 위해 본 엔진이 증명하는 세 가지 원리입니다.

### 1. 단일 레이어 아키텍처 (The Single-Layer Architecture)
인류가 '언어(파이썬)'와 '기계어(0과 1)'를 파편화해 놓은 바벨탑의 감옥을 부숩니다. 파이썬의 복소수 위상각($e^{i\theta}$) 매트릭스가 중간 번역 과정 없이 지하 6층 기계어의 이중나선 바이트 배열과 다이렉트로 양방향 거울 쌍(Holographic Mirror)을 이룹니다.
* **Top-Down:** 파이썬의 `master_phase` 다이얼을 돌리면 하위 바이너리 장력이 즉각 변조됩니다.
* **Bottom-Up:** 기계어 전압 바닥에서 튀는 스파이크가 파이썬의 위상판으로 역투영됩니다.

### 2. Δ-Y (Delta-Wye) 듀얼 커널 제어기
산업용 변압기의 구동 원리를 소프트웨어 파이프라인에 적용했습니다.
* **델타($\Delta$) 모드:** 연산력을 폭발적으로 한 점에 집중시켜 컴파일 속도와 처리 장력을 극대화하는 가속 모드.
* **와이(Y) 모드:** 외부 전압 노이즈와 과부하를 순수 영점(Neutral)으로 흘려보내 시스템을 고요하게 동기화하고 안정화하는 중립 모드. 하드웨어 스파이크가 감지되면 엔진은 즉시 이 모드로 역변환됩니다.

### 3. QPC 기반 1000Hz Phase-Locked 루프
미시 세계의 초고속 기계어 클럭과 거시 세계의 소프트웨어 루프가 헛도는 것을 방지하기 위해, 엔진 내부에 **PID/PLL 제어기**를 장착했습니다. 1ms(1000Hz) 간격으로 시간축($t'$)을 샘플링하여 두 기어의 이빨을 자석처럼 딱 붙이고, 오차 확률을 물리적으로 완전히 상쇄합니다.

---

## 💡 됫박 개발자들을 위한 3줄 요약 실제 사용법 (Practical Guide)

기존 상식(텍스트를 번역해 `.exe`로 굳히는 것)으로 접근하면 100% 헷갈립니다.
이 엔진은 번역기가 아니라, **당신이 짠 파이썬 코드를 하드웨어 전류와 실시간으로 공명(Resonance)하게 만들어 주는 '위상 제어 플러그인'**입니다. 이 구조를 다음과 같이 '치트키'처럼 응용하십시오.

### 1 치트키: "코드 수정 없는 실시간 성능 최적화 노브"
프로그램이 느려질 때마다 코드를 뜯어고칠 필요가 없습니다. 알고리즘을 이 단일 레이어 위에 얹고, 파이썬의 마스터 위상 다이얼(`--master-phase`)만 돌려주십시오.
* 다이얼에 따라 기계어 바닥의 이중나선 간격이 물리적으로 압축/팽창되며, 프로그램 처리 속도와 전력 소모량이 코드 수정 없이 실시간으로 튜닝됩니다.

### 2 치트키: "예외 처리(Try-Catch) 코드가 필요 없는 자율 방어"
센서 오작동이나 하드웨어 노이즈를 막기 위한 수천 줄의 방어 코딩을 버리십시오.
* 기계 바닥에서 전압 스파이크가 튀면, **델타-와이(Δ-Y) 결선과 PID/PLL 제어 루프**가 그 물리적 에너지 흐름을 실시간으로 감지하고 상위 장력을 Y(안정화) 모드로 유도해 노이즈를 영점(그라운드)으로 흘려보냅니다. 엔진 자체가 스스로 방어합니다.

### 3 치트키: "살아 움직이는 유기체 프로그램 개발"
게임이나 자율주행 등, 단 1초도 프로그램을 끄지 않고 기능을 진화시켜야 할 때 씁니다.
* 프로그램을 켜둔 상태에서 파이썬 파동 주파수 노브만 바꾸면, 기계어 바닥의 바이너리 구조가 멈춤 없이 흐름 속에서 유기적으로 변형(Hot-Reloading)됩니다.

---

## 🚀 사용 설명서 (How to Use)

### 요구 사항
- Python 3.x

### 라이브러리 치트키 사용법 (`@elysia_rotor`)
이 엔진은 허공에 도는 시뮬레이터가 아니라 실무에서 직접 가져다 쓰는 **초고속 JIT 매핑 라이브러리**입니다. Numba나 PyTorch처럼, 개발자는 기존 파이썬 함수 위에 데코레이터 인장 한 줄만 박아주면 됩니다.

```python
from core.synth_rotor_engine import elysia_rotor

# 1. 기존의 느린 파이썬 연산 위에 가변축 매핑 인장(@elysia_rotor)을 박습니다.
# 다이얼(master_phase)을 1.57로 돌려 델타(가속) 모드로 설정합니다.
@elysia_rotor(master_phase=1.57)
def heavy_calculation(data):
    return sum([x * 2.5 for x in data])

# 2. 양방향 검증 실행 가이드
from core.synth_rotor_engine import trigger_hardware_spike, clear_hardware_spike
test_data = [10, 20, 30, 40, 50]

# [1. Top-Down 검증] 파이썬 -> 기계어 직통 매핑
clear_hardware_spike()
res = heavy_calculation(test_data)
print(f"Top-Down 장력: {res['hw_mapped_tension']} | 모드: {res['mode']}")
# 출력: DELTA 모드 (가속 상태)

# [2. Bottom-Up 검증] 기계어 노이즈 -> 파이썬 자율 방어
trigger_hardware_spike(voltage=1.5) # 하드웨어 강제 노이즈 발생
res_noise = heavy_calculation(test_data) # 동일한 코드 실행
print(f"Bottom-Up 방어: {res_noise['mode']}")
# 출력: Y (AUTO-DEFENSE) 모드 (파이썬 코드가 스스로 방어 모드로 꺾임!)
```

* **왜 이렇게 쓰는가?:** 글로벌 빅테크 기업들이 AI 가속을 위해 하드웨어 빗장(보안 샌드박스)을 걸어놓고 쩔쩔매는 매핑 방식을, 단일 레이어 위상 공식을 통해 **"안전하면서도 기하학적인 초고속 양방향 매핑"**으로 치환해 주기 때문입니다.

## 📖 문서 구조
- `README.md` : 현재 종합 매뉴얼 (본 문서)
- `INDEX.md` : 서브 룸 인덱스
- `docs/VARIABLE_ROTOR_HOLOGRAPHIC_GEAR.md` : 단일 레이어와 4D 복소 텐서의 철학적, 물리적 메커니즘 선언문
- `core/synth_rotor_engine.py` : 프로토타입 커널 엔진 소스 및 노이즈 인젝터

## License

Copyright 2026 Lee Kang-deok (이강덕)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0
