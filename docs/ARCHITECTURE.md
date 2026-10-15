# Illegal Mining Detection by Using Satellite Data System Architecture

## Overview
Illegal Mining Detection by Using Satellite Data is an AI-assisted satellite surveillance and early warning platform designed to monitor mining sectors, detect potential unauthorized mining disturbances, intersect them against official cadastral lease boundaries and statutory 500m surveillance buffers, calculate an explainable Risk Score (0-100), and guide human-in-the-loop field verification.

```mermaid
flowchart TD
    subgraph S1_Ingestion ["1. Ingestion"]
        S2["Sentinel-2 MSI"]
        S1["Sentinel-1 SAR"]
        L8["Landsat 8/9"]
    end

    subgraph S2_Prep ["2. Preprocessing"]
        SCL["SCL Cloud Filter"]
        IND["NDVI, BSI, NDWI, NDBI"]
        SAR["VV/VH Radar Ratio"]
    end

    subgraph S3_AI ["3. Modular AI"]
        CD["Siamese CNN Change Detector"]
        SEG["U-Net 12-Class Segmenter"]
        PRED["Expansion Trend Forecaster"]
    end

    subgraph S4_GIS ["4. GIS Topology"]
        CAD["Official Mining Leases"]
        BUF["500m Surveillance Buffer"]
        SHP["Shapely Intersection Engine"]
    end

    subgraph S5_Risk ["5. Explainable Risk"]
        RE["7-Factor Scoring (0-100)"]
        DOS["Alert Dossier (#MG-2026-00421)"]
    end

    subgraph S6_HITL ["6. Human-in-the-Loop"]
        PATROL["Officer Inspection & DGPS"]
        STATUS["Status Update & Retraining Loop"]
    end

    S1_Ingestion --> S2_Prep --> S3_AI --> S4_GIS --> S5_Risk --> S6_HITL
    S6_HITL -.-> S3_AI
```

## Modular AI Strategy
- Base Interfaces: `BaseChangeDetectionModel`, `BaseSegmentationModel`, `BaseRiskModel`, `BasePredictiveExpansionModel`.
- The system decouples model interfaces from business logic so pre-trained PyTorch weights can be dropped in seamlessly.
