function fib(n) {
    function fn(i) {
        if i < 2 {
            return 1
        } else {
            return fn(i - 2) + fn(i - 1)
        }
    };
    for x from 0 to n {
        println(fn(x))
    }
}

fib(int(readline('type maximum fibonachi: ')))