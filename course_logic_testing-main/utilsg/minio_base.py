import io
import minio
from minio import Minio
from minio.error import S3Error
from logger import logger



class minio_client():
    '''
    minio class
    '''

    def __init__(self, url_minio ="192.168.12.159:9000/",
            access_key="xdai",
            secret_key="xdaiasdfghjkl",
            secure=False):
        # Create a client with the MinIO server playground, its access key
        # and secret key.
        self.client = Minio(
            url_minio,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure
        )
        self.url_minio = url_minio
        self.dir_parent = "images"
        self.make_parent(self.dir_parent)

    def make_parent(self, bucket_parent):
        found = self.client.bucket_exists(bucket_parent)
        if not found:
            self.client.make_bucket(bucket_parent)
        else:
            logger.info("Bucket %s already exists" % bucket_parent)

    def make_bucket(self, bucket_dir):
        full_path_parent = bucket_dir
        found = self.client.bucket_exists(full_path_parent)
        if not found:
            self.client.make_bucket(full_path_parent)
        else:
            logger.info("Bucket %s already exists" % full_path_parent)

    def put_images(self, image_data, path_bucket, name):
        try:
            self.make_bucket(path_bucket)
            raw_img = io.BytesIO(image_data)
            raw_img_size = raw_img.getbuffer().nbytes
            obj_write_result = self.client.put_object(path_bucket, name, raw_img, raw_img_size,
                                                      content_type='application/octet-stream')
            logger.info("created {0} object; etag:{1}, version-id: {2}".format(
                obj_write_result.object_name, obj_write_result.etag, obj_write_result.version_id
            ))
            url_minio_image = "http://" + self.url_minio + path_bucket+"/"+name
            return True, url_minio_image
        except Exception as e:
            logger.info("upload minio error::{}".format(e))
            return False, "uploadminioerror"

    def download_file(self,url,bucketname,filename,savepath):
        self.client.fget_object(bucket_name=bucketname,object_name=filename,file_path=savepath)
    # Upload '/home/user/Photos/asiaphotos.zip' as object name
    # 'asiaphotos-2015.zip' to bucket 'asiatrip'.
    # client.fput_object(
    #     "asiatrip", "asiaphotos-2015.zip", "/home/user/Photos/asiaphotos.zip",
    # )
    # print(
    #     "'/home/user/Photos/asiaphotos.zip' is successfully uploaded as "
    #     "object 'asiaphotos-2015.zip' to bucket 'asiatrip'."
    # )

# if __name__ == "__main__":
#     try:
#         main()
#     except S3Error as exc:
#         print("error occurred.", exc)
