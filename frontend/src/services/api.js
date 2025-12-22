const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:5000";

export const getOfficialByAddress = async (address) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/official`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(address),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || "Failed to fetch official data");
    }

    const data = await response.json();
    return data.official;
  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
};
