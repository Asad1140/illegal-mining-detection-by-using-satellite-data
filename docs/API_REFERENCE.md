# Illegal Mining Detection by Using Satellite Data REST API Reference

All routes are served under `/api` by default.

## 1. Authentication & Roles
- `GET /api/auth/me?role={ADMIN|ANALYST|FIELD_OFFICER|VIEWER}`
- `GET /api/auth/roles`

## 2. Dashboard KPIs & Analytics
- `GET /api/dashboard/stats?region={Keonjhar|Bellary|Sukinda|Singrauli|ALL}`

## 3. Early Warning Alerts
- `GET /api/alerts?district={name}&priority={HIGH|CRITICAL}&status={status}&sort_by={risk_score}`
- `GET /api/alerts/{alert_id}`

## 4. Mining Leases & GIS Layers
- `GET /api/mines/leases?district={name}&mineral={type}`
- `GET /api/mines/leases/{lease_id}`
- `GET /api/mines/gis/layers/{region_name}` (Returns 12 GeoJSON vector layers)

## 5. Satellite Pipeline & Observations
- `GET /api/satellite/timeline/{region}` (Returns 5-year multi-sensor observations 2022-2026)
- `GET /api/satellite/preprocessing/status`
- `GET /api/satellite/sources`

## 6. Modular AI Inference
- `POST /api/ai/analyze` (Body: `{ region, algorithm, sensitivity }`)
- `GET /api/ai/models/status`

## 7. Human-in-the-Loop Verification
- `GET /api/verification/queue?status={status}`
- `POST /api/verification/submit` (Body: `{ alert_id, status, comments, gps_coordinates, evidence_notes }`)
- `GET /api/verification/history/{alert_id}`

## 8. System Settings & Reports
- `GET /api/settings`
- `POST /api/settings/update`
- `GET /api/reports/alert/{alert_id}`
