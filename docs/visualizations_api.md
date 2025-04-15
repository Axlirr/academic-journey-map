# Visualization API Documentation

The Academic Journey Map provides a powerful visualization API for generating interactive graphs and charts to visualize academic progress, skills, and goals.

## Base URL

```
https://api.academic-journey-map.com/v1/visualizations
```

## Authentication

All endpoints require authentication using a Bearer token:

```http
Authorization: Bearer <your_token>
```

## Common Response Format

All visualization endpoints return data in the following format:

```json
{
  "plot_data": {
    // Plotly figure data
  },
  "title": "string",
  "description": "string",
  "additional_metadata": {
    // Endpoint-specific metadata
  }
}
```

## Endpoints

### 1. Skill Network Visualization

Generate an interactive network visualization of skills, courses, and projects.

```http
GET /skill-network/{user_id}
```

#### Parameters

| Name | Type | In | Description |
|------|------|------|------------|
| user_id | integer | path | **Required**. User ID |
| min_proficiency | integer | query | Minimum skill proficiency level (1-10) |
| category_filter | string | query | Filter skills by category |

#### Example Request

```http
GET /skill-network/123?min_proficiency=7&category_filter=Programming
```

#### Example Response

```json
{
  "plot_data": {
    "data": [
      {
        "type": "network",
        "node": {
          "x": [...],
          "y": [...],
          "text": [...],
          "color": [...]
        },
        "link": {
          "source": [...],
          "target": [...],
          "value": [...]
        }
      }
    ],
    "layout": {
      "title": "Skill Network",
      "showlegend": true
    }
  },
  "title": "Skill Network for John Doe",
  "description": "Interactive visualization of skills, courses, and projects",
  "node_count": 15,
  "edge_count": 23,
  "categories": ["Programming", "Data Science", "AI"]
}
```

### 2. Progress Timeline

Generate an interactive timeline of academic progress and achievements.

```http
GET /progress-timeline/{user_id}
```

#### Parameters

| Name | Type | In | Description |
|------|------|------|------------|
| user_id | integer | path | **Required**. User ID |
| start_date | string | query | Filter events after this date (ISO format) |
| end_date | string | query | Filter events before this date (ISO format) |

#### Example Request

```http
GET /progress-timeline/123?start_date=2024-01-01&end_date=2024-12-31
```

#### Example Response

```json
{
  "plot_data": {
    "data": [
      {
        "type": "scatter",
        "mode": "markers+lines",
        "x": [...],
        "y": [...],
        "text": [...],
        "marker": {
          "size": [...],
          "color": [...]
        }
      }
    ],
    "layout": {
      "title": "Academic Progress Timeline",
      "xaxis": {"title": "Date"},
      "yaxis": {"title": "Achievement Level"}
    }
  },
  "title": "Academic Progress Timeline for John Doe",
  "description": "Interactive timeline of courses and achievements",
  "start_date": "2024-01-01T00:00:00Z",
  "end_date": "2024-12-31T23:59:59Z",
  "event_count": 12
}
```

### 3. Skill Radar Chart

Generate a radar chart visualization of skill proficiencies.

```http
GET /skill-radar/{user_id}
```

#### Parameters

| Name | Type | In | Description |
|------|------|------|------------|
| user_id | integer | path | **Required**. User ID |
| category_filter | string | query | Filter skills by category |

#### Example Request

```http
GET /skill-radar/123?category_filter=Programming
```

#### Example Response

```json
{
  "plot_data": {
    "data": [
      {
        "type": "scatterpolar",
        "r": [...],
        "theta": [...],
        "fill": "toself"
      }
    ],
    "layout": {
      "polar": {
        "radialaxis": {"visible": true, "range": [0, 10]}
      },
      "showlegend": true
    }
  },
  "title": "Skill Proficiency Radar for John Doe",
  "description": "Interactive radar chart of skill proficiencies",
  "skill_categories": ["Programming", "Data Science", "AI"],
  "total_skills": 8,
  "average_proficiency": 7.5
}
```

### 4. Goal Progress Chart

Generate a visualization of goal progress.

```http
GET /goal-progress/{user_id}
```

#### Parameters

| Name | Type | In | Description |
|------|------|------|------------|
| user_id | integer | path | **Required**. User ID |
| category_filter | string | query | Filter goals by category |
| include_completed | boolean | query | Include completed goals (default: false) |

#### Example Request

```http
GET /goal-progress/123?category_filter=Career&include_completed=true
```

#### Example Response

```json
{
  "plot_data": {
    "data": [
      {
        "type": "bar",
        "x": [...],
        "y": [...],
        "text": [...],
        "marker": {"color": [...]}
      }
    ],
    "layout": {
      "title": "Goal Progress",
      "xaxis": {"title": "Goals"},
      "yaxis": {"title": "Progress (%)"}
    }
  },
  "title": "Goal Progress for John Doe",
  "description": "Interactive visualization of goal progress by category",
  "goal_categories": ["Career", "Education", "Skills"],
  "total_goals": 5,
  "average_progress": 65.0
}
```

## Export Functionality

All visualizations can be exported in various formats using the `/export` endpoint:

```http
GET /{visualization-endpoint}/{user_id}/export?format={format}
```

### Supported Export Formats

- `html`: Interactive HTML visualization
- `png`: Static PNG image
- `svg`: Vector graphics format
- `pdf`: PDF document
- `json`: Raw JSON data
- `csv`: CSV data export

### Example Export Request

```http
GET /skill-network/123/export?format=pdf
```

## Caching

Visualizations are cached for improved performance:

- Default cache duration: 1 hour
- Cache is automatically invalidated when related data changes
- Cache can be manually invalidated using the `/cache/invalidate` endpoint

### Cache Control Headers

```http
Cache-Control: max-age=3600
ETag: "visualization-hash"
```

## Rate Limiting

- 100 requests per minute per user
- 1000 requests per hour per user
- Export endpoints: 10 requests per minute per user

## Error Responses

```json
{
  "detail": "Error message",
  "error_code": "ERROR_CODE",
  "timestamp": "2024-04-15T12:00:00Z"
}
```

### Common Error Codes

- `404_NOT_FOUND`: User or resource not found
- `422_VALIDATION_ERROR`: Invalid parameters
- `429_TOO_MANY_REQUESTS`: Rate limit exceeded
- `500_INTERNAL_ERROR`: Server error

## Best Practices

1. Use appropriate filtering to reduce data load
2. Cache visualizations on the client side when possible
3. Use the export functionality for reports and presentations
4. Monitor rate limits and implement appropriate backoff strategies
5. Handle errors gracefully in your application

## SDK Examples

### Python

```python
from academic_journey_client import AcademicJourneyAPI

api = AcademicJourneyAPI(api_key="your_api_key")

# Get skill network visualization
skill_network = api.visualizations.get_skill_network(
    user_id=123,
    min_proficiency=7,
    category_filter="Programming"
)

# Export as PDF
skill_network.export(format="pdf", filename="skill_network.pdf")
```

### JavaScript

```javascript
import { AcademicJourneyAPI } from 'academic-journey-client';

const api = new AcademicJourneyAPI('your_api_key');

// Get progress timeline
const timeline = await api.visualizations.getProgressTimeline({
  userId: 123,
  startDate: '2024-01-01',
  endDate: '2024-12-31'
});

// Export as HTML
await timeline.export({
  format: 'html',
  filename: 'progress_timeline.html'
});
```