import setuptools

setuptools.setup(
    name="pytest-notifier",
    version="0.3",
    url="https://github.com/ratson/pytest-notifier",

    author="Ratson",
    author_email="contact@ratson.name",

    description="A pytest plugin to notify test result",
    long_description=open('README.rst').read(),
    keywords=[
        'pytest', 'pytest-', 'osx', 'linux', 'notifications', 'notifier',
        'notificationcenter', 'py.test', 'terminal-notifier', 'libnotify'],

    packages=setuptools.find_packages(),

    install_requires=['pytest'],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    entry_points={
        'pytest11': [
            'notifier = pytest_notifier',
        ],
    },
)
