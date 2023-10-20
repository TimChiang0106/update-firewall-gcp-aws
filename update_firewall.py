import subprocess
import requests


# get the ipv4 address
response = requests.get('https://httpbin.org/ip')
data = response.json()
external_ip = data['origin']
print(external_ip)


# GCP
firewall_rule_name = 'firewall_rule_name'
source_range = f'{external_ip}/32'

command = f'gcloud compute firewall-rules update {firewall_rule_name} --source-ranges={source_range}'
result = subprocess.run(command, shell=True, capture_output=True, text=True)

if result.returncode == 0:
    print('GCP Firewall rule updated successfully.')
else:
    print('GCP Failed to update the firewall rrule.')
    print('Error:', result.stderr)


# AWS
group_id = 'group_id'
group_rule_id = 'group_rule_id'


command_aws = "aws ec2 modify-security-group-rules --group-id sg-{0} --security-group-rules SecurityGroupRuleId=sgr-{1},SecurityGroupRule='{{IpProtocol=-1,CidrIpv4={2}/32}}'".format(group_id, group_rule_id, external_ip)
result_aws = subprocess.run(command_aws, shell=True, capture_output=True, text=True)
if result_aws.returncode == 0:
    print('AWS Firewall rule updated successfully.')
else:
    print('AWS Failed to update the firewall rule.')
    print('Error:', result.stderr)