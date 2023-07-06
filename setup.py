import re

from setuptools import setup


version = ''
with open('docx/__init__.py', 'r') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)  # type: ignore # never None
if not version:
    raise RuntimeError('version is not set')
if version.endswith(('a', 'b', 'rc')):
    # append version identifier based on commit count
    try:
        import subprocess

        p = subprocess.Popen(['git', 'rev-list', '--count', 'HEAD'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if out:
            version += out.decode('utf-8').strip()
        p = subprocess.Popen(['git', 'rev-parse', '--short', 'HEAD'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if out:
            version += '+g' + out.decode('utf-8').strip()
    except Exception:
        pass


readme = ''
with open('README.md', 'r') as f:
    readme = f.read()


packages = ['docx']

install_requires = ['lxml>=4.9.2,<5.0.0']

extras_require = {
    'dev': [
        'black==23.3.0',
        'ipython==8.14.0 ; python_version >= "3.9"',
        'isort==5.12.0',
        'types-lxml',
        'typing-extensions==4.7.1',
    ]
}

setup(
    name='replace-docx',
    version=version,
    description='Simple utility to replace text in docx files.',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='lmaotrigine',
    author_email='varun.j@krtrimaiq.ai',
    url='https://github.com/KrtrimaIQ-Cognitive-Solutions/replace-docx-pdf',
    packages=packages,
    install_requires=install_requires,
    extras_require=extras_require,
    python_requires='>=3.8.0',
)
