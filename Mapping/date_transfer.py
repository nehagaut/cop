from datetime import datetime
import pytz

# Define the input date string
date_string = "June 14, 2022"

date_object = datetime.strptime(date_string, "%B %d, %Y")
desired_timezone = pytz.timezone("US/Pacific")
localized_datetime = desired_timezone.localize(date_object.replace(hour=0, minute=0, second=0))
formatted_date = localized_datetime.isoformat()

print(formatted_date)