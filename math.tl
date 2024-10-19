/* Standard Math Libray */

/* Some normal constants */
var pi = 3.141592653589793
var e = 2.718281828459045
var tau = 6.283185307179586

/* Power */
function pow(n, p) {
    return n ** p;
}

/* Absolute value */
function abs(n) {
    if n < 0 {
        return -n;
    } else {
        return n;
    }
}

/* factorial */
function factorial(n) {
    var result = 1;
    for x from 1 to n {
        var result = result * x;
    }
    return result;
}

/* Special factorial to compute trigonometric functions */
private function _factorial(n) {
    if n == 0 or n == 1 {
        return 1;
    }
    var result = 1;
    for x from 2 to n {
        var result = result * x;
    }
    return result
}

/* Square root */
function sqrt(n) {
    return n ** 0.5;
}

/* Trigonometric 'cos' by Taylor series */
function cos(n, terms = 10) {
    var result = 0;
    for x from 0 to terms - 1 {
        var term = ((-1) ** x) * (n ** (2 * x)) / _factorial(2 * x);
        var result = result + term;
    }
    return result;
}

/* Trigonometric 'sin' by Taylor series */
function sin(n, terms = 10) {
    var result = 0;
    for x from 0 to terms - 1 {
        var term = ((-1) ** x) * (n ** (2 * x + 1)) / _factorial(2 * x + 1);
        var result = result + term;
    }
    return result;
}

/* Test each math function 'test' */
function test() {
    var result = [];
    var result = result + pow(2, 2);
    var result = result + factorial(5);
    var result = result + abs(5);
    var result = result + abs(-5)
    println(['math.pow(2, 2)', 'math.factorial(5)', 'math.abs(5)', 'math.abs(-5)']);
    println(result)
    var result = [];
    var result = result + cos(pi / 2);
    var result = result + sin(pi / 2);
    println(['math.cos(pi / 2)', 'math.sin(pi / 2)']);
    println(result)

    println('Function end successfully')

    return null;
}

