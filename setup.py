from distutils.core import setup

setup(
    name='dnsReaper',
    version='1.2.0',
    packages=['providers', 'signatures', 'signatures.checks', 'signatures.templates'],
    url='',
    license='GNU Affero',
    author='Punk Security',
    author_email='',
    description='subdomain takeover tool for attackers, bug bounty hunters and the blue team!'
)
