#!/usr/bin/env python3
"""
Azure Monitor Dashboard Creation Script
This script creates comprehensive monitoring dashboards using Azure Monitor
for visualizing Azure resource metrics and application insights.

Author: Real-Time Monitoring Dashboard Project
Date: November 2025
"""

from azure.identity import DefaultAzureCredential
from azure.mgmt.dashboard import DashboardManagementClient
from azure.mgmt.monitor import MonitorManagementClient
from azure.mgmt.resource import ResourceManagementClient
import json
from typing import List, Dict, Optional

class Azure MonitorDashboard:
    def __init__(self, subscription_id: str, resource_group: str):
        """
        Initialize Azure Monitor Dashboard client
        
        Args:
            subscription_id: Azure subscription ID
            resource_group: Resource group name
        """
        self.subscription_id = subscription_id
        self.resource_group = resource_group
        self.credential = DefaultAzureCredential()
        self.dashboard_client = DashboardManagementClient(self.credential, subscription_id)
        self.monitor_client = MonitorManagementClient(self.credential, subscription_id)
        self.resource_client = ResourceManagementClient(self.credential, subscription_id)
    
    def create_dashboard(self, dashboard_name: str = 'RealTimeMonitoringDashboard'):
        """
        Create a comprehensive Azure Monitor dashboard
        """
        dashboard_properties = {
            "lenses": [
                {
                    "order": 0,
                    "parts": [
                        # VM CPU Utilization
                        {
                            "position": {"x": 0, "y": 0, "colSpan": 6, "rowSpan": 4},
                            "metadata": {
                                "inputs": [
                                    {
                                        "name": "options",
                                        "value": {
                                            "chart": {
                                                "metrics": [
                                                    {
                                                        "resourceMetadata": {
                                                            "id": f"/subscriptions/{self.subscription_id}/resourceGroups/{self.resource_group}/providers/Microsoft.Compute/virtualMachines"
                                                        },
                                                        "name": "Percentage CPU",
                                                        "aggregationType": "Average"
                                                    }
                                                ],
                                                "title": "VM CPU Utilization",
                                                "titleKind": "Auto",
                                                "visualization": {"chartType": "Line"}
                                            }
                                        }
                                    }
                                ],
                                "type": "Extension/HubsExtension/PartType/MonitorChartPart"
                            }
                        },
                        # SQL Database DTU Percentage
                        {
                            "position": {"x": 6, "y": 0, "colSpan": 6, "rowSpan": 4},
                            "metadata": {
                                "inputs": [
                                    {
                                        "name": "options",
                                        "value": {
                                            "chart": {
                                                "metrics": [
                                                    {
                                                        "resourceMetadata": {
                                                            "id": f"/subscriptions/{self.subscription_id}/resourceGroups/{self.resource_group}/providers/Microsoft.Sql/servers/databases"
                                                        },
                                                        "name": "dtu_consumption_percent",
                                                        "aggregationType": "Average"
                                                    }
                                                ],
                                                "title": "SQL Database DTU Usage",
                                                "titleKind": "Auto",
                                                "visualization": {"chartType": "Line"}
                                            }
                                        }
                                    }
                                ],
                                "type": "Extension/HubsExtension/PartType/MonitorChartPart"
                            }
                        },
                        # App Service HTTP Requests
                        {
                            "position": {"x": 0, "y": 4, "colSpan": 6, "rowSpan": 4},
                            "metadata": {
                                "inputs": [
                                    {
                                        "name": "options",
                                        "value": {
                                            "chart": {
                                                "metrics": [
                                                    {
                                                        "resourceMetadata": {
                                                            "id": f"/subscriptions/{self.subscription_id}/resourceGroups/{self.resource_group}/providers/Microsoft.Web/sites"
                                                        },
                                                        "name": "Requests",
                                                        "aggregationType": "Total"
                                                    }
                                                ],
                                                "title": "App Service Requests",
                                                "titleKind": "Auto",
                                                "visualization": {"chartType": "Bar"}
                                            }
                                        }
                                    }
                                ],
                                "type": "Extension/HubsExtension/PartType/MonitorChartPart"
                            }
                        },
                        # Storage Account Transactions
                        {
                            "position": {"x": 6, "y": 4, "colSpan": 6, "rowSpan": 4},
                            "metadata": {
                                "inputs": [
                                    {
                                        "name": "options",
                                        "value": {
                                            "chart": {
                                                "metrics": [
                                                    {
                                                        "resourceMetadata": {
                                                            "id": f"/subscriptions/{self.subscription_id}/resourceGroups/{self.resource_group}/providers/Microsoft.Storage/storageAccounts"
                                                        },
                                                        "name": "Transactions",
                                                        "aggregationType": "Total"
                                                    }
                                                ],
                                                "title": "Storage Transactions",
                                                "titleKind": "Auto",
                                                "visualization": {"chartType": "Line"}
                                            }
                                        }
                                    }
                                ],
                                "type": "Extension/HubsExtension/PartType/MonitorChartPart"
                            }
                        },
                        # Application Insights Response Time
                        {
                            "position": {"x": 0, "y": 8, "colSpan": 12, "rowSpan": 4},
                            "metadata": {
                                "inputs": [
                                    {
                                        "name": "options",
                                        "value": {
                                            "chart": {
                                                "metrics": [
                                                    {
                                                        "resourceMetadata": {
                                                            "id": f"/subscriptions/{self.subscription_id}/resourceGroups/{self.resource_group}/providers/Microsoft.Insights/components"
                                                        },
                                                        "name": "requests/duration",
                                                        "aggregationType": "Average"
                                                    },
                                                    {
                                                        "resourceMetadata": {
                                                            "id": f"/subscriptions/{self.subscription_id}/resourceGroups/{self.resource_group}/providers/Microsoft.Insights/components"
                                                        },
                                                        "name": "exceptions/count",
                                                        "aggregationType": "Sum"
                                                    }
                                                ],
                                                "title": "Application Insights - Response Time & Exceptions",
                                                "titleKind": "Auto",
                                                "visualization": {"chartType": "Line"}
                                            }
                                        }
                                    }
                                ],
                                "type": "Extension/HubsExtension/PartType/MonitorChartPart"
                            }
                        }
                    ]
                }
            ],
            "metadata": {
                "model": {
                    "timeRange": {
                        "value": {"relative": {"duration": 24, "timeUnit": 1}},
                        "type": "MsPortalFx.Composition.Configuration.ValueTypes.TimeRange"
                    }
                }
            }
        }
        
        dashboard = {
            "location": "global",
            "tags": {"hidden-title": dashboard_name},
            "properties": {
                "lenses": dashboard_properties["lenses"],
                "metadata": dashboard_properties["metadata"]
            }
        }
        
        try:
            result = self.dashboard_client.grafana.create_or_update(
                resource_group_name=self.resource_group,
                workspace_name=dashboard_name,
                request_body_parameters=dashboard
            )
            print(f"✓ Dashboard '{dashboard_name}' created successfully!")
            print(f"  Dashboard ID: {result.id}")
            return result
        except Exception as e:
            print(f"✗ Error creating dashboard: {str(e)}")
            return None
    
    def list_dashboards(self):
        """
        List all dashboards in the resource group
        """
        try:
            dashboards = self.resource_client.resources.list_by_resource_group(
                self.resource_group,
                filter="resourceType eq 'Microsoft.Portal/dashboards'"
            )
            
            print("\n📊 Available Azure Dashboards:")
            for dashboard in dashboards:
                print(f"  - {dashboard.name}")
                print(f"    Location: {dashboard.location}")
                print()
            
            return list(dashboards)
        except Exception as e:
            print(f"✗ Error listing dashboards: {str(e)}")
            return None
    
    def get_metrics(self, resource_id: str, metric_names: List[str], 
                    aggregation: str = "Average", timespan: str = "PT1H"):
        """
        Get metrics for a specific Azure resource
        
        Args:
            resource_id: Full resource ID
            metric_names: List of metric names to retrieve
            aggregation: Aggregation type (Average, Total, Maximum, etc.)
            timespan: Time span in ISO 8601 duration format
        """
        try:
            metrics_data = self.monitor_client.metrics.list(
                resource_id,
                timespan=timespan,
                interval='PT5M',
                metricnames=','.join(metric_names),
                aggregation=aggregation
            )
            
            print(f"\n📈 Metrics for resource: {resource_id}")
            for metric in metrics_data.value:
                print(f"  Metric: {metric.name.value}")
                print(f"  Unit: {metric.unit}")
                for timeseries in metric.timeseries:
                    for data in timeseries.data:
                        if hasattr(data, aggregation.lower()):
                            value = getattr(data, aggregation.lower())
                            print(f"    {data.time_stamp}: {value}")
            
            return metrics_data
        except Exception as e:
            print(f"✗ Error getting metrics: {str(e)}")
            return None
    
    def delete_dashboard(self, dashboard_name: str):
        """
        Delete a dashboard
        """
        try:
            self.resource_client.resources.delete_by_id(
                f"/subscriptions/{self.subscription_id}/resourceGroups/{self.resource_group}/providers/Microsoft.Portal/dashboards/{dashboard_name}",
                api_version="2020-09-01-preview"
            )
            print(f"✓ Dashboard '{dashboard_name}' deleted successfully")
            return True
        except Exception as e:
            print(f"✗ Error deleting dashboard: {str(e)}")
            return False


def main():
    """
    Main function to demonstrate dashboard creation
    """
    print("\n" + "="*60)
    print("Azure Monitor Dashboard Creator")
    print("Real-Time Monitoring Dashboard Project")
    print("="*60 + "\n")
    
    # Replace with your Azure subscription ID and resource group
    subscription_id = "your-subscription-id"
    resource_group = "your-resource-group"
    
    # Create dashboard instance
    dashboard = AzureMonitorDashboard(subscription_id, resource_group)
    
    # Create the dashboard
    print("Creating Azure Monitor Dashboard...")
    dashboard.create_dashboard()
    
    # List all dashboards
    print("\nListing all dashboards...")
    dashboard.list_dashboards()
    
    print("\n" + "="*60)
    print("Dashboard creation completed!")
    print("Visit Azure Portal > Dashboards to view")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
