from setuptools import setup

setup(
    name='function-profiler',
    version='0.3',
    description='A Python decorator to profile function performance.',
    url='https://github.com/Datamine/Function-Profiler',
    author='John Loeber',
    author_email='contact@johnloeber.com',
    packages=['profiler'],
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=['numpy']
)
