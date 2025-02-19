from os import environ, listdir, path
import json
import __main__
from pyspark import SparkFiles
from pyspark.sql import SparkSession
from ETLJob.customLogging import Log4j

def start_spark(app_name= 'my_spark_app', master= 'local[*]', jar_packages = [], files = [], spark_config={}):
    print(files)

    flag_repl = not (hasattr(__main__, '__file__'))
    flag_debug = 'DEBUG' in environ.keys()

    if  (flag_repl or flag_debug):
        spark_builder = (SparkSession.builder.appName(app_name))
    else:
        spark_builder = (SparkSession.builder.master(master).appName(app_name))
        spark_jar_packages = ','.join(list(jar_packages))
        spark_builder.config('spark.jars.packages', spark_jar_packages)

        spark_files = ','.join(files)
        spark_builder.config('spark.files', spark_files)

        for key, value in spark_config.items():
            spark_builder.config(key, value)

    spark_sess = spark_builder.getOrCreate()
    spark_logger = Log4j(spark_sess)


    spark_files_dir = SparkFiles.getRootDirectory()
    config_files = [filename for filename in listdir(spark_files_dir)
                     if filename.endswith('config.json')]

    if config_files:
        path_to_config_file = path.join(spark_files_dir, config_files[0])
        with open(path_to_config_file) as config_file:
            config_dict = json.load(config_file)
            spark_logger.warn('loaded config from' + config_files[0])
    else:
        spark_logger.warn('no config file found')
        config_dict = None

    return spark_sess, spark_logger, config_dict



