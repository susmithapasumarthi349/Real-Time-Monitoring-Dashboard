#!/usr/bin/env python3
"""
AWS CloudWatch Alarms Configuration Script
This script creates and manages CloudWatch alarms for monitoring
AWS resources and application metrics.

Author: Real-Time Monitoring Dashboard Project
Date: November 2025
"""

import boto3
import json
from typing import List, Dict, Optional

# Initialize CloudWatch client
cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')
sns = boto3.client('sns', region_name='us-east-1')

class CloudWatchAlarms:
    def __init__(self, sns_topic_arn=None):
        self.cloudwatch = cloudwatch
        self.sns = sns
        self.sns_topic_arn = sns_topic_arn
    
    def create_sns_topic(self, topic_name='MonitoringAlerts'):
        """
        Create an SNS topic for alarm notifications
        """
        try:
            response = self.sns.create_topic(Name=topic_name)
            self.sns_topic_arn = response['TopicArn']
            print(f"✓ SNS Topic created: {self.sns_topic_arn}")
            return self.sns_topic_arn
        except Exception as e:
            print(f"✗ Error creating SNS topic: {str(e)}")
            return None
    
    def subscribe_email_to_topic(self, email_address: str):
        """
        Subscribe an email address to the SNS topic for alarm notifications
        """
        if not self.sns_topic_arn:
            print("✗ Error: SNS topic ARN not set")
            return None
        
        try:
            response = self.sns.subscribe(
                TopicArn=self.sns_topic_arn,
                Protocol='email',
                Endpoint=email_address
            )
            print(f"✓ Email subscription created. Check {email_address} for confirmation.")
            return response['SubscriptionArn']
        except Exception as e:
            print(f"✗ Error subscribing email: {str(e)}")
            return None
    
    def create_ec2_cpu_alarm(self, instance_id: str, threshold: float = 80.0):
        """
        Create alarm for EC2 CPU utilization
        """
        alarm_name = f'EC2-HighCPU-{instance_id}'
        
        try:
            response = self.cloudwatch.put_metric_alarm(
                AlarmName=alarm_name,
                ComparisonOperator='GreaterThanThreshold',
                EvaluationPeriods=2,
                MetricName='CPUUtilization',
                Namespace='AWS/EC2',
                Period=300,
                Statistic='Average',
                Threshold=threshold,
                ActionsEnabled=True,
                AlarmActions=[self.sns_topic_arn] if self.sns_topic_arn else [],
                AlarmDescription=f'Alarm when EC2 CPU exceeds {threshold}%',
                Dimensions=[
                    {
                        'Name': 'InstanceId',
                        'Value': instance_id
                    }
                ]
            )
            print(f"✓ Alarm created: {alarm_name}")
            return alarm_name
        except Exception as e:
            print(f"✗ Error creating EC2 CPU alarm: {str(e)}")
            return None
    
    def create_rds_connection_alarm(self, db_instance_id: str, threshold: float = 80):
        """
        Create alarm for RDS database connections
        """
        alarm_name = f'RDS-HighConnections-{db_instance_id}'
        
        try:
            response = self.cloudwatch.put_metric_alarm(
                AlarmName=alarm_name,
                ComparisonOperator='GreaterThanThreshold',
                EvaluationPeriods=2,
                MetricName='DatabaseConnections',
                Namespace='AWS/RDS',
                Period=300,
                Statistic='Average',
                Threshold=threshold,
                ActionsEnabled=True,
                AlarmActions=[self.sns_topic_arn] if self.sns_topic_arn else [],
                AlarmDescription=f'Alarm when RDS connections exceed {threshold}',
                Dimensions=[
                    {
                        'Name': 'DBInstanceIdentifier',
                        'Value': db_instance_id
                    }
                ]
            )
            print(f"✓ Alarm created: {alarm_name}")
            return alarm_name
        except Exception as e:
            print(f"✗ Error creating RDS connection alarm: {str(e)}")
            return None
    
    def create_lambda_error_alarm(self, function_name: str, threshold: float = 5):
        """
        Create alarm for Lambda function errors
        """
        alarm_name = f'Lambda-Errors-{function_name}'
        
        try:
            response = self.cloudwatch.put_metric_alarm(
                AlarmName=alarm_name,
                ComparisonOperator='GreaterThanThreshold',
                EvaluationPeriods=1,
                MetricName='Errors',
                Namespace='AWS/Lambda',
                Period=300,
                Statistic='Sum',
                Threshold=threshold,
                ActionsEnabled=True,
                AlarmActions=[self.sns_topic_arn] if self.sns_topic_arn else [],
                AlarmDescription=f'Alarm when Lambda errors exceed {threshold}',
                Dimensions=[
                    {
                        'Name': 'FunctionName',
                        'Value': function_name
                    }
                ]
            )
            print(f"✓ Alarm created: {alarm_name}")
            return alarm_name
        except Exception as e:
            print(f"✗ Error creating Lambda error alarm: {str(e)}")
            return None
    
    def create_alb_target_health_alarm(self, load_balancer_name: str, target_group_name: str):
        """
        Create alarm for ALB unhealthy target count
        """
        alarm_name = f'ALB-UnhealthyTargets-{load_balancer_name}'
        
        try:
            response = self.cloudwatch.put_metric_alarm(
                AlarmName=alarm_name,
                ComparisonOperator='GreaterThanThreshold',
                EvaluationPeriods=2,
                MetricName='UnHealthyHostCount',
                Namespace='AWS/ApplicationELB',
                Period=300,
                Statistic='Average',
                Threshold=0,
                ActionsEnabled=True,
                AlarmActions=[self.sns_topic_arn] if self.sns_topic_arn else [],
                AlarmDescription='Alarm when ALB has unhealthy targets',
                Dimensions=[
                    {
                        'Name': 'LoadBalancer',
                        'Value': load_balancer_name
                    },
                    {
                        'Name': 'TargetGroup',
                        'Value': target_group_name
                    }
                ]
            )
            print(f"✓ Alarm created: {alarm_name}")
            return alarm_name
        except Exception as e:
            print(f"✗ Error creating ALB health alarm: {str(e)}")
            return None
    
    def create_custom_metric_alarm(self, metric_name: str, namespace: str, 
                                   threshold: float, comparison_operator: str = 'GreaterThanThreshold'):
        """
        Create alarm for custom application metrics
        """
        alarm_name = f'Custom-{metric_name}-Alert'
        
        try:
            response = self.cloudwatch.put_metric_alarm(
                AlarmName=alarm_name,
                ComparisonOperator=comparison_operator,
                EvaluationPeriods=2,
                MetricName=metric_name,
                Namespace=namespace,
                Period=300,
                Statistic='Average',
                Threshold=threshold,
                ActionsEnabled=True,
                AlarmActions=[self.sns_topic_arn] if self.sns_topic_arn else [],
                AlarmDescription=f'Alarm for custom metric {metric_name}'
            )
            print(f"✓ Alarm created: {alarm_name}")
            return alarm_name
        except Exception as e:
            print(f"✗ Error creating custom metric alarm: {str(e)}")
            return None
    
    def list_alarms(self, state_value: Optional[str] = None):
        """
        List all CloudWatch alarms, optionally filtered by state
        """
        try:
            params = {}
            if state_value:
                params['StateValue'] = state_value
            
            response = self.cloudwatch.describe_alarms(**params)
            
            print(f"\n🔔 CloudWatch Alarms:")
            for alarm in response['MetricAlarms']:
                state_icon = "✅" if alarm['StateValue'] == 'OK' else "🚨"
                print(f"  {state_icon} {alarm['AlarmName']}")
                print(f"     State: {alarm['StateValue']}")
                print(f"     Metric: {alarm['MetricName']}")
                print(f"     Threshold: {alarm['Threshold']}")
                print()
            
            return response['MetricAlarms']
        except Exception as e:
            print(f"✗ Error listing alarms: {str(e)}")
            return None
    
    def delete_alarm(self, alarm_name: str):
        """
        Delete a specific CloudWatch alarm
        """
        try:
            response = self.cloudwatch.delete_alarms(
                AlarmNames=[alarm_name]
            )
            print(f"✓ Alarm deleted: {alarm_name}")
            return response
        except Exception as e:
            print(f"✗ Error deleting alarm: {str(e)}")
            return None
    
    def delete_all_alarms(self):
        """
        Delete all CloudWatch alarms
        """
        try:
            alarms = self.cloudwatch.describe_alarms()
            alarm_names = [alarm['AlarmName'] for alarm in alarms['MetricAlarms']]
            
            if not alarm_names:
                print("ℹ️ No alarms to delete")
                return
            
            response = self.cloudwatch.delete_alarms(AlarmNames=alarm_names)
            print(f"✓ Deleted {len(alarm_names)} alarms")
            return response
        except Exception as e:
            print(f"✗ Error deleting alarms: {str(e)}")
            return None


