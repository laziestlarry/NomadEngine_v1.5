import datetime as dt
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Text,
    Boolean,
    ForeignKey,
    JSON,
    Index,
)

Base = declarative_base()

# ---------------------------------------------------------
# TASK MODEL
# ---------------------------------------------------------

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    blueprint_id = Column(Integer, ForeignKey("blueprints.id"), nullable=True)

    # Human understanding fields
    name = Column(String(255), nullable=False)
    short_description = Column(String(512), nullable=True)  # ← for your clarity
    category = Column(String(100), nullable=True)  # e.g. "income_scan", "platform_exec", "audit"

    # Execution-related
    status = Column(String(50), default="pending", index=True)  # pending, running, completed, failed, cancelled
    priority = Column(Integer, default=50, index=True)  # 1–100 (1=highest)
    importance = Column(Integer, default=50)  # 1–100 meaning level

    payload = Column(JSON, nullable=True)  # structured data for worker

    # Ownership / routing
    assigned_worker_id = Column(Integer, ForeignKey("workers.id"), nullable=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=True)

    # Timing
    created_at = Column(DateTime, default=dt.datetime.utcnow, index=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    last_error_at = Column(DateTime, nullable=True)

    last_error_message = Column(Text, nullable=True)

    blueprint = relationship("Blueprint", back_populates="tasks")
    worker = relationship("Worker", back_populates="tasks")
    agent = relationship("Agent", back_populates="tasks")

    def __repr__(self):
        return f"<Task #{self.id} {self.status} {self.name} (P={self.priority} I={self.importance})>"


# ---------------------------------------------------------
# BLUEPRINT MODEL
# ---------------------------------------------------------

class Blueprint(Base):
    __tablename__ = "blueprints"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255), nullable=False)
    source = Column(String(100), nullable=True)      # e.g. youtube, reddit, toloka, lazy_larry_hunt
    origin_url = Column(Text, nullable=True)

    # Scores
    roi_score = Column(Float, default=0.0)           # 0–100 expected profitability
    automation_score = Column(Float, default=0.0)    # 0–100 automation potential
    risk_score = Column(Float, default=0.0)          # 0–100 risk level
    confidence = Column(Float, default=0.0)          # 0–100 agent confidence

    # JSON payload with structured strategy
    strategy = Column(JSON, nullable=True)

    created_at = Column(DateTime, default=dt.datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=dt.datetime.utcnow, onupdate=dt.datetime.utcnow)

    status = Column(String(50), default="new")  # new, approved, rejected, active, archived

    tasks = relationship("Task", back_populates="blueprint")

    def __repr__(self):
        return f"<Blueprint #{self.id} {self.title} ROI={self.roi_score:.1f} AUTO={self.automation_score:.1f}>"


# ---------------------------------------------------------
# EVENT LOG
# ---------------------------------------------------------

class EventLog(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(100), nullable=False)  # e.g. task_created, task_completed, blueprint_discovered
    category = Column(String(100), nullable=True)  # e.g. system, worker, income, scheduler

    # Optional foreign keys
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    blueprint_id = Column(Integer, ForeignKey("blueprints.id"), nullable=True)
    worker_id = Column(Integer, ForeignKey("workers.id"), nullable=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=True)

    payload = Column(JSON, nullable=True)  # extra info

    created_at = Column(DateTime, default=dt.datetime.utcnow, index=True)

    def __repr__(self):
        return f"<EventLog #{self.id} [{self.type}]>"


# ---------------------------------------------------------
# WORKER MODEL
# ---------------------------------------------------------

class Worker(Base):
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)           # e.g. "python_worker_1", "node_worker_1"
    kind = Column(String(50), nullable=False)            # e.g. python, node, platform
    capabilities = Column(JSON, nullable=True)           # e.g. ["toloka", "remotasks"]
    is_active = Column(Boolean, default=True)

    last_seen_at = Column(DateTime, nullable=True)
    last_heartbeat_at = Column(DateTime, nullable=True)

    tasks = relationship("Task", back_populates="worker")

    def __repr__(self):
        return f"<Worker #{self.id} {self.name} ({self.kind})>"


# ---------------------------------------------------------
# AGENT MODEL
# ---------------------------------------------------------

class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)          # e.g. "OpportunityClassifier"
    role = Column(String(100), nullable=True)           # e.g. "classifier", "planner", "roi_ranker"
    description = Column(Text, nullable=True)
    config = Column(JSON, nullable=True)

    tasks = relationship("Task", back_populates="agent")

    def __repr__(self):
        return f"<Agent #{self.id} {self.name} ({self.role})>"


# ---------------------------------------------------------
# INCOME RECORD
# ---------------------------------------------------------

class IncomeRecord(Base):
    __tablename__ = "income_records"

    id = Column(Integer, primary_key=True, index=True)

    platform = Column(String(100), nullable=False)   # e.g. "toloka", "hive", "remotasks"
    amount = Column(Float, nullable=False, default=0.0)
    currency = Column(String(10), nullable=False, default="USD")

    reference = Column(String(255), nullable=True)   # transaction id, invoice id, etc.
    blueprint_id = Column(Integer, ForeignKey("blueprints.id"), nullable=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)

    received_at = Column(DateTime, default=dt.datetime.utcnow, index=True)
    created_at = Column(DateTime, default=dt.datetime.utcnow, index=True)

    notes = Column(Text, nullable=True)

    def __repr__(self):
        return f"<IncomeRecord #{self.id} {self.amount} {self.currency} via {self.platform}>"


# ---------------------------------------------------------
# SCHEDULE JOB MIRROR (OPTIONAL)
# ---------------------------------------------------------

class ScheduleJob(Base):
    __tablename__ = "schedule_jobs"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(200), nullable=False)      # e.g. "alpha_scan", "income_scan"
    trigger = Column(String(100), nullable=True)    # cron string or description
    next_run_time = Column(DateTime, nullable=True)
    enabled = Column(Boolean, default=True)

    meta = Column(JSON, nullable=True)

    def __repr__(self):
        return f"<ScheduleJob #{self.id} {self.name} enabled={self.enabled}>"

# Useful indexes
Index("idx_task_status_priority", Task.status, Task.priority)
Index("idx_blueprint_status_roi", Blueprint.status, Blueprint.roi_score)
Index("idx_event_type_category", EventLog.type, EventLog.category)
Index("idx_income_platform_time", IncomeRecord.platform, IncomeRecord.received_at)