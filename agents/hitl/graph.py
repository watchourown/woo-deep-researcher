from typing import cast
from typing_extensions import Literal
from langgraph.types import interrupt, Command
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, START, END
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.mongodb import MongoDBSaver
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from agents.hitl.configuration import Configuration
from agents.hitl.state import HitlState, HitlStateInput, HitlStateOutput, AssessmentData, TaskRequestBody
from app.core.config import get_settings
from database.mongo import mongo_db, mongo_client

# Load settings
settings = get_settings()
chat_llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    openai_api_key=settings.OPENAI_API_KEY
)

def collect_constraints(state: HitlState, config: RunnableConfig) -> Command[Literal["generate_plan"]]:
     # If there's no assessment yet, initialize
    if state.assessment is None:
        state.assessment = AssessmentData()
    print("Collecting constraints from user.")
    # Collect constraints from user
    print(state.assessment)
    if state.assessment.current_symptoms is None:
        response = interrupt("Ask user for current symptoms.")
        state.assessment.current_symptoms = response["edited_text"]
    print("Collected constraints from user.")
    # Optionally store user_text in your state, if desired:
    print(state.assessment)
    # Move on to the 'generate_plan' node
    return Command(
        update={"assessment": state.assessment},
        goto="generate_plan"
    )

def generate_plan(state: HitlState, config: RunnableConfig):
    """
    Generates a plan by prompting a GPT-4 chat model with ANA standards,
    using system & user messages.
    """
    if not state.assessment:
        return {"final_result": "No assessment data found. Cannot generate plan."}

    a = state.assessment
    patient_name = a.patient_name or "Unknown"
    patient_age = a.patient_age or "Unknown"
    known_conditions = a.known_conditions if isinstance(a.known_conditions, list) else []
    medications = a.medications or "None"
    dietary = a.dietary_restrictions or "None"
    vital_signs = a.vital_signs or "None"
    allergies = a.allergies or "None"
    symptoms = a.current_symptoms or "None"

    # System-level instructions: the nurse persona, or any rules
    system_message = SystemMessage(
        content=(
            "You are a knowledgeable nursing professional following the ANA Standards "
            "of Professional Nurse Practice. Produce a thorough but concise plan."
        )
    )

    # Human-level message with the actual request
    human_prompt = f"""
    Given this patient's assessment data, address:

    - Standard 2 (Diagnosis)
    - Standard 3 (Outcomes Identification)
    - Standard 4 (Planning)
    - Standard 5 (Implementation), including 5A (Coordination of Care).

    === Patient Assessment Data ===
    Name: {patient_name}
    Age: {patient_age}
    Conditions: {", ".join(known_conditions)}
    Medications: {medications}
    Diet: {dietary}
    Vitals: {vital_signs}
    Allergies: {allergies}
    Special Instructions: {a.special_instructions or 'None'}
    Current Symptoms: {symptoms}

    Please return:
    1) Nursing diagnoses (actual or potential).
    2) SMART outcomes (Specific, Measurable, Attainable, Relevant, Time-bound).
    3) A care plan with interventions & rationale.
    4) Steps for implementation & coordination with other providers.
    5) Any necessary patient education or follow-up.
    """

    user_message = HumanMessage(content=human_prompt.strip())
    print("ai key: ")
    print(settings.OPENAI_API_KEY) 
    # Now call the GPT-4 chat model with these messages
    response_message = chat_llm.invoke([system_message, user_message])
    # ^ returns an AIMessage object

    # The text is in response_message.content
    plan_result = response_message.content
    state.final_result = plan_result
    print(plan_result)
    return {"final_result": plan_result}

def human_review(
    state: HitlState, 
    config: RunnableConfig
) -> Command[Literal["collect_constraints", "generate_tasks", "finalize_conversation"]]:
    print("Human is reviewing the plan. user says?")
    feedback = interrupt("Review or confirm the plan:")
    user_text = feedback["edited_text"].lower()
    print("User said: ", user_text)

    # Optionally store user_text in your state, if desired:
    # state.user_provided_info = user_text

    if user_text == "confirm":
        # If caretaker confirmed plan, go to push_tasks
        return Command(goto="push_tasks")
    elif user_text == "restart":
        # If caretaker wants to start over with constraints
        return Command(goto="collect_constraints")
    else:
        # For any other input, finalize conversation
        return Command(goto="finalize_conversation")

def generate_tasks(state: HitlState, config: RunnableConfig):
    print("Pushing tasks to system with final plan info.")
    configuration = Configuration.from_runnable_config(config)
    # e.g. call external API

    prompt_template = ChatPromptTemplate([
        ("system", "You are a helpful assistant"),
        ("user", "Tell me a joke about {topic}")
    ])
    
    messages = [
        {"role": "system", "content": configuration.router_system_prompt}
    ] + state.messages
    response = cast(
        TaskRequestBody,
        chat_llm.with_structured_output(TaskRequestBody).ainvoke(messages)
    )
    interrupt(response.content)
    return {"task_result": "Tasks created successfully."}

def push_tasks(state: HitlState, config: RunnableConfig):
    print("Pushing tasks to system with final plan info.")
    # e.g. call external API
    return {"task_result": "Tasks created successfully."}

def finalize_conversation(state: HitlState):
    print("Finalizing conversation.")
    return {"final_result": "Care Plan conversation complete."}

builder = StateGraph(
    state_schema=HitlState,
    input=HitlStateInput,
    output=HitlStateOutput,
    config_schema=Configuration
)

builder.add_node("collect_constraints", collect_constraints)
builder.add_node("generate_plan", generate_plan)
builder.add_node("human_review", human_review)
builder.add_node("generate_tasks", generate_tasks)
builder.add_node("push_tasks", push_tasks)
builder.add_node("finalize_conversation", finalize_conversation)

# Edges
builder.add_edge(START, "collect_constraints")
# builder.add_edge("collect_constraints", "generate_plan")

builder.add_edge("generate_tasks", "push_tasks")
builder.add_edge("generate_plan", "human_review")

builder.add_edge("push_tasks", "finalize_conversation")
builder.add_edge("finalize_conversation", END)

# Mongo checkpointer
checkpointer = MongoDBSaver(
    client=mongo_client,
    db_name="woo_threads",
    checkpoint_collection_name="hitl_checkpoints",
    writes_collection_name="checkpoint_writes"
)

graph = builder.compile(checkpointer=checkpointer)