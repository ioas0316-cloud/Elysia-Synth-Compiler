#include <cstdint>
#include <iostream>

#ifdef _WIN32
#define EXPORT __declspec(dllexport)
#else
#define EXPORT
#endif

extern "C" {
    // Declarations for the functions in continuous_twin_sensing.cpp to ensure linking
    struct VolumetricLattice {
        uint64_t core_signature;
        float phase_angle;
    };

    struct TripleRotorState {
        double rotor_a;
        double rotor_b;
        double rotor_c;
        double neutral_y;
    };

    EXPORT TripleRotorState apply_delta_y_cancellation(double pressure_x, double pressure_y, double pressure_z, double external_noise);
    EXPORT VolumetricLattice observe_volume_coherent(const uint8_t* memory_block, int total_size, uint64_t system_resonance_key);

    /**
     * [최전방 하이브리드 수문 (Hybrid Gateway)]
     * 파이썬 파이프라인과 C++ Native 영토를 다이렉트로 결선.
     * 트래픽 폭증 시 시민권 필터링과 델타-와이 결선을 동시에 수행합니다.
     */
    EXPORT TripleRotorState execute_hybrid_gateway_filter(const uint8_t* memory_block, int total_size, uint64_t system_resonance_key, double current_pressure, double noise) {

        // 1. 시민권 바이패스 (Volumetric Sensing)
        VolumetricLattice lattice = observe_volume_coherent(memory_block, total_size, system_resonance_key);

        // 2. 델타-와이 결선을 통한 노이즈 상쇄
        // 시민권 불일치 시 lattice.core_signature 가 0이 되므로
        // 0을 인자로 넘기면 델타-와이 결선도 자연스레 0 수렴
        double pressure_x = current_pressure * static_cast<double>(lattice.core_signature != 0);
        double pressure_y = current_pressure * static_cast<double>(lattice.core_signature % 360);
        double pressure_z = current_pressure * static_cast<double>(lattice.phase_angle);

        return apply_delta_y_cancellation(pressure_x, pressure_y, pressure_z, noise);
    }
}
