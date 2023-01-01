import setuptools

with open("README.md", "r") as fh:
    _LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="openai-kira",
    license='GPLv2',
    author="sudoskys",
    version="0.0.1",
    author_email="me@dianas.cyou",
    description="A asynchronous Chat client for OpenAI API",
    long_description=_LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/sudoskys/openai-kira",
    packages=setuptools.find_namespace_packages(),
    install_requires=["httpx", "pytest", "httpx", "redis", "nltk", "Pillow", "numpy", "jieba", "transformers",
                      "beautifulsoup4", "pydantic", "loguru", "elara", "openai-async"],
)
