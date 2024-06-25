import boto3
import json
import logging
import pprint
import uuid

logger = logging.getLogger(__name__)

boto3.setup_default_session(profile_name='<YOUR_AWS_PROFILE>')
bedrock_agent_runtime_client = boto3.client('bedrock-agent-runtime')

AGENT_ID = '<YOUR_AGENT_ID>'
ALIAS_ID = '<YOUR_AGENT_ALIAS_ID>'
SESSION_ID = str(uuid.uuid1())

def invoke_agent(query: str, 
                 session_id=SESSION_ID, 
                 enable_trace=False, 
                 session_state=dict()):
    end_session:bool = False
    
    # invoke the agent API
    agentResponse = bedrock_agent_runtime_client.invoke_agent(
        inputText=query,
        agentId=AGENT_ID,
        agentAliasId=ALIAS_ID, 
        sessionId=session_id,
        enableTrace=enable_trace, 
        endSession= end_session,
        sessionState=session_state
    )
    
    if enable_trace:
        logger.info(pprint.pprint(agentResponse))
    
    event_stream = agentResponse['completion']
    try:
        for event in event_stream:        
            if 'chunk' in event:
                data = event['chunk']['bytes']
                if enable_trace:
                    logger.info(f"Final answer ->\n{data.decode('utf8')}")
                agent_answer = data.decode('utf8')
                return agent_answer
            elif 'trace' in event:
                if enable_trace:
                    logger.info(json.dumps(event['trace'], indent=2))
            else:
                raise Exception("unexpected event.", event)
    except Exception as e:
        raise Exception("unexpected event.", e)

if __name__ == "__main__": 
    query = "Can you please provide me pricing info?"
    answer = invoke_agent(query=query)
    print(answer)