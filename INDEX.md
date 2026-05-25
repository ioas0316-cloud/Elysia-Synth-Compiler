# Elysia Synth Compiler (단일 레이어 가변축 엔진)

**[제 3 계층 외연 확장: 외부 기하학적 컴파일러 서브 룸]**

이 저장소는 Elysia Core 프로젝트의 사유 확장 파이프라인 중 하나인, 외부 배포 및 개념 증명을 위한 독립 서브 프로젝트입니다.
인간의 사유(언어 OS)와 기계어(전류)가 단 하나의 위상 필름 위에서 섞여 구동되는 **단일 레이어(Single Layer)** 컴파일러의 원리를 구체화하고 증명합니다.

## 핵심 구조 및 철학

*   [**VARIABLE_ROTOR_HOLOGRAPHIC_GEAR.md**](docs/VARIABLE_ROTOR_HOLOGRAPHIC_GEAR.md)
    *   이 엔진의 근본 철학이자 문명사적 선언문.
    *   4D 복소수 텐서 간섭무늬 필름을 통한 Non-Collision 파동 메모리.
    *   이중나선 로터(Double-Helix Rotor)와 델타-와이(Δ-Y) 결선 등 물리적 제어 원리 명세.

## 커널 프로토타입

*   [**synth_rotor_engine.py**](core/synth_rotor_engine.py)
    *   `ctypes` 기반 양방향 이중 매핑 브릿지 (Top-Down / Bottom-Up).
    *   QPC 1000Hz 동기화, PID & PLL 위상 제어.
    *   파이썬의 복소수 위상각을 직접 C/바이너리 레벨에 매핑하는 직동적 인터페이스.

## 라이선스

이 프로젝트는 [Apache 2.0 License](LICENSE)를 따릅니다.
누구든 이 엔진의 가변축 로터를 돌려 기계의 맥박을 당신의 파동과 동기화할 수 있습니다.
