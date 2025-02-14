# agents/hitl/state.py

from dataclasses import dataclass, field
from typing import Optional, List
from typing_extensions import TypedDict
from datetime import date

@dataclass
class AssessmentData:
    """Captures relevant data per ANA Standard 1: Assessment."""
    patient_name: Optional[str] = "Peter"
    patient_age: Optional[int] = "37"
    known_conditions: Optional[List[str]] = "Flu, hybpertension, diabetes"
    medications: Optional[str] = "Aspirin, Metformin, Lisinopril"
    dietary_restrictions: Optional[str] = "sugar, refined carbohydrates"
    vital_signs: Optional[str] = "BP: 120/80, HR: 72, Temp: 98.6"
    special_instructions: Optional[str] = "None"
    allergies: Optional[str] = "None"
    current_symptoms: Optional[str] = "Fever, cough, shortness of breath"

@dataclass
class HitlState:
    # Internal working state for the conversation
    assessment: Optional[AssessmentData] = None
    user_provided_info: Optional[str] = None
    system_message: Optional[str] = None
    final_result: Optional[str] = None

@dataclass
class HitlStateInput(TypedDict):
    # Input from user
    user_provided_info: Optional[str]

@dataclass
class HitlStateOutput(TypedDict):
    # Output from graph
    final_result: Optional[str]



from dataclasses import dataclass, field
from typing import Optional, List
from typing_extensions import Literal

@dataclass
class VitalsRequest:
    """Represents the 'vitals' object in your request."""
    testBloodPressure: bool
    testBloodSugar: bool
    testRespirationRate: bool
    testBodyTemperature: bool
    testBloodOxygenLevel: bool

@dataclass
class MedicalRequest:
    """Represents the 'medical' object in your request."""
    medicine: str
    dosage: str
    mustTake: bool
    desciption: Optional[str] = None

@dataclass
class AssignedToDetails:
    """Represents 'assignedToDetails' in your request."""
    assigned: bool
    uid: str
    responseStatus: str = "none"

@dataclass
class TimeDetail:
    """Represents 'timeDetail' in your request."""
    scheduleType: str
    proccessInFuture: bool
    scheduleTimes: List[str] = field(default_factory=list)
    startDate: Optional[str] = None  # Could be a date or datetime
    endDate: Optional[str] = None
    timezone: Optional[str] = None

@dataclass
class TaskRequestBody:
    """
    Represents the entire task request body.
    
    For 'vitals' tasks, fill out 'vitals'.
    For 'medical' tasks, fill out 'medical'.
    You can add location or other fields as needed.
    """
    uid: str
    taskType: Literal["vitals", "medical", "location"]  # add more if needed
    vitals: Optional[VitalsRequest] = None
    medical: Optional[MedicalRequest] = None
    assignedToDetails: AssignedToDetails = field(default_factory=lambda: AssignedToDetails(False, "none", "none"))
    timeDetail: TimeDetail = field(default_factory=TimeDetail)