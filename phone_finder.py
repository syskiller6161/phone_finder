import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import sys
import requests
from colorama import Fore

def get_coordinates_online(city_name):
    """Search online for real coordinates"""
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': city_name,
            'format': 'json',
            'limit': 1
        }
        headers = {'User-Agent': 'FindNumberTool/1.0 (Educational Tool)'}
        
        response = requests.get(url, params=params, headers=headers, timeout=8)
        data = response.json()
        
        if data:
            lat = data[0]['lat']
            lon = data[0]['lon']
            display_name = data[0].get('display_name', city_name)
            return f"{lat}° N, {lon}° E ({display_name.split(',')[0]})", f"https://maps.google.com/?q={lat},{lon}"
    except:
        pass
    return "N/A (Online search failed)", "N/A"

def get_phone_info(phone_str, region=None):
    try:
        if region:
            phone = phonenumbers.parse(phone_str, region)
        else:
            phone = phonenumbers.parse(phone_str)
        
        if not phonenumbers.is_valid_number(phone):
            return f"❌ Invalid number: {phone_str}"
        
        region_name = geocoder.description_for_number(phone, "en") or "Unknown"
        
        info = {
            "Number": phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
            "Valid": phonenumbers.is_valid_number(phone),
            "Possible": phonenumbers.is_possible_number(phone),
            "Region": region_name,
            "Carrier": carrier.name_for_number(phone, "en") or "Unknown",
            "Timezone": ", ".join(timezone.time_zones_for_number(phone)) or "Unknown",
            "Type": "Mobile" if phonenumbers.number_type(phone) == phonenumbers.PhoneNumberType.MOBILE else "Fixed line / Other"
        }
        
        # Online search for coordinates
        coords, maps_link = get_coordinates_online(region_name)
        info["Approximate Coordinates"] = coords
        info["Google Maps"] = maps_link
        
        return info
    except Exception as e:
        return f"❌ Error: {str(e)}"



def main():
    
    print(Fore.MAGENTA + """
                                               __   _  ____             __              __
                               ______  _______/ /__(_) / /__   _____   / /_____  ____  / /
                             / ___/ / / / ___/ //_/ / / / _ \ / ___/  / __/ __ \/ __ \/ / 
                             (__  ) /_/ (__  ) ,< / / / /  __/ /     / /_/ /_/ / /_/ / /  
                            /____/\__, /____/_/|_/_/_/_/\___/_/      \__/\____/\____/_/   
                                 /____/                                    
        git: https://github.com/syskiller6161/phone_finder                             by:syskiller6161              
""")
    print("=" * 55)
    
    if len(sys.argv) > 1:
        number = sys.argv[1]
    else:
        number = input("Enter phone number: ").strip()
    
    print("\n📋 Analyzing...")
    info = get_phone_info(number)
    
    if isinstance(info, dict):
        for key, value in info.items():
            print(f"{key:25}: {value}")
    else:
        print(info)

if __name__ == "__main__":
    main()
