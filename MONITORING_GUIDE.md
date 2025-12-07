# Monitoring & Observability Guide for Epilot Platform

**Target Audience:** Developer learning production monitoring  
**Context:** Monitoring Epilot workflows, automations, and API integrations  
**Prerequisites:** Basic understanding of logging

---

## Table of Contents

1. [Observability Fundamentals](#1-observability-fundamentals)
2. [The Three Pillars](#2-the-three-pillars)
3. [Structured Logging](#3-structured-logging)
4. [Metrics & Dashboards](#4-metrics--dashboards)
5. [Tracing & Performance](#5-tracing--performance)
6. [Error Tracking](#6-error-tracking)
7. [Alerting Strategies](#7-alerting-strategies)
8. [Epilot-Specific Monitoring](#8-epilot-specific-monitoring)

---

## 1. Observability Fundamentals

### What is Observability?

**Monitoring:** "Is it working?"  
**Observability:** "Why isn't it working?" + "How can we improve it?"

### Your Current Situation

```python
# Current approach (print statements)
print("Creating workflow...")
result = await client.post(url, data)
print(f"Created workflow: {result['id']}")
```

**Problems:**
- ❌ No timestamps
- ❌ No context (which customer? which environment?)
- ❌ Hard to search
- ❌ Can't aggregate
- ❌ Disappears after script ends

### Observable Approach

```python
import logging
import structlog

logger = structlog.get_logger()

logger.info(
    "workflow_created",
    workflow_id=result['id'],
    workflow_name="Tarifabschluss",
    customer="Stadtwerke Wülfrath",
    environment="production",
    duration_ms=elapsed_time
)
```

**Benefits:**
- ✅ Structured data (JSON)
- ✅ Searchable by any field
- ✅ Timestamps automatic
- ✅ Can aggregate (avg duration, error rate)
- ✅ Persisted to logging service

---

## 2. The Three Pillars

### Pillar 1: Logs (What happened?)

**Purpose:** Detailed event records

```python
# Good log example
logger.info(
    "api_request_started",
    method="POST",
    url="https://workflows-definition.sls.epilot.io/v1/workflows",
    request_id="abc-123",
    user_id="deploy-bot"
)

logger.info(
    "api_request_completed",
    method="POST",
    url="https://workflows-definition.sls.epilot.io/v1/workflows",
    request_id="abc-123",
    status_code=201,
    duration_ms=450,
    workflow_id="wfc5jpYf0r"
)
```

### Pillar 2: Metrics (How much/how many?)

**Purpose:** Time-series data for dashboards

```python
from prometheus_client import Counter, Histogram

# Counter: Things that only increase
workflows_created = Counter(
    'epilot_workflows_created_total',
    'Total workflows created',
    ['customer', 'workflow_type']
)

workflows_created.labels(
    customer='stadtwerke_wuelfrath',
    workflow_type='tarifabschluss'
).inc()

# Histogram: Measure distributions
api_request_duration = Histogram(
    'epilot_api_request_duration_seconds',
    'API request duration',
    ['endpoint', 'method']
)

with api_request_duration.labels(
    endpoint='/workflows',
    method='POST'
).time():
    result = await client.post(url, data)
```

### Pillar 3: Traces (Where's the slowness?)

**Purpose:** Follow request through entire system

```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("create_workflow") as span:
    span.set_attribute("workflow.name", "Tarifabschluss")
    span.set_attribute("customer.id", "20000382")
    
    # Sub-operation
    with tracer.start_as_current_span("build_workflow_definition"):
        workflow_data = build_definition()
    
    # Another sub-operation
    with tracer.start_as_current_span("api_call"):
        result = await client.post(url, workflow_data)
    
    span.set_attribute("workflow.id", result['id'])
```

**Output visualization:**
```
create_workflow (1200ms)
  ├─ build_workflow_definition (800ms) ← Slow!
  └─ api_call (400ms)
```

---

## 3. Structured Logging

### Setting Up Structured Logging

```python
# lib/logging_config.py
import structlog
import logging
import sys

def setup_logging(environment: str = "development", level: str = "INFO"):
    """
    Configure structured logging for Epilot scripts.
    
    Args:
        environment: development, staging, or production
        level: DEBUG, INFO, WARNING, ERROR
    """
    
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, level.upper()),
    )
    
    # Configure structlog
    processors = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]
    
    # Development: Human-readable
    if environment == "development":
        processors.append(structlog.dev.ConsoleRenderer())
    # Production: JSON for log aggregation
    else:
        processors.append(structlog.processors.JSONRenderer())
    
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

# Usage in scripts
from lib.logging_config import setup_logging
setup_logging(environment="production", level="INFO")
logger = structlog.get_logger(__name__)
```

### Using Structured Logs

```python
# scripts/workflows/create_tarifabschluss_fulfillment.py
import structlog
from lib.logging_config import setup_logging

setup_logging()
logger = structlog.get_logger(__name__)

async def main():
    logger.info(
        "script_started",
        script_name="create_tarifabschluss_fulfillment",
        environment=os.getenv("ENVIRONMENT", "development")
    )
    
    try:
        # Bind context that persists for all subsequent logs
        logger = logger.bind(
            customer="Stadtwerke Wülfrath",
            customer_id="20000382"
        )
        
        logger.info("building_workflow_definition")
        workflow_data = build_workflow_definition()
        
        logger.info(
            "workflow_definition_built",
            steps_count=len(workflow_data['flow']),
            phases_count=5
        )
        
        logger.info("calling_epilot_api", url=WORKFLOW_API)
        result = await client.post(WORKFLOW_API, workflow_data)
        
        logger.info(
            "workflow_created_successfully",
            workflow_id=result['id'],
            workflow_name=result['name']
        )
        
    except Exception as e:
        logger.error(
            "workflow_creation_failed",
            error=str(e),
            error_type=type(e).__name__,
            exc_info=True  # Includes full stack trace
        )
        raise
```

### Log Output Examples

**Development (human-readable):**
```
2025-12-07 10:30:15 [info     ] script_started                 script_name=create_tarifabschluss_fulfillment
2025-12-07 10:30:15 [info     ] building_workflow_definition   customer=Stadtwerke Wülfrath
2025-12-07 10:30:16 [info     ] workflow_definition_built      steps_count=24 phases_count=5
2025-12-07 10:30:17 [info     ] workflow_created_successfully  workflow_id=wfc5jpYf0r
```

**Production (JSON):**
```json
{
  "timestamp": "2025-12-07T10:30:15.123Z",
  "level": "info",
  "event": "script_started",
  "script_name": "create_tarifabschluss_fulfillment",
  "environment": "production"
}
{
  "timestamp": "2025-12-07T10:30:17.456Z",
  "level": "info",
  "event": "workflow_created_successfully",
  "workflow_id": "wfc5jpYf0r",
  "workflow_name": "Tarifabschluss Fulfillment",
  "customer": "Stadtwerke Wülfrath",
  "customer_id": "20000382"
}
```

---

## 4. Metrics & Dashboards

### Prometheus Metrics

```python
# lib/metrics.py
from prometheus_client import Counter, Histogram, Gauge, start_http_server

# Counters (monotonically increasing)
workflows_created_total = Counter(
    'epilot_workflows_created_total',
    'Total number of workflows created',
    ['customer', 'workflow_type', 'environment']
)

automations_triggered_total = Counter(
    'epilot_automations_triggered_total',
    'Total automations triggered',
    ['automation_name', 'status']
)

api_errors_total = Counter(
    'epilot_api_errors_total',
    'Total API errors',
    ['endpoint', 'status_code']
)

# Histograms (distributions)
api_request_duration_seconds = Histogram(
    'epilot_api_request_duration_seconds',
    'API request duration',
    ['endpoint', 'method'],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
)

workflow_execution_duration_seconds = Histogram(
    'epilot_workflow_execution_duration_seconds',
    'Workflow execution duration',
    ['workflow_name'],
    buckets=[60, 300, 900, 1800, 3600]  # 1min to 1hour
)

# Gauges (can go up or down)
active_workflows = Gauge(
    'epilot_active_workflows',
    'Number of currently active workflows',
    ['customer']
)

# Start metrics server (exposes metrics on :8000/metrics)
def start_metrics_server(port=8000):
    start_http_server(port)
```

### Using Metrics in Code

```python
# scripts/workflows/create_tarifabschluss_fulfillment.py
from lib.metrics import (
    workflows_created_total,
    api_request_duration_seconds,
    api_errors_total
)
import time

async def main():
    customer = "stadtwerke_wuelfrath"
    
    start_time = time.time()
    
    try:
        # Time the API call
        with api_request_duration_seconds.labels(
            endpoint='/workflows',
            method='POST'
        ).time():
            result = await client.post(WORKFLOW_API, workflow_data)
        
        # Increment success counter
        workflows_created_total.labels(
            customer=customer,
            workflow_type='tarifabschluss',
            environment='production'
        ).inc()
        
    except Exception as e:
        # Track error
        api_errors_total.labels(
            endpoint='/workflows',
            status_code=getattr(e, 'status_code', 500)
        ).inc()
        raise
```

### Grafana Dashboard Configuration

```json
{
  "dashboard": {
    "title": "Epilot Platform Monitoring",
    "panels": [
      {
        "title": "Workflows Created (Rate)",
        "targets": [
          {
            "expr": "rate(epilot_workflows_created_total[5m])"
          }
        ],
        "type": "graph"
      },
      {
        "title": "API Request Duration (p95)",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(epilot_api_request_duration_seconds_bucket[5m]))"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Error Rate",
        "targets": [
          {
            "expr": "rate(epilot_api_errors_total[5m]) / rate(epilot_api_request_duration_seconds_count[5m])"
          }
        ],
        "type": "graph",
        "alert": {
          "condition": "> 0.01",  // Alert if >1% error rate
          "frequency": "5m"
        }
      }
    ]
  }
}
```

---

## 5. Tracing & Performance

### OpenTelemetry Setup

```python
# lib/tracing.py
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import Resource

def setup_tracing(service_name: str = "epilot-scripts", environment: str = "development"):
    """Configure distributed tracing."""
    
    # Create resource (identifies your service)
    resource = Resource.create({
        "service.name": service_name,
        "deployment.environment": environment
    })
    
    # Set up tracer provider
    provider = TracerProvider(resource=resource)
    
    # Configure exporter (Jaeger, Zipkin, etc.)
    jaeger_exporter = JaegerExporter(
        agent_host_name="localhost",
        agent_port=6831,
    )
    
    # Add span processor
    provider.add_span_processor(
        BatchSpanProcessor(jaeger_exporter)
    )
    
    # Set as global tracer
    trace.set_tracer_provider(provider)

# Usage
from lib.tracing import setup_tracing
setup_tracing()
```

### Instrumenting Code with Traces

```python
# scripts/workflows/create_tarifabschluss_fulfillment.py
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

async def main():
    # Top-level span
    with tracer.start_as_current_span("create_tarifabschluss_workflow") as span:
        span.set_attribute("customer.id", "20000382")
        span.set_attribute("customer.name", "Stadtwerke Wülfrath")
        
        # Child span 1
        with tracer.start_as_current_span("build_workflow_definition"):
            workflow_data = build_workflow_definition()
            span.set_attribute("workflow.steps_count", len(workflow_data['flow']))
        
        # Child span 2
        with tracer.start_as_current_span("api_post_workflow") as api_span:
            api_span.set_attribute("http.url", WORKFLOW_API)
            api_span.set_attribute("http.method", "POST")
            
            start = time.time()
            result = await client.post(WORKFLOW_API, workflow_data)
            duration = time.time() - start
            
            api_span.set_attribute("http.status_code", 201)
            api_span.set_attribute("workflow.id", result['id'])
            api_span.set_attribute("duration_ms", int(duration * 1000))
        
        span.set_attribute("success", True)
```

**Visualized in Jaeger:**
```
create_tarifabschluss_workflow (1200ms)
  ├─ build_workflow_definition (800ms)
  │   └─ validate_steps (100ms)
  └─ api_post_workflow (400ms)
      ├─ serialize_json (50ms)
      └─ http_request (350ms)
```

---

## 6. Error Tracking

### Sentry Integration

```python
# lib/error_tracking.py
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
import logging

def setup_sentry(dsn: str, environment: str = "development"):
    """Configure Sentry error tracking."""
    
    sentry_sdk.init(
        dsn=dsn,
        environment=environment,
        traces_sample_rate=0.1,  # Sample 10% of transactions for performance
        
        # Include log messages as breadcrumbs
        integrations=[
            LoggingIntegration(
                level=logging.INFO,
                event_level=logging.ERROR
            )
        ],
        
        # Release tracking
        release=f"epilot-scripts@{get_git_commit_hash()}",
    )

# Usage in scripts
from lib.error_tracking import setup_sentry
setup_sentry(dsn=os.getenv("SENTRY_DSN"), environment="production")
```

### Enhanced Error Context

```python
import sentry_sdk

async def create_workflow():
    # Add context to all errors in this function
    with sentry_sdk.configure_scope() as scope:
        scope.set_tag("workflow_type", "tarifabschluss")
        scope.set_tag("customer", "stadtwerke_wuelfrath")
        scope.set_context("workflow", {
            "steps_count": 24,
            "phases_count": 5,
            "estimated_duration": "2-3 days"
        })
        
        try:
            result = await client.post(WORKFLOW_API, workflow_data)
        except Exception as e:
            # Sentry automatically captures
            # Additional manual context
            sentry_sdk.capture_exception(e)
            sentry_sdk.capture_message(
                "Workflow creation failed",
                level="error",
                extras={
                    "workflow_data_size": len(json.dumps(workflow_data)),
                    "api_url": WORKFLOW_API
                }
            )
            raise
```

---

## 7. Alerting Strategies

### Alert Rules

```yaml
# alerts.yml (Prometheus AlertManager)
groups:
  - name: epilot_platform
    interval: 30s
    rules:
      # High error rate
      - alert: HighAPIErrorRate
        expr: |
          rate(epilot_api_errors_total[5m])
          /
          rate(epilot_api_request_duration_seconds_count[5m])
          > 0.05
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High API error rate (>5%)"
          description: "{{ $value }}% of API requests are failing"
      
      # Slow API calls
      - alert: SlowAPIRequests
        expr: |
          histogram_quantile(0.95,
            rate(epilot_api_request_duration_seconds_bucket[5m])
          ) > 5
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "API requests are slow (p95 > 5s)"
      
      # Workflow creation failures
      - alert: WorkflowCreationFailures
        expr: |
          increase(epilot_workflows_created_total{status="failed"}[1h]) > 5
        labels:
          severity: critical
        annotations:
          summary: "Multiple workflow creation failures"
          description: "{{ $value }} workflows failed to create in the last hour"
      
      # Service down
      - alert: EpilotScriptsDown
        expr: up{job="epilot-scripts"} == 0
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Epilot scripts service is down"
```

### Notification Channels

```yaml
# alertmanager.yml
receivers:
  - name: 'team-slack'
    slack_configs:
      - api_url: 'https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK'
        channel: '#epilot-alerts'
        title: '{{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'
  
  - name: 'oncall-pagerduty'
    pagerduty_configs:
      - service_key: 'YOUR_PAGERDUTY_KEY'
        description: '{{ .GroupLabels.alertname }}'

route:
  receiver: 'team-slack'
  group_by: ['alertname', 'customer']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  
  routes:
    # Critical alerts go to PagerDuty
    - match:
        severity: critical
      receiver: 'oncall-pagerduty'
      continue: true
    
    # All alerts to Slack
    - match:
        severity: warning
      receiver: 'team-slack'
```

---

## 8. Epilot-Specific Monitoring

### Monitoring Workflow Executions

```python
# lib/epilot_monitoring.py
import structlog
from prometheus_client import Counter, Histogram

logger = structlog.get_logger()

workflow_steps_completed = Counter(
    'epilot_workflow_steps_completed_total',
    'Workflow steps completed',
    ['workflow_id', 'step_name', 'customer']
)

workflow_step_duration = Histogram(
    'epilot_workflow_step_duration_seconds',
    'Duration of workflow steps',
    ['workflow_id', 'step_name']
)

async def monitor_workflow_execution(workflow_id: str, customer_id: str):
    """Poll Epilot API to track workflow progress."""
    
    logger.info(
        "monitoring_workflow_started",
        workflow_id=workflow_id,
        customer_id=customer_id
    )
    
    while True:
        # Fetch workflow state
        workflow = await client.get(f"{WORKFLOW_API}/executions/{workflow_id}")
        
        # Log progress
        logger.info(
            "workflow_progress",
            workflow_id=workflow_id,
            current_step=workflow['current_step'],
            progress_percent=workflow['progress'],
            status=workflow['status']
        )
        
        # Track metrics
        if workflow['status'] == 'completed':
            workflow_steps_completed.labels(
                workflow_id=workflow_id,
                step_name=workflow['current_step'],
                customer=customer_id
            ).inc()
            break
        
        await asyncio.sleep(60)  # Check every minute
```

### Dashboard for Stadtwerke Customers

```python
# Generate customer-specific metrics
customers = ["stadtwerke_wuelfrath", "stadtwerke_mettmann"]

for customer in customers:
    # Active workflows per customer
    active_count = await get_active_workflows(customer)
    active_workflows.labels(customer=customer).set(active_count)
    
    # Completed today
    completed_today = await get_completed_workflows(customer, date="today")
    workflows_completed_total.labels(
        customer=customer,
        date=date.today().isoformat()
    ).inc(completed_today)
```

---

## Summary & Quick Start

### Quick Start Checklist

- [ ] **Week 1:** Add structured logging to 5 scripts
- [ ] **Week 2:** Set up Prometheus metrics
- [ ] **Week 3:** Integrate Sentry for errors
- [ ] **Week 4:** Create Grafana dashboard
- [ ] **Month 2:** Add distributed tracing
- [ ] **Month 3:** Set up alerting

### Recommended Stack

**Logging:** structlog + CloudWatch/ELK  
**Metrics:** Prometheus + Grafana  
**Tracing:** OpenTelemetry + Jaeger  
**Errors:** Sentry  
**Alerting:** AlertManager → Slack/PagerDuty

**Total Cost:** ~$50/month for small deployment

You now have a complete monitoring strategy for production Epilot deployments! 📊