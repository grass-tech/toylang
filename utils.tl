/* Multiple Function Package File */

/* fibonacci with factorial*/
function factorial_fib(n) {
    var result = [];
    function factor(i) {
        if i < 2 {
            return 1;
        } else {
            return factor(i - 2) + factor(i - 1);
        }
    }

    for x from 0 to n {
        var result = result + factor(x);
    }
    return result
}

/* fibonacci with Repeat */
function repeat_fib(n) {
    var result = [];
    for i from 0 to n {
        if i <= 1 {
            var result = result + [1];
        } else {
            var result = result + (result[i-2] + result[i-1]);
        }
    }
    return result;
}

/* mapping function */
function map(func, ld) {
    var result = [];
    for x from 0 to length(ld) - 1 {
        var result = result + func(ld[x]);
    }
    return result;
}

/* access array element(s) */
function access(ld, i) {
    return ld[i];
}