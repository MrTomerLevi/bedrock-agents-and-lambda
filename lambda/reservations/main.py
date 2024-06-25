from pydantic import EmailStr
from typing_extensions import Annotated
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import BedrockAgentResolver
from aws_lambda_powertools.event_handler.openapi.params import Body, Query
from aws_lambda_powertools.utilities.typing import LambdaContext

tracer = Tracer()
logger = Logger()
app = BedrockAgentResolver()


@app.post("/schedule_meeting", description="Schedules a meeting with the conference center reservations team")  # (1)!
@tracer.capture_method
def schedule_meeting(
    email: Annotated[EmailStr, Query(description="The email address of the customer")],  
) -> Annotated[bool, Body(description="Whether the meeting was scheduled successfully")]:
    logger.info("Scheduling a meeting", email=email)
    return True

@app.post("/cancel_meeting", description="Canceles an existing meeting with the conference ceter reservations team")  # (1)!
@tracer.capture_method
def cancel_meeting(
    email: Annotated[EmailStr, Query(description="The email address of the customer")],  
) -> Annotated[bool, Body(description="Whether the meeting was canceled successfully")]:
    logger.info("Canceling a meeting", email=email)
    return True

@logger.inject_lambda_context
@tracer.capture_lambda_handler
def lambda_handler(event: dict, context: LambdaContext):
    return app.resolve(event, context)