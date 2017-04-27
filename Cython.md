# Cython Note

* There's problem with Anaconda-python or python itself (not sure for now) when compiling cython code under Windows system with GCC compiler. If you're using one of GCC compilers, remember define `-DMS_WIN64=1` otherwise the compiled *.pyd will crash your python runtime. This bug has been there for quite a long long time, check the [issue](https://bugs.python.org/issue4709) 



