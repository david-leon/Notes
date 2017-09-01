# Cython Note

* There's problem with Anaconda-python or python itself (not sure for now) when compiling cython code under Windows system with GCC compiler. If you're using one of GCC compilers, remember define `-DMS_WIN64=1` otherwise the compiled *.pyd will crash your python runtime. This bug has been there for quite a long time, check the [issue](https://bugs.python.org/issue4709) 

* You can specify which compiler to use by cmdline parameter `--compiler` as `python setup.py build_ext --inplace --compiler msvc`.
* When using MSVC as compiler, you may encounter a LINK error:
```
LINK : fatal error LNK1158: cannot run 'rc.exe'
```
As [stackoverflow disscussion](https://stackoverflow.com/questions/14372706/visual-studio-cant-build-due-to-rc-exe), you'll need find a proper version `rc.exe` and corresponding `rcdll.dll` and copy them into the MSVC compiler folder. Then it'll compile without any problem.


