from setuptools import find_packages, setup

package_name = 'facial_analysis_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='hoashal',
    maintainer_email='hoashal@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'camera_publisher = facial_analysis_pkg.camera_publisher:main',
            'expression_estimator = facial_analysis_pkg.expression_estimator:main',
            'expression_visualizer = facial_analysis_pkg.expression_visualizer:main'
        ],
    },
)
