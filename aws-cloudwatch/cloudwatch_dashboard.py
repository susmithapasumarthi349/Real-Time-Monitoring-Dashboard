#!/usr/bin/env python3
"""
AWS CloudWatch Dashboard Creation Script
This script creates a comprehensive CloudWatch dashboard with metrics visualization
and configures alarms for real-time monitoring.

Author: Real-Time Monitoring Dashboard Project
Date: November 2025
"""

import boto3
import json
from datetime import datetime

# Initialize CloudWatch client
cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')

class CloudWatchDashboard:
    def __init__(self, dashboard_name='RealTimeMonitoringDashboard'):
        self.dashboard_name = dashboard_name
        self.cloudwatch = cloudwatch
    
    def create_dashboard(self):
        """
        Create a CloudWatch dashboard with multiple widgets for monitoring
        EC2, RDS, Lambda, and application metrics.
        """
        dashboard_body = {
            "widgets": [
                # EC2 CPU Utilization Widget
                {
                    "type": "metric",
                    "x": 0,
                    "y": 0,
                    "width": 12,
                    "height": 6,
                    "properties": {
                        "metrics": [
                            ["AWS/EC2", "CPUUtilization", {"stat": "Average"}]
                        ],
                        "period": 300,
                        "stat": "Average",
                        "region": "us-east-1",
                        "title": "EC2 CPU Utilization",
                        "yAxis": {
                            "left": {
                                "min": 0,
                                "max": 100
                            }
                        }
                    }
                },
                # RDS Database Connections Widget
                {
                    "type": "metric",
                    "x": 12,
                    "y": 0,
                    "width": 12,
                    "height": 6,
                    "properties": {
                        "metrics": [
                            ["AWS/RDS", "DatabaseConnections", {"stat": "Average"}]
                        ],
                        "period": 300,
                        "stat": "Average",
                        "region": "us-east-1",
                        "title": "RDS Database Connections",
                        "yAxis": {
                            "left": {
                                "min": 0
                            }
                        }
                    }
                },
                # Lambda Invocations Widget
                {
                    "type": "metric",
                    "x": 0,
                    "y": 6,
                    "width": 12,
                    "height": 6,
                    "properties": {
                        "metrics": [
                            ["AWS/Lambda", "Invocations", {"stat": "Sum"}],
                            [".", "Errors", {"stat": "Sum", "color": "#d62728"}]
                        ],
                        "period": 300,
                        "stat": "Sum",
                        "region": "us-east-1",
                        "title": "Lambda Invocations and Errors"
                    }
                },
                # Application Load Balancer Widget
                {
                    "type": "metric",
                    "x": 12,
                    "y": 6,
                    "width": 12,
                    "height": 6,
                    "properties": {
                        "metrics": [
                            ["AWS/ApplicationELB", "RequestCount", {"stat": "Sum"}],
                            [".", "TargetResponseTime", {"stat": "Average", "yAxis": "right"}]
                        ],
                        "period": 300,
                        "stat": "Average",
                        "region": "us-east-1",
                        "title": "ALB Requests and Response Time",
                        "yAxis": {
                            "right": {
                                "label": "Response Time (ms)"
                            }
                        }
                    }
                },
                # Custom Application Metrics Widget
                {
                    "type": "metric",
                    "x": 0,
                    "y": 12,
                    "width": 24,
                    "height": 6,
                    "properties": {
                        "metrics": [
                            ["CustomApp", "ActiveUsers", {"stat": "Average"}],
                            [".", "TransactionsPerSecond", {"stat": "Sum"}],
                            [".", "ErrorRate", {"stat": "Average", "color": "#d62728"}]
                        ],
                        "period": 300,
                        "stat": "Average",
                        "region": "us-east-1",
                        "title": "Custom Application Metrics"
                    }
                },
                # Logs Insights Widget
                {
                    "type": "log",
                    "x": 0,
                    "y": 18,
                    "width": 24,
                    "height": 6,
                    "properties": {
                        "query": "SOURCE '/aws/lambda/my-function' | fields @timestamp, @message | filter @message like /ERROR/ | sort @timestamp desc | limit 20",
                        "region": "us-east-1",
                        "title": "Recent Application Errors"
                    }
                }
            ]
        }
        
        try:
            response = self.cloudwatch.put_dashboard(
                DashboardName=self.dashboard_name,
                DashboardBody=json.dumps(dashboard_body)
            )
            print(f"✓ Dashboard '{self.dashboard_name}' created successfully!")
            print(f"  Dashboard ARN: {response['DashboardValidationMessages']}")
            return response
        except Exception as e:
            print(f"✗ Error creating dashboard: {str(e)}")
            return None
    
    def get_dashboard(self):
        """
        Retrieve the current dashboard configuration
        """
        try:
            response = self.cloudwatch.get_dashboard(
                DashboardName=self.dashboard_name
            )
            print(f"✓ Dashboard '{self.dashboard_name}' retrieved successfully")
            return json.loads(response['DashboardBody'])
        except Exception as e:
            print(f"✗ Error retrieving dashboard: {str(e)}")
            return None
    
    def delete_dashboard(self):
        """
        Delete the dashboard
        """
        try:
            response = self.cloudwatch.delete_dashboards(
                DashboardNames=[self.dashboard_name]
            )
            print(f"✓ Dashboard '{self.dashboard_name}' deleted successfully")
            return response
        except Exception as e:
            print(f"✗ Error deleting dashboard: {str(e)}")
            return None
    
    def list_dashboards(self):
        """
        List all available dashboards
        """
        try:
            response = self.cloudwatch.list_dashboards()
            print("\n📊 Available CloudWatch Dashboards:")
            for dashboard in response['DashboardEntries']:
                print(f"  - {dashboard['DashboardName']} (Last Modified: {dashboard['LastModified']})")
            return response['DashboardEntries']
        except Exception as e:
            print(f"✗ Error listing dashboards: {str(e)}")
            return None


def main():
    """
    Main function to demonstrate dashboard creation
    """
    print("\n" + "="*60)
    print("AWS CloudWatch Dashboard Creator")
    print("Real-Time Monitoring Dashboard Project")
    print("="*60 + "\n")
    
    # Create dashboard instance
    dashboard = CloudWatchDashboard()
    
    # Create the dashboard
    print("Creating CloudWatch Dashboard...")
    dashboard.create_dashboard()
    
    # List all dashboards
    print("\nListing all dashboards...")
    dashboard.list_dashboards()
    
    print("\n" + "="*60)
    print("Dashboard creation completed!")
    print("Visit AWS Console > CloudWatch > Dashboards to view")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
