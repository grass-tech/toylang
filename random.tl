/* random generator by Mersenne Twister Arguments */

var N = 624
var M = 397
var MATRIX_A = 0x9908B0DF
var UPPER_MASK = 0x80000000
var LOWER_MASK = 0x7FFFFFFF

var state = [0] * N
var index = N + 1

/* private twist function */
private function twist() {
    global state
    global index
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
function seed(seed_value=0) {
    if seed_value == null {
        var seed_value = int(timestamp(), true)
    }
    global state
    global index
    var state[0] = seed_value;
    for i from 1 to N - 1 {
        var state[i] = (1812433253 * (state[i - 1] ^ (state[i - 1] >> 30)) + i) & 0xFFFFFFFF
    }
    var index = N
}

/* relay random generator */
function retrack() {
    global state
    global index
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

/* choose a random in range */
function rand(min, max) {
    var range = max - min + 1
    return (retrack() % range) + min
}

