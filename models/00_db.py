# -*- coding: utf-8 -*-

"""
Database configuration and core initialization module

This module handles:
1. Database connection setup
2. Session management
3. Core system initialization
4. Authentication configuration
"""

# Standard imports grouped together
import datetime
import json

# Third-party imports grouped together
from gluon.storage import Messages, Storage
from gluon.tools import Mail
import s3 as s3base
import s3log

# Constants should be in UPPERCASE at the top
DEFAULT_POOL_SIZE = 10
SUPPORTED_DB_TYPES = {'mysql', 'postgres'}

def init_database():
    """
    Initialize database connection with proper error handling
    Returns database connection object
    """
    # Get configuration
    migrate = settings.get_base_migrate()
    fake_migrate = settings.get_base_fake_migrate()
    db_type, db_string, pool_size = settings.get_database_string()
    
    # Validate database type
    if not pool_size:
        pool_size = DEFAULT_POOL_SIZE
        
    # Set reserved words checking based on database type
    check_reserved = []
    if migrate and db_type in SUPPORTED_DB_TYPES:
        check_reserved = ["postgres"] if db_type == "mysql" else ["mysql"]
    
    try:
        db = DAL(
            db_string,
            check_reserved=check_reserved,
            pool_size=pool_size,
            migrate_enabled=migrate,
            fake_migrate_all=fake_migrate,
            lazy_tables=not migrate,
            ignore_field_case=db_type != "postgres",
        )
        db.set_folder("upload")
        return db
        
    except Exception as e:
        db_location = db_string.split("@", 1)[1]
        raise HTTP(503, f"Cannot connect to {db_type} Database at {db_location}: {str(e)}")

def init_session(db):
    """
    Initialize session storage based on configuration
    """
    if settings.get_base_session_db():
        # Database sessions for avoiding locks
        session.connect(request, response, db)
        
    elif settings.get_base_session_memcache():
        # Memcache sessions for better performance
        from gluon.contrib.memcache import MemcacheClient
        from gluon.contrib.memdb import MEMDB
        
        cache.memcache = MemcacheClient(
            request,
            [settings.get_base_session_memcache()]
        )
        session.connect(request, response, db=MEMDB(cache.memcache))

def init_core_modules():
    """
    Initialize core system modules and store in current
    """
    # Basic utilities
    current.mail = Mail()
    current.messages = Messages(T)
    current.ERROR = Messages(T)
    
    # Set up logging
    s3log.S3Log.setup()
    
    # Initialize authentication
    current.auth = auth = s3base.AuthS3()
    auth.settings.hmac_key = settings.get_auth_hmac_key()
    auth.define_tables(
        migrate=settings.get_base_migrate(),
        fake_migrate=settings.get_base_fake_migrate()
    )
    
    # Initialize session storage if needed
    if not session.s3:
        session.s3 = Storage()
    
    # Core modules
    current.audit = s3base.S3Audit(
        migrate=settings.get_base_migrate(),
        fake_migrate=settings.get_base_fake_migrate()
    )
    current.calendar = s3base.S3Calendar()
    current.gis = s3base.S3GIS()
    current.xml = s3base.S3XML()
    current.msg = s3base.S3Msg()
    current.sync = s3base.S3Sync()

def clear_session():
    """
    Clear session data safely
    """
    from s3 import s3_remove_last_record_id
    
    # Clear last record ID
    s3_remove_last_record_id()
    
    # Clear owned records
    if "owned_records" in session:
        del session["owned_records"]
    
    # Clear specific s3 session data
    if "s3" in session:
        for key in ("hrm", "report_options", "deduplicate"):
            session.s3.pop(key, None)

def auth_on_login(form):
    """Handle post-login actions"""
    clear_session()

def auth_on_logout(user):
    """Handle post-logout actions"""
    clear_session()

# Main initialization
if __name__ == "__main__":
    # Check debug mode
    debug = settings.check_debug()
    
    # Set language mode
    if settings.get_L10n_languages_readonly():
        T.is_writable = False
    
    # Initialize database
    db = init_database()
    current.db = db
    
    # Initialize session
    init_session(db)
    
    # Initialize core modules
    init_core_modules()