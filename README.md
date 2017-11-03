## Steps to deploy on EC2
Online reference

### Create EC2 instance
1. On EC2, Select "Amazon Linux AMI 2017.09.0 (HVM)" -> review and launch
2. Set security group (Online reference)
3. review -> set security pair or use existing pair
### 


nocache pip install
install gcc

EC2 Credential
account alias: ‎212252083097
user name: dev-ops
user password: EzSwitch2017

gunicorn app:app -b localhost:8000 -w 1 --threads 4


https://www.matthealy.com.au/blog/post/deploying-flask-to-amazon-web-services-ec2/