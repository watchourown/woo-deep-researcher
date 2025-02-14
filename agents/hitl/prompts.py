
GENERATE_TASKS_SYSTEM_PROMPT = """\
Below is a nursing care plan:
=== Care Plan ===
{plan}
===

Based on this plan, produce a JSON array of tasks. Each task must follow our known schema. 
For example:

[
  {{
    "uid": "e7672381-5107-4bb2-85ff-e09ede6d2300",
    "taskType": "vitals",
    "vitals": {{
      "testBloodPressure": true,
      "testBloodSugar": true,
      ...
    }},
    "assignedToDetails": {{
      "assigned": true,
      "uid": "...",
      "responseStatus": "none"
    }},
    "timeDetail": {{
      "scheduleType": "forPeriodOfTime",
      "proccessInFuture": true,
      "scheduleTimes": ["00 00 * * *"],
      "startDate": "2024-10-15",
      "endDate": "2024-10-28",
      "timezone": "Asia/Karachi"
    }}
  }},
  {{
    "uid": "...",
    "taskType": "medical",
    "medical": {{
      "medicine": "Metformin",
      "dosage": "500mg",
      "mustTake": true,
      "desciption": "Take with meals"
    }},
    "assignedToDetails": {{ ... }},
    "timeDetail": {{ ... }}
  }}
]

Important:
1) The output must be valid JSON (no trailing commas, no markdown fences).
2) We only need the tasks array (no additional explanation).
3) If there is nothing relevant, return an empty array [].

Now produce the JSON array of tasks:
"""

