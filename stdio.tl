/* 多个函数包文件 */

function fib(n) {
    var result = [];
    function factor(i) {
        if i < 2 {
            return 1;
        } else {
            return factor(i - 2) + factor(i - 1)
        }
    }

    for x from 0 to n {
        var result = result + factor(x);
    }
    return result
}
