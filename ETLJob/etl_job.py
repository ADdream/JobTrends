from pyspark.sql.functions import udf
from pyspark.sql.types import StructType, StructField, StringType, DateType
import pyspark.sql.functions as f
from ETLJob.spark import start_spark
import os


def main():

    spark, log, config = start_spark(
        app_name='Job_Crawler',
        files=['configs/etl_config.json'])

    log.warn('etl_job is up-and-running')

    data = extract_data(spark)
    data_transformed = transform_data(data)
    load_data(data_transformed)

    log.warn('test_etl_job is finished')
    spark.stop()
    return None


def extract_data(spark):
    schema = StructType([
        StructField("status", StringType()),
        StructField("title", StringType()),
        StructField("company", StringType()),
        StructField("location", StringType()),
        StructField("date", DateType()),
        StructField("blurb", StringType()),
        StructField("tags", StringType()),
        StructField("link", StringType()),
        StructField("id", StringType()),
        StructField("provider", StringType()),
        StructField("query", StringType())
    ])
    inputPath = os.path.normpath(os.path.join(os.path.dirname(os.getcwd()), 'search/master_list.csv'))


    JobInfo = spark.read.csv(inputPath, header=True, schema=schema, sep='|')

    return JobInfo

def editBlurb(jobDescription: str):
    if jobDescription is not None:
        jobDescription.replace('"', '')
    return jobDescription

def transform_data(jobInfo):

    editBlurbUDF = udf(editBlurb, StringType())
    jobInfo = jobInfo.withColumn("blurb", editBlurbUDF(jobInfo['blurb']))

    # Getting the missing stats for each column
    jobInfo.agg(*[
        (1 - (f.count(c) / f.count('*'))).alias(c + '_missing')
        for c in jobInfo.columns]
                ).show()

    # Excluding tags column as it has no data in all the rows
    jobInfo = jobInfo.select([c for c in jobInfo.columns if c != 'tags' or c != 'blurb'])

    return jobInfo

def deleteDirContent(outputPath):
    fileList = os.listdir(outputPath)
    for filename in fileList:
        os.remove(os.path.join(outputPath, filename))

    return None

def load_data(jobInfo):
    outputPath = os.path.normpath(os.path.join(os.path.dirname(os.getcwd()), 'search/output'))
    deleteDirContent(outputPath)

    print("No of files {}".format(len(os.listdir(outputPath))))

    (jobInfo
     .coalesce(1)
     .write
     .csv(outputPath, mode='overwrite', header=True, sep='|'))
    return None


# def create_test_data(spark, config):
#     local_records = [
#         Row(id=1, first_name='Dan', second_name='Germain', floor=1),
#         Row(id=2, first_name='Dan', second_name='Sommerville', floor=1),
#         Row(id=3, first_name='Alex', second_name='Ioannides', floor=2),
#         Row(id=4, first_name='Ken', second_name='Lai', floor=2),
#         Row(id=5, first_name='Stu', second_name='White', floor=3),
#         Row(id=6, first_name='Mark', second_name='Sweeting', floor=3),
#         Row(id=7, first_name='Phil', second_name='Bird', floor=4),
#         Row(id=8, first_name='Kim', second_name='Suter', floor=4)
#     ]
#
#     df = spark.createDataFrame(local_records)
#
#     (df
#      .coalesce(1)
#      .write
#      .parquet('tests/test_data/employees', mode='overwrite'))

    # df_tf = transform_data(df, config['steps_per_floor'])
    #
    # (df_tf
    #  .coalesce(1)
    #  .write
    #  .parquet('tests/test_data/employees_report', mode='overwrite'))
    #
    # return None



if __name__ == '__main__':
    main()