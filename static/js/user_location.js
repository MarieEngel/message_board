const getLocation = async () => {
    const location = document.querySelector('.location');
    const lat = document.querySelector('.latitude');
    const lon = document.querySelector('.longitude');
    const postcode = document.querySelector('.postcode');
    const city = document.querySelector('.city');
    const street = document.querySelector('.street');
    const street_number = document.querySelector('.street_number');


    const success = async (position) => {

        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;

        const API_KEY = 'AIzaSyBPR88unXRLKLEz3pK3soTyZpdQYI4hj6E';

        try {
            const geocodingApiUrl = `https://maps.googleapis.com/maps/api/geocode/json?latlng=${latitude},${longitude}&key=${API_KEY}`;
            const response = await fetch(geocodingApiUrl);
            const data = await response.json();
            lat.value = latitude;
            lon.value = longitude;
            const [firstResult, ...rest] = data.results;
            const parts = firstResult.address_components;
            console.log(parts);
            for (const part of parts) {
                if (part.types.includes("postal_code")) {
                    console.log(part.long_name);
                    postcode.value = part.long_name;
                }
                if (part.types.includes("locality")) {
                    console.log(part.long_name);
                    city.value = part.long_name;
                }
                if (part.types.includes("route")) {
                    console.log(part.long_name);
                    street.value = part.long_name;
                }
                if (part.types.includes("street_number")) {
                    console.log(part.long_name);
                    street_number.value = part.long_name;
                }
            }

        } catch (ex) {
            console.log(ex);
        }
    }

    const error = () => {
        location.textContent = 'Your location will not be saved';
        lat.value = null;
        lon.value = null;
        postcode.value = null;
        city.value = null;
        street.value = null;
        street_number.value = null;


    }

    navigator.geolocation.getCurrentPosition(success, error);

}

document.querySelector('.find-location').addEventListener('click', getLocation);
