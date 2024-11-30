import folium
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from folium.plugins import HeatMap
from collections import Counter

def geocode_address(address):
    """Convert address to coordinates"""
    geolocator = Nominatim(user_agent="my_geocoder")
    try:
        location = geolocator.geocode(address)
        if location:
            return (location.latitude, location.longitude)
    except GeocoderTimedOut:
        return None
    return None

def plot_addresses(addresses):
    """Plot addresses on a map"""
    # Create a map centered at the first valid address
    for address in addresses:
        coords = geocode_address(address)
        if coords:
            map_center = coords
            break
    else:
        map_center = (0, 0)  # Default center if no valid addresses
    
    # Create map
    m = folium.Map(location=map_center, zoom_start=12)
    
    # Add markers for each address
    for address in addresses:
        coords = geocode_address(address)
        if coords:
            folium.Marker(
                coords,
                popup=address,
                tooltip=address
            ).add_to(m)
    
    # Save map to HTML file
    m.save('address_map.html')

def plot_zipcode_heatmap(zipcodes):
    # Create a base map
    m = folium.Map(location=[45.5236, -122.6750], zoom_start=10)

    # Count the frequency of each zipcode
    zipcode_counts = Counter(zipcodes)

    # Create a list of [latitude, longitude, weight] for the heat map
    heat_data = []
    for zipcode, count in zipcode_counts.items():
        # Here you would need to convert the zipcode to a latitude and longitude
        # For simplicity, let's assume we have a function `get_lat_lon(zipcode)` that does this
        lat, lon = get_lat_lon(zipcode)
        heat_data.append([lat, lon, count])

    # Add the heat map to the base map
    HeatMap(heat_data).add_to(m)

    # Save map to HTML file
    m.save('zipcode_heatmap.html')

def get_lat_lon(zipcode):
    # Dummy function to convert zipcode to latitude and longitude
    # In a real scenario, you would use a geocoding service
    zipcode_to_lat_lon = {
        "97209": [45.528, -122.684],
        "97215": [45.515, -122.617],
        "97219": [45.458, -122.708],
        "97232": [45.528, -122.645],
        "97225": [45.497, -122.769],
        "97213": [45.536, -122.599],
        "97206": [45.490, -122.600],
        "97266": [45.484, -122.560],
        "97210": [45.536, -122.708]
    }
    return zipcode_to_lat_lon.get(zipcode, [45.5236, -122.6750])  # Default to Portland center

# Example usage
if __name__ == "__main__":
    # Example list of addresses
    addresses = [
    "1234 NW Johnson St, Portland, OR 97209",
    "5678 SE Hawthorne Blvd, Portland, OR 97215",
    "9101 SW Barbur Blvd, Portland, OR 97219",
    "2345 NE Sandy Blvd, Portland, OR 97232",
    "6789 SW Beaverton-Hillsdale Hwy, Portland, OR 97225",
    "3456 NE 42nd Ave, Portland, OR 97213",
    "7890 SE Division St, Portland, OR 97206",
    "4567 SW Vermont St, Portland, OR 97219",
    "8901 SE Powell Blvd, Portland, OR 97266",
    "5678 NW St Helens Rd, Portland, OR 97210"
]
    
    plot_addresses(addresses)

    # Example list of zip codes
    zipcodes = [
        "97209",
        "97215",
        "97219",
        "97232",
        "97225",
        "97213",
        "97206",
        "97219",
        "97266",
        "97210"
    ]
    
    plot_zipcode_heatmap(zipcodes)