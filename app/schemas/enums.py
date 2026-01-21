from enum import Enum


class Environment(str, Enum):
    prod = "prod"
    staging = "staging"
    dev = "dev"


class IssueStatus(str, Enum):
    new = "new"
    triaged = "triaged"
    closed = "closed"


class Severity(str, Enum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"


class Category(str, Enum):
    outage = "outage"
    performance = "performance"
    access = "access"
    request = "request"
