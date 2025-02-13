# HBnB Evolution Technical Documentation

## Table of Contents
1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Domain Models](#domain-models)
4. [Business Rules](#business-rules)
5. [Data Layer](#data-layer)

## Overview

HBnB Evolution is a property rental platform inspired by AirBnB. The system allows users to list properties, manage bookings, and leave reviews.

### Core Features
- User registration and profile management
- Property listing and management
- Review and rating system
- Amenity management

## System Architecture

The application follows a three-tier architecture:

### 1. Presentation Layer
- Handles client interactions
- Implements REST APIs
- Manages authentication/authorization
- Validates input data

### 2. Business Logic Layer
- Implements core business rules
- Manages domain models
- Handles data validation
- Coordinates operations

### 3. Persistence Layer
- Manages data storage
- Implements CRUD operations
- Ensures data integrity

## Domain Models

### BaseModel
Common attributes for all entities:
```python
class BaseModel:
    id: str          # Unique identifier
    created_at: datetime  # Creation timestamp
    updated_at: datetime  # Last update timestamp
