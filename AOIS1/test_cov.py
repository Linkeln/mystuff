import coverage
import unittest

# Начало измерения покрытия
cov = coverage.Coverage()
cov.start()

# Запуск тестов
loader = unittest.TestLoader()
tests = loader.discover('.')
test_runner = unittest.TextTestRunner()
test_runner.run(tests)

# Остановка измерения покрытия
cov.stop()
cov.save()

# Отчет о покрытии
cov.report()
cov.html_report(directory='coverage_html_report')