/* random generator by Mersenne Twister Algorithm */

var N = 624
var M = 397
var MATRIX_A = 0x9908B0DF
var UPPER_MASK = 0x80000000
var LOWER_MASK = 0x7FFFFFFF

var state = [0] * N
var index = N + 1

/* private twist function (Computing Core) */
private function twist() {
    for i from 0 to N - 1 {
        var x = (state[i] & UPPER_MASK) + (state[(i + 1) % N] & LOWER_MASK)
        var xA = x >> 1;
        if (x % 2 == 1) {
            var xA = xA ^ MATRIX_A;
        }
        var state[i] = state[(i + M) % N] ^ xA;
    }
    var index = 0;
}

/* seed generator */
private function seed(seed_value=0) {
    if seed_value == null {
        var seed_value = int(timestamp(), true)
    }
    var state[0] = seed_value;
    for i from 1 to N - 1 {
        var state[i] = (1812433253 * (state[i - 1] ^ (state[i - 1] >> 30)) + i) & 0xFFFFFFFF
    }
    var index = 0
}

/* relay random generator */
private function retrack() {
    seed()

    if index >= N {
        twist()
    }
    var y = state[index]
    var y = y ^  ((y >> 11) & 0xFFFFFFFF)
    var y = y ^ ((y << 7) & 0x9D2C5680)
    var y = y ^ ((y << 15) & 0xEFC60000)
    var y = y ^ (y >> 18)
    var index = index + 1
    return y & 0xFFFFFFFF
}

/* decimal random generator in range */
function uniform(a, b) {
    global state, index
    return a + (b - a) * (retrack() / 4294967295.0);
}

/* choose a random in range */
function rand(min, max) {
    global state, index
    var range = max - min + 1
    return (retrack() % range) + min
}
