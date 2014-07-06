from distutils.core import setup
from distutils.core import Command


class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from django.conf import settings
        settings.configure(
            DATABASES={
                'default': {
                    'NAME': ':memory:',
                    'ENGINE': 'django.db.backends.sqlite3'
                }
            },
            INSTALLED_APPS=('urlarchivefield',)
        )
        from django.core.management import call_command
        call_command('test', 'urlarchivefield')


setup(
    name='django-urlarchivefield',
    version='0.0.4',
    description='A custom Django model field that automatically archives a URL',
    author='Ben Welsh',
    author_email='ben.welsh@gmail.com',
    url='https://github.com/pastpages/django-urlarchivefield',
    license='MIT',
    packages=('urlarchivefield',),
    install_requires=(
        'storytracker==0.0.2',
        'six==1.7.2',
    ),
    cmdclass={'test': TestCommand}
)
