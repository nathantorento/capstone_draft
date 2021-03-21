from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_jsglue import JSGlue
# import sqlalchemy
import os

db = SQLAlchemy()
# db = None
login = LoginManager()
migrate = Migrate()
jsglue = JSGlue()

from .controllers import main, errors, home
from .config import DevelopmentConfig

blueprints = (main, errors, home)


# def init_connection_engine():
#    db_config = {
#       # [START cloud_sql_mysql_sqlalchemy_limit]
#       # Pool size is the maximum number of permanent connections to keep.
#       "pool_size": 5,
#       # Temporarily exceeds the set pool_size if no connections are available.
#       "max_overflow": 2,
#       # The total number of concurrent connections for your application will be
#       # a total of pool_size and max_overflow.
#       # [END cloud_sql_mysql_sqlalchemy_limit]
#
#       # [START cloud_sql_mysql_sqlalchemy_backoff]
#       # SQLAlchemy automatically uses delays between failed connection attempts,
#       # but provides no arguments for configuration.
#       # [END cloud_sql_mysql_sqlalchemy_backoff]
#
#       # [START cloud_sql_mysql_sqlalchemy_timeout]
#       # 'pool_timeout' is the maximum number of seconds to wait when retrieving a
#       # new connection from the pool. After the specified amount of time, an
#       # exception will be thrown.
#       "pool_timeout": 30,  # 30 seconds
#       # [END cloud_sql_mysql_sqlalchemy_timeout]
#
#       # [START cloud_sql_mysql_sqlalchemy_lifetime]
#       # 'pool_recycle' is the maximum number of seconds a connection can persist.
#       # Connections that live longer than the specified amount of time will be
#       # reestablished
#       "pool_recycle": 1800,  # 30 minutes
#       # [END cloud_sql_mysql_sqlalchemy_lifetime]
#
#    }
#
#    if os.environ.get("DB_HOST"):
#       return init_tcp_connection_engine(db_config)
#    else:
#       return init_unix_connection_engine(db_config)
#
#
# def init_tcp_connection_engine(db_config):
#    # [START cloud_sql_mysql_sqlalchemy_create_tcp]
#    # Remember - storing secrets in plaintext is potentially unsafe. Consider using
#    # something like https://cloud.google.com/secret-manager/docs/overview to help keep
#    # secrets secret.
#    db_user = os.environ["DB_USER"]
#    db_pass = os.environ["DB_PASS"]
#    db_name = os.environ["DB_NAME"]
#    db_host = os.environ["DB_HOST"]
#
#    # Extract host and port from db_host
#    host_args = db_host.split(":")
#    db_hostname, db_port = host_args[0], int(host_args[1])
#
#    pool = sqlalchemy.create_engine(
#       # Equivalent URL:
#       # mysql+pymysql://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>
#       sqlalchemy.engine.url.URL(
#          drivername="mysql+pymysql",
#          username=db_user,  # e.g. "my-database-user"
#          password=db_pass,  # e.g. "my-database-password"
#          host=db_hostname,  # e.g. "127.0.0.1"
#          port=db_port,  # e.g. 3306
#          database=db_name,  # e.g. "my-database-name"
#       ),
#       **db_config
#    )
#    # [END cloud_sql_mysql_sqlalchemy_create_tcp]
#
#    return pool
#
#
# def init_unix_connection_engine(db_config):
#    # [START cloud_sql_mysql_sqlalchemy_create_socket]
#    # Remember - storing secrets in plaintext is potentially unsafe. Consider using
#    # something like https://cloud.google.com/secret-manager/docs/overview to help keep
#    # secrets secret.
#    db_user = os.environ["DB_USER"]
#    db_pass = os.environ["DB_PASS"]
#    db_name = os.environ["DB_NAME"]
#    db_socket_dir = os.environ.get("DB_SOCKET_DIR", "/cloudsql")
#    cloud_sql_connection_name = os.environ["CLOUD_SQL_CONNECTION_NAME"]
#
#    pool = sqlalchemy.create_engine(
#       # Equivalent URL:
#       # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=<socket_path>/<cloud_sql_instance_name>
#       sqlalchemy.engine.url.URL(
#          drivername="mysql+pymysql",
#          username=db_user,  # e.g. "my-database-user"
#          password=db_pass,  # e.g. "my-database-password"
#          database=db_name,  # e.g. "my-database-name"
#          query={
#             "unix_socket": "{}/{}".format(
#                db_socket_dir,  # e.g. "/cloudsql"
#                cloud_sql_connection_name)  # i.e "<PROJECT-NAME>:<INSTANCE-REGION>:<INSTANCE-NAME>"
#          }
#       ),
#       **db_config
#    )
#    # [END cloud_sql_mysql_sqlalchemy_create_socket]
#
#    return pool



def create_app():
   app = Flask(__name__, template_folder='views')
   app.config.from_object(DevelopmentConfig())
   # app.config.from_object(config.ConfigObject)
   init_blueprints(app)
   init_extensions(app)
   init_other(app)
   return app


def init_blueprints(app):
   for bp in blueprints:
      app.register_blueprint(bp)


def init_extensions(app):
   pass


def init_other(app):
   # global db
   # db = init_connection_engine()
   # with db.connect() as conn:
   #    conn.execute(
   #       "CREATE TABLE IF NOT EXISTS votes "
   #       "( vote_id SERIAL NOT NULL, time_cast timestamp NOT NULL, "
   #       "candidate CHAR(6) NOT NULL, PRIMARY KEY (vote_id) );"
   #    )
   db.init_app(app)
   login.init_app(app)
   jsglue.init_app(app)
   migrate.init_app(app, db)


