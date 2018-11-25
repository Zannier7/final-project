import unittest
import coverage
from flask.cli import FlaskGroup

from project import create_app, db   # <-- nuevo
from project.api.models import Auto # <-- nuevo

# configurando informes de covertura con coverage 4.5.1
COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/test/*',
        'project/config.py',
    ]
)
COV.start()
app = create_app()  # <-- nuevo
cli = FlaskGroup(create_app=create_app)  # <-- nuevo

# nuevo
@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command()
def test():
    """ Ejecuta las pruebas sin cobertura de codigo"""
    tests = unittest.TestLoader().discover('project/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@cli.command()
def seed_db():
    """Sembrado la base de datos."""
    db.session.add(Auto(marca='bmw', modelo='ci3', tipo='deportivo', color='blanco', placa='7u456a'))
    db.session.add(Auto(marca='audio', modelo='uik', tipo='4x4', color='negro', placa='5625as'))
    db.session.commit()

@cli.command()
def cov():
    """Ejecuta las pruebas unitarias con covertura."""
    tests = unittest.TestLoader().discover('project/test')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Resumen de covertura:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1

if __name__ == "__main__":
    cli()