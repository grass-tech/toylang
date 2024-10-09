/* Standard Math Libray */

var pi = 3.141592653589793
var e = 2.718281828459045
var tau = 6.283185307179586

function pow(n, p) {
    return n ** p;
}

function factorial(n) {
    var result = 1;
    for x from 1 to n {
        var result = result * x;
    }
    return result;
}

function abs(n) {
    if n < 0 {
        return -n;
    } else {
        return n;
    }
}

function test() {
    var result = [];
    var result = result + pow(2, 2);
    var result = result + pow(2, 3)
    var result = result + factorial(5);
    var result = result + factorial(3);
    var result = result + abs(5);
    var result = result + abs(-5)
    println(['math.pow(2, 2)', 'math.pow(2, 3)', 'math.factorial(5)', 'math.abs(5)', 'math.pow(2, 3)', 'math.factorial(3)', 'math.abs(-5)']);
    return result;
}

