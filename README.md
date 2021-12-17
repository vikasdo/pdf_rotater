# pdf_rotater

Input :

- REST API  will take a given PDF file, angle of rotation, page number

Output:

- The API should rotate the specified page in the given angle and replace that page back into the PDF. 

Sending  Multipart/Form-Data using API Gateway(aws)  and a Python Lambda Proxy for storage in S3

For api we are sending the Request  in the form of Multipart/Form-Data .
Why should we use Multipart-formdata rather we can also use binary data file (but in this we need to send file along with the other
