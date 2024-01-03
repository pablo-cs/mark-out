import axios from 'axios';

const API = axios.create({
  baseURL: `http://127.0.0.1:8000/wrestling_matches/`,
  // Add other Axios configurations if needed (headers, authentication, etc.)
});

export const fetchData = async (endpoint, params) => {
    try {
      const response = await API.get(endpoint, { params });
      return response.data;
    } catch (error) {
      throw new Error(`Failed to fetch data for ${endpoint}: ${error.message}`);
    }
  };

export const getWrestler = async (wrestlerID) => {
    return await fetchData('wrestler/', { wrestler_id: wrestlerID });
  };
  
export const getWrestlerMatches = async (wrestlerID) => {
    return await fetchData('wrestler_matches/', { wrestler_id: wrestlerID });
  };

export const searchWrestler = async(query) => {
    return await fetchData('search_wrestler/', { query: query });
}

export const getMatch = async(matchID) => {
    return await fetchData('match/', { match_id: matchID });
}

export const searchMatch = async(query) => {
    return await fetchData('search_match/', { query: query });
}

export const getPromotion = async(promotionID) => {
    return await fetchData('promotion/', { promotion_id: promotionID });
}

export const getPromotionEvents = async(promotionID) => {
    return await fetchData('promotion_events/', { promotion_id: promotionID });
}

export const searchPromotion = async(query) => {
    return await fetchData('search_promotion/', { query: query });
}

export const getVenue = async(venueID) => {
    return await fetchData('venue/', { venue_id: venueID });
}

export const getVenueEvents = async(venueID) => {
    return await fetchData('venue_events/', { venue_id: venueID });
}

export const searchVenue = async(query) => {
    return await fetchData('search_venue/', { query: query });
}

export const getTagTeam = async(tagTeamID) => {
    return await fetchData('tag_team/', { tag_team_id: tagTeamID });
}

export const getTagTeamMatches = async(tagTeamID) => {
    return await fetchData('tag_team_matches/', { tag_team_id: tagTeamID });
}

export const searchTagTeam = async(query) => {
    return await fetchData('search_tag_team/', { query: query });
}

export const getTitle = async(titleID) => {
    return await fetchData('title/', { title_id: titleID });
}

export const getTitleMatches = async(titleID) => {
    return await fetchData('title_matches/', { title_id: titleID });
}

export const searchTitle = async(query) => {
    return await fetchData('search_title/', { query: query });
}

export const getEvent = async(eventID) => {
    return await fetchData('event/', { event_id: eventID });
}

export const getEventMatches = async(eventID) => {
    return await fetchData('event_matches/', { event_id: eventID });
}

export const searchEvent = async(query) => {
    return await fetchData('search_event/', { query: query });
}
export default API;
