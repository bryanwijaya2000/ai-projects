import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import ollama
import gradio as gr

def add_event(summary: str, location: str, description: str, start_time: str, end_time: str, timezone="Asia/Jakarta") -> str:
    """
    Creates a new event in Google Calendar
    Args:
        summary (str): Name of the event
        location (str): Address where the event will be held
        description (str): Description of the event
        start_time (str): Start date and time of the event in RFC 3339 string format (YYYY-MM-DDTHH:MM:SSZ for UTC, YYYY-MM-DDTHH:MM:SS+HH:MM or YYYY-MM-DDTHH:MM:SS-HH:MM for offset in hours and minutes)
        end_time (str): End date and time of the event in RFC 3339 string format (YYYY-MM-DDTHH:MM:SSZ for UTC, YYYY-MM-DDTHH:MM:SS+HH:MM or YYYY-MM-DDTHH:MM:SS-HH:MM for offset in hours and minutes)
        timezone (str): The timezone used for start_time and end_time, default is "Asia/Jakarta".
    Returns:
        str: Success message
    """
    
    try:
        event_details = {
            "summary": summary,
            "location": location,
            "description": description,
            "start": {
                "dateTime": start_time,
                "timezone": timezone
            },
            "end": {
                "dateTime": end_time,
                "timezone": timezone
            }
        }

        event = service.events().insert(calendarId="primary", body=event_details).execute()

        return f"Event created successfully! ID: {event.get('id')}"
    except Exception as e:
        raise e

def update_event(event_id: str, new_summary=None, new_location=None, new_description=None, new_start_time=None, new_end_time=None, timezone="Asia/Jakarta") -> str:
    """
    Updates an existing event in Google Calendar
    Args:
        event_id (str): ID of the event to be updated
        new_summary (str): The new name of the event, default is None.
        new_location (str): The new address of the event, default is None.
        new_description (str): The new description of the event, default is None.
        new_start_time (str): The new start date and time of the event in RFC 3339 string format (YYYY-MM-DDTHH:MM:SSZ for UTC, YYYY-MM-DDTHH:MM:SS+HH:MM or YYYY-MM-DDTHH:MM:SS-HH:MM for offset in hours and minutes), default is None.
        new_end_time (str): The new end date and time of the event in RFC 3339 string format (YYYY-MM-DDTHH:MM:SSZ for UTC, YYYY-MM-DDTHH:MM:SS+HH:MM or YYYY-MM-DDTHH:MM:SS-HH:MM for offset in hours and minutes), default is None.
        timezone (str): The timezone used for new_start_time and new_end_time, default is "Asia/Jakarta".
    Returns:
        str: Success message
    """

    try:
        event = service.events().get(calendarId="primary", eventId=event_id).execute()

        if new_summary:
            event["summary"] = new_summary

        if new_location:
            event["location"] = new_location

        if new_description:
            event["description"] = new_description

        if new_start_time:
            event["start"] = {
                "dateTime": new_start_time,
                "timezone": timezone
            }
        
        if new_end_time:
            event["end"] = {
                "dateTime": new_end_time,
                "timezone": timezone
            }

        service.events().patch(calendarId="primary", eventId=event_id, body=event).execute()

        return f"Event {event_id} updated successfully!"
    except Exception as e:
        raise e

def delete_event(event_id: str) -> str:
    """
    Deletes an existing event in Google Calendar
    Args:
        event_id (str): ID of the event to be deleted
    Returns:
        str: Success message
    """

    try:
        service.events().delete(calendarId="primary", eventId=event_id).execute()
        return f"Event {event_id} deleted successfully!"
    except Exception as e:
        raise e

def setup_google_calendar_api_service():
    creds = None

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)
        return service
    except HttpError as error:
        raise error

def book_appointment(command: str) -> str:
    messages.append(
        {
            "role": "user",
            "content": command
        }
    )

    response = ollama.chat(
        model="qwen3",
        messages=messages,
        tools=[add_event, update_event, delete_event],
        think=False
    )

    messages.append(response.message)

    responses = ""

    if response.message.tool_calls:
        for tc in response.message.tool_calls:
            if tc.function.name in available_functions:
                result = available_functions[tc.function.name](**tc.function.arguments)
                content = str(result)
                responses += content + "\n"
                messages.append(
                    {
                        "role": "tool",
                        "tool_name": tc.function.name,
                        "content": content
                    }
                )

    if responses == "":
        responses = response.message.content

    return responses

SCOPES = ["https://www.googleapis.com/auth/calendar"]

service = setup_google_calendar_api_service()

available_functions = {
    "add_event": add_event,
    "update_event": update_event,
    "delete_event": delete_event
}

messages = [
    {
        "role": "system",
        "content": "You are a Calendar Booking Assistant."
    }
]

interface = gr.Interface(
    inputs=gr.Textbox(
        lines=2,
        placeholder="Enter your command here"
    ),
    outputs=gr.TextArea(),
    title="Calendar Booking Assistant",
    description="Tell me what you need, and I will book your appointment.",
    fn=book_appointment
)

interface.launch(debug=True)