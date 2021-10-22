# App: users
MAX_PROFILE_IMAGE_SIZE = 200

MAPBOX_ACCESS_TOKEN = "pk.eyJ1Ijoic3R1ZGVudHN1YmxlYXNlIiwiYSI6ImNrYXFiMDRnczAydTIycm14M3Z0d29taGQifQ.dPhJ_IPH0SCIQTIsdhQc9Q"
MAPBOX_API_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places/{0}.json?access_token={1}"
GOOGLE_MAPS_API_URL = "https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}"
GOOGLE_MAPS_API_KEY = "AIzaSyBNi6f3eB0eXe2hxRyDo0V8e9WhxnrPSqY"

DEFAULT_DISTANCE_BETWEEN_COLLEGES = 15

# App: sublease
MAX_LISTING_IMAGE_SIZE_HEIGHT = 300
MAX_LISTING_IMAGE_SIZE_WIDTH = 500

US_STATES = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
             'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
             'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
             'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
             'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']

SUPPORTED_AMENITIES = ['A/C & Heating',
                       'Washer & Dryer',
                       'Kitchen',
                       'TV',
                       'Dishwasher',
                       'Furnished',
                       'Parking Available',
                       'Gym',
                       'Pool',
                       'Pet Friendly',
                       'Furnished']

SUPPORTED_IMAGE_FILES = ('.png', '.jpg', '.jpeg')

SEARCH_CRITERIA_URL_PARAMETER = 'criteria'
SEARCH_CRITERIA_COORDINATES_URL_PARAMETER = 'criteria_coordinates'

# This is in months
MAX_PAST_START_DATE = 1

## Default parameters for filtering
NUM_BED_BATH_MIN_DEFAULT = 1
NUM_BED_BATH_MAX_DEFAULT = 6
NUM_RENT_PER_MONTH_MIN_DEFAULT = 0
NUM_RENT_PER_MONTH_MAX_DEFAULT = 10000
FEES_MIN_DEFAULT = 0

SORT_CHOICE_DEFAULT = 'distance'

# LIST OF SUPPORTED COLLEGES
SUPPORTED_COLLEGES = [
    "Georgia Institute of Technology",
    "Emory University",
    "Georgia State University",
    "Kennesaw State University",
    "University of Georgia"
]






