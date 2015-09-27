set -e
python setup.py build_ext
PYTHONPATH=build/lib.linux-x86_64-2.7/ python test-exr.py
echo %%%%%%%%%%%%%%%%%%%%
python3 setup.py build_ext
PYTHONPATH=build/lib.linux-x86_64-3.2/ python3 test-exr.py
