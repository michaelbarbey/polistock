
// hardcoded states for better performance and less reliance
const US_STATES = [
  { isoCode: "AL", name: "Alabama" },
  { isoCode: "AK", name: "Alaska" },
  { isoCode: "AZ", name: "Arizona" },
  { isoCode: "AR", name: "Arkansas" },
  { isoCode: "CA", name: "California" },
  { isoCode: "CO", name: "Colorado" },
  { isoCode: "CT", name: "Connecticut" },
  { isoCode: "DE", name: "Delaware" },
  { isoCode: "FL", name: "Florida" },
  { isoCode: "GA", name: "Georgia" },
  { isoCode: "HI", name: "Hawaii" },
  { isoCode: "ID", name: "Idaho" },
  { isoCode: "IL", name: "Illinois" },
  { isoCode: "IN", name: "Indiana" },
  { isoCode: "IA", name: "Iowa" },
  { isoCode: "KS", name: "Kansas" },
  { isoCode: "KY", name: "Kentucky" },
  { isoCode: "LA", name: "Louisiana" },
  { isoCode: "ME", name: "Maine" },
  { isoCode: "MD", name: "Maryland" },
  { isoCode: "MA", name: "Massachusetts" },
  { isoCode: "MI", name: "Michigan" },
  { isoCode: "MN", name: "Minnesota" },
  { isoCode: "MS", name: "Mississippi" },
  { isoCode: "MO", name: "Missouri" },
  { isoCode: "MT", name: "Montana" },
  { isoCode: "NE", name: "Nebraska" },
  { isoCode: "NV", name: "Nevada" },
  { isoCode: "NH", name: "New Hampshire" },
  { isoCode: "NJ", name: "New Jersey" },
  { isoCode: "NM", name: "New Mexico" },
  { isoCode: "NY", name: "New York" },
  { isoCode: "NC", name: "North Carolina" },
  { isoCode: "ND", name: "North Dakota" },
  { isoCode: "OH", name: "Ohio" },
  { isoCode: "OK", name: "Oklahoma" },
  { isoCode: "OR", name: "Oregon" },
  { isoCode: "PA", name: "Pennsylvania" },
  { isoCode: "RI", name: "Rhode Island" },
  { isoCode: "SC", name: "South Carolina" },
  { isoCode: "SD", name: "South Dakota" },
  { isoCode: "TN", name: "Tennessee" },
  { isoCode: "TX", name: "Texas" },
  { isoCode: "UT", name: "Utah" },
  { isoCode: "VT", name: "Vermont" },
  { isoCode: "VA", name: "Virginia" },
  { isoCode: "WA", name: "Washington" },
  { isoCode: "WV", name: "West Virginia" },
  { isoCode: "WI", name: "Wisconsin" },
  { isoCode: "WY", name: "Wyoming" },
  { isoCode: "DC", name: "District of Columbia" }
];

export const getUSStates = () => US_STATES;

export const getCitiesOfState = async (stateCode) => {
  if (!stateCode) return [];
  
  try {
    // filters by 'state_code' and sort by population in descending order
    const response = await fetch(
      `https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/geonames-all-cities-with-a-population-1000/records?where=country_code%3D%22US%22%20AND%20admin1_code%3D%22${stateCode}%22&limit=100&order_by=population%20desc`
    );

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    const data = await response.json();
    const records = data.results || []; // in V2.1 API, data is in 'results'

    // extract unique city names
    const citySet = new Set();
    records.forEach(record => {
      if (record.city) {
        if (record.name) citySet.add(record.name);
      }
    });

    return Array.from(citySet)
      .map(city => ({ name: city }))
      .sort((a, b) => a.name.localeCompare(b.name));

  } catch (error) {
    console.error('Error fetching cities:', error);
    return [];
  }
};
