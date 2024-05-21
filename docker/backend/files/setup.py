
from setuptools import setup, find_packages

__name__ = 'copr-messaging'
__description__ = "A schema and tooling for Copr fedora-messaging"
__author__ = "Copr team"
__author_email__ = "copr-devel@lists.fedorahosted.org"
__url__ = "https://github.com/fedora-copr/copr"

setup(
    name=__name__,
    version="0.11",
    description=__description__,
    url=__url__,

    classifiers=[
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Programming Language :: Python :: 3.9",
    ],
    license="GPLv2+",
    maintainer="Copr Team",
    maintainer_email=__author_email__,
    keywords="fedora",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "fedora.messages": [
            "copr.build.start=euler_schema:BuildChrootStarted",
            "copr.build.end=euler_schema:BuildChrootEnded",
        ]
    },
)