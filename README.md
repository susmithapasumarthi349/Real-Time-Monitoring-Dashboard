# 📊 Real-Time Monitoring Dashboard

**A comprehensive multi-cloud monitoring solution showcasing AWS CloudWatch, GCP Cloud Monitoring, and Azure Monitor integration**

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-brightgreen)
![AWS](https://img.shields.io/badge/AWS-CloudWatch-orange)
![GCP](https://img.shields.io/badge/GCP-Cloud_Monitoring-blue)
![Azure](https://img.shields.io/badge/Azure-Monitor-lightblue)

## 🎯 Project Overview

This project demonstrates enterprise-grade real-time monitoring and observability across three major cloud platforms. It features:

- ✅ **Visualized Logs & Metrics** - Comprehensive dashboards for all major cloud services
- ✅ **Automated Alarms** - Intelligent alerting with SNS/email notifications
- ✅ **Multi-Cloud Observability** - Unified monitoring approach across AWS, GCP, and Azure
- ✅ **Production-Ready Code** - Well-structured, documented, and tested implementations

## 📚 Table of Contents

- [Features](#-features)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Platform Implementations](#-platform-implementations)
  - [AWS CloudWatch](#aws-cloudwatch)
  - [GCP Cloud Monitoring](#gcp-cloud-monitoring)
  - [Azure Monitor](#azure-monitor)
- [Usage Examples](#-usage-examples)
- [Best Practices](#-best-practices)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### AWS CloudWatch
- 📊 **Dashboard Creation**: Automated creation of comprehensive dashboards
- 🚨 **Alarm Management**: EC2, RDS, Lambda, ALB, and custom metric alarms
- 📧 **SNS Integration**: Email and SMS notifications for critical events
- 📈 **Metrics Visualization**: EC2 CPU, RDS connections, Lambda invocations, ALB requests
- 📝 **Log Insights**: Query and analyze CloudWatch Logs

### GCP Cloud Monitoring
- 🔧 **Dashboard Management**: Programmatic dashboard creation and management
- 🛠️ **Resource Monitoring**: Compute Engine, Cloud SQL, Cloud Functions, Load Balancer, GKE
- 📊 **Custom Metrics**: Write and visualize custom application metrics
- 🔔 **Alert Policies**: Configure alerts for critical thresholds
- 📉 **Time Series Data**: Query and analyze historical metrics

### Azure Monitor
- 🎯 **Portal Dashboards**: Create dashboards programmatically
- 📊 **Metrics Explorer**: Visualize VM, SQL, App Service, Storage metrics
- 🔔 **Alert Rules**: Configure metric and log-based alerts
- 📈 **Application Insights**: Monitor application performance and exceptions
- 🔍 **Log Analytics**: Query and analyze log data

## 📂 Project Structure

```
Real-Time-Monitoring-Dashboard/
├── aws-cloudwatch/
│   ├── cloudwatch_dashboard.py    # Dashboard creation and management
│   └── cloudwatch_alarms.py        # Alarm configuration with SNS
├── gcp-monitoring/
│   └── gcp_monitoring_dashboard.py # GCP monitoring implementation
├── azure-monitor/
│   └── azure_monitor_dashboard.py  # Azure monitoring implementation
├── docs/
│   ├── AWS_SETUP.md              # AWS-specific setup guide
│   ├── GCP_SETUP.md              # GCP-specific setup guide
│   └── AZURE_SETUP.md            # Azure-specific setup guide
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## ⚙️ Prerequisites

### General Requirements
- Python 3.9 or higher
- pip package manager
- Git

### AWS Requirements
- AWS Account with appropriate permissions
- AWS CLI installed and configured
- IAM permissions for CloudWatch, SNS, and monitored services

### GCP Requirements
- GCP Project with billing enabled
- gcloud CLI installed and configured
- Service account with Monitoring Admin role

### Azure Requirements
- Azure subscription
- Azure CLI installed and configured
- Contributor role on the resource group

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/susmithapasumarthi349/Real-Time-Monitoring-Dashboard.git
cd Real-Time-Monitoring-Dashboard
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Cloud Credentials

**AWS:**
```bash
aws configure
# Enter your AWS Access Key ID, Secret Access Key, and region
```

**GCP:**
```bash
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
```

**Azure:**
```bash
az login
az account set --subscription YOUR_SUBSCRIPTION_ID
```

## 🛠️ Platform Implementations

### AWS CloudWatch

#### Create Dashboard

```python
from aws_cloudwatch.cloudwatch_dashboard import CloudWatchDashboard

# Initialize
dashboard = CloudWatchDashboard()

# Create dashboard
dashboard.create_dashboard()

# List dashboards
dashboard.list_dashboards()
```

#### Create Alarms

```python
from aws_cloudwatch.cloudwatch_alarms import CloudWatchAlarms

# Initialize with SNS topic
alarms = CloudWatchAlarms()
alarms.create_sns_topic('MonitoringAlerts')
alarms.subscribe_email_to_topic('your-email@example.com')

# Create EC2 CPU alarm
alarms.create_ec2_cpu_alarm('i-1234567890abcdef0', threshold=80.0)

# Create RDS connection alarm
alarms.create_rds_connection_alarm('my-database', threshold=80)

# List alarms
alarms.list_alarms()
```

### GCP Cloud Monitoring

#### Create Dashboard

```python
from gcp_monitoring.gcp_monitoring_dashboard import GCPMonitoringDashboard

# Initialize
dashboard = GCPMonitoringDashboard('your-project-id')

# Create dashboard
dashboard.create_dashboard()

# List dashboards
dashboard.list_dashboards()
```

#### Write Custom Metrics

```python
# Write custom metric
dashboard.write_custom_metric(
    metric_type='application/active_users',
    value=150.0,
    labels={'region': 'us-central1'}
)
```

### Azure Monitor

#### Create Dashboard

```python
from azure_monitor.azure_monitor_dashboard import AzureMonitorDashboard

# Initialize
dashboard = AzureMonitorDashboard(
    subscription_id='your-subscription-id',
    resource_group='your-resource-group'
)

# Create dashboard
dashboard.create_dashboard()

# List dashboards
dashboard.list_dashboards()
```

#### Get Metrics

```python
# Get VM metrics
resource_id = '/subscriptions/xxx/resourceGroups/xxx/providers/Microsoft.Compute/virtualMachines/my-vm'
metrics = dashboard.get_metrics(
    resource_id=resource_id,
    metric_names=['Percentage CPU', 'Network In'],
    aggregation='Average',
    timespan='PT1H'
)
```

## 📝 Usage Examples

### Example 1: Monitor EC2 Instances

```python
# Create dashboard with EC2 metrics
from aws_cloudwatch.cloudwatch_dashboard import CloudWatchDashboard

dashboard = CloudWatchDashboard()
dashboard.create_dashboard()

# Set up alarms for high CPU
from aws_cloudwatch.cloudwatch_alarms import CloudWatchAlarms

alarms = CloudWatchAlarms()
alarms.create_sns_topic()
alarms.create_ec2_cpu_alarm('i-xxxxx', threshold=80)
```

### Example 2: Monitor GKE Containers

```python
from gcp_monitoring.gcp_monitoring_dashboard import GCPMonitoringDashboard

dashboard = GCPMonitoringDashboard('my-project')
dashboard.create_dashboard()  # Includes GKE metrics
```

### Example 3: Monitor Azure App Services

```python
from azure_monitor.azure_monitor_dashboard import AzureMonitorDashboard

dashboard = AzureMonitorDashboard('sub-id', 'rg-name')
dashboard.create_dashboard()  # Includes App Service metrics
```

## 👨‍💻 Best Practices

### 1. Security
- 🔒 Never hardcode credentials in source code
- 🔐 Use environment variables or secret management services
- 🛡️ Follow the principle of least privilege for IAM roles
- 🔑 Rotate credentials regularly

### 2. Cost Optimization
- 💰 Set appropriate retention periods for logs and metrics
- 📉 Use metric filters to reduce data ingestion costs
- ⏰ Configure reasonable alarm evaluation periods
- 📊 Archive old dashboard data

### 3. Monitoring Strategy
- 🎯 Focus on actionable metrics
- 🔔 Set meaningful alarm thresholds
- 📊 Use composite alarms for complex scenarios
- 🔄 Regularly review and update monitoring configurations

### 4. Multi-Cloud Management
- 🌐 Standardize metric naming conventions
- 📊 Maintain consistent dashboard layouts
- 📄 Document platform-specific differences
- 🔄 Implement unified alerting strategies

## 📈 Metrics Covered

### Infrastructure Metrics
- CPU Utilization
- Memory Usage
- Disk I/O
- Network Traffic
- Database Connections

### Application Metrics
- Request Count
- Response Time
- Error Rate
- Active Users
- Transaction Throughput

### Custom Metrics
- Business KPIs
- Application-specific metrics
- Custom health checks

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

**Susmitha Pasumarthi**
- GitHub: [@susmithapasumarthi349](https://github.com/susmithapasumarthi349)
- Repository: [Real-Time-Monitoring-Dashboard](https://github.com/susmithapasumarthi349/Real-Time-Monitoring-Dashboard)

## 🌟 Acknowledgments

- AWS CloudWatch Documentation
- GCP Cloud Monitoring Documentation
- Azure Monitor Documentation
- Multi-cloud observability best practices

---

**Built with ❤️ for cloud observability and monitoring excellence**
