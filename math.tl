/* Standard Math Libray */

var pi = 3.141592653589793
var e = 2.718281828459045
var tau = 6.283185307179586

function pow(n, p) {
    return int(n) ** int(p);
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
        return 0-n;
    } else {
        return n;
    }
}