def main():
    """
    Main function to demonstrate alarm creation
    """
    print("\n" + "="*60)
    print("AWS CloudWatch Alarms Manager")
    print("Real-Time Monitoring Dashboard Project")
    print("="*60 + "\n")
    
    # Initialize alarms manager
    alarms = CloudWatchAlarms()
    
    # Create SNS topic for notifications
    print("Creating SNS topic for alarm notifications...")
    topic_arn = alarms.create_sns_topic('MonitoringAlerts')
    
    # Subscribe email (replace with actual email)
    print("\nSubscribing email to SNS topic...")
    # alarms.subscribe_email_to_topic('your-email@example.com')
    
    # Create sample alarms
    print("\nCreating CloudWatch Alarms...")
    
    # EC2 CPU Alarm
    # alarms.create_ec2_cpu_alarm('i-1234567890abcdef0', threshold=80.0)
    
    # RDS Connection Alarm
    # alarms.create_rds_connection_alarm('my-database', threshold=80)
    
    # Lambda Error Alarm
    # alarms.create_lambda_error_alarm('my-function', threshold=5)
    
    # Custom Metric Alarm
    alarms.create_custom_metric_alarm(
        metric_name='ErrorRate',
        namespace='CustomApp',
        threshold=5.0,
        comparison_operator='GreaterThanThreshold'
    )
    
    # List all alarms
    print("\nListing all alarms...")
    alarms.list_alarms()
    
    print("\n" + "="*60)
    print("Alarm configuration completed!")
    print("Check AWS Console > CloudWatch > Alarms to view")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
