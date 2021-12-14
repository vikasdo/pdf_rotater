import json
import base64
import boto3
from requests_toolbelt.multipart import decoder
from PyPDF2 import PdfFileReader, PdfFileWriter
from io import BytesIO

BUCKET_NAME = 'curiousfile'
def lambda_handler(event, context):
  
    from requests_toolbelt.multipart import decoder
    content_type_header = event['headers']['Content-Type']
    postdata = base64.b64decode(event['body']).decode('iso-8859-1')
    imgInput = ''
    lst = []
    out={}

    # Need this line as it does 'b'b'pdfdatacontent'.
    

    for part in decoder.MultipartDecoder(postdata.encode('utf-8'), content_type_header).parts:
 


        disposition = part.headers[b'Content-Disposition']
        params = {}
        for dispPart in str(disposition).split(';'):
            kv = dispPart.split('=', 2)
            params[str(kv[0]).strip()] = str(kv[1]).strip('\"\'\t \r\n') if len(kv)>1 else str(kv[0]).strip()
        type = part.headers[b'Content-Type'] if b'Content-Type' in part.headers else None
        out[ params["name"]]=part.content
        lst.append(part.text)

    file_path = 'file2.pdf'
    s3 = boto3.client('s3')   
    s3_response = s3.put_object(Bucket=BUCKET_NAME, Key=file_path, Body=lst[0].encode('iso-8859-1'))    
    rotate(file_path,int(out["angle"]),int(out["pageno"]))
   
    return {
        'statusCode': 200,
        'headers': { 'Content-Type': 'text/html' },
        'body': "https://curiousfile.s3.eu-west-1.amazonaws.com/file2.pdf"
    }  

    
from PyPDF2 import PdfFileReader, PdfFileWriter
def rotate(pdf_path,angle_of_rotation,n):
    s3 = boto3.resource('s3')
    obj = s3.Object(BUCKET_NAME, pdf_path)
    fs = obj.get()['Body'].read()
    pdf_read = PdfFileReader(BytesIO(fs))
    pdf_write = PdfFileWriter()
    print(n,angle_of_rotation)
    for page_num in range(1,pdf_read.getNumPages()+1):
        if page_num==n:
            page1 = pdf_read.getPage(page_num-1).rotateClockwise(angle_of_rotation)
            pdf_write.addPage(page1)
        else:

            pdf_write.addPage(pdf_read.getPage(page_num-1))
    with open('/tmp/' + 'test.pdf', 'wb') as fh:
            pdf_write.write(fh)
    saved='/tmp/' + 'test.pdf'
    s3_client = boto3.client('s3')
    s3_response = s3_client.upload_file(saved,BUCKET_NAME, pdf_path)    

        
if __name__ == '__main__':
    path = 'https://curiousfile.s3.eu-west-1.amazonaws.com/file1.pdf'
    rotate(path,1,180)