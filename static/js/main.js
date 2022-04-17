const getLocation = () => {
    const location = document.querySelector('.location');
    const lat = document.querySelector('.latitude');
    const lon = document.querySelector('.longitude');
    const postcode = document.querySelector('.postcode');
    const city = document.querySelector('.city');

    const success = (position) => {
        // console.log(position)

        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;

        const API_KEY = 'AIzaSyBPR88unXRLKLEz3pK3soTyZpdQYI4hj6E'
        // const latitude = 52.5432870179525400
        // const longitude = 13.4146936213831380
        // const latitude = 55.820032
        // const longitude = 10.634549

        const geocodingApiUrl = `https://maps.googleapis.com/maps/api/geocode/json?latlng=${latitude},${longitude}&key=${API_KEY}`
        fetch(geocodingApiUrl)
        .then(res => res.json())
        .then(data => {
            console.log(data.results[0].address_components)
            console.log(latitude)
            lat.value = latitude
            console.log(longitude)
            lon.value = longitude
            let parts = data.results[0].address_components;
            parts.forEach(part => {
                if (part.types.includes("postal_code")) {
                    console.log(part.long_name)
                    postcode.value = part.long_name
                }
                if (part.types.includes("locality")) {
                    console.log(part.long_name)
                    city.value = part.long_name
                }
            });
        })
        .catch(err => console.error(err));
    }

    const error = () => {
        location.textContent = 'Your location will not be saved'
        lat.value = null
        lon.value = null
        postcode.value = null
        city.value = null

    }

    navigator.geolocation.getCurrentPosition(success, error);

}

document.querySelector('.find-location').addEventListener('click', getLocation);
