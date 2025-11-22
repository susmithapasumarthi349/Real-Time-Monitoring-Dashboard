#!/usr/bin/env python3
"""
GCP Cloud Monitoring Dashboard Creation Script
This script creates comprehensive monitoring dashboards using Google Cloud Monitoring (formerly Stackdriver)
for visualizing GCP resource metrics and custom application metrics.

Author: Real-Time Monitoring Dashboard Project
Date: November 2025
"""

from google.cloud import monitoring_v3
from google.cloud.monitoring_dashboard import v1
import json
from typing import List, Dict

class GCPMonitoringDashboard:
    def __init__(self, project_id: str):
        """
        Initialize GCP Monitoring Dashboard client
        
        Args:
            project_id: GCP project ID
        """
        self.project_id = project_id
        self.project_name = f"projects/{project_id}"
        self.dashboard_client = v1.DashboardsServiceClient()
        self.metric_client = monitoring_v3.MetricServiceClient()
    
    def create_dashboard(self, dashboard_name: str = 'Real-Time-Monitoring-Dashboard'):
        """
        Create a comprehensive GCP monitoring dashboard
        """
        dashboard = {
            "displayName": dashboard_name,
            "mosaicLayout": {
                "columns": 12,
                "tiles": [
                    # Compute Engine CPU Utilization
                    {
                        "width": 6,
                        "height": 4,
                        "widget": {
                            "title": "Compute Engine CPU Utilization",
                            "xyChart": {
                                "dataSets": [{
                                    "timeSeriesQuery": {
                                        "timeSeriesFilter": {
                                            "filter": 'metric.type="compute.googleapis.com/instance/cpu/utilization" resource.type="gce_instance"',
                                            "aggregation": {
                                                "alignmentPeriod": "300s",
                                                "perSeriesAligner": "ALIGN_MEAN"
                                            }
                                        }
                                    },
                                    "plotType": "LINE",
                                    "targetAxis": "Y1"
                                }],
                                "yAxis": {
                                    "label": "CPU Utilization",
                                    "scale": "LINEAR"
                                }
                            }
                        }
                    },
                    # Cloud SQL Database Connections
                    {
                        "xPos": 6,
                        "width": 6,
                        "height": 4,
                        "widget": {
                            "title": "Cloud SQL Database Connections",
                            "xyChart": {
                                "dataSets": [{
                                    "timeSeriesQuery": {
                                        "timeSeriesFilter": {
                                            "filter": 'metric.type="cloudsql.googleapis.com/database/network/connections" resource.type="cloudsql_database"',
                                            "aggregation": {
                                                "alignmentPeriod": "300s",
                                                "perSeriesAligner": "ALIGN_MEAN"
                                            }
                                        }
                                    },
                                    "plotType": "LINE",
                                    "targetAxis": "Y1"
                                }],
                                "yAxis": {
                                    "label": "Connections",
                                    "scale": "LINEAR"
                                }
                            }
                        }
                    },
                    # Cloud Functions Execution Count
                    {
                        "yPos": 4,
                        "width": 6,
                        "height": 4,
                        "widget": {
                            "title": "Cloud Functions Executions",
                            "xyChart": {
                                "dataSets": [
                                    {
                                        "timeSeriesQuery": {
                                            "timeSeriesFilter": {
                                                "filter": 'metric.type="cloudfunctions.googleapis.com/function/execution_count" resource.type="cloud_function"',
                                                "aggregation": {
                                                    "alignmentPeriod": "300s",
                                                    "perSeriesAligner": "ALIGN_RATE"
                                                }
                                            }
                                        },
                                        "plotType": "LINE",
                                        "targetAxis": "Y1"
                                    }
                                ],
                                "yAxis": {
                                    "label": "Executions/sec",
                                    "scale": "LINEAR"
                                }
                            }
                        }
                    },
                    # Load Balancer Request Count
                    {
                        "xPos": 6,
                        "yPos": 4,
                        "width": 6,
                        "height": 4,
                        "widget": {
                            "title": "Load Balancer Request Rate",
                            "xyChart": {
                                "dataSets": [{
                                    "timeSeriesQuery": {
                                        "timeSeriesFilter": {
                                            "filter": 'metric.type="loadbalancing.googleapis.com/https/request_count" resource.type="https_lb_rule"',
                                            "aggregation": {
                                                "alignmentPeriod": "300s",
                                                "perSeriesAligner": "ALIGN_RATE"
                                            }
                                        }
                                    },
                                    "plotType": "LINE",
                                    "targetAxis": "Y1"
                                }],
                                "yAxis": {
                                    "label": "Requests/sec",
                                    "scale": "LINEAR"
                                }
                            }
                        }
                    },
                    # GKE Container CPU Utilization
                    {
                        "yPos": 8,
                        "width": 12,
                        "height": 4,
                        "widget": {
                            "title": "GKE Container CPU Utilization",
                            "xyChart": {
                                "dataSets": [{
                                    "timeSeriesQuery": {
                                        "timeSeriesFilter": {
                                            "filter": 'metric.type="kubernetes.io/container/cpu/core_usage_time" resource.type="k8s_container"',
                                            "aggregation": {
                                                "alignmentPeriod": "300s",
                                                "perSeriesAligner": "ALIGN_RATE"
                                            }
                                        }
                                    },
                                    "plotType": "LINE",
                                    "targetAxis": "Y1"
                                }],
                                "yAxis": {
                                    "label": "CPU Cores",
                                    "scale": "LINEAR"
                                }
                            }
                        }
                    },
                    # Custom Application Metrics
                    {
                        "yPos": 12,
                        "width": 12,
                        "height": 4,
                        "widget": {
                            "title": "Custom Application Metrics",
                            "xyChart": {
                                "dataSets": [
                                    {
                                        "timeSeriesQuery": {
                                            "timeSeriesFilter": {
                                                "filter": 'metric.type="custom.googleapis.com/application/active_users" resource.type="global"',
                                                "aggregation": {
                                                    "alignmentPeriod": "300s",
                                                    "perSeriesAligner": "ALIGN_MEAN"
                                                }
                                            }
                                        },
                                        "plotType": "LINE",
                                        "targetAxis": "Y1"
                                    },
                                    {
                                        "timeSeriesQuery": {
                                            "timeSeriesFilter": {
                                                "filter": 'metric.type="custom.googleapis.com/application/error_rate" resource.type="global"',
                                                "aggregation": {
                                                    "alignmentPeriod": "300s",
                                                    "perSeriesAligner": "ALIGN_MEAN"
                                                }
                                            }
                                        },
                                        "plotType": "LINE",
                                        "targetAxis": "Y2"
                                    }
                                ],
                                "yAxis": {
                                    "label": "Active Users",
                                    "scale": "LINEAR"
                                },
                                "y2Axis": {
                                    "label": "Error Rate",
                                    "scale": "LINEAR"
                                }
                            }
                        }
                    }
                ]
            }
        }
        
        try:
            request = v1.CreateDashboardRequest(
                parent=self.project_name,
                dashboard=dashboard
            )
            response = self.dashboard_client.create_dashboard(request=request)
            print(f"✓ Dashboard '{dashboard_name}' created successfully!")
            print(f"  Dashboard name: {response.name}")
            return response
        except Exception as e:
            print(f"✗ Error creating dashboard: {str(e)}")
            return None
    
    def list_dashboards(self):
        """
        List all dashboards in the project
        """
        try:
            request = v1.ListDashboardsRequest(parent=self.project_name)
            page_result = self.dashboard_client.list_dashboards(request=request)
            
            print("\n📊 Available GCP Monitoring Dashboards:")
            for dashboard in page_result:
                print(f"  - {dashboard.display_name}")
                print(f"    Name: {dashboard.name}")
                print()
            
            return list(page_result)
        except Exception as e:
            print(f"✗ Error listing dashboards: {str(e)}")
            return None
    
    def get_dashboard(self, dashboard_name: str):
        """
        Get a specific dashboard
        """
        try:
            request = v1.GetDashboardRequest(name=dashboard_name)
            dashboard = self.dashboard_client.get_dashboard(request=request)
            print(f"✓ Dashboard retrieved: {dashboard.display_name}")
            return dashboard
        except Exception as e:
            print(f"✗ Error getting dashboard: {str(e)}")
            return None
    
    def delete_dashboard(self, dashboard_name: str):
        """
        Delete a dashboard
        """
        try:
            request = v1.DeleteDashboardRequest(name=dashboard_name)
            self.dashboard_client.delete_dashboard(request=request)
            print(f"✓ Dashboard deleted: {dashboard_name}")
            return True
        except Exception as e:
            print(f"✗ Error deleting dashboard: {str(e)}")
            return False
    
    def write_custom_metric(self, metric_type: str, value: float, labels: Dict = None):
        """
        Write a custom metric value to Cloud Monitoring
        """
        try:
            series = monitoring_v3.TimeSeries()
            series.metric.type = f"custom.googleapis.com/{metric_type}"
            series.resource.type = "global"
            
            if labels:
                for key, value_label in labels.items():
                    series.metric.labels[key] = value_label
            
            now = time.time()
            seconds = int(now)
            nanos = int((now - seconds) * 10 ** 9)
            interval = monitoring_v3.TimeInterval(
                {"end_time": {"seconds": seconds, "nanos": nanos}}
            )
            point = monitoring_v3.Point(
                {"interval": interval, "value": {"double_value": value}}
            )
            series.points = [point]
            
            self.metric_client.create_time_series(
                name=self.project_name, time_series=[series]
            )
            print(f"✓ Custom metric written: {metric_type} = {value}")
            return True
        except Exception as e:
            print(f"✗ Error writing custom metric: {str(e)}")
            return False


def main():
    """
    Main function to demonstrate dashboard creation
    """
    print("\n" + "="*60)
    print("GCP Cloud Monitoring Dashboard Creator")
    print("Real-Time Monitoring Dashboard Project")
    print("="*60 + "\n")
    
    # Replace with your GCP project ID
    project_id = "your-gcp-project-id"
    
    # Create dashboard instance
    dashboard = GCPMonitoringDashboard(project_id)
    
    # Create the dashboard
    print("Creating GCP Monitoring Dashboard...")
    dashboard.create_dashboard()
    
    # List all dashboards
    print("\nListing all dashboards...")
    dashboard.list_dashboards()
    
    print("\n" + "="*60)
    print("Dashboard creation completed!")
    print("Visit GCP Console > Monitoring > Dashboards to view")
    print("="*60 + "\n")

if __name__ == "__main__":
    import time
    main()
