rm -rf dist/
rm -rf src/coyote.egg-info/
mkdir dist/
python setup.py sdist bdist_wheel

