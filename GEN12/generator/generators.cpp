#include <iostream>
#include <vector>
#include <stdint.h>
#include <fstream>
#include <chrono>

// Code to implemente Mersenne Twister, PCG  and LCG algorithms to generate
// random numbers9.

// Mersenne Twister generetor implementation can be found in:
//
// Wikipedia contributors. (2024, September 9). Mersenne Twister.
// In Wikipedia, The Free Encyclopedia. Retrieved 15:11, November 14, 2024,
// from https://en.wikipedia.org/w/index.php?title=Mersenne_Twister&oldid=1244854560
//

// PCG minimal implementation is obtained from the official website:
// https://www.pcg-random.org, retrieved 16:11, November 14, 2024
//

// Mersenne Twister
#define n 624
#define m 397
#define w 32
#define r 31
#define UMASK (0xffffffffUL << r)
#define LMASK (0xffffffffUL >> (w - r))
#define a 0x9908b0dfUL
#define u 11
#define s 7
#define t 15
#define l 18
#define b 0x9d2c5680UL
#define c 0xefc60000UL
#define f 1812433253UL

class MersenneTwister
{
public:
    MersenneTwister(uint32_t seed)
    {
        initialize_state(seed);
    }

    uint32_t random_uint32()
    {
        uint32_t *state_array = state_array_;
        int k = state_index_;
        int j = k - (n - 1);
        if (j < 0)
            j += n;

        uint32_t x = (state_array[k] & UMASK) | (state_array[j] & LMASK);
        uint32_t xA = x >> 1;
        if (x & 0x00000001UL)
            xA ^= a;

        j = k - (n - m);
        if (j < 0)
            j += n;

        x = state_array[j] ^ xA;
        state_array[k++] = x;
        if (k >= n)
            k = 0;
        state_index_ = k;

        uint32_t y = x ^ (x >> u);
        y ^= (y << s) & b;
        y ^= (y << t) & c;
        uint32_t z = y ^ (y >> l);

        return z;
    }

private:
    uint32_t state_array_[n];
    int state_index_;

    void initialize_state(uint32_t seed)
    {
        state_array_[0] = seed;
        for (int i = 1; i < n; i++)
        {
            seed = f * (seed ^ (seed >> (w - 2))) + i;
            state_array_[i] = seed;
        }
        state_index_ = 0;
    }
};

// PCG32
class PCG32
{
public:
    PCG32(uint64_t seed, uint64_t inc) : state(seed), inc(inc | 1) {}

    uint32_t random_uint32()
    {
        uint64_t oldstate = state;
        state = oldstate * 6364136223846793005ULL + inc;
        uint32_t xorshifted = ((oldstate >> 18u) ^ oldstate) >> 27u;
        uint32_t rot = oldstate >> 59u;
        return (xorshifted >> rot) | (xorshifted << ((-rot) & 31));
    }

private:
    uint64_t state;
    uint64_t inc;
};

// Linear Congruential Generator (LCG)
class LCG
{
public:
    LCG(uint32_t seed) : state(seed) {}

    uint32_t random_uint32()
    {
        state = (a_lcg * state + c_lcg) % m_lcg;
        return state;
    }

private:
    uint32_t state;
    static const uint32_t a_lcg = 1103515245;
    static const uint32_t c_lcg = 12345;
    static const uint32_t m_lcg = 1 << 31; // 2^31
};

// function to generate a .txt of *quantity* random numbers using MT, PCG or LCG algorithm

template <typename Generator>
double random_number_generator(Generator &generator, size_t quantity, const std::string &file_name)
{

    std::chrono::high_resolution_clock::time_point start = std::chrono::high_resolution_clock::now();

    std::ofstream file(file_name);
    if (!file.is_open())
    {
        std::cerr << "There was a mistake opening the file." << "\n";
        return 1;
    }

    for (size_t i = 0; i < quantity; i++)
    {
        file << generator.random_uint32() << "\n";
    }
    file.close();

    std::chrono::high_resolution_clock::time_point end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end - start;
    std::cout << "Generator: " << file_name << " took " << elapsed.count() * 1000 << " ms to generate " << quantity << " numbers\n";

    return elapsed.count() * 1000;
}

int main()
{
    size_t generations = 100;
    size_t quantity = 100000000;

    std::ofstream time_file("algorithm_times.txt");

    if (!time_file.is_open())
    {
        std::cerr << "There was a mistake opening the times file." << "\n";
        return 1;
    }

    time_file << "MT PCG32 LCG\n";

    for (size_t i = 0; i < generations; i++)
    {

        uint32_t base_seed = 12345; // Using the same base seed for better comparation

        MersenneTwister mt(base_seed);
        PCG32 pcg(static_cast<uint64_t>(base_seed), 1); // fixed increment for pcg
        LCG lcg(base_seed);

        // Separate files for each generator
        double mt_time = random_number_generator(mt, quantity, "mt_numbers.txt");
        double pcg_time = random_number_generator(pcg, quantity, "pcg_numbers.txt");
        double lcg_time = random_number_generator(lcg, quantity, "lcg_numbers.txt");

        time_file << mt_time << " " << pcg_time << " " << lcg_time << "\n";
    }

    std::cout << generations << " random number generations finished.\n";

    return 0;
}
