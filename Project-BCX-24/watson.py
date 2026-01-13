import json
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


# Set up the authenticator and assistant instance
authenticator = IAMAuthenticator("SpsGMioL_Fdb8SUtpf_cM3GrkYdn8YmDgAtaiTO4ncYc")
assistant = AssistantV2(
    version='2023-06-15',
    authenticator=authenticator
)
assistant.set_service_url("https://api.au-syd.assistant.watson.cloud.ibm.com/instances/bd899c3b-4aac-4109-a348-6d9c4f6908a7")

# Create a session
response = assistant.create_session("039debef-f7c3-4ae4-a422-83ae31897e37")

# Extract and print the session ID
session_id = response.result['session_id']


response = assistant.message(
    assistant_id='039debef-f7c3-4ae4-a422-83ae31897e37',
    session_id=session_id,
    input={
        'message_type': 'text',
        'text': 'Hello, What is the Capital of France?'
    }
).get_result()

# print(json.dumps(response["output"]["generic"][0]["text"], indent=2))
print(json.dumps(response, indent=2))