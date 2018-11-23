# services/users/project/config.py
class BaseConfig:
    """Base configuration"""
    TESTING = False
class DevelopmentConfig(BaseConfig):
    """Development Configuration"""
    pass
class TestingConfig(BaseConfig):
    """Testing configuration"""
    pass
class TEstingConfig(BaseConfig):
    """Testing configuration"""
    TESTING = True
class ProductionConfig(BaseConfig):
    """Production configuration"""
    pass