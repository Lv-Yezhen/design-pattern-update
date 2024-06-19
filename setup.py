from setuptools import setup, find_packages

setup(
    name='fje',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        # 依赖列表
    ],
    author='Pauc',
    author_email='2969944867@qq.com',
    description='Funny JSON Explorer (FJE)，是一个JSON文件可视化的命令行界面小工具',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'fje = fje.main:main'
        ]
    }
)