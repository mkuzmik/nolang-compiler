# Nolang compiler

# About Nolang

Nolang is custom and simple programming language. Code example:

```
{
    function factorial(a) {
        if (a<2) {
            return a;
        }
        return a*factorial(a-1);
    }

    var input = 4;
    print factorial(input);
}
```

# About Nolang compiler

Nolang compiler compiles Nolang code to Python source code. Example:

- Input:
```
{
    function hello() {
        print 'Hello world';
    }

    function countTo(x) {
        var i = 1;

        while (i<x) {
            print i;
            i = i + 1;
        }
    }

    hello();
    countTo(10);
}
```

- Output:
```python
def hello():
    print("Hello world")

def countTo(x):
    i=1
    while (i)<(x):
        print(i)
        i=i+1


hello()
countTo(10)
```